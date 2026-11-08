# =====================================================================
# CPS 2 - VENTILAÇÃO E ILUMINAÇÃO DA ESTUFA
# Disciplina: Conectividade de Sistemas Ciberfísicos (CSCF 2026.2)
# Plataforma: ESP32 + MicroPython (Wokwi)
#
# Sensor   : LDR (luminosidade)               -> GPIO 34 (analógico)
# Atuadores: Servo motor = janela da estufa   -> GPIO 18 (PWM)
#            LED branco = iluminação          -> GPIO 5
#
# O que este sistema faz:
#  1. Lê a luminosidade, classifica em "dia" ou "noite" e publica.
#  2. Escuta o alerta do CPS1: se for "CALOR", ABRE a janela (servo 90°).
#     Quando volta ao normal, fecha. (CPS1 -> CPS2)
#  3. Liga a iluminação à noite (decisão com o sensor local).
#  4. Recebe comandos do dashboard (modo, janela, luz).
#  5. Publica o estado da janela para o CPS3 usar (CPS2 -> CPS3).
# =====================================================================

import network
import time
import ujson
import random
from machine import Pin, ADC, PWM
from umqtt.simple import MQTTClient

# ---------------------- CONFIGURAÇÃO ----------------------
WIFI_SSID = "Wokwi-GUEST"
WIFI_SENHA = ""
BROKER = "broker.hivemq.com"
PORTA = 1883
EQUIPE = "zupeli_vilela_dib"
INTERVALO_MS = 3000

BASE = "cscf/" + EQUIPE
ID_CLIENTE = "cps2-" + EQUIPE + "-" + str(random.getrandbits(16))

# Tópicos que este sistema PUBLICA
T_SENSOR = BASE + "/cps2/sensor"
T_ESTADO = BASE + "/cps2/estado"
T_STATUS = BASE + "/cps2/status"
# Tópicos que este sistema ASSINA
T_COMANDO = BASE + "/cps2/comando"
T_ALERTA_CPS1 = BASE + "/cps1/alerta"    # vem do CPS1

# ---------------------- HARDWARE ----------------------
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)                 # leitura de 0 a 3,3 V
servo = PWM(Pin(18), freq=50)            # servo trabalha com pulsos a 50 Hz
led_luz = Pin(5, Pin.OUT)

ANGULO_ABERTA = 90
ANGULO_FECHADA = 0

# ---------------------- ESTADO DO SISTEMA ----------------------
luz = None               # luminosidade em % (0 a 100)
periodo = "dia"          # "dia" ou "noite"
calor_cps1 = False       # último alerta recebido do CPS1
angulo = ANGULO_FECHADA
luz_ligada = False
modo = "auto"
janela_manual = False    # usado só no modo manual
luz_manual = False
motivo = "iniciando"
ultimo_estado = None     # último estado publicado (só publica de novo se mudar)

wlan = network.WLAN(network.STA_IF)
cliente = None


def mover_servo(graus):
    """Converte o ângulo (0-180) em pulso de 0,5 a 2,5 ms e aplica no servo."""
    pulso_us = 500 + graus * 2000 // 180
    servo.duty_u16(pulso_us * 65535 // 20000)    # período de 20 ms (50 Hz)


# ---------------------- WI-FI ----------------------
def conectar_wifi():
    wlan.active(True)
    if wlan.isconnected():
        return True
    print("Conectando ao Wi-Fi", end="")
    wlan.connect(WIFI_SSID, WIFI_SENHA)
    for _ in range(100):
        if wlan.isconnected():
            print(" conectado!")
            return True
        print(".", end="")
        time.sleep(0.1)
    print(" falhou, tentando de novo...")
    return False


# ---------------------- MQTT ----------------------
def conectar_mqtt():
    global cliente, ultimo_estado
    print("Conectando ao broker", BROKER, "...")
    c = MQTTClient(ID_CLIENTE, BROKER, port=PORTA, keepalive=30)
    c.set_callback(ao_receber)
    c.set_last_will(T_STATUS, b"offline", retain=True)
    c.connect()
    c.subscribe(T_COMANDO)
    c.subscribe(T_ALERTA_CPS1)
    c.publish(T_STATUS, b"online", retain=True)
    cliente = c
    ultimo_estado = None               # depois de reconectar, republica o estado
    print("MQTT conectado!")


def ao_receber(topico, mensagem):
    """Chamada automaticamente sempre que chega uma mensagem MQTT."""
    global calor_cps1, modo, janela_manual, luz_manual
    topico = topico.decode()
    print("RECEBIDO", topico, mensagem)
    try:
        dados = ujson.loads(mensagem)
    except ValueError:
        print("Mensagem inválida (não é JSON), ignorada")
        return
    if not isinstance(dados, dict):
        return

    if topico == T_ALERTA_CPS1:
        # Informação vinda de OUTRO sistema: o CPS1 detectou calor?
        calor_cps1 = (dados.get("condicao") == "CALOR")
        decidir_e_atuar()              # reage na hora, sem esperar o próximo ciclo

    elif topico == T_COMANDO:
        # Exemplos: {"modo":"auto"}  {"janela":"abrir"}  {"luz":"on"}
        if "modo" in dados and dados["modo"] in ("auto", "manual"):
            modo = dados["modo"]
        if "janela" in dados:
            janela_manual = (dados["janela"] == "abrir")
            modo = "manual"
        if "luz" in dados:
            luz_manual = (dados["luz"] == "on")
            modo = "manual"
        decidir_e_atuar()


def publicar(topico, dados, retida=False):
    # .encode() transforma o texto em bytes UTF-8: sem isso, letras com acento
    # (ç, ã...) fazem a mensagem sair maior que o tamanho declarado e chegar cortada
    cliente.publish(topico, ujson.dumps(dados).encode(), retain=retida)


# ---------------------- LÓGICA DO SISTEMA ----------------------
def ler_luminosidade():
    """Lê o LDR e classifica em dia/noite (com histerese para não ficar piscando)."""
    global luz, periodo
    luz = ldr.read() * 100 // 4095
    if luz < 30:
        periodo = "noite"
    elif luz >= 35:
        periodo = "dia"


def decidir_e_atuar():
    """Decide o que fazer com a janela e com a luz e aciona os atuadores."""
    global angulo, luz_ligada, motivo
    if modo == "auto":
        abrir = calor_cps1                 # decisão baseada em dado REMOTO (CPS1)
        acender = (periodo == "noite")     # decisão baseada em dado LOCAL (LDR)
        motivo = "alerta de calor do CPS1" if abrir else "sem alerta de calor"
    else:
        abrir = janela_manual
        acender = luz_manual
        motivo = "comando manual do dashboard"

    angulo = ANGULO_ABERTA if abrir else ANGULO_FECHADA
    luz_ligada = acender
    mover_servo(angulo)
    led_luz.value(1 if luz_ligada else 0)


def publicar_mudancas():
    """Publica o estado dos atuadores, mas só quando mudou (evita mensagens repetidas)."""
    global ultimo_estado
    estado = {
        "sistema": "CPS2", "modo": modo,
        "janela": "aberta" if angulo == ANGULO_ABERTA else "fechada",
        "angulo": angulo,
        "luz": "on" if luz_ligada else "off",
        "motivo": motivo,
    }
    if estado != ultimo_estado:
        # retido: o CPS3 e o dashboard recebem o último estado mesmo se conectarem depois
        publicar(T_ESTADO, estado, retida=True)
        ultimo_estado = estado
        print("Janela:", angulo, "graus | luz:", luz_ligada, "|", motivo)


def ciclo():
    ler_luminosidade()
    decidir_e_atuar()
    publicar(T_SENSOR, {"sistema": "CPS2", "luz": luz, "periodo": periodo})


# ---------------------- PROGRAMA PRINCIPAL ----------------------
print("CPS2 - Ventilação e iluminação iniciando")
mover_servo(ANGULO_FECHADA)
ultimo_ciclo = time.ticks_add(time.ticks_ms(), -INTERVALO_MS)
ultimo_ping = time.ticks_ms()
tentativas = 0

while True:
    try:
        if not conectar_wifi():
            cliente = None
            time.sleep(2)
            continue
        if cliente is None:
            conectar_mqtt()
            tentativas = 0
        cliente.check_msg()
        agora = time.ticks_ms()
        if time.ticks_diff(agora, ultimo_ciclo) >= INTERVALO_MS:
            ultimo_ciclo = agora
            ciclo()
        publicar_mudancas()
        if time.ticks_diff(agora, ultimo_ping) >= 15000:
            ultimo_ping = agora
            cliente.ping()
        time.sleep_ms(100)
    except Exception as erro:
        tentativas += 1
        espera = min(2 * tentativas, 10)
        print("Falha de conexão:", erro, "- nova tentativa em", espera, "s")
        try:
            cliente.disconnect()
        except Exception:
            pass
        cliente = None
        time.sleep(espera)
