const MQTT_BROKER = "wss://broker.hivemq.com:8884/mqtt";
const MQTT_TOPICO_BASE = "smartcity/bueiro";

const LIMITE_ATENCAO = 50;
const LIMITE_PERIGO = 80;

const niveis = { 1: 0, 2: 0, 3: 0 };

const niveisPrev = { 1: 0, 2: 0, 3: 0 };

let bueiroSelecionado = null;

const estiloExtra = document.createElement("style");
estiloExtra.textContent = `
  .bueiro.perigo .alerta-icone {
    display: block;
    background: #e53935;
    color: #fff;
    animation: pulsar 0.5s infinite;
  }

  .lista-item .ponto.perigo { background: #e53935; }

  .badge-status {
    display: block;
    margin: 0 0 14px;
    padding: 8px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: bold;
  }
  .badge-status.normal  { background: #43a047; color: #fff; }
  .badge-status.atencao { background: #f2c94c; color: #1c1c24; }
  .badge-status.perigo  {
    background: #e53935;
    color: #fff;
    animation: piscarBadge 0.8s infinite;
  }
  @keyframes piscarBadge {
    0%, 100% { opacity: 1; }
    50%      { opacity: 0.35; }
  }
`;
document.head.appendChild(estiloExtra);

const badgeStatus = document.createElement("span");
badgeStatus.className = "badge-status normal";
badgeStatus.textContent = "Nível Normal";
const popupEl = document.querySelector(".popup");
popupEl.insertBefore(badgeStatus, popupEl.firstChild);

const bannerAlerta = document.createElement("div");
bannerAlerta.style.cssText =
  "position:fixed; top:0; left:0; width:100%;" +
  "background:rgba(220,38,38,0.92); color:#fff;" +
  "padding:12px 24px; font-weight:bold; text-align:center;" +
  "z-index:9999; transition:opacity 0.5s; opacity:0; display:none;";
document.body.appendChild(bannerAlerta);
let timerBanner = null;

const SOM_ATENCAO = { frequencia: 620, duracao: 0.15, vezes: 2, intervalo: 0.2 };
const SOM_PERIGO  = { frequencia: 960, duracao: 0.10, vezes: 3, intervalo: 0.15 };

let audioCtx = null;

function obterAudioContext() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === "suspended") audioCtx.resume();
  return audioCtx;
}

function criarSom(frequencia, duracao, vezes, intervalo) {
  try {
    const ctx = obterAudioContext();
    for (let i = 0; i < vezes; i++) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "square";
      osc.frequency.value = frequencia;
      osc.connect(gain);
      gain.connect(ctx.destination);

      const inicio = ctx.currentTime + i * intervalo;
      gain.gain.setValueAtTime(0.2, inicio);
      gain.gain.exponentialRampToValueAtTime(0.001, inicio + duracao);
      osc.start(inicio);
      osc.stop(inicio + duracao);
    }
  } catch (e) {
  }
}

function verificarSom(id, valor) {
  const anterior = niveisPrev[id];
  if (anterior < LIMITE_PERIGO && valor >= LIMITE_PERIGO) {
    criarSom(SOM_PERIGO.frequencia, SOM_PERIGO.duracao, SOM_PERIGO.vezes, SOM_PERIGO.intervalo);
  } else if (anterior < LIMITE_ATENCAO && valor >= LIMITE_ATENCAO) {
    criarSom(SOM_ATENCAO.frequencia, SOM_ATENCAO.duracao, SOM_ATENCAO.vezes, SOM_ATENCAO.intervalo);
  }
  niveisPrev[id] = valor;
}

const CIDADE_BASE = 700;
const cidadeEl = document.getElementById("cidade");
const cidadeWrapper = document.getElementById("cidadeWrapper");

function ajustarEscalaCidade() {
  const margem = 80;
  const disponivelLargura = (window.innerWidth - margem) / 2;
  const disponivelAltura = window.innerHeight - 150;

  let escala = Math.min(disponivelLargura / CIDADE_BASE, disponivelAltura / CIDADE_BASE);
  escala = Math.max(0.5, escala);

  cidadeEl.style.transform = "scale(" + escala + ")";
  cidadeWrapper.style.width = CIDADE_BASE * escala + "px";
  cidadeWrapper.style.height = CIDADE_BASE * escala + "px";
}

window.addEventListener("resize", ajustarEscalaCidade);
ajustarEscalaCidade();

function atualizarBueiro(id, valor) {
  valor = Math.max(0, Math.min(100, Math.round(valor)));

  verificarSom(id, valor);
  niveis[id] = valor;

  const el = document.querySelector('.bueiro[data-id="' + id + '"]');
  if (el) {
    el.classList.toggle("cheio", valor > 0);
    el.classList.toggle("atencao", valor >= LIMITE_ATENCAO && valor < LIMITE_PERIGO);
    el.classList.toggle("perigo", valor >= LIMITE_PERIGO);
    el.querySelector(".alerta-icone").textContent =
      valor >= LIMITE_PERIGO ? "!!" : "!";
  }

  atualizarListaPainel(id, valor);
  atualizarBanner();

  if (bueiroSelecionado === id) renderizarPopup(id);
}

function atualizarListaPainel(id, valor) {
  const item = document.querySelector('.lista-item[data-id="' + id + '"]');
  if (!item) return;
  item.querySelector(".valor").textContent = valor + "%";

  const ponto = item.querySelector(".ponto");
  ponto.classList.remove("cheio", "atencao", "perigo");
  if (valor >= LIMITE_PERIGO) {
    ponto.classList.add("perigo");
  } else if (valor >= LIMITE_ATENCAO) {
    ponto.classList.add("atencao");
  }
}

function atualizarBanner() {
  let pior = null;
  [1, 2, 3].forEach(function (id) {
    if (niveis[id] >= LIMITE_PERIGO && (pior === null || niveis[id] > niveis[pior])) {
      pior = id;
    }
  });

  if (pior !== null) {
    clearTimeout(timerBanner);
    bannerAlerta.textContent =
      "⚠️ ALERTA: Bueiros em nível crítico! Risco de alagamento.";
    bannerAlerta.style.display = "block";
    requestAnimationFrame(function () {
      bannerAlerta.style.opacity = "1";
    });
  } else if (bannerAlerta.style.display === "block") {
    bannerAlerta.style.opacity = "0";
    clearTimeout(timerBanner);
    timerBanner = setTimeout(function () {
      bannerAlerta.style.display = "none";
    }, 500);
  }
}

function renderizarPopup(id) {
  const valor = niveis[id];
  document.getElementById("popupTitulo").textContent = "Bueiro " + id;
  document.getElementById("popupNivel").textContent = valor + "%";
  document.getElementById("popupAgua").style.height = valor + "%";

  if (valor >= LIMITE_PERIGO) {
    badgeStatus.className = "badge-status perigo";
    badgeStatus.textContent = "PERIGO: Risco de alagamento!";
  } else if (valor >= LIMITE_ATENCAO) {
    badgeStatus.className = "badge-status atencao";
    badgeStatus.textContent = "Atenção: Bueiro sobrecarregado";
  } else {
    badgeStatus.className = "badge-status normal";
    badgeStatus.textContent = "Nível Normal";
  }

  const alerta = document.getElementById("popupAlerta");
  if (valor >= LIMITE_PERIGO) {
    alerta.className = "alerta perigo";
    alerta.textContent = "Risco de alagamento! Nível crítico.";
  } else if (valor <= 30) {
    alerta.className = "alerta ok";
    alerta.textContent = "Nível normal.";
  } else {
    alerta.className = "alerta";
    alerta.textContent = "";
  }
}

document.querySelectorAll(".bueiro").forEach(function (b) {
  b.addEventListener("click", function () {
    bueiroSelecionado = parseInt(b.dataset.id, 10);
    renderizarPopup(bueiroSelecionado);
    document.getElementById("overlay").classList.add("aberto");
  });
});

document.getElementById("btnFechar").addEventListener("click", fecharPopup);
document.getElementById("overlay").addEventListener("click", function (e) {
  if (e.target.id === "overlay") fecharPopup();
});
function fecharPopup() {
  document.getElementById("overlay").classList.remove("aberto");
  bueiroSelecionado = null;
}

document.getElementById("knobH").style.display = "none";
const knobDica = document.querySelector(".knob-dica");
if (knobDica) knobDica.style.display = "none";

const bolinha = document.getElementById("bolinhaStatus");
const textoStatus = document.getElementById("textoStatus");

function statusConectado() {
  bolinha.classList.add("online");
  textoStatus.textContent = "Conectado ao ESP32";
}

function statusDesconectado() {
  bolinha.classList.remove("online");
  textoStatus.textContent = "Desconectado";
}

try {
  const client = mqtt.connect(MQTT_BROKER, {
    clientId: "html-smartcity-" + Math.random().toString(16).slice(2, 10),
    reconnectPeriod: 5000,
  });

  client.on("connect", function () {
    statusConectado();
    client.subscribe(MQTT_TOPICO_BASE + "/+");
  });

  client.on("message", function (topico, mensagem) {
    const partes = topico.split("/");
    const id = parseInt(partes[partes.length - 1], 10);
    const valor = parseFloat(mensagem.toString());
    if ([1, 2, 3].includes(id) && !isNaN(valor)) {
      atualizarBueiro(id, valor);
    }
  });

  client.on("error", statusDesconectado);
  client.on("close", statusDesconectado);
  client.on("offline", statusDesconectado);
} catch (e) {
  statusDesconectado();
}
