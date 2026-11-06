# Itinera

Itinera é o produto de roteiro de viagem: destino, dias e eventos no mesmo lugar. A tela fica em `client/`. O PHP fica em `server/`: `server/api/viagens.php` e `server/api/eventos.php`. O banco é o TiDB Cloud, compatível com MySQL.

Não use o XAMPP e não abra o HTML por outro servidor (Live Server, porta 5500). O PHP embutido entrega a página e a API no mesmo endereço.

## Como rodar

1. Instale o PHP e ative a extensão `pdo_mysql` no `php.ini`.
   Para achar o arquivo: `php --ini`. A linha fica assim (sem `;` na frente):

   ```ini
   extension=pdo_mysql
   ```

   Se existir `extension=mbstring`, deixe ativa também. Ela faz o limite de 120 caracteres contar letras com acento, não bytes.

2. Crie um cluster no [TiDB Cloud](https://tidbcloud.com). Na janela **Connect**, copie host, porta `4000`, usuário e senha. Anote também o caminho do certificado CA (ou baixe o arquivo).

3. No SQL Editor do TiDB Cloud, abra `database/schema.sql`, cole o conteúdo e execute. Isso cria as tabelas `viagem` e `evento` e alguns roteiros de exemplo. Rodar de novo apaga o que já estiver nessas tabelas.

4. Copie a configuração e preencha com os seus dados:

   ```bash
   cp server/config/config.example.php server/config/config.local.php
   ```

   No Windows, se `cp` não existir:

   ```bash
   copy server\config\config.example.php server\config\config.local.php
   ```

   O arquivo `server/config/config.local.php` está no `.gitignore`. Não commite a senha.

5. Na pasta deste projeto (a pasta onde estão `client` e `server`):

   ```bash
   php -S localhost:8000
   ```

6. Abra [http://localhost:8000](http://localhost:8000).

## Problemas comuns

**`could not find driver` ou a mensagem sobre `pdo_mysql`**  
A extensão não está ativa. Edite o `php.ini` que o comando `php --ini` mostrar, tire o `;` de `extension=pdo_mysql`, salve e suba o `php -S` de novo.

**Erro de SSL / `certificate verify failed`**  
O TiDB exige TLS. Confira `ssl_ca` em `server/config/config.local.php`.

- Windows: o PHP não usa o cofre do sistema. Baixe o CA na janela Connect e use um caminho com barras normais, por exemplo `C:/Users/seu-usuario/Downloads/ca.pem`.
- macOS: `/etc/ssl/cert.pem`
- Linux (Debian/Ubuntu): `/etc/ssl/certs/ca-certificates.crt`
- Linux (CentOS/Fedora): `/etc/pki/tls/certs/ca-bundle.crt`

Se o caminho estiver certo e o erro continuar, mude `ssl_verificar` para `false` (sem aspas) só para destravar.

**Não conecta, demora ou fala em IP**  
No painel do cluster, em Networking, libere o IP desta máquina. A porta é `4000`, não `3306`.

**Usuário ou senha recusados**  
A senha da janela Connect só aparece uma vez. Se perdeu, gere outra no painel e atualize `config.local.php`. O usuário costuma terminar com `.root`.

**As tabelas ainda não existem**  
Execute `database/schema.sql` no SQL Editor. O nome do banco (muitas vezes `test`) tem de ser o mesmo de `banco` no `config.local.php`.

**A página abre mas criar/editar não grava, ou o navegador bloqueia PUT/DELETE**  
Você provavelmente abriu o HTML por outro programa. Pare esse servidor e use só `php -S localhost:8000` dentro desta pasta.

**`config.local.php` não encontrado ou campos vazios**  
O passo 4 não foi feito, ou host/usuário/senha ficaram em branco.

## Onde mexer depois

**Cores:** variáveis no topo de `client/css/style.css` (`:root` e `:root[data-tema="escuro"]`).

**Categoria nova:** três lugares, com o mesmo identificador (por exemplo `show`):

- a lista de categorias em `server/api/eventos.php`, dentro de `validar_evento()`
- a lista `CATEGORIAS` em `client/js/app.js`
- as cores `--cat-show` nos dois blocos de `client/css/style.css`, mais `.cat-show` e `.icone-cat.cat-show`
- se quiser um ícone, o objeto `ICONES` em `client/js/ui.js`

**Campo novo no evento:** a ordem prática é esta.

1. Coluna em `database/schema.sql` (e o mesmo `ALTER` no TiDB, se o banco já existir).
2. `validar_evento()` em `server/api/eventos.php`.
3. O `INSERT`, o `UPDATE` e o `SELECT` em `server/api/eventos.php`.
4. `formatar_evento()` para o JSON incluir o campo.
5. O formulário em `criarFormularioEvento()` e o objeto enviado em `salvarEvento()`, ambos em `client/js/app.js`.
6. Se o campo aparecer no card, `htmlEvento()` no mesmo arquivo.

A validação do JavaScript só antecipa o erro na tela. A do PHP é a que vale.
