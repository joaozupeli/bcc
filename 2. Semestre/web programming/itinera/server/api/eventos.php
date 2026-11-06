<?php
declare(strict_types=1);

require_once __DIR__ . '/../config/database.php';

ini_set('display_errors', '0');
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept');

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
    http_response_code(200);
    exit;
}

try {
    $pdo = obter_conexao();
    $metodo = $_SERVER['REQUEST_METHOD'] ?? 'GET';

    if ($metodo === 'GET') {
        listar($pdo);
    } elseif ($metodo === 'POST') {
        criar($pdo);
    } elseif ($metodo === 'PUT') {
        atualizar($pdo);
    } elseif ($metodo === 'DELETE') {
        excluir($pdo);
    } else {
        header('Allow: GET, POST, PUT, DELETE');
        responder_erro('Método não permitido.', 405);
    }
} catch (Throwable $e) {
    error_log($e->getMessage());
    responder_erro(mensagem_banco($e), 500);
}

function listar(PDO $pdo): void
{
    $viagemId = id_da_url('viagem_id');
    if (buscar_viagem($pdo, $viagemId) === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $stmt = $pdo->prepare(
        'SELECT id, viagem_id, data, horario, titulo, local, categoria, valor, status, observacoes, criado_em
         FROM evento
         WHERE viagem_id = ?
         ORDER BY data ASC, horario ASC, id ASC'
    );
    $stmt->execute([$viagemId]);

    $lista = [];
    foreach ($stmt->fetchAll() as $linha) {
        $lista[] = formatar_evento($linha);
    }
    responder_ok($lista);
}

function criar(PDO $pdo): void
{
    $dados = ler_json();
    $viagemId = isset($dados['viagem_id']) ? (int)$dados['viagem_id'] : 0;
    if ($viagemId <= 0) {
        responder_erro('Informe a viagem do evento.', 400, [
            'viagem_id' => 'Informe a viagem do evento.',
        ]);
    }

    $viagem = buscar_viagem($pdo, $viagemId);
    if ($viagem === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $erros = validar_evento($dados, $viagem);
    if ($erros !== []) {
        responder_erro('Verifique os campos destacados.', 400, $erros);
    }

    $stmt = $pdo->prepare(
        'INSERT INTO evento (viagem_id, data, horario, titulo, local, categoria, valor, status, observacoes)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    );
    $stmt->execute([
        $viagemId,
        $dados['data'],
        horario_banco($dados['horario']),
        trim((string)$dados['titulo']),
        texto_ou_nulo($dados['local'] ?? null),
        $dados['categoria'],
        numero($dados['valor']),
        $dados['status'],
        texto_ou_nulo($dados['observacoes'] ?? null),
    ]);

    responder_ok(buscar_formatado($pdo, (int)$pdo->lastInsertId()), 201);
}

function atualizar(PDO $pdo): void
{
    $id = id_da_url('id');
    $atual = buscar_linha($pdo, $id);
    if ($atual === null) {
        responder_erro('Evento não encontrado.', 404);
    }

    $viagem = buscar_viagem($pdo, (int)$atual['viagem_id']);
    if ($viagem === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $dados = ler_json();
    $erros = validar_evento($dados, $viagem);
    if ($erros !== []) {
        responder_erro('Verifique os campos destacados.', 400, $erros);
    }

    $stmt = $pdo->prepare(
        'UPDATE evento
         SET data = ?, horario = ?, titulo = ?, local = ?, categoria = ?, valor = ?, status = ?, observacoes = ?
         WHERE id = ?'
    );
    $stmt->execute([
        $dados['data'],
        horario_banco($dados['horario']),
        trim((string)$dados['titulo']),
        texto_ou_nulo($dados['local'] ?? null),
        $dados['categoria'],
        numero($dados['valor']),
        $dados['status'],
        texto_ou_nulo($dados['observacoes'] ?? null),
        $id,
    ]);

    responder_ok(buscar_formatado($pdo, $id));
}

function excluir(PDO $pdo): void
{
    $id = id_da_url('id');
    if (buscar_linha($pdo, $id) === null) {
        responder_erro('Evento não encontrado.', 404);
    }

    $stmt = $pdo->prepare('DELETE FROM evento WHERE id = ?');
    $stmt->execute([$id]);
    responder_ok(['id' => $id]);
}

function buscar_viagem(PDO $pdo, int $id): ?array
{
    $stmt = $pdo->prepare('SELECT id, data_ida, data_volta FROM viagem WHERE id = ?');
    $stmt->execute([$id]);
    $linha = $stmt->fetch();
    if ($linha === false) {
        return null;
    }
    $linha['data_ida'] = substr((string)$linha['data_ida'], 0, 10);
    $linha['data_volta'] = substr((string)$linha['data_volta'], 0, 10);
    return $linha;
}

function buscar_linha(PDO $pdo, int $id): ?array
{
    $stmt = $pdo->prepare(
        'SELECT id, viagem_id, data, horario, titulo, local, categoria, valor, status, observacoes, criado_em
         FROM evento
         WHERE id = ?'
    );
    $stmt->execute([$id]);
    $linha = $stmt->fetch();
    return $linha === false ? null : $linha;
}

function buscar_formatado(PDO $pdo, int $id): array
{
    $linha = buscar_linha($pdo, $id);
    if ($linha === null) {
        responder_erro('Evento não encontrado.', 404);
    }
    return formatar_evento($linha);
}

function formatar_evento(array $linha): array
{
    return [
        'id' => (int)$linha['id'],
        'viagem_id' => (int)$linha['viagem_id'],
        'data' => substr((string)$linha['data'], 0, 10),
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

function validar_evento(array $dados, array $viagem): array
{
    $erros = [];
    $titulo = trim((string)($dados['titulo'] ?? ''));
    $data = trim((string)($dados['data'] ?? ''));
    $horario = trim((string)($dados['horario'] ?? ''));
    $local = trim((string)($dados['local'] ?? ''));
    $categoria = trim((string)($dados['categoria'] ?? ''));
    $status = trim((string)($dados['status'] ?? ''));
    $valor = numero($dados['valor'] ?? null);
    $categorias = ['voo', 'hospedagem', 'comida', 'passeio', 'transporte', 'outro'];
    $statusValidos = ['pendente', 'confirmado'];

    if ($titulo === '') {
        $erros['titulo'] = 'Título é obrigatório.';
    } elseif (tamanho($titulo) > 150) {
        $erros['titulo'] = 'Título deve ter no máximo 150 caracteres.';
    }

    if (!data_valida($data) || $data < $viagem['data_ida'] || $data > $viagem['data_volta']) {
        $erros['data'] = 'A data do evento deve estar dentro do período da viagem.';
    }

    if (!preg_match('/^(?:[01][0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?$/', $horario)) {
        $erros['horario'] = 'Informe o horário.';
    }

    if (tamanho($local) > 150) {
        $erros['local'] = 'Local deve ter no máximo 150 caracteres.';
    }

    if (!in_array($categoria, $categorias, true)) {
        $erros['categoria'] = 'Selecione uma categoria válida.';
    }
    if (!in_array($status, $statusValidos, true)) {
        $erros['status'] = 'Selecione um status válido.';
    }

    if ($valor === null) {
        $erros['valor'] = 'Informe um valor válido.';
    } elseif ($valor < 0) {
        $erros['valor'] = 'O valor não pode ser negativo.';
    } elseif ($valor > 99999999.99) {
        $erros['valor'] = 'Valor maior do que o permitido.';
    }

    return $erros;
}

function horario_banco(string $horario): string
{
    $horario = trim($horario);
    if (strlen($horario) === 5) {
        return $horario . ':00';
    }
    return $horario;
}

function id_da_url(string $nome): int
{
    if (!isset($_GET[$nome]) || $_GET[$nome] === '') {
        responder_erro('Informe o identificador.', 400);
    }

    if (!preg_match('/^[1-9][0-9]*$/', (string)$_GET[$nome])) {
        responder_erro('Identificador inválido.', 400);
    }

    return (int)$_GET[$nome];
}

function ler_json(): array
{
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

function numero($valor): ?string
{
    if (is_array($valor) || is_object($valor) || $valor === null) {
        return null;
    }

    $texto = trim((string)$valor);
    if ($texto === '') {
        return null;
    }

    if (str_contains($texto, ',')) {
        $texto = str_replace('.', '', $texto);
        $texto = str_replace(',', '.', $texto);
    }

    if (!preg_match('/^-?\d+(\.\d+)?$/', $texto)) {
        return null;
    }

    return number_format(round((float)$texto, 2), 2, '.', '');
}

function texto_ou_nulo($valor): ?string
{
    if ($valor === null || is_array($valor) || is_object($valor)) {
        return null;
    }

    $texto = trim((string)$valor);
    return $texto === '' ? null : $texto;
}

function tamanho(string $texto): int
{
    return function_exists('mb_strlen') ? mb_strlen($texto) : strlen($texto);
}

function data_valida(string $data): bool
{
    $objeto = DateTime::createFromFormat('!Y-m-d', $data);
    return $objeto instanceof DateTime && $objeto->format('Y-m-d') === $data;
}

function responder_ok($dados, int $codigo = 200): void
{
    http_response_code($codigo);
    echo json_encode(['ok' => true, 'dados' => $dados], JSON_UNESCAPED_UNICODE);
    exit;
}

function responder_erro(string $mensagem, int $codigo = 400, array $campos = []): void
{
    http_response_code($codigo);
    $corpo = ['ok' => false, 'erro' => $mensagem];
    if ($campos !== []) {
        $corpo['campos'] = $campos;
    }
    echo json_encode($corpo, JSON_UNESCAPED_UNICODE);
    exit;
}

function mensagem_banco(Throwable $e): string
{
    if ($e instanceof PDOException) {
        if (str_contains($e->getMessage(), '1146')) {
            return 'As tabelas ainda não existem no banco.';
        }
        return 'Não foi possível acessar o banco de dados.';
    }

    if ($e instanceof RuntimeException) {
        return $e->getMessage();
    }

    return 'Ocorreu um erro inesperado.';
}
