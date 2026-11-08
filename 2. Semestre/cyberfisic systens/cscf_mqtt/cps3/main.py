# =====================================================================
# CPS 3 - IRRIGAÇÃO DA ESTUFA
# Disciplina: Conectividade de Sistemas Ciberfísicos (CSCF 2026.2)
# Plataforma: ESP32 + MicroPython (Wokwi)
#
# Sensor   : Potenciômetro = umidade do solo  -> GPIO 35 (analógico)
# Atuadores: Módulo relé = bomba d'água       -> GPIO 26
#            LED verde = indicador da bomba   -> GPIO 27
#
# O que este sistema faz:
#  1. Lê a umidade do solo (0 a 100%) e publica.
#  2. Liga a bomba quando o solo está mais seco que o "limite efetivo".
#  3. O limite efetivo depende de DADOS DE OUTROS SISTEMAS:
#       - alerta de CALOR do CPS1  -> irriga mais cedo (+20)
#       - janela aberta do CPS2    -> o ar seca mais o solo (+10)
#  4. Publica o estado da bomba (o CPS1 acende o LED azul com isso).
#  5. Recebe comandos do dashboard (modo, bomba, limite).
# =====================================================================

import network
import time
import ujson
import random
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# ---------------------- CONFIGURAÇÃO ----------------------
WIFI_SSID = "Wokwi-GUEST"
WIFI_SENHA = ""
BROKER = "broker.hivemq.com"
PORTA = 1883
EQUIPE = "zupeli_vilela_dib"
INTERVALO_MS = 3000

BASE = "cscf/" + EQUIPE
ID_CLIENTE = "cps3-" + EQUIPE + "-" + str(random.getrandbits(16))

# Tópicos que este sistema PUBLICA
T_SENSOR = BASE + "/cps3/sensor"
T_ESTADO = BASE + "/cps3/estado"
T_STATUS = BASE + "/cps3/status"
# Tópicos que este sistema ASSINA
T_COMANDO = BASE + "/cps3/comando"
T_ALERTA_CPS1 = BASE + "/cps1/alerta"    # vem do CPS1
T_ESTADO_CPS2 = BASE + "/cps2/estado"    # vem do CPS2

# ---------------------- HARDWARE ----------------------
solo_adc = ADC(Pin(35))
solo_adc.atten(ADC.ATTN_11DB)
rele = Pin(26, Pin.OUT)
led_bomba = Pin(27, Pin.OUT)

# ---------------------- ESTADO DO SISTEMA ----------------------
solo = None                # umidade do solo em %
limite_base = 30           # abaixo disso o solo está seco (pode ser mudado pelo dashboard)
limite_efetivo = 30
calor_cps1 = False         # informação do CPS1
janela_aberta = False      # informação do CPS2
bomba = False
modo = "auto"
bomba_manual = False
motivo = "iniciando"
ultimo_estado = None       # último estado publicado (só publica de novo se mudar)

wlan = network.WLAN(network.STA_IF)
cliente = None


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
    c.subscribe(T_ESTADO_CPS2)
    c.publish(T_STATUS, b"online", retain=True)
    cliente = c
    ultimo_estado = None               # depois de reconectar, republica o estado
    print("MQTT conectado!")


def ao_receber(topico, mensagem):
    """Chamada automaticamente sempre que chega uma mensagem MQTT."""
    global calor_cps1, janela_aberta, limite_base, modo, bomba_manual
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
        calor_cps1 = (dados.get("condicao") == "CALOR")
        decidir_e_atuar()              # reage na hora, sem esperar o próximo ciclo

    elif topico == T_ESTADO_CPS2:
        janela_aberta = (dados.get("janela") == "aberta")
        decidir_e_atuar()

    elif topico == T_COMANDO:
        # Exemplos: {"modo":"auto"}  {"bomba":"on"}  {"limite_solo":40}
        if "modo" in dados and dados["modo"] in ("auto", "manual"):
            modo = dados["modo"]
        if "limite_solo" in dados:
            try:
                limite_base = int(dados["limite_solo"])
            except (ValueError, TypeError):
                pass
        if "bomba" in dados:
            bomba_manual = (dados["bomba"] == "on")
            modo = "manual"
        decidir_e_atuar()


def publicar(topico, dados, retida=False):
    # .encode() transforma o texto em bytes UTF-8: sem isso, letras com acento
    # (ç, ã...) fazem a mensagem sair maior que o tamanho declarado e chegar cortada
    cliente.publish(topico, ujson.dumps(dados).encode(), retain=retida)


# ---------------------- LÓGICA DO SISTEMA ----------------------
def ler_solo():
    global solo
    solo = solo_adc.read() * 100 // 4095


def decidir_e_atuar():
    """Calcula o limite efetivo (com dados dos outros CPS) e decide sobre a bomba."""
    global limite_efetivo, bomba, motivo
    limite_efetivo = limite_base
    partes = []
    if calor_cps1:
        limite_efetivo += 20
        partes.append("calor no CPS1 (+20)")
    if janela_aberta:
        limite_efetivo += 10
        partes.append("janela aberta no CPS2 (+10)")

    if solo is None:                       # ainda não leu o sensor
        return
    if modo == "auto":
        # histerese: liga abaixo do limite e só desliga 10 pontos acima dele
        if solo < limite_efetivo:
            nova = True
        elif solo >= limite_efetivo + 10:
            nova = False
        else:
            nova = bomba
        if partes:
            motivo = "limite " + str(limite_efetivo) + "%: " + " e ".join(partes)
        else:
            motivo = "limite " + str(limite_efetivo) + "%: condições normais"
    else:
        nova = bomba_manual
        motivo = "comando manual do dashboard"

    bomba = nova
    rele.value(1 if bomba else 0)
    led_bomba.value(1 if bomba else 0)


def publicar_mudancas():
    """Publica o estado da bomba, mas só quando mudou (evita mensagens repetidas)."""
    global ultimo_estado
    estado = {
        "sistema": "CPS3", "modo": modo,
        "bomba": "ligada" if bomba else "desligada",
        "limite_efetivo": limite_efetivo,
        "motivo": motivo,
    }
    if estado != ultimo_estado:
        # retido: o CPS1 e o dashboard recebem o último estado mesmo se conectarem depois
        publicar(T_ESTADO, estado, retida=True)
        ultimo_estado = estado
        print("Solo:", solo, "% | bomba:", bomba, "|", motivo)


def ciclo():
    ler_solo()
    decidir_e_atuar()
    publicar(T_SENSOR, {
        "sistema": "CPS3", "solo": solo,
        "limite_base": limite_base, "limite_efetivo": limite_efetivo,
    })


# ---------------------- PROGRAMA PRINCIPAL ----------------------
print("CPS3 - Irrigação iniciando")
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
