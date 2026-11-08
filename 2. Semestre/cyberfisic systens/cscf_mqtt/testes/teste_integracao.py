#!/usr/bin/env python3
"""
Teste automático dos 3 main.py (CPS1, CPS2, CPS3).

Como funciona:
  - sobe um broker Mosquitto local (porta 18830)
  - roda os 3 main.py no MicroPython do PC (versão "unix"), com módulos de
    mentira (stubs/) no lugar de machine/network/dht, que leem e escrevem
    arquivos em vez de pinos de verdade
  - um cliente paho-mqtt faz o papel do dashboard
  - altera os "sensores" e confere se os "atuadores" e as mensagens MQTT estão certos

Uso:  python3 teste_integracao.py            (precisa de mosquitto, micropython e paho-mqtt)
      python3 teste_integracao.py --real     (usa o broker.hivemq.com de verdade)
"""
import json, os, re, shutil, subprocess, sys, tempfile, time
import paho.mqtt.client as mqtt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
REAL = "--real" in sys.argv
EQUIPE = "teste" + str(int(time.time()) % 100000) if REAL else "teste"
BROKER, PORTA = ("broker.hivemq.com", 1883) if REAL else ("127.0.0.1", 18830)
TMP = tempfile.mkdtemp(prefix="cscf_")
procs, mosq = {}, None
falhas = []

def ok(cond, nome):
    print(("  [OK]    " if cond else "  [FALHA] ") + nome)
    if not cond:
        falhas.append(nome)

def esperar(fn, tempo=12):
    fim = time.time() + tempo
    while time.time() < fim:
        if fn():
            return True
        time.sleep(0.2)
    return False

# ---------------- preparação ----------------
def iniciar_mosquitto():
    global mosq
    conf = os.path.join(TMP, "mosq.conf")
    open(conf, "w").write("listener %d 127.0.0.1\nallow_anonymous true\n" % PORTA)
    mosq = subprocess.Popen(["mosquitto", "-c", conf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

def preparar(nome, pasta):
    """Copia o main.py trocando só broker, porta, equipe e intervalo."""
    codigo = open(os.path.join(RAIZ, pasta, "main.py"), encoding="utf-8").read()
    codigo = re.sub(r'BROKER = ".*?"', 'BROKER = "%s"' % BROKER, codigo)
    codigo = re.sub(r'PORTA = \d+', 'PORTA = %d' % PORTA, codigo)
    codigo = re.sub(r'EQUIPE = ".*?"', 'EQUIPE = "%s"' % EQUIPE, codigo)
    codigo = re.sub(r'INTERVALO_MS = \d+', 'INTERVALO_MS = 500', codigo)
    d = os.path.join(TMP, nome)
    os.makedirs(os.path.join(d, "hw"), exist_ok=True)
    open(os.path.join(d, "main.py"), "w", encoding="utf-8").write(codigo)
    return d

def iniciar(nome, pasta):
    d = preparar(nome, pasta)
    env = dict(os.environ, HW_DIR=os.path.join(d, "hw"),
               MICROPYPATH=os.path.join(AQUI, "stubs") + ":" + os.path.join(AQUI, "lib"))
    log = open(os.path.join(d, "saida.log"), "w")
    procs[nome] = subprocess.Popen(["micropython", "main.py"], cwd=d, env=env, stdout=log, stderr=subprocess.STDOUT)
    return d

def hw(nome, arq, valor=None, padrao=None):
    caminho = os.path.join(TMP, nome, "hw", arq)
    if valor is None:
        try:
            return open(caminho).read().strip()
        except OSError:
            return padrao
    if valor == "":
        if os.path.exists(caminho): os.remove(caminho)
    else:
        open(caminho, "w").write(str(valor))

def angulo_servo():
    duty = int(hw("cps2", "pwm_18", padrao="0"))
    return round(((duty * 20000 / 65535) - 500) * 180 / 2000)

# ---------------- "dashboard" ----------------
msgs = {}        # último JSON por tópico
conta = {}       # quantas mensagens por tópico
def ao_msg(c, u, m):
    t = m.topic.replace("cscf/%s/" % EQUIPE, "")
    conta[t] = conta.get(t, 0) + 1
    try:
        msgs[t] = json.loads(m.payload)
    except ValueError:
        msgs[t] = m.payload.decode()

dash = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
dash.on_message = ao_msg
dash.on_connect = lambda c, u, f, rc, p=None: c.subscribe("cscf/%s/#" % EQUIPE)
def comando(sistema, dados):
    dash.publish("cscf/%s/%s/comando" % (EQUIPE, sistema), json.dumps(dados) if not isinstance(dados, str) else dados)

# ---------------- cenários ----------------
def main():
    global mosq
    print("Broker: %s:%d | equipe: %s" % (BROKER, PORTA, EQUIPE))
    if not REAL:
        iniciar_mosquitto()
    # sensores iniciais: 24 °C, solo ~54 %, luz ~76 %
    for n, p in [("cps1", "cps1"), ("cps2", "cps2"), ("cps3", "cps3")]:
        d = preparar(n, p)
    hw("cps1", "dht_temp", 24); hw("cps3", "adc_35", 2201); hw("cps2", "adc_34", 3100)
    dash.connect(BROKER, PORTA); dash.loop_start()
    dash.subscribe("cscf/%s/#" % EQUIPE)
    for n, p in [("cps1", "cps1"), ("cps2", "cps2"), ("cps3", "cps3")]:
        iniciar(n, p)

    print("\n1) Conexão, publicação e status")
    ok(esperar(lambda: all(k in msgs for k in ["cps1/sensor", "cps2/sensor", "cps3/sensor"])), "os 3 CPS publicam seus sensores")
    ok(all(msgs.get("cps%d/status" % i) == "online" for i in (1, 2, 3)), "status online (retido) dos 3 CPS")
    ok(msgs["cps1/sensor"]["temp"] == 24.0 and msgs["cps3/sensor"]["solo"] == 53, "valores dos sensores chegam corretos: %s / %s" % (msgs["cps1/sensor"], msgs["cps3/sensor"]))
    ok(msgs["cps2/sensor"]["periodo"] == "dia", "CPS2 classifica 'dia'")
    ok(angulo_servo() == 0 and hw("cps3", "out_26") == "0", "estado inicial: janela fechada e bomba desligada")

    antes = {k: conta.get(k, 0) for k in ("cps1/alerta", "cps1/estado", "cps2/estado", "cps3/estado")}
    time.sleep(3)
    ok(all(conta.get(k, 0) == antes[k] for k in antes), "sem mudanças, ninguém republica alerta/estado (sem laço de mensagens entre os CPS)")

    print("\n2) Integração: calor no CPS1 -> janela (CPS2) -> bomba (CPS3) -> LED azul (CPS1)")
    hw("cps1", "dht_temp", 35)
    ok(esperar(lambda: msgs.get("cps1/alerta", {}).get("condicao") == "CALOR"), "CPS1 publica alerta CALOR")
    ok(hw("cps1", "out_2") == "1", "CPS1 acende o LED vermelho")
    ok(esperar(lambda: angulo_servo() == 90), "CPS2 recebe o alerta e ABRE a janela (servo 90°)")
    ok(esperar(lambda: msgs.get("cps2/estado", {}).get("janela") == "aberta"), "CPS2 publica estado 'aberta'")
    ok(esperar(lambda: msgs.get("cps3/estado", {}).get("limite_efetivo") == 60), "CPS3 sobe o limite efetivo para 60 (30+20+10)")
    ok(esperar(lambda: hw("cps3", "out_26") == "1" and hw("cps3", "out_27") == "1"), "CPS3 liga relé e LED da bomba (solo 53% < 60%)")
    ok(esperar(lambda: hw("cps1", "out_4") == "1"), "CPS1 acende o LED azul ao saber que a bomba ligou (CPS3 -> CPS1)")
    print("     motivo CPS3:", msgs["cps3/estado"]["motivo"])

    print("\n3) Volta ao normal")
    hw("cps1", "dht_temp", 22)
    ok(esperar(lambda: msgs.get("cps1/alerta", {}).get("condicao") == "NORMAL"), "CPS1 publica NORMAL")
    ok(esperar(lambda: angulo_servo() == 0), "CPS2 fecha a janela")
    ok(esperar(lambda: hw("cps3", "out_26") == "0"), "CPS3 desliga a bomba")
    ok(esperar(lambda: hw("cps1", "out_4") == "0" and hw("cps1", "out_2") == "0"), "CPS1 apaga os dois LEDs")

    print("\n4) Comandos do dashboard")
    comando("cps2", {"janela": "abrir"})
    ok(esperar(lambda: angulo_servo() == 90 and msgs["cps2/estado"]["modo"] == "manual"), "CPS2: comando janela=abrir (modo manual)")
    comando("cps2", {"luz": "on"})
    ok(esperar(lambda: hw("cps2", "out_5") == "1"), "CPS2: comando luz=on")
    comando("cps2", {"modo": "auto"})
    ok(esperar(lambda: angulo_servo() == 0 and hw("cps2", "out_5") == "0"), "CPS2: volta ao automático")
    comando("cps3", {"bomba": "on"})
    ok(esperar(lambda: hw("cps3", "out_26") == "1" and msgs["cps3/estado"]["modo"] == "manual"), "CPS3: comando bomba=on")
    ok(esperar(lambda: hw("cps1", "out_4") == "1"), "CPS1 reflete a bomba ligada pelo dashboard")
    comando("cps3", {"modo": "auto"})
    ok(esperar(lambda: hw("cps3", "out_26") == "0"), "CPS3: volta ao automático")
    comando("cps1", {"led_alerta": "on"})
    ok(esperar(lambda: hw("cps1", "out_2") == "1" and msgs["cps1/estado"]["modo"] == "manual"), "CPS1: comando led_alerta=on")
    comando("cps1", {"modo": "auto"})
    ok(esperar(lambda: hw("cps1", "out_2") == "0"), "CPS1: volta ao automático")
    comando("cps1", {"limite": 20})
    ok(esperar(lambda: msgs.get("cps1/alerta", {}).get("condicao") == "CALOR"), "CPS1: baixar o limite para 20 °C gera alerta (22 °C >= 20)")
    ok(esperar(lambda: angulo_servo() == 90), "   ... e isso abre a janela do CPS2")
    comando("cps1", {"limite": 30})
    ok(esperar(lambda: msgs.get("cps1/alerta", {}).get("condicao") == "NORMAL"), "CPS1: limite de volta a 30 °C")
    comando("cps3", {"limite_solo": 60})
    ok(esperar(lambda: hw("cps3", "out_26") == "1"), "CPS3: limite_solo=60 liga a bomba (solo 53%)")
    comando("cps3", {"limite_solo": 30})
    ok(esperar(lambda: hw("cps3", "out_26") == "0"), "CPS3: limite_solo=30 desliga a bomba")

    print("\n5) Mensagens inválidas não derrubam os sistemas")
    for s in ("cps1", "cps2", "cps3"):
        comando(s, "isto não é json")
        comando(s, "123")
    n0 = conta.get("cps1/sensor", 0)
    time.sleep(2)
    ok(conta.get("cps1/sensor", 0) > n0 and all(p.poll() is None for p in procs.values()), "os 3 continuam rodando e publicando")

    print("\n6) Luminosidade: noite liga a iluminação")
    hw("cps2", "adc_34", 400)
    ok(esperar(lambda: msgs["cps2/sensor"]["periodo"] == "noite" and hw("cps2", "out_5") == "1"), "CPS2: pouca luz -> 'noite' e LED de iluminação ligado")
    hw("cps2", "adc_34", 3100)
    ok(esperar(lambda: hw("cps2", "out_5") == "0"), "CPS2: luz volta -> 'dia' e LED apagado")

    print("\n7) Queda de Wi-Fi do CPS1 (simulada)")
    hw("cps1", "wifi_down", "1")
    time.sleep(3)
    n0 = conta.get("cps1/sensor", 0)
    time.sleep(2)
    ok(conta.get("cps1/sensor", 0) == n0, "sem Wi-Fi o CPS1 para de publicar")
    hw("cps1", "wifi_down", "")
    ok(esperar(lambda: conta.get("cps1/sensor", 0) > n0, 25), "Wi-Fi volta: CPS1 reconecta ao Wi-Fi e ao MQTT e volta a publicar")

    print("\n8) Queda do broker MQTT" + (" (pulado no broker real)" if REAL else ""))
    if not REAL:
        mosq.terminate(); mosq.wait()
        time.sleep(3)
        n = {k: conta.get(k, 0) for k in ("cps1/sensor", "cps2/sensor", "cps3/sensor")}
        mosq = None
        iniciar_mosquitto()
        ok(esperar(lambda: all(conta.get(k, 0) > n[k] for k in n), 40), "broker volta: os 3 CPS reconectam sozinhos e voltam a publicar")
        ok(esperar(lambda: all(msgs.get("cps%d/status" % i) == "online" for i in (1, 2, 3))), "status 'online' republicado")
        hw("cps1", "dht_temp", 36)
        ok(esperar(lambda: angulo_servo() == 90, 20), "a integração continua funcionando depois da reconexão")

    print("\nResultado:", "TUDO OK" if not falhas else "%d FALHA(S): %s" % (len(falhas), falhas))

try:
    main()
finally:
    for p in procs.values():
        p.terminate()
    dash.loop_stop()
    if mosq:
        mosq.terminate()
    if falhas:
        print("Logs em", TMP)
    else:
        shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if falhas else 0)
