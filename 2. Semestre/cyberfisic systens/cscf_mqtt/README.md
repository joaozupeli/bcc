# Projeto Final CSCF 2026.2 — Estufa Inteligente (3 CPS integrados por MQTT)

**Equipe:** João Francisco Zupeli, Gustavo Vilela, João Dib — PUCPR  
**Disciplina:** Conectividade de Sistemas Ciberfísicos · **Ambiente:** Wokwi + ESP32 + MicroPython  
**Broker:** HiveMQ público (`broker.hivemq.com`, 1883 para os ESP32, `wss://...:8884/mqtt` para o dashboard)  
**Prefixo dos tópicos:** `cscf/zupeli_vilela_dib/`

## O que tem aqui
```
cps1/            main.py + diagram.json  (DHT22 + LED alerta + LED irrigação)
cps2/            main.py + diagram.json  (LDR + servo da janela + LED de luz)
cps3/            main.py + diagram.json  (potenciômetro/solo + relé da bomba + LED)
dashboard/       index.html  (HTML/CSS/JS, mqtt.js por CDN, MQTT sobre WebSocket)
Relatorio_CSCF_MQTT.pdf / .docx   relatório (arquitetura, tópicos, perguntas, roteiro do vídeo)
arquitetura.png  diagrama de arquitetura (fonte em docs/arquitetura.py)
testes/          teste automático local (opcional)
```

## Passo a passo no Wokwi (repetir 3 vezes: CPS 1, CPS 2, CPS 3)
1. Entre em https://wokwi.com, faça login e clique em **New Project → ESP32 → MicroPython** (template "MicroPython on ESP32").
2. Abra a aba **diagram.json**, apague tudo e cole o conteúdo de `cpsN/diagram.json`.
3. Abra a aba **main.py**, apague tudo e cole o conteúdo de `cpsN/main.py`.
4. Clique em ▶ (Start). No terminal tem que aparecer `Conectando ao Wi-Fi... conectado!` e `MQTT conectado!`.
   - Se der `ImportError: umqtt.simple`, abra o **Library Manager** (botão +) e adicione `umqtt.simple`.
5. Clique em **Save** e depois em **Share** (ou copie a URL do projeto). Deixe o projeto **público/não listado** para o professor abrir. Cole o link na capa do relatório.
6. Dê nome aos projetos, por exemplo `CSCF CPS1 Clima`, `CSCF CPS2 Ventilacao`, `CSCF CPS3 Irrigacao`.

## Rodar tudo junto
1. Abra os 3 projetos em 3 abas e dê ▶ nos três ao mesmo tempo (a ordem não importa: os estados são retidos no broker).
2. Abra `dashboard/index.html` no navegador (duplo clique; precisa de internet por causa do CDN do mqtt.js e do broker). Devem aparecer os 3 sistemas como **online**.
3. Teste a integração: no Wokwi 1 clique no DHT22 e suba a temperatura para 35 °C → o alerta CALOR sai, a janela abre (servo do CPS 2), a bomba liga (relé/LED do CPS 3) e o LED azul acende no CPS 1. Baixe para 24 °C e tudo volta ao normal.
4. Teste os comandos: botões do dashboard (abrir janela, bomba ON, LED de alerta...). **Automático** devolve o controle à lógica de cada sistema.

Para hospedar o dashboard (opcional, para ter um link): suba o `index.html` no GitHub Pages, Netlify, Vercel ou similar. Para conferir as mensagens cruas: https://www.hivemq.com/demos/websocket-client/ assinando `cscf/zupeli_vilela_dib/#`.

## Se outra equipe usar o mesmo prefixo
Troque `EQUIPE = "zupeli_vilela_dib"` nos 3 `main.py` e abra o dashboard com `index.html?equipe=novo_id`.

## Integração (resumo)
`CPS1` mede calor → publica `cps1/alerta` → `CPS2` abre a janela e publica `cps2/estado` → `CPS3` sobe o limite de umidade do solo (+20 calor, +10 janela aberta) e liga a bomba → publica `cps3/estado` → `CPS1` acende o LED azul. Detalhes e tabela de tópicos no relatório.

## Teste local (opcional)
`python3 testes/teste_integracao.py` (precisa de `micropython`, `mosquitto` e `paho-mqtt`) roda os 3 `main.py` com hardware simulado e confere toda a cadeia, comandos, mensagens inválidas e reconexão.
