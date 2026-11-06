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

## Pending decision
None.
