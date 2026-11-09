const params = new URLSearchParams(location.search);
const EQUIPE = params.get("equipe") || "zupeli_vilela_dib";
const BROKER_URL = params.get("broker") || "wss://broker.hivemq.com:8884/mqtt";
const BASE = "cscf/" + EQUIPE;

const $ = (id) => document.getElementById(id);
const setLed = (id, ligado) => $(id).classList.toggle("on", !!ligado);
const estado = { alerta: null, janela: null, bomba: null };

if (typeof mqtt === "undefined") {
  $("pillConexao").textContent = "sem mqtt.js";
  throw new Error("mqtt.js não carregou");
}

const cliente = mqtt.connect(BROKER_URL, {
  clientId:
    "dashboard-" + EQUIPE + "-" + Math.random().toString(16).slice(2, 8),
  reconnectPeriod: 2000,
  connectTimeout: 10000,
  clean: true,
});

cliente.on("connect", () => {
  $("pillConexao").textContent = "conectado";
  $("pillConexao").className = "pill on";
  cliente.subscribe(BASE + "/#");
  registrar("sub", BASE + "/#", "");
});
cliente.on("reconnect", () => {
  $("pillConexao").textContent = "reconectando...";
  $("pillConexao").className = "pill";
});
cliente.on("close", () => {
  $("pillConexao").textContent = "desconectado";
  $("pillConexao").className = "pill off";
});
cliente.on("error", (e) => registrar("sub", "erro", e.message));
cliente.on("message", (topico, payload) => {
  const texto = payload.toString();
  registrar("rx", topico.replace(BASE + "/", ""), texto);
  let dados = texto;
  try {
    dados = JSON.parse(texto);
  } catch (e) {}
  tratar(topico.replace(BASE + "/", ""), dados);
});

function enviar(cps, comando) {
  const topico = BASE + "/" + cps + "/comando";
  const texto = JSON.stringify(comando);
  cliente.publish(topico, texto);
  registrar("tx", cps + "/comando", texto);
}

function tratar(nome, d) {
  switch (nome) {
    case "cps1/sensor":
      $("temp").textContent = d.temp;
      $("umid").textContent = d.umid;
      $("limite1").textContent = d.limite;
      break;
    case "cps1/alerta":
      estado.alerta = d.condicao === "CALOR";
      $("alerta1").textContent = estado.alerta
        ? "CALOR: " +
          d.temp +
          " °C (limite " +
          d.limite +
          "). CPS 2 abre a janela e CPS 3 irriga mais cedo."
        : "Normal: " + d.temp + " °C (limite " + d.limite + ").";
      atualizarResumo();
      break;
    case "cps1/estado":
      setLed("ledAlerta", d.led_alerta === "on");
      setLed("ledIrrig", d.led_irrig === "on");
      modo("modo1", d.modo);
      break;
    case "cps2/sensor":
      $("luz").textContent = d.luz;
      $("periodo").textContent = d.periodo;
      break;
    case "cps2/estado":
      estado.janela = d.janela === "aberta";
      $("janela").textContent = d.janela;
      setLed("ledJanela", estado.janela);
      setLed("ledLuz", d.luz === "on");
      $("motivo2").textContent = d.motivo;
      modo("modo2", d.modo);
      atualizarResumo();
      break;
    case "cps3/sensor":
      $("solo").textContent = d.solo;
      $("limBase").textContent = d.limite_base;
      $("limEf").textContent = d.limite_efetivo;
      break;
    case "cps3/estado":
      estado.bomba = d.bomba === "ligada";
      setLed("ledBomba", estado.bomba);
      $("motivo3").textContent = "Bomba " + d.bomba + " — " + d.motivo;
      modo("modo3", d.modo);
      atualizarResumo();
      break;
    case "cps1/status":
    case "cps2/status":
    case "cps3/status": {
      const el = $("status" + nome[3]);
      el.textContent = d;
      el.className = "pill " + (d === "online" ? "on" : "off");
      break;
    }
  }
}

function modo(id, m) {
  $(id).textContent = m;
  $(id).classList.toggle("manual", m === "manual");
}

function atualizarResumo() {
  const partes = [
    estado.alerta ? "CPS 1 em CALOR" : "CPS 1 normal",
    estado.janela ? "janela aberta" : "janela fechada",
    estado.bomba ? "bomba ligada" : "bomba desligada",
  ];
  $("resumo").textContent = partes.join("  ·  ");
}

function registrar(tipo, topico, texto) {
  const linha = document.createElement("div");
  linha.className = tipo;
  const rotulo = { rx: "recebido ", tx: "enviado  ", sub: "assinou   " }[tipo];
  linha.textContent =
    new Date().toLocaleTimeString() + "  " + rotulo + topico + "  " + texto;
  const log = $("log");
  log.appendChild(linha);
  while (log.children.length > 80) log.removeChild(log.firstChild);
  log.scrollTop = log.scrollHeight;
}
