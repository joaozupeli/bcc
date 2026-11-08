import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import glob
for f in glob.glob("/home/box/.fonts/inter-static/*.ttf"): fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Inter"

fig, ax = plt.subplots(figsize=(16, 10.5), dpi=200)
ax.set_xlim(0, 16); ax.set_ylim(0, 10.8); ax.axis("off")

def box(x, y, w, h, lw=2.0, fill="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12", fc=fill, ec="black", lw=lw))

def txt(x, y, s, **k):
    k.setdefault("ha", "center"); k.setdefault("va", "center")
    ax.text(x, y, s, **k)

def arrow(p, q, style="<|-|>", dashed=False, lw=1.6, rad=0.0, color="black", ms=14):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, lw=lw, color=color,
                 linestyle=(0, (5, 4)) if dashed else "-", connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))

# --- CPS boxes
cps = [
 (2.6, "Sistema CPS 1", "Estação climática", "Sensor: DHT22 (temp/umid)", "Atuadores: LED alerta + LED irrigação"),
 (8.0, "Sistema CPS 2", "Ventilação e iluminação", "Sensor: LDR (luz)", "Atuadores: servo (janela) + LED luz"),
 (13.4, "Sistema CPS 3", "Irrigação", "Sensor: potenciômetro (solo)", "Atuadores: relé (bomba) + LED"),
]
BY, BH, BW = 6.1, 2.5, 3.9
for cx, t, sub, s, a in cps:
    box(cx - BW/2, BY, BW, BH)
    txt(cx, BY+BH-0.35, t, fontsize=15, fontweight="bold")
    txt(cx, BY+BH-0.80, sub, fontsize=11, color="#444")
    txt(cx, BY+1.1, "Wokwi + ESP32 · MicroPython", fontsize=10.5)
    txt(cx, BY+0.72, s, fontsize=10)
    txt(cx, BY+0.40, a, fontsize=10)
    ax.add_patch(FancyBboxPatch((cx-0.75, BY+BH-1.28), 1.5, 0.3, boxstyle="round,pad=0,rounding_size=0.1", fc="black", ec="black"))
    txt(cx, BY+BH-1.13, "PUB + SUB", fontsize=9, color="white", fontweight="bold")

# --- Broker
box(2.2, 3.35, 11.6, 1.55, lw=2.6)
txt(8, 4.5, "BROKER MQTT", fontsize=19, fontweight="bold")
txt(8, 4.08, "broker.hivemq.com  ·  TCP 1883 (ESP32)  ·  WSS 8884 (dashboard)", fontsize=10.5, color="#333")
txt(8, 3.70, "Recebe e distribui mensagens  ·  Tópicos  ·  Publish  ·  Subscribe", fontsize=10.5, color="#333")

# --- Dashboard
box(4.6, 0.35, 6.8, 1.7)
txt(8, 1.62, "DASHBOARD", fontsize=17, fontweight="bold")
txt(8, 1.22, "HTML + JavaScript (mqtt.js, WebSocket)", fontsize=10.5, color="#333")
txt(8, 0.85, "Monitoramento + Comandos  ·  PUB / SUB", fontsize=10.5, color="#333")
txt(8, 0.52, "assina cscf/zupeli_vilela_dib/#", fontsize=9, color="#555", family="DejaVu Sans Mono")

# --- CPS <-> Broker (dashed, bidirectional)
for cx, n in [(2.6, 1), (8.0, 2), (13.4, 3)]:
    arrow((cx, BY), (cx, 4.9), dashed=True)
pub = {1: "PUB  sensor · alerta\n        estado · status", 2: "PUB  sensor · estado\n        status", 3: "PUB  sensor · estado\n        status"}
sub = {1: "SUB  cps1/comando\n        cps3/estado", 2: "SUB  cps2/comando\n        cps1/alerta", 3: "SUB  cps3/comando\n        cps1/alerta · cps2/estado"}
for cx, n in [(2.6, 1), (8.0, 2), (13.4, 3)]:
    txt(cx-0.15, 5.5, pub[n], fontsize=8.6, ha="right", family="DejaVu Sans Mono", color="#222")
    txt(cx+0.15, 5.5, sub[n], fontsize=8.6, ha="left", family="DejaVu Sans Mono", color="#222")

# --- Broker <-> dashboard
arrow((8, 3.35), (8, 2.05), dashed=True)
txt(7.85, 2.7, "SUB  cscf/…/# (tudo)", fontsize=8.8, ha="right", family="DejaVu Sans Mono")
txt(8.15, 2.7, "PUB  cps1|2|3/comando", fontsize=8.8, ha="left", family="DejaVu Sans Mono")

# --- cross-system interaction (solid, through the broker)
arrow((cx_ := 2.6+BW/2, BY+BH-0.55), (8.0-BW/2, BY+BH-0.55), style="-|>", lw=2.6, ms=18)
txt(5.3, BY+BH-0.2, "cps1/alerta", fontsize=8.2, fontweight="bold", family="DejaVu Sans Mono")
txt(5.3, BY+BH-0.9, "abre\njanela", fontsize=8, color="#333")
arrow((8.0+BW/2, BY+BH-0.55), (13.4-BW/2, BY+BH-0.55), style="-|>", lw=2.6, ms=18)
txt(10.7, BY+BH-0.2, "cps2/estado", fontsize=8.2, fontweight="bold", family="DejaVu Sans Mono")
txt(10.7, BY+BH-0.9, "limite\n+10", fontsize=8, color="#333")
# CPS1 -> CPS3 alerta (arc above)
arrow((2.6+0.9, BY+BH), (13.4-0.9, BY+BH), style="-|>", lw=2.6, rad=-0.16, ms=18)
txt(8, 9.38, "cps1/alerta  (CALOR → CPS3 sobe o limite do solo em +20 e liga a bomba)", fontsize=8.6, fontweight="bold", family="DejaVu Sans Mono", bbox=dict(fc="white", ec="none", pad=3))
# CPS3 -> CPS1 estado (bigger arc above)
arrow((13.4+0.9, BY+BH), (2.6-0.9, BY+BH), style="-|>", lw=2.6, rad=0.30, ms=18)
txt(8, 10.02, "cps3/estado  (bomba ligada → CPS1 acende o LED azul)", fontsize=8.6, fontweight="bold", family="DejaVu Sans Mono", bbox=dict(fc="white", ec="none", pad=3))

# --- legend
ax.plot([0.35, 1.0], [2.15, 2.15], color="black", lw=1.6, ls=(0, (5, 4)))
txt(1.15, 2.15, "conexão MQTT com o broker (PUB/SUB)", fontsize=8.8, ha="left")
ax.plot([0.35, 1.0], [1.7, 1.7], color="black", lw=2.6)
txt(1.15, 1.7, "interação entre sistemas", fontsize=8.8, ha="left")
txt(0.35, 1.25, "Os dispositivos nunca falam direto entre si:\ntoda mensagem vai ao broker, que entrega\nas cópias a quem assinou o tópico.", fontsize=8.2, ha="left", va="top", color="#444")
txt(15.7, 0.15, "prefixo de todos os tópicos:  cscf/zupeli_vilela_dib/", fontsize=8.5, ha="right", family="DejaVu Sans Mono", color="#333")

fig.savefig("arquitetura.png", bbox_inches="tight", facecolor="white")
