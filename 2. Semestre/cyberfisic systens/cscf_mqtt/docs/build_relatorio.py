from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Inter"
PRETO = RGBColor(0, 0, 0)
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin = Cm(2.2); sec.bottom_margin = Cm(2.0)

def setfont(style, size, bold=False):
    style.font.name = FONT; style.font.size = Pt(size); style.font.bold = bold
    style.font.color.rgb = PRETO
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), FONT)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]

st = doc.styles
setfont(st["Normal"], 10.5)
st["Normal"].paragraph_format.space_after = Pt(6)
st["Normal"].paragraph_format.line_spacing = 1.25
setfont(st["Heading 1"], 17, True); st["Heading 1"].paragraph_format.space_before = Pt(22); st["Heading 1"].paragraph_format.space_after = Pt(8)
setfont(st["Heading 2"], 12.5, True); st["Heading 2"].paragraph_format.space_before = Pt(14); st["Heading 2"].paragraph_format.space_after = Pt(4)
setfont(st["List Bullet"], 10.5); setfont(st["List Number"], 10.5)

def p(text="", bold=False, size=None, align=None, after=None, italic=False, mono=False):
    para = doc.add_paragraph()
    add_runs(para, text, bold, size, italic, mono)
    if align == "c": para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if after is not None: para.paragraph_format.space_after = Pt(after)
    return para

def add_runs(para, text, bold=False, size=None, italic=False, mono=False):
    # **negrito** e `código` inline
    import re
    for part in re.split(r"(\*\*.+?\*\*|`.+?`)", text):
        if not part: continue
        if part.startswith("**"):
            r = para.add_run(part[2:-2]); r.bold = True
        elif part.startswith("`"):
            r = para.add_run(part[1:-1]); r.font.name = "DejaVu Sans Mono"; r.font.size = Pt((size or 10.5) - 1.5)
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "DejaVu Sans Mono")
            continue
        else:
            r = para.add_run(part); r.bold = bold
        r.italic = italic
        if size: r.font.size = Pt(size)
        r.font.color.rgb = PRETO

def h1(t): doc.add_heading(t, 1)
def h2(t): doc.add_heading(t, 2)
def bl(t):
    para = doc.add_paragraph(style="List Bullet"); add_runs(para, t); para.paragraph_format.space_after = Pt(2)
def nl(t):
    para = doc.add_paragraph(style="List Number"); add_runs(para, t); para.paragraph_format.space_after = Pt(2)

def borders(cell, **kw):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{edge}")
        sz = kw.get(edge, 4)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz)); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000")
        b.append(e)
    tcPr.append(b)

def table(header, rows, widths, size=8.5):
    t = doc.add_table(rows=1, cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]; c.width = Cm(widths[i]); c.text = ""
        add_runs(c.paragraphs[0], h, bold=True, size=size)
        c.paragraphs[0].paragraph_format.space_after = Pt(2)
        borders(c, bottom=12, top=8, left=4, right=4)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].width = Cm(widths[i]); cells[i].text = ""
            lines = v.split("\n")
            for k, ln in enumerate(lines):
                para = cells[i].paragraphs[0] if k == 0 else cells[i].add_paragraph()
                add_runs(para, ln, size=size); para.paragraph_format.space_after = Pt(1); para.paragraph_format.line_spacing = 1.1
            borders(cells[i])
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    # repete cabeçalho
    trPr = t.rows[0]._tr.get_or_add_trPr(); th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t

def pagebreak(): doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# rodapé com número de página
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run("CSCF 2026.2 · Projeto Final MQTT · página "); r.font.size = Pt(8); r.font.name = FONT; r.font.color.rgb = PRETO
r2 = fp.add_run(); r2.font.size = Pt(8); r2.font.name = FONT
for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if tag:
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tag)
    else:
        e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
    r2._r.append(e)

# ============ CAPA ============
for _ in range(3): p("", after=14)
p("PUCPR · 2026.2", size=11, after=40)
p("Projeto Final CSCF", bold=True, size=34, after=4)
p("Estufa Inteligente: três sistemas ciberfísicos integrados por MQTT", size=15, after=30)
p("Disciplina: Conectividade de Sistemas Ciberfísicos", size=11.5, after=2)
p("Ambiente: Wokwi · ESP32 · MicroPython · Broker MQTT público (HiveMQ)", size=11.5, after=40)
p("Equipe", bold=True, size=11.5, after=4)
for n in ("João Francisco Zupeli", "Gustavo Vilela", "João Dib"):
    p(n, size=12, after=2)
p("", after=30)
p("Entregas (links)", bold=True, size=11.5, after=8)
for lab in ("Link Wokwi 1 (CPS 1):", "Link Wokwi 2 (CPS 2):", "Link Wokwi 3 (CPS 3):", "Link do dashboard:"):
    p(lab + "  ______________________________________________", size=10.5, after=10)
p("", after=4)
p("Identificador da equipe nos tópicos MQTT: `cscf/zupeli_vilela_dib/`", size=9.5)
pagebreak()

# ============ 1. IDEIA ============
h1("1. A ideia do projeto")
p("A gente montou uma **estufa inteligente**. Em vez de fazer um sistema só gigante, dividimos a estufa em três sistemas ciberfísicos pequenos, cada um com seu ESP32, seu sensor e seus atuadores, rodando em um projeto Wokwi separado. Cada um funciona sozinho, mas eles conversam entre si pela rede usando MQTT, e um dashboard no navegador mostra tudo e deixa a gente mandar comandos.")
p("A graça é que o que um sistema percebe muda o que o outro faz. Se esquenta demais, o CPS 1 avisa; o CPS 2 abre a janela; o CPS 3 percebe que com calor e janela aberta o solo seca mais rápido e passa a regar mais cedo. Ninguém fala direto com ninguém, tudo passa pelo broker.")
h2("Resumo dos três sistemas")
table(["Sistema", "Sensor", "Atuadores", "Papel na estufa"],
 [["CPS 1 · Estação climática", "DHT22 (temperatura e umidade do ar), GPIO 15", "LED vermelho (alerta de calor), GPIO 2\nLED azul (irrigando), GPIO 4", "Mede o clima e avisa quando está quente demais."],
  ["CPS 2 · Ventilação e iluminação", "LDR / fotoresistor (luminosidade), GPIO 34", "Servo motor = janela, GPIO 18\nLED branco = iluminação, GPIO 5", "Abre a janela quando tem calor e acende a luz à noite."],
  ["CPS 3 · Irrigação", "Potenciômetro = umidade do solo, GPIO 35", "Módulo relé = bomba d'água, GPIO 26\nLED verde, GPIO 27", "Decide quando regar, levando em conta o clima."]],
 [3.4, 4.2, 4.6, 4.4], size=8.5)

# ============ 2. COMO FUNCIONA ============
h1("2. Como cada sistema funciona")
p("Os três programas têm a mesma estrutura (é mais fácil de explicar e de depurar): conectam no Wi-Fi, conectam no broker, assinam seus tópicos e ficam num laço que recebe mensagens (`check_msg`), lê o sensor a cada 3 segundos, decide, aciona o atuador e publica.")
h2("CPS 1 · Estação climática")
p("O DHT22 lê temperatura e umidade. Se a temperatura passa do limite (30 °C por padrão, dá para mudar pelo dashboard; tem histerese de 1 °C para não ficar oscilando), o sistema entende que há **CALOR**, acende o LED vermelho e publica o alerta em `cps1/alerta`. Ele também assina `cps3/estado`: quando a bomba do CPS 3 está ligada, acende o LED azul. Ou seja, o atuador do CPS 1 também depende de um dado que veio de outro sistema.")
h2("CPS 2 · Ventilação e iluminação")
p("O LDR mede a luz e o programa converte para porcentagem. Abaixo de 30% é \"noite\" e o LED branco acende (essa decisão é local; histerese até 35%). Além disso o CPS 2 assina `cps1/alerta`: se chegar **CALOR**, o servo vai para 90° (janela aberta); quando volta ao **NORMAL**, fecha (0°). O estado da janela é publicado em `cps2/estado`, que o CPS 3 usa.")
h2("CPS 3 · Irrigação")
p("O potenciômetro simula a umidade do solo (0 a 100%). A bomba (relé + LED verde) liga quando o solo está mais seco que o **limite efetivo** e só desliga 10 pontos acima dele (histerese). O limite efetivo é calculado com dados da rede:")
bl("limite base = 30% (ajustável pelo dashboard);")
bl("+ 20 pontos se o CPS 1 avisou CALOR (`cps1/alerta`);")
bl("+ 10 pontos se a janela do CPS 2 está aberta (`cps2/estado`), porque o ar fica mais seco.")
p("Com calor e janela aberta o limite vai a 60%: a bomba liga mesmo com o solo \"razoável\". Depois o CPS 3 publica `cps3/estado` e o CPS 1 acende o LED azul.")
h2("Modo automático e manual")
p("Todo comando vindo do dashboard coloca aquele sistema em modo `manual` (ele obedece o botão). O botão **Automático** do dashboard devolve a decisão para a lógica local.")

# ============ 3. BROKER ============
h1("3. O broker MQTT")
p("Usamos o broker público **HiveMQ** (`broker.hivemq.com`), o mesmo dos exemplos do Wokwi usados nas aulas.")
table(["Quem conecta", "Endereço", "Observação"],
 [["ESP32 (MicroPython, `umqtt.simple`)", "`broker.hivemq.com`, porta **1883** (TCP, sem TLS)", "O Wokwi dá internet pelo Wi-Fi simulado `Wokwi-GUEST`."],
  ["Dashboard (mqtt.js no navegador)", "`wss://broker.hivemq.com:8884/mqtt`", "Navegador não abre TCP puro, então usa MQTT sobre WebSocket seguro."]],
 [4.6, 6.0, 6.0], size=8.5)
p("Recursos do MQTT que usamos:")
bl("**Publish/Subscribe** com tópicos hierárquicos e o curinga `#` no dashboard.")
bl("**Mensagens retidas** (`retain`) em alerta, estado e status: quem conecta depois (ou reconecta) já recebe o último valor.")
bl("**Last Will**: cada ESP32 deixa registrado `offline` em `.../status`; se ele cair sem avisar, o próprio broker publica isso.")
bl("**Keep-alive** de 30 s e `ping` periódico para detectar conexão morta.")
bl("**QoS 0**: tá bom para o caso, porque o sensor é republicado a cada 3 s e os estados são retidos.")
p("**Limitação honesta:** é um broker público e sem senha, então qualquer pessoa que souber o prefixo dos tópicos lê e envia mensagens. Por isso o prefixo é único (`zupeli_vilela_dib`). Num sistema real usaríamos usuário/senha e TLS.")

# ============ 4. TÓPICOS ============
pagebreak()
h1("4. Tabela de tópicos MQTT")
p("Todos os tópicos começam com o prefixo `cscf/zupeli_vilela_dib/` (escrito só uma vez abaixo para a tabela caber). Todas as mensagens são JSON em UTF-8, exceto `status`, que é texto simples.")
T = [
 ["`cps1/sensor`", "CPS 1", "Dashboard", "JSON a cada 3 s\n`{\"sistema\":\"CPS1\",\"temp\":24.0,\"umid\":60.0,\"limite\":30.0,\"alerta\":false}`"],
 ["`cps1/alerta` (retida)", "CPS 1", "**CPS 2**, **CPS 3**, Dashboard", "JSON só quando muda\n`{\"sistema\":\"CPS1\",\"condicao\":\"CALOR\",\"temp\":35.0,\"limite\":30.0}`"],
 ["`cps1/estado` (retida)", "CPS 1", "Dashboard", "JSON só quando muda\n`{\"sistema\":\"CPS1\",\"modo\":\"auto\",\"led_alerta\":\"on\",\"led_irrig\":\"off\"}`"],
 ["`cps1/status` (retida)", "CPS 1 (Last Will)", "Dashboard", "texto: `online` / `offline`"],
 ["`cps1/comando`", "Dashboard", "CPS 1", "JSON\n`{\"modo\":\"manual\",\"led_alerta\":\"on\",\"limite\":28}`"],
 ["`cps2/sensor`", "CPS 2", "Dashboard", "JSON a cada 3 s\n`{\"sistema\":\"CPS2\",\"luz\":72,\"periodo\":\"dia\"}`"],
 ["`cps2/estado` (retida)", "CPS 2", "**CPS 3**, Dashboard", "JSON só quando muda\n`{\"sistema\":\"CPS2\",\"modo\":\"auto\",\"janela\":\"aberta\",\"angulo\":90,\"luz\":\"off\",\"motivo\":\"alerta de calor do CPS1\"}`"],
 ["`cps2/status` (retida)", "CPS 2 (Last Will)", "Dashboard", "texto: `online` / `offline`"],
 ["`cps2/comando`", "Dashboard", "CPS 2", "JSON\n`{\"modo\":\"manual\",\"janela\":\"abrir\",\"luz\":\"on\"}`"],
 ["`cps3/sensor`", "CPS 3", "Dashboard", "JSON a cada 3 s\n`{\"sistema\":\"CPS3\",\"solo\":53,\"limite_base\":30,\"limite_efetivo\":60}`"],
 ["`cps3/estado` (retida)", "CPS 3", "**CPS 1**, Dashboard", "JSON só quando muda\n`{\"sistema\":\"CPS3\",\"modo\":\"auto\",\"bomba\":\"ligada\",\"limite_efetivo\":60,\"motivo\":\"limite 60%: calor no CPS1 (+20) e janela aberta no CPS2 (+10)\"}`"],
 ["`cps3/status` (retida)", "CPS 3 (Last Will)", "Dashboard", "texto: `online` / `offline`"],
 ["`cps3/comando`", "Dashboard", "CPS 3", "JSON\n`{\"modo\":\"manual\",\"bomba\":\"on\",\"limite_solo\":40}`"],
]
table(["Tópico", "Publicador", "Assinantes", "Tipo de mensagem / exemplo"], T, [3.2, 2.6, 3.0, 7.8], size=8)
h2("Visão por dispositivo")
table(["Dispositivo", "Publica", "Assina"],
 [["CPS 1 (DHT22 + LEDs)", "`cps1/sensor`, `cps1/alerta`, `cps1/estado`, `cps1/status`", "`cps1/comando`, `cps3/estado`"],
  ["CPS 2 (LDR + servo + LED)", "`cps2/sensor`, `cps2/estado`, `cps2/status`", "`cps2/comando`, `cps1/alerta`"],
  ["CPS 3 (solo + relé + LED)", "`cps3/sensor`, `cps3/estado`, `cps3/status`", "`cps3/comando`, `cps1/alerta`, `cps2/estado`"],
  ["Dashboard", "`cps1/comando`, `cps2/comando`, `cps3/comando`", "`cscf/zupeli_vilela_dib/#` (tudo)"]],
 [4.2, 6.6, 5.8], size=8.5)

# ============ 5. ARQUITETURA ============
from docx.enum.section import WD_SECTION, WD_ORIENT
ls = doc.add_section(WD_SECTION.NEW_PAGE); ls.orientation = WD_ORIENT.LANDSCAPE
ls.page_width, ls.page_height = Cm(29.7), Cm(21)
ls.left_margin = ls.right_margin = Cm(1.8); ls.top_margin = Cm(1.6); ls.bottom_margin = Cm(1.5)
h1("5. Arquitetura de conectividade")
p("O diagrama abaixo mostra os três ESP32 (cada um com sensor e atuador, publicando e assinando), o broker no meio e o dashboard. As setas tracejadas são as conexões MQTT de cada dispositivo com o broker; as setas pretas grossas são as interações entre os sistemas (que também passam pelo broker, o desenho só mostra a relação lógica).")
doc.add_picture("arquitetura.png", width=Cm(20))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
ps = doc.add_section(WD_SECTION.NEW_PAGE); ps.orientation = WD_ORIENT.PORTRAIT
ps.page_width, ps.page_height = Cm(21), Cm(29.7)
ps.left_margin = ps.right_margin = Cm(2.2); ps.top_margin = Cm(2.2); ps.bottom_margin = Cm(2.0)

# ============ 6. INTEGRAÇÃO ============
h1("6. A integração entre os três sistemas")
p("O ponto principal do trabalho: não são três projetos mandando dado para o dashboard. Os sistemas usam as mensagens uns dos outros para decidir. A cadeia é essa:")
nl("O CPS 1 mede temperatura ≥ 30 °C, decide que é **CALOR**, acende o LED vermelho e publica `cps1/alerta = CALOR` (retida).")
nl("O CPS 2 recebe o alerta pelo broker e **abre a janela** (servo vai a 90°). Em seguida publica `cps2/estado = aberta`.")
nl("O CPS 3 recebe os dois (alerta do CPS 1 e estado da janela do CPS 2), calcula o limite efetivo (30 + 20 + 10 = 60%). Como o solo está abaixo disso, **liga a bomba** (relé + LED verde).")
nl("O CPS 3 publica `cps3/estado = ligada` e o CPS 1 recebe e **acende o LED azul**. É a realimentação: o primeiro sistema \"fica sabendo\" do efeito da cadeia.")
nl("Quando a temperatura cai, o CPS 1 publica `NORMAL`: a janela fecha, o limite volta a 30%, a bomba desliga e os LEDs apagam.")
table(["Fluxo", "Tópico", "O que muda no assinante"],
 [["CPS 1 → CPS 2", "`cps1/alerta`", "CALOR abre a janela (servo 90°); NORMAL fecha."],
  ["CPS 1 → CPS 3", "`cps1/alerta`", "CALOR aumenta em 20 pontos o limite de umidade do solo."],
  ["CPS 2 → CPS 3", "`cps2/estado`", "Janela aberta aumenta em mais 10 pontos o limite."],
  ["CPS 3 → CPS 1", "`cps3/estado`", "Bomba ligada acende o LED azul do CPS 1."]],
 [3.4, 3.4, 9.8], size=8.5)
p("Detalhe de implementação: alerta e estado só são publicados quando **mudam** (o sensor sim, a cada 3 s), e cada sistema reage na hora dentro do callback da mensagem. Isso evita um laço infinito de mensagens entre os sistemas.")
h2("Tratamento de falhas e reconexão")
bl("**Wi-Fi:** o laço principal checa `wlan.isconnected()`; se caiu, reconecta antes de qualquer coisa.")
bl("**MQTT:** qualquer erro em `check_msg`/`publish` cai num `try/except`, o cliente é fechado e o programa tenta reconectar com espera crescente (2 s, 4 s... até 10 s). Ao reconectar, assina os tópicos de novo e republica o estado.")
bl("**Mensagens inválidas:** JSON quebrado ou campo desconhecido é ignorado, o programa não cai.")
bl("**Last Will:** se um ESP32 cair, o dashboard mostra `offline`.")

# ============ 7. CICLO CPS ============
h1("7. O ciclo ciberfísico")
table(["Etapa", "Como aparece no projeto"],
 [["Aquisição", "DHT22 (temperatura e umidade), LDR (luz) e potenciômetro no ADC (umidade do solo) leem o \"ambiente\" simulado no Wokwi."],
  ["Processamento", "Conversão para unidades, limites com histerese, classificação dia/noite e cálculo do limite efetivo de irrigação com dados de outros sistemas."],
  ["Conectividade", "JSON sobre MQTT via broker HiveMQ: sensores, alertas, estados e comandos."],
  ["Atuação", "LEDs, servo (janela) e relé (bomba), influenciados por dado local, por mensagens de outros sistemas e por comandos do dashboard."],
  ["Realimentação", "O estado de cada atuador volta para o broker (retido) e é usado pelos outros CPS e pelo dashboard, fechando o ciclo."]],
 [3.4, 13.2], size=9)

# ============ 8. DASHBOARD ============
h1("8. Dashboard")
p("É um arquivo só (`dashboard/index.html`), HTML + CSS + JavaScript, que usa a biblioteca mqtt.js (carregada por CDN) e conecta no broker por WebSocket seguro. Para usar, é só abrir no navegador (ou publicar em qualquer hospedagem estática). Ele:")
bl("assina `cscf/zupeli_vilela_dib/#` e atualiza em tempo real os sensores dos três sistemas, o estado dos atuadores, o modo (auto/manual) e se cada um está online/offline;")
bl("tem botões que publicam comandos JSON em `cps1/comando`, `cps2/comando` e `cps3/comando` (LED de alerta, limite de calor; janela e luz; bomba e limite do solo; botão Automático);")
bl("mostra a **cadeia de integração** CPS 1 → CPS 2 → CPS 3 → CPS 1 acendendo conforme as mensagens chegam;")
bl("tem um painel de **alertas e interações entre sistemas** (log com hora de cada mudança: calor detectado, janela aberta, bomba ligada) e um log de todas as mensagens MQTT recebidas e enviadas.")
p("Se outra equipe usar o mesmo prefixo as mensagens se misturam. Dá para trocar o identificador com `index.html?equipe=outroid` (e nos três `main.py`, na constante `EQUIPE`).")

# ============ 9. PERGUNTAS ============
h1("9. Perguntas da demonstração")
h2("Qual é a função do broker MQTT e como ele encaminha as mensagens?")
p("O broker é o intermediário do modelo publish/subscribe. Cada cliente (os três ESP32 e o dashboard) abre uma conexão só com ele. Quando alguém publica uma mensagem em um tópico, o broker olha quem assinou aquele tópico e entrega uma cópia para cada assinante. Também guarda a última mensagem retida e dispara o Last Will quando um cliente some.")
h2("Qual é a diferença entre publicar e assinar um tópico?")
p("Publicar é **enviar** uma mensagem para um tópico (ex.: o CPS 1 publica o alerta em `cps1/alerta`). Assinar é **pedir ao broker** para receber tudo o que for publicado naquele tópico (ex.: o CPS 2 assina `cps1/alerta`). Quem publica não sabe quem está ouvindo, e quem assina não sabe quem publicou.")
h2("Quais tópicos são usados e quem publica e assina cada um?")
p("Estão na tabela da seção 4. Resumindo: cada CPS publica seus `sensor`, `estado` e `status` (o CPS 1 também publica `alerta`) e assina o próprio `comando` mais os tópicos de outros sistemas que influenciam o seu atuador (CPS 1 assina `cps3/estado`; CPS 2 assina `cps1/alerta`; CPS 3 assina `cps1/alerta` e `cps2/estado`). O dashboard assina tudo (`#`) e publica nos três `comando`.")
h2("Como uma mensagem enviada por um sistema chega aos demais?")
p("Exemplo: o CPS 1 publica `CALOR` em `cps1/alerta` pelo `MQTTClient.publish`. A mensagem vai ao broker HiveMQ, que vê que CPS 2, CPS 3 e dashboard assinaram esse tópico e manda uma cópia para cada um. No CPS 2 e no CPS 3 o `check_msg()` do laço principal chama a função `ao_receber`, que lê o JSON e reage.")
h2("Como a informação recebida pela rede é processada e usada para acionar um atuador?")
p("A função `ao_receber` converte o JSON (`ujson.loads`), confere o tópico e atualiza uma variável de estado (por exemplo `calor_cps1 = True` no CPS 2). Logo depois chama a função de decisão: no CPS 2, `calor_cps1` verdadeiro faz o servo ir para 90° via PWM; no CPS 3, a informação entra no cálculo do limite efetivo e o relé liga se o solo estiver abaixo; no CPS 1, `bomba: ligada` acende o LED azul.")
h2("Como o dashboard participa da comunicação MQTT?")
p("Ele é mais um cliente MQTT, só que no navegador (mqtt.js por WebSocket seguro). Assina `cscf/zupeli_vilela_dib/#` para mostrar sensores e estados e publica comandos nos tópicos `.../comando`, que os ESP32 recebem como qualquer outra mensagem. Não existe nenhum canal fora do MQTT: o que o dashboard mostra é o que chegou pelo broker.")
h2("Quais as vantagens do MQTT em sistemas ciberfísicos distribuídos?")
bl("Protocolo leve, bom para microcontroladores como o ESP32 e para redes ruins.")
bl("Desacoplamento: dá para adicionar um quarto sistema só assinando tópicos, sem mexer nos outros.")
bl("Um-para-muitos nativo: uma publicação chega a vários assinantes.")
bl("Mensagens retidas e Last Will ajudam a manter o estado e detectar falhas.")
bl("Tópicos hierárquicos organizam bem sensores, estados e comandos.")
bl("Funciona sobre a internet comum (e WebSocket para navegadores).")

# ============ 10. ROTEIRO ============
h1("10. Roteiro do vídeo de demonstração (6 a 8 minutos)")
p("Antes de gravar: abrir em abas separadas os três projetos Wokwi e o dashboard, rodar os três (▶) e conferir os três \"online\" no dashboard. Gravar a tela inteira, falar devagar e mostrar sempre a mensagem MQTT correspondente no log do dashboard.")
table(["Tempo", "O que mostrar", "Quem fala / o que dizer"],
 [["0:00", "Capa e diagrama de arquitetura", "Apresentar o grupo e a ideia: estufa com 3 CPS ligados por MQTT."],
  ["0:40", "Broker HiveMQ e tabela de tópicos", "Broker recebe e distribui; os dispositivos só conhecem o broker; prefixo único da equipe."],
  ["1:20", "Wokwi 1: diagrama + `main.py`", "DHT22, LEDs; mostrar `conectar_wifi`, `conectar_mqtt` (Last Will), `ao_receber` e o laço com reconexão."],
  ["2:10", "Wokwi 2", "LDR, servo e LED; assina `cps1/alerta`."],
  ["2:50", "Wokwi 3", "Potenciômetro, relé e LED; assina `cps1/alerta` e `cps2/estado`; limite efetivo."],
  ["3:30", "Dashboard com os três online", "Valores chegando por MQTT; mostrar o log de mensagens."],
  ["4:00", "**Integração:** no Wokwi 1 subir a temperatura do DHT22 para 35 °C", "CPS 1 detecta CALOR e publica `cps1/alerta`."],
  ["4:30", "Servo do Wokwi 2 gira; relé/LED do Wokwi 3 liga; LED azul do Wokwi 1 acende; dashboard mostra a cadeia e o painel de interações", "Explicar a cadeia CPS 1 → CPS 2 → CPS 3 → CPS 1."],
  ["5:20", "Baixar a temperatura para 24 °C", "Volta a NORMAL: janela fecha, bomba desliga, LEDs apagam."],
  ["5:40", "**Comandos do dashboard:** Abrir janela (CPS 2), Bomba ON (CPS 3), LED de alerta (CPS 1), depois \"Automático\"", "Dashboard publica em `.../comando`; mostrar cada atuador reagindo no Wokwi."],
  ["6:30", "Girar o LDR para pouca luz", "CPS 2 vira \"noite\" e acende a iluminação (decisão local)."],
  ["6:50", "Parar o Wokwi 1 e depois iniciar de novo", "Aparece `offline` (Last Will) e depois `online`: reconexão."],
  ["7:20", "Encerramento", "Resumir: aquisição, processamento, conectividade, atuação e realimentação; vantagens do MQTT."]],
 [1.4, 7.4, 7.8], size=8.5)

# ============ 11. TESTES ============
h1("11. Como testamos")
bl("Os três `main.py` foram executados em MicroPython (versão unix) com módulos simulados de hardware, contra um broker Mosquitto local: publicação, assinatura, a cadeia CPS 1 → CPS 2 → CPS 3 → CPS 1, comandos do dashboard, mensagens inválidas, queda do Wi-Fi e queda do broker (teste em `testes/teste_integracao.py`, tudo passou).")
bl("O dashboard foi aberto num Chrome real, recebeu mensagens MQTT publicadas por um cliente paho-mqtt, atualizou os valores e o painel de interações, e os botões publicaram os comandos esperados nos tópicos corretos.")
bl("Os `diagram.json` foram validados como JSON e as conexões conferidas pino a pino.")
p("O que **não** foi possível aqui: rodar dentro do Wokwi online e contra o HiveMQ de verdade. Por isso, ao montar os projetos, conferir se o terminal mostra \"Wi-Fi conectado\" e \"MQTT conectado\" (se faltar o módulo, adicionar `umqtt.simple` no Library Manager).")

doc.save("../Relatorio_CSCF_MQTT.docx")
