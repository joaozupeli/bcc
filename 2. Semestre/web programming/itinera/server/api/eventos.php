<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers.php';
require_once __DIR__ . '/../config/database.php';

iniciar_api();

try {
    $pdo = obter_conexao();
    $metodo = $_SERVER['REQUEST_METHOD'] ?? 'GET';

    if ($metodo === 'GET') {
        obter_eventos($pdo);
    } elseif ($metodo === 'POST') {
        criar_evento($pdo);
    } elseif ($metodo === 'PUT') {
        atualizar_evento($pdo);
    } elseif ($metodo === 'DELETE') {
        excluir_evento($pdo);
    } else {
        header('Allow: GET, POST, PUT, DELETE');
        responder_erro('Método não permitido.', 405);
    }
} catch (Throwable $e) {
    tratar_excecao($e);
}

function obter_eventos(PDO $pdo): void
{
    $viagemId = inteiro_da_url('viagem_id', true);
    if (buscar_viagem($pdo, $viagemId) === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $lista = [];
    foreach (listar_eventos_da_viagem($pdo, $viagemId) as $linha) {
        $lista[] = mapear_evento($linha);
    }
    responder_ok($lista);
}

function criar_evento(PDO $pdo): void
{
    $dados = ler_corpo_json();
    $viagemId = inteiro_positivo($dados['viagem_id'] ?? null);
    if ($viagemId === null) {
        responder_erro('Informe a viagem do evento.', 400, [
            'viagem_id' => 'Informe a viagem do evento.',
        ]);
    }

    $viagem = buscar_viagem($pdo, $viagemId);
    if ($viagem === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $resultado = validar_evento($dados, $viagem);
    if ($resultado['erros'] !== []) {
        responder_erro('Verifique os campos destacados.', 400, $resultado['erros']);
    }

    $limpos = $resultado['limpos'];
    $stmt = $pdo->prepare(
        'INSERT INTO eventos (viagem_id, data, horario, titulo, local, categoria, valor, status, observacoes)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    );
    $stmt->execute([
        $viagemId,
        $limpos['data'],
        $limpos['horario'],
        $limpos['titulo'],
        $limpos['local'],
        $limpos['categoria'],
        $limpos['valor'],
        $limpos['status'],
        $limpos['observacoes'],
    ]);

    $id = (int)$pdo->lastInsertId();
    $criado = buscar_evento($pdo, $id);
    if ($criado === null) {
        throw new RuntimeException('O evento foi gravado, mas não consegui lê-lo de volta.');
    }

    responder_ok(mapear_evento($criado), 201);
}

function atualizar_evento(PDO $pdo): void
{
    $id = inteiro_da_url('id', true);
    $atual = buscar_evento($pdo, $id);
    if ($atual === null) {
        responder_erro('Evento não encontrado.', 404);
    }

    // O evento não troca de viagem por esta tela. A data nova precisa caber
    // no período da viagem à qual ele já pertence.
    $viagem = buscar_viagem($pdo, (int)$atual['viagem_id']);
    if ($viagem === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $resultado = validar_evento(ler_corpo_json(), $viagem);
    if ($resultado['erros'] !== []) {
        responder_erro('Verifique os campos destacados.', 400, $resultado['erros']);
    }

    $limpos = $resultado['limpos'];
    $stmt = $pdo->prepare(
        'UPDATE eventos
         SET data = ?, horario = ?, titulo = ?, local = ?, categoria = ?, valor = ?, status = ?, observacoes = ?
         WHERE id = ?'
    );
    $stmt->execute([
        $limpos['data'],
        $limpos['horario'],
        $limpos['titulo'],
        $limpos['local'],
        $limpos['categoria'],
        $limpos['valor'],
        $limpos['status'],
        $limpos['observacoes'],
        $id,
    ]);

    $atualizado = buscar_evento($pdo, $id);
    if ($atualizado === null) {
        responder_erro('Evento não encontrado.', 404);
    }

    responder_ok(mapear_evento($atualizado));
}

function excluir_evento(PDO $pdo): void
{
    $id = inteiro_da_url('id', true);
    if (buscar_evento($pdo, $id) === null) {
        responder_erro('Evento não encontrado.', 404);
    }

    $stmt = $pdo->prepare('DELETE FROM eventos WHERE id = ?');
    $stmt->execute([$id]);
    responder_ok(['id' => $id]);
}
