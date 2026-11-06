<?php
declare(strict_types=1);

// Funções compartilhadas pela API: JSON, validação e leitura do banco.
// A tela nunca imprime HTML vindo daqui. O que sai é JSON.
// O JavaScript é quem monta o HTML, e lá cada texto do usuário passa por escapeHtml.

error_reporting(E_ALL);
ini_set('display_errors', '0');
ini_set('log_errors', '1');

// Categorias e status ficam nestas funções para existir um único lugar no PHP.
// Se criar uma categoria nova, inclua o valor aqui e também em client/js/app.js.
function categorias_evento(): array
{
    return ['voo', 'hospedagem', 'comida', 'passeio', 'transporte', 'outro'];
}

function status_evento(): array
{
    return ['pendente', 'confirmado'];
}

function limite_dias_viagem(): int
{
    // A tela cria uma aba por dia. Um ano ainda é usável;
    // um intervalo de séculos travaria o navegador.
    return 366;
}

function iniciar_api(): void
{
    header('Content-Type: application/json; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    // GET de lista não pode ficar guardado no navegador, senão a viagem criada
    // some até o usuário atualizar a página na mão.
    header('Cache-Control: no-store');
}

function responder_json(array $corpo, int $codigo): void
{
    http_response_code($codigo);
    $json = json_encode(
        $corpo,
        JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT
    );

    if ($json === false) {
        error_log('Falha ao gerar JSON: ' . json_last_error_msg());
        http_response_code(500);
        echo '{"ok":false,"erro":"Não foi possível montar a resposta."}';
        exit;
    }

    echo $json;
    exit;
}

function responder_ok($dados, int $codigo = 200): void
{
    responder_json(['ok' => true, 'dados' => $dados], $codigo);
}

function responder_erro(string $mensagem, int $codigo = 400, array $campos = []): void
{
    $corpo = ['ok' => false, 'erro' => $mensagem];
    // "campos" não substitui "erro": a tela usa os dois.
    // erro vai para o toast; campos desenha a frase embaixo do input.
    if ($campos !== []) {
        $corpo['campos'] = $campos;
    }
    responder_json($corpo, $codigo);
}

function tratar_excecao(Throwable $e): void
{
    error_log($e::class . ': ' . $e->getMessage());

    if ($e instanceof PDOException) {
        responder_erro(mensagem_amigavel_pdo($e), 500);
    }

    if ($e instanceof RuntimeException) {
        // Estas mensagens foram escritas por nós (config, extensão, certificado).
        // A mensagem do PDO não entra aqui, para não vazar host ou usuário.
        responder_erro($e->getMessage(), 500);
    }

    responder_erro('Ocorreu um erro inesperado.', 500);
}

function mensagem_amigavel_pdo(PDOException $e): string
{
    // O código costuma vir como HY000, e o número do MySQL fica no texto.
    $texto = $e->getMessage();

    if (stripos($texto, 'certificate') !== false || stripos($texto, 'SSL') !== false || stripos($texto, 'TLS') !== false) {
        return 'Falha na conexão segura (SSL). Confira o caminho do certificado em ssl_ca.';
    }

    if (stripos($texto, 'not allowed') !== false || stripos($texto, 'ip address') !== false) {
        return 'O TiDB recusou este computador. Libere o seu IP na área Networking do cluster.';
    }

    if (strpos($texto, '1045') !== false || stripos($texto, 'Access denied') !== false) {
        return 'Usuário ou senha do banco foram recusados. Confira o config.local.php.';
    }

    if (
        strpos($texto, '2002') !== false
        || strpos($texto, '2003') !== false
        || stripos($texto, 'timed out') !== false
        || stripos($texto, 'getaddrinfo') !== false
        || stripos($texto, 'Connection refused') !== false
    ) {
        return 'Não foi possível alcançar o TiDB. Confira host, porta 4000 e se o seu IP está liberado no painel.';
    }

    if (strpos($texto, '1049') !== false || stripos($texto, 'Unknown database') !== false) {
        return 'O banco informado não existe. Confira o nome em config.local.php.';
    }

    if (strpos($texto, '1146') !== false || stripos($texto, 'Base table') !== false || stripos($texto, "doesn't exist") !== false) {
        return 'As tabelas ainda não existem. Execute database/schema.sql no SQL Editor do TiDB Cloud.';
    }

    return 'Não foi possível acessar o banco de dados.';
}

function ler_corpo_json(): array
{
    // $_POST só é preenchido em formulário tradicional (application/x-www-form-urlencoded).
    // O fetch manda JSON, então o corpo cru está em php://input.
    $bruto = file_get_contents('php://input');
    if ($bruto === false || trim($bruto) === '') {
        return [];
    }

    $dados = json_decode($bruto, true);
    if (!is_array($dados)) {
        responder_erro('O corpo da requisição não é um JSON válido.', 400);
    }

    return $dados;
}

function inteiro_positivo($valor): ?int
{
    if (is_int($valor) && $valor > 0) {
        return $valor;
    }

    if ((is_string($valor) || is_numeric($valor)) && preg_match('/^[1-9][0-9]*$/', (string)$valor)) {
        return (int)$valor;
    }

    return null;
}

function inteiro_da_url(string $nome, bool $obrigatorio): ?int
{
    if (!isset($_GET[$nome]) || $_GET[$nome] === '') {
        if ($obrigatorio) {
            responder_erro('Informe o identificador.', 400);
        }
        return null;
    }

    $id = inteiro_positivo((string)$_GET[$nome]);
    if ($id === null) {
        responder_erro('Identificador inválido.', 400);
    }

    return $id;
}

function ler_texto($valor): ?string
{
    if ($valor === null) {
        return null;
    }

    if (is_array($valor) || is_object($valor)) {
        return null;
    }

    $texto = str_replace("\0", '', (string)$valor);
    return trim($texto);
}

function tamanho_texto(string $texto): int
{
    // strlen conta bytes. "São" tem 2 caracteres e mais bytes, e estouraria o limite à toa.
    if (function_exists('mb_strlen')) {
        return mb_strlen($texto);
    }

    return strlen($texto);
}

function data_iso_valida(string $data): bool
{
    // O ! zera a hora. Sem ele, o relógio atual do servidor entraria na conta.
    $objeto = DateTime::createFromFormat('!Y-m-d', $data);
    return $objeto instanceof DateTime && $objeto->format('Y-m-d') === $data;
}

function horario_valido(string $horario): bool
{
    return preg_match('/^(?:[01][0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?$/', $horario) === 1;
}

function quantidade_dias(string $ida, string $volta): int
{
    $inicio = DateTime::createFromFormat('!Y-m-d', $ida);
    $fim = DateTime::createFromFormat('!Y-m-d', $volta);
    if (!$inicio instanceof DateTime || !$fim instanceof DateTime) {
        return 0;
    }

    return (int)$inicio->diff($fim)->days + 1;
}

function ler_decimal($valor): ?string
{
    if (is_array($valor) || is_object($valor) || $valor === null) {
        return null;
    }

    if (is_int($valor) || is_float($valor)) {
        if (!is_finite((float)$valor)) {
            return null;
        }
        return number_format(round((float)$valor, 2), 2, '.', '');
    }

    $texto = trim((string)$valor);
    if ($texto === '') {
        return null;
    }

    // A tela manda 10.50, mas alguém pode colar 1.234,56.
    if (strpos($texto, ',') !== false) {
        $texto = str_replace('.', '', $texto);
        $texto = str_replace(',', '.', $texto);
    }

    if (!preg_match('/^-?\d+(\.\d+)?$/', $texto)) {
        return null;
    }

    return number_format(round((float)$texto, 2), 2, '.', '');
}

function validar_viagem(array $dados): array
{
    $erros = [];
    $destino = ler_texto($dados['destino'] ?? null) ?? '';
    $ida = ler_texto($dados['data_ida'] ?? null) ?? '';
    $volta = ler_texto($dados['data_volta'] ?? null) ?? '';
    $orcamento = ler_decimal($dados['orcamento'] ?? null);
    $observacoes = ler_texto($dados['observacoes'] ?? null);

    if ($destino === '') {
        $erros['destino'] = 'Destino é obrigatório.';
    } elseif (tamanho_texto($destino) > 120) {
        $erros['destino'] = 'Destino deve ter no máximo 120 caracteres.';
    }

    if ($ida === '') {
        $erros['data_ida'] = 'Informe a data de ida.';
    } elseif (!data_iso_valida($ida)) {
        $erros['data_ida'] = 'Data de ida inválida.';
    }

    if ($volta === '') {
        $erros['data_volta'] = 'Informe a data de volta.';
    } elseif (!data_iso_valida($volta)) {
        $erros['data_volta'] = 'Data de volta inválida.';
    }

    // YYYY-MM-DD com zeros pode ser comparado como texto: "2026-12-23" > "2026-12-20".
    if (!isset($erros['data_ida']) && !isset($erros['data_volta']) && $volta < $ida) {
        $erros['data_volta'] = 'A data de volta não pode ser anterior à data de ida.';
    }

    if (!isset($erros['data_ida']) && !isset($erros['data_volta'])) {
        $dias = quantidade_dias($ida, $volta);
        if ($dias > limite_dias_viagem()) {
            $erros['data_volta'] = 'A viagem pode ter no máximo ' . limite_dias_viagem() . ' dias.';
        }
    }

    if ($orcamento === null) {
        $erros['orcamento'] = 'Informe um orçamento válido.';
    } elseif ((float)$orcamento < 0) {
        $erros['orcamento'] = 'O orçamento não pode ser negativo.';
    } elseif ((float)$orcamento > 99999999.99) {
        // O mesmo teto da coluna DECIMAL(10,2). Acima disso o banco recusaria com erro cru.
        $erros['orcamento'] = 'Orçamento maior do que o permitido.';
    }

    if ($observacoes === '') {
        $observacoes = null;
    }

    if (array_key_exists('observacoes', $dados) && $dados['observacoes'] !== null && ler_texto($dados['observacoes']) === null && $dados['observacoes'] !== '') {
        $erros['observacoes'] = 'Observações inválidas.';
    }

    return [
        'erros' => $erros,
        'limpos' => [
            'destino' => $destino,
            'data_ida' => $ida,
            'data_volta' => $volta,
            'orcamento' => $orcamento ?? '0.00',
            'observacoes' => $observacoes,
        ],
    ];
}

function validar_evento(array $dados, array $viagem): array
{
    $erros = [];
    $titulo = ler_texto($dados['titulo'] ?? null) ?? '';
    $data = ler_texto($dados['data'] ?? null) ?? '';
    $horario = ler_texto($dados['horario'] ?? null) ?? '';
    $local = ler_texto($dados['local'] ?? null);
    $categoria = ler_texto($dados['categoria'] ?? null) ?? '';
    $status = ler_texto($dados['status'] ?? null) ?? '';
    $valor = ler_decimal($dados['valor'] ?? null);
    $observacoes = ler_texto($dados['observacoes'] ?? null);

    if ($titulo === '') {
        $erros['titulo'] = 'Título é obrigatório.';
    } elseif (tamanho_texto($titulo) > 150) {
        $erros['titulo'] = 'Título deve ter no máximo 150 caracteres.';
    }

    $ida = somente_data((string)$viagem['data_ida']);
    $volta = somente_data((string)$viagem['data_volta']);

    if ($data === '' || !data_iso_valida($data)) {
        $erros['data'] = 'Informe a data do evento.';
    } elseif ($data < $ida || $data > $volta) {
        $erros['data'] = 'A data do evento deve estar dentro do período da viagem.';
    }

    if ($horario === '') {
        $erros['horario'] = 'Informe o horário.';
    } elseif (!horario_valido($horario)) {
        $erros['horario'] = 'Horário inválido.';
    } elseif (strlen($horario) === 5) {
        $horario .= ':00';
    }

    if ($local === '') {
        $local = null;
    } elseif ($local !== null && tamanho_texto($local) > 150) {
        $erros['local'] = 'Local deve ter no máximo 150 caracteres.';
    }

    if (!in_array($categoria, categorias_evento(), true)) {
        $erros['categoria'] = 'Selecione uma categoria válida.';
    }

    if (!in_array($status, status_evento(), true)) {
        $erros['status'] = 'Selecione um status válido.';
    }

    if ($valor === null) {
        $erros['valor'] = 'Informe um valor válido.';
    } elseif ((float)$valor < 0) {
        $erros['valor'] = 'O valor não pode ser negativo.';
    } elseif ((float)$valor > 99999999.99) {
        $erros['valor'] = 'Valor maior do que o permitido.';
    }

    if ($observacoes === '') {
        $observacoes = null;
    }

    return [
        'erros' => $erros,
        'limpos' => [
            'titulo' => $titulo,
            'data' => $data,
            'horario' => $horario,
            'local' => $local,
            'categoria' => $categoria,
            'status' => $status,
            'valor' => $valor ?? '0.00',
            'observacoes' => $observacoes,
        ],
    ];
}

function somente_data(string $valor): string
{
    // Alguns drivers devolvem DATE como "2026-12-20 00:00:00". A tela precisa só do dia.
    return substr($valor, 0, 10);
}

function mapear_viagem(array $linha): array
{
    return [
        'id' => (int)$linha['id'],
        'destino' => $linha['destino'],
        'data_ida' => somente_data((string)$linha['data_ida']),
        'data_volta' => somente_data((string)$linha['data_volta']),
        // String com duas casas: o JSON numérico pode arredondar centavos.
        'orcamento' => number_format((float)$linha['orcamento'], 2, '.', ''),
        'observacoes' => $linha['observacoes'],
        'criado_em' => $linha['criado_em'],
    ];
}

function mapear_evento(array $linha): array
{
    return [
        'id' => (int)$linha['id'],
        'viagem_id' => (int)$linha['viagem_id'],
        'data' => somente_data((string)$linha['data']),
        'horario' => substr((string)$linha['horario'], 0, 5),
        'titulo' => $linha['titulo'],
        'local' => $linha['local'],
        'categoria' => $linha['categoria'],
        'valor' => number_format((float)$linha['valor'], 2, '.', ''),
        'status' => $linha['status'],
        'observacoes' => $linha['observacoes'],
        'criado_em' => $linha['criado_em'],
    ];
}

// Colunas repetidas de propósito ao lado do mapeamento.
// Se adicionar um campo, inclua a coluna no SELECT, em mapear_* e no INSERT/UPDATE da API.

function buscar_viagem(PDO $pdo, int $id): ?array
{
    // O ? nunca é concatenado. O driver envia o id separado do texto SQL.
    $stmt = $pdo->prepare(
        'SELECT id, destino, data_ida, data_volta, orcamento, observacoes, criado_em
         FROM viagens
         WHERE id = ?'
    );
    $stmt->execute([$id]);
    $linha = $stmt->fetch();
    return $linha === false ? null : $linha;
}

function listar_viagens(PDO $pdo): array
{
    $stmt = $pdo->prepare(
        'SELECT id, destino, data_ida, data_volta, orcamento, observacoes, criado_em
         FROM viagens
         ORDER BY data_ida ASC, id ASC'
    );
    $stmt->execute();
    return $stmt->fetchAll();
}

function buscar_evento(PDO $pdo, int $id): ?array
{
    $stmt = $pdo->prepare(
        'SELECT id, viagem_id, data, horario, titulo, local, categoria, valor, status, observacoes, criado_em
         FROM eventos
         WHERE id = ?'
    );
    $stmt->execute([$id]);
    $linha = $stmt->fetch();
    return $linha === false ? null : $linha;
}

function listar_eventos_da_viagem(PDO $pdo, int $viagemId): array
{
    $stmt = $pdo->prepare(
        'SELECT id, viagem_id, data, horario, titulo, local, categoria, valor, status, observacoes, criado_em
         FROM eventos
         WHERE viagem_id = ?
         ORDER BY data ASC, horario ASC, id ASC'
    );
    $stmt->execute([$viagemId]);
    return $stmt->fetchAll();
}

function existe_evento_fora_do_periodo(PDO $pdo, int $viagemId, string $ida, string $volta): bool
{
    $stmt = $pdo->prepare(
        'SELECT id
         FROM eventos
         WHERE viagem_id = ? AND (data < ? OR data > ?)
         LIMIT 1'
    );
    $stmt->execute([$viagemId, $ida, $volta]);
    return $stmt->fetch() !== false;
}
