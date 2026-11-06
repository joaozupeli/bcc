# Project Map

## Purpose
Itinera: produto de roteiro de viagem. Cadastra viagens e, dentro de cada dia, os eventos.

## Requirements
Specified by the learner for a college assignment: vanilla HTML, CSS, JavaScript, and PHP; TiDB Cloud via PDO with TLS; JSON API; trip and event CRUD; day tabs; budget; filters; print; light/dark theme. No libraries.

## Components
- `2. Semestre/web programming/itinera/index.php` — redirect to the page
- `client/index.html` — single page
- `client/js/api.js` — fetch to `/server/api`
- `client/js/ui.js` — modal, toast, dates, money, escapeHtml
- `client/js/app.js` — screen rules and forms
- `client/css/style.css` — theme variables
- `server/api/viagens.php`, `server/api/eventos.php` — HTTP methods
- `server/helpers.php` — JSON, validation, queries
- `server/config/database.php` — PDO
- `server/config/config.local.php` — secrets, gitignored
- `database/schema.sql` — tables and sample rows

## Main Flow
Browser (client/index.html) -> Api.fetch /server/api -> helpers validation -> PDO -> TiDB Cloud
Delete trip: beginTransaction -> delete eventos -> delete viagem -> commit

## Data and Trust Boundaries
TiDB Cloud holds the rows. Credentials stay in server/config/config.local.php. PHP is the validation that counts. HTML is escaped in JavaScript before innerHTML.

## Build and Deployment
From the project folder: `php -S localhost:8000`. Schema is run by hand in the TiDB Cloud SQL editor. `obter_conexao()` reached the cluster after `config.local.php` was filled. The database name in that file is `escola`.

## Unknowns
Whether the tables from `database/schema.sql` already exist inside the `escola` database.
