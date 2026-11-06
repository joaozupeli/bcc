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
        listar_ou_buscar($pdo);
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

function listar_ou_buscar(PDO $pdo): void
{
    $id = id_da_url(false);

    if ($id !== null) {
        $stmt = $pdo->prepare(
            'SELECT id, destino, data_ida, data_volta, orcamento, observacoes, criado_em
             FROM viagem
             WHERE id = ?'
        );
        $stmt->execute([$id]);
        $viagem = $stmt->fetch();
        if ($viagem === false) {
            responder_erro('Viagem não encontrada.', 404);
        }
        responder_ok(formatar_viagem($viagem));
    }

    $stmt = $pdo->query(
        'SELECT id, destino, data_ida, data_volta, orcamento, observacoes, criado_em
         FROM viagem
         ORDER BY data_ida ASC, id ASC'
    );

    $lista = [];
    foreach ($stmt->fetchAll() as $linha) {
        $lista[] = formatar_viagem($linha);
    }
    responder_ok($lista);
}

function criar(PDO $pdo): void
{
    $dados = ler_json();
    $erros = validar_viagem($dados);
    if ($erros !== []) {
        responder_erro('Verifique os campos destacados.', 400, $erros);
    }

    $stmt = $pdo->prepare(
        'INSERT INTO viagem (destino, data_ida, data_volta, orcamento, observacoes)
         VALUES (?, ?, ?, ?, ?)'
    );
    $stmt->execute([
        trim((string)$dados['destino']),
        $dados['data_ida'],
        $dados['data_volta'],
        numero($dados['orcamento']),
        texto_ou_nulo($dados['observacoes'] ?? null),
    ]);

    responder_ok(buscar_formatada($pdo, (int)$pdo->lastInsertId()), 201);
}

function atualizar(PDO $pdo): void
{
    $id = id_da_url(true);
    $atual = buscar_linha($pdo, $id);
    if ($atual === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $dados = ler_json();
    $erros = validar_viagem($dados);
    if ($erros !== []) {
        responder_erro('Verifique os campos destacados.', 400, $erros);
    }

    $ida = $dados['data_ida'];
    $volta = $dados['data_volta'];

    $fora = $pdo->prepare(
        'SELECT id FROM evento WHERE viagem_id = ? AND (data < ? OR data > ?) LIMIT 1'
    );
    $fora->execute([$id, $ida, $volta]);
    if ($fora->fetch() !== false) {
        $mensagem = 'Há eventos fora do novo período. Apague ou mova esses eventos antes de encurtar a viagem.';
        responder_erro($mensagem, 400, [
            'data_ida' => $mensagem,
            'data_volta' => $mensagem,
        ]);
    }

    $stmt = $pdo->prepare(
        'UPDATE viagem
         SET destino = ?, data_ida = ?, data_volta = ?, orcamento = ?, observacoes = ?
         WHERE id = ?'
    );
    $stmt->execute([
        trim((string)$dados['destino']),
        $ida,
        $volta,
        numero($dados['orcamento']),
        texto_ou_nulo($dados['observacoes'] ?? null),
        $id,
    ]);

    responder_ok(buscar_formatada($pdo, $id));
}

function excluir(PDO $pdo): void
{
    $id = id_da_url(true);
    if (buscar_linha($pdo, $id) === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $pdo->beginTransaction();
    try {
        $eventos = $pdo->prepare('DELETE FROM evento WHERE viagem_id = ?');
        $eventos->execute([$id]);

        $viagem = $pdo->prepare('DELETE FROM viagem WHERE id = ?');
        $viagem->execute([$id]);

        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) {
            $pdo->rollBack();
        }
        throw $e;
    }

    responder_ok(['id' => $id]);
}

function buscar_linha(PDO $pdo, int $id): ?array
{
    $stmt = $pdo->prepare(
        'SELECT id, destino, data_ida, data_volta, orcamento, observacoes, criado_em
         FROM viagem
         WHERE id = ?'
    );
    $stmt->execute([$id]);
    $linha = $stmt->fetch();
    return $linha === false ? null : $linha;
}

function buscar_formatada(PDO $pdo, int $id): array
{
    $linha = buscar_linha($pdo, $id);
    if ($linha === null) {
        responder_erro('Viagem não encontrada.', 404);
    }
    return formatar_viagem($linha);
}

function formatar_viagem(array $linha): array
{
    return [
        'id' => (int)$linha['id'],
        'destino' => $linha['destino'],
        'data_ida' => substr((string)$linha['data_ida'], 0, 10),
        'data_volta' => substr((string)$linha['data_volta'], 0, 10),
        'orcamento' => number_format((float)$linha['orcamento'], 2, '.', ''),
        'observacoes' => $linha['observacoes'],
        'criado_em' => $linha['criado_em'],
    ];
}

function validar_viagem(array $dados): array
{
    $erros = [];
    $destino = trim((string)($dados['destino'] ?? ''));
    $ida = trim((string)($dados['data_ida'] ?? ''));
    $volta = trim((string)($dados['data_volta'] ?? ''));
    $orcamento = numero($dados['orcamento'] ?? null);

    if ($destino === '') {
        $erros['destino'] = 'Destino é obrigatório.';
    } elseif (tamanho($destino) > 120) {
        $erros['destino'] = 'Destino deve ter no máximo 120 caracteres.';
    }

    if (!data_valida($ida)) {
        $erros['data_ida'] = 'Informe a data de ida.';
    }
    if (!data_valida($volta)) {
        $erros['data_volta'] = 'Informe a data de volta.';
    }
    if (!isset($erros['data_ida']) && !isset($erros['data_volta']) && $volta < $ida) {
        $erros['data_volta'] = 'A data de volta não pode ser anterior à data de ida.';
    }
    if (!isset($erros['data_ida']) && !isset($erros['data_volta'])) {
        $inicio = new DateTime($ida);
        $fim = new DateTime($volta);
        $dias = (int)$inicio->diff($fim)->days + 1;
        if ($dias > 366) {
            $erros['data_volta'] = 'A viagem pode ter no máximo 366 dias.';
        }
    }

    if ($orcamento === null) {
        $erros['orcamento'] = 'Informe um orçamento válido.';
    } elseif ($orcamento < 0) {
        $erros['orcamento'] = 'O orçamento não pode ser negativo.';
    } elseif ($orcamento > 99999999.99) {
        $erros['orcamento'] = 'Orçamento maior do que o permitido.';
    }

    return $erros;
}

function id_da_url(bool $obrigatorio): ?int
{
    if (!isset($_GET['id']) || $_GET['id'] === '') {
        if ($obrigatorio) {
            responder_erro('Informe o identificador.', 400);
        }
        return null;
    }

    if (!preg_match('/^[1-9][0-9]*$/', (string)$_GET['id'])) {
        responder_erro('Identificador inválido.', 400);
    }

    return (int)$_GET['id'];
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
