# =====================================================================
# CPS 1 - ESTAÇÃO CLIMÁTICA DA ESTUFA
# Disciplina: Conectividade de Sistemas Ciberfísicos (CSCF 2026.2)
# Plataforma: ESP32 + MicroPython (Wokwi)
#
# Sensor   : DHT22 (temperatura e umidade)   -> GPIO 15
# Atuadores: LED vermelho (alerta de calor)  -> GPIO 2
#            LED azul (irrigação ligada)     -> GPIO 4
#
# O que este sistema faz:
#  1. Lê temperatura e umidade e publica em MQTT.
#  2. Se a temperatura passar do limite, publica o alerta "CALOR".
#     (CPS2 e CPS3 escutam esse alerta e mudam o comportamento deles)
#  3. Escuta o estado da bomba do CPS3 e acende o LED azul quando
#     a irrigação está ligada (CPS3 -> CPS1).
#  4. Recebe comandos do dashboard (modo, limite, LED).
# =====================================================================

import network
import time
import ujson
import random
from machine import Pin
import dht
from umqtt.simple import MQTTClient

# ---------------------- CONFIGURAÇÃO ----------------------
WIFI_SSID = "Wokwi-GUEST"          # rede Wi-Fi simulada do Wokwi
WIFI_SENHA = ""
BROKER = "broker.hivemq.com"       # broker MQTT público
PORTA = 1883
EQUIPE = "zupeli_vilela_dib"               # identificador da equipe (evita conflito com outros)
INTERVALO_MS = 3000                # de quanto em quanto tempo lê o sensor e publica

BASE = "cscf/" + EQUIPE
ID_CLIENTE = "cps1-" + EQUIPE + "-" + str(random.getrandbits(16))

# Tópicos que este sistema PUBLICA
T_SENSOR = BASE + "/cps1/sensor"    # dados do DHT22
T_ALERTA = BASE + "/cps1/alerta"    # CALOR / NORMAL (usado por CPS2 e CPS3)
T_ESTADO = BASE + "/cps1/estado"    # estado dos atuadores
T_STATUS = BASE + "/cps1/status"    # online / offline (Last Will)
# Tópicos que este sistema ASSINA
T_COMANDO = BASE + "/cps1/comando"  # comandos do dashboard
T_ESTADO_CPS3 = BASE + "/cps3/estado"  # saber se a bomba está ligada

# ---------------------- HARDWARE ----------------------
sensor = dht.DHT22(Pin(15))
led_alerta = Pin(2, Pin.OUT)
led_irrig = Pin(4, Pin.OUT)

# ---------------------- ESTADO DO SISTEMA ----------------------
temp = None
umid = None
limite = 30.0            # acima disso é "CALOR" (pode ser mudado pelo dashboard)
alerta = False           # True quando está em CALOR
modo = "auto"            # "auto" = decide sozinho | "manual" = obedece o dashboard
led_alerta_manual = False
bomba_ligada = False     # informação que veio do CPS3
ultimo_estado = None     # último estado publicado (só publica de novo se mudar)
ultimo_alerta = None     # última condição de alerta publicada

wlan = network.WLAN(network.STA_IF)
cliente = None


# ---------------------- WI-FI ----------------------
def conectar_wifi():
    """Garante que o Wi-Fi está conectado. Retorna True/False."""
    wlan.active(True)
    if wlan.isconnected():
        return True
    print("Conectando ao Wi-Fi", end="")
    wlan.connect(WIFI_SSID, WIFI_SENHA)
    for _ in range(100):               # espera até ~10 segundos
        if wlan.isconnected():
            print(" conectado!")
            return True
        print(".", end="")
        time.sleep(0.1)
    print(" falhou, tentando de novo...")
    return False


# ---------------------- MQTT ----------------------
def conectar_mqtt():
    """Cria o cliente MQTT, conecta no broker e assina os tópicos."""
    global cliente, ultimo_estado, ultimo_alerta
    print("Conectando ao broker", BROKER, "...")
    c = MQTTClient(ID_CLIENTE, BROKER, port=PORTA, keepalive=30)
    c.set_callback(ao_receber)
    # Last Will: se este ESP32 cair, o broker publica "offline" por ele
    c.set_last_will(T_STATUS, b"offline", retain=True)
    c.connect()
    c.subscribe(T_COMANDO)
    c.subscribe(T_ESTADO_CPS3)
    c.publish(T_STATUS, b"online", retain=True)
    cliente = c
    ultimo_estado = None               # depois de reconectar, republica tudo
    ultimo_alerta = None
    print("MQTT conectado!")


def ao_receber(topico, mensagem):
    """Chamada automaticamente sempre que chega uma mensagem MQTT."""
    global limite, modo, led_alerta_manual, bomba_ligada
    topico = topico.decode()
    print("RECEBIDO", topico, mensagem)
    try:
        dados = ujson.loads(mensagem)
    except ValueError:
        print("Mensagem inválida (não é JSON), ignorada")
        return
    if not isinstance(dados, dict):
        return

    if topico == T_COMANDO:
        # Exemplos: {"modo":"manual","led_alerta":"on"}   {"limite":28}   {"modo":"auto"}
        if "modo" in dados and dados["modo"] in ("auto", "manual"):
            modo = dados["modo"]
        if "limite" in dados:
            try:
                limite = float(dados["limite"])
            except (ValueError, TypeError):
                pass
        if "led_alerta" in dados:
            led_alerta_manual = (dados["led_alerta"] == "on")
            modo = "manual"            # mexer no LED à mão entra em modo manual
        processar()                    # reage na hora, sem esperar o próximo ciclo

    elif topico == T_ESTADO_CPS3:
        # Informação vinda de OUTRO sistema: a bomba do CPS3 está ligada?
        bomba_ligada = (dados.get("bomba") == "ligada")
        processar()                    # acende/apaga o LED azul na hora


def publicar(topico, dados, retida=False):
    # .encode() transforma o texto em bytes UTF-8: sem isso, letras com acento
    # (ç, ã...) fazem a mensagem sair maior que o tamanho declarado e chegar cortada
    cliente.publish(topico, ujson.dumps(dados).encode(), retain=retida)


# ---------------------- LÓGICA DO SISTEMA ----------------------
def ler_sensor():
    """Lê o DHT22. Se der erro de leitura, mantém o último valor."""
    global temp, umid
    try:
        sensor.measure()
        temp = sensor.temperature()
        umid = sensor.humidity()
    except OSError:
        print("Falha ao ler o DHT22")


def avaliar_alerta():
    """Compara a temperatura com o limite (com histerese de 1 grau)."""
    global alerta
    if temp is None:
        return False
    antes = alerta
    if temp >= limite:
        alerta = True
    elif temp < limite - 1:
        alerta = False
    return alerta != antes             # True se o alerta mudou


def aplicar_atuadores():
    """Liga/desliga os LEDs conforme o modo."""
    if modo == "auto":
        led_alerta.value(1 if alerta else 0)
    else:
        led_alerta.value(1 if led_alerta_manual else 0)
    # LED azul sempre mostra o que o CPS3 informou (integração entre sistemas)
    led_irrig.value(1 if bomba_ligada else 0)


def processar():
    """Decide e aciona os atuadores com os dados que já temos."""
    avaliar_alerta()
    aplicar_atuadores()


def publicar_mudancas():
    """Publica alerta e estado, mas só quando mudaram (evita mensagens repetidas)."""
    global ultimo_estado, ultimo_alerta
    if alerta != ultimo_alerta:
        # alerta e estado são "retidos": quem conectar depois já recebe o último valor
        publicar(T_ALERTA, {
            "sistema": "CPS1",
            "condicao": "CALOR" if alerta else "NORMAL",
            "temp": temp, "limite": limite,
        }, retida=True)
        ultimo_alerta = alerta
        print("Alerta:", "CALOR" if alerta else "NORMAL", "| temp:", temp)
    estado = {
        "sistema": "CPS1", "modo": modo,
        "led_alerta": "on" if led_alerta.value() else "off",
        "led_irrig": "on" if led_irrig.value() else "off",
    }
    if estado != ultimo_estado:
        publicar(T_ESTADO, estado, retida=True)
        ultimo_estado = estado


def ciclo():
    """Um ciclo completo: sensor -> decisão -> atuador -> publicação."""
    ler_sensor()
    processar()
    publicar(T_SENSOR, {
        "sistema": "CPS1", "temp": temp, "umid": umid,
        "limite": limite, "alerta": alerta,
    })


# ---------------------- PROGRAMA PRINCIPAL ----------------------
print("CPS1 - Estação climática iniciando")
ultimo_ciclo = time.ticks_add(time.ticks_ms(), -INTERVALO_MS)
ultimo_ping = time.ticks_ms()
tentativas = 0

while True:
    try:
        # 1) Wi-Fi
        if not conectar_wifi():
            cliente = None             # sem Wi-Fi, a conexão MQTT também caiu
            time.sleep(2)
            continue
        # 2) MQTT (reconecta sozinho se cair)
        if cliente is None:
            conectar_mqtt()
            tentativas = 0
        # 3) recebe mensagens pendentes (chama ao_receber)
        cliente.check_msg()
        agora = time.ticks_ms()
        # 4) ciclo do sensor
        if time.ticks_diff(agora, ultimo_ciclo) >= INTERVALO_MS:
            ultimo_ciclo = agora
            ciclo()
        # 5) publica alerta/estado se algo mudou
        publicar_mudancas()
        # 6) mantém a conexão viva
        if time.ticks_diff(agora, ultimo_ping) >= 15000:
            ultimo_ping = agora
            cliente.ping()
        time.sleep_ms(100)
    except Exception as erro:
        # qualquer falha de rede/MQTT cai aqui: espera um pouco e tenta de novo
        tentativas += 1
        espera = min(2 * tentativas, 10)
        print("Falha de conexão:", erro, "- nova tentativa em", espera, "s")
        try:
            cliente.disconnect()
        except Exception:
            pass
        cliente = None
        time.sleep(espera)
