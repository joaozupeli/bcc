# Learning Progress

## Organizador de Viagens

### Introduced
- The learner supplied the full architecture, schema, API contract, validations, and UX, and asked for every file to be generated.
- Implementation followed that specification. The previous book CRUD under `2. Semestre/web programming/crud` was removed.

### Demonstrated understanding
- No design reasoning demonstrated yet. The specification was the assignment to implement.

### Needs reinforcement
- Why the PHP prepared statement and the transaction exist, and why `new Date('YYYY-MM-DD')` shifts the calendar day, when the learner starts changing the code.

### Configuração da conexão
- O aprendiz enviou a URL JDBC da janela Connect. Os valores foram gravados em `config/config.local.php`, que já fica fora do Git.
- A opção de um `.env` lido por um config versionado não foi repetida nessa mensagem.
- No Windows o certificado usado é a raiz pública ISRG Root X1, em `C:/Users/zupeli/certs/isrgrootx1.pem`.
- Um script PHP chamou `obter_conexao()` e a conexão com o TiDB respondeu.

### Pastas
- A pasta foi dividida em `client` (tela) e `server` (PHP). O banco não mudou. O caminho da senha passou a ser `server/config/config.local.php`.

## Sistema ciberfísico — janelas Wokwi

### Introduced
- O aprendiz quer os iframes do Wokwi como janelas do projeto, para o MQTT aparecer ao vivo junto com as simulações.

### Decided
- Três janelas no `dashboard/index.html`, uma por projeto: CPS1 `480087264328094721`, CPS2 `480087477963940865`, CPS3 `480087507036763137`.
- Os botões continuam publicando o JSON que cada `main.py` já espera em `cscf/zupeli_vilela_dib/<cps>/comando`.

### Implemented
- `cscf_mqtt/dashboard/index.html` reescrito com um iframe por sistema, números, botões e o log de mensagens.
- O CSS foi para `dashboard/style.css` e o JavaScript da página para `dashboard/script.js`. O HTML só liga esses arquivos. A biblioteca mqtt.js continua no HTML, vinda do CDN.
- Os links “abrir” saíram. O iframe de cada CPS voltou, porque é a janela que mostra o projeto. O título e o painel continuam.
- A barra do site do Wokwi (logo, Sign in e abas) fica cortada no CSS. O circuito e o botão de play continuam visíveis.

### Pending decision
None.
