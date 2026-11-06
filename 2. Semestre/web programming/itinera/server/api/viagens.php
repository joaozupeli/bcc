<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers.php';
require_once __DIR__ . '/../config/database.php';

iniciar_api();

// Cada endereço desta pasta é um recurso.
// O método HTTP diz a ação: GET lista ou lê, POST cria, PUT atualiza, DELETE apaga.
// A página e esta API saem do mesmo php -S, então não há CORS.

try {
    $pdo = obter_conexao();
    $metodo = $_SERVER['REQUEST_METHOD'] ?? 'GET';

    if ($metodo === 'GET') {
        obter_viagens($pdo);
    } elseif ($metodo === 'POST') {
        criar_viagem($pdo);
    } elseif ($metodo === 'PUT') {
        atualizar_viagem($pdo);
    } elseif ($metodo === 'DELETE') {
        excluir_viagem($pdo);
    } else {
        header('Allow: GET, POST, PUT, DELETE');
        responder_erro('Método não permitido.', 405);
    }
} catch (Throwable $e) {
    tratar_excecao($e);
}

function obter_viagens(PDO $pdo): void
{
    $id = inteiro_da_url('id', false);
    if ($id !== null) {
        $viagem = buscar_viagem($pdo, $id);
        if ($viagem === null) {
            responder_erro('Viagem não encontrada.', 404);
        }
        responder_ok(mapear_viagem($viagem));
    }

    $lista = [];
    foreach (listar_viagens($pdo) as $linha) {
        $lista[] = mapear_viagem($linha);
    }
    responder_ok($lista);
}

function criar_viagem(PDO $pdo): void
{
    $resultado = validar_viagem(ler_corpo_json());
    if ($resultado['erros'] !== []) {
        responder_erro('Verifique os campos destacados.', 400, $resultado['erros']);
    }

    $limpos = $resultado['limpos'];
    $stmt = $pdo->prepare(
        'INSERT INTO viagens (destino, data_ida, data_volta, orcamento, observacoes)
         VALUES (?, ?, ?, ?, ?)'
    );
    $stmt->execute([
        $limpos['destino'],
        $limpos['data_ida'],
        $limpos['data_volta'],
        $limpos['orcamento'],
        $limpos['observacoes'],
    ]);

    $id = (int)$pdo->lastInsertId();
    $criada = buscar_viagem($pdo, $id);
    if ($criada === null) {
        throw new RuntimeException('A viagem foi gravada, mas não consegui lê-la de volta.');
    }

    responder_ok(mapear_viagem($criada), 201);
}

function atualizar_viagem(PDO $pdo): void
{
    $id = inteiro_da_url('id', true);
    $atual = buscar_viagem($pdo, $id);
    if ($atual === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    $resultado = validar_viagem(ler_corpo_json());
    if ($resultado['erros'] !== []) {
        responder_erro('Verifique os campos destacados.', 400, $resultado['erros']);
    }

    $limpos = $resultado['limpos'];

    // Sem esta checagem, encurtar a viagem deixaria evento com data órfã.
    if (existe_evento_fora_do_periodo($pdo, $id, $limpos['data_ida'], $limpos['data_volta'])) {
        $mensagem = 'Há eventos fora do novo período. Apague ou mova esses eventos antes de encurtar a viagem.';
        responder_erro($mensagem, 400, [
            'data_ida' => $mensagem,
            'data_volta' => $mensagem,
        ]);
    }

    $stmt = $pdo->prepare(
        'UPDATE viagens
         SET destino = ?, data_ida = ?, data_volta = ?, orcamento = ?, observacoes = ?
         WHERE id = ?'
    );
    $stmt->execute([
        $limpos['destino'],
        $limpos['data_ida'],
        $limpos['data_volta'],
        $limpos['orcamento'],
        $limpos['observacoes'],
        $id,
    ]);

    // Não usamos rowCount: se os dados não mudaram, o MySQL devolve 0
    // e a tela acharia que a viagem não existe. Por isso lemos de novo.
    $atualizada = buscar_viagem($pdo, $id);
    if ($atualizada === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    responder_ok(mapear_viagem($atualizada));
}

function excluir_viagem(PDO $pdo): void
{
    $id = inteiro_da_url('id', true);
    if (buscar_viagem($pdo, $id) === null) {
        responder_erro('Viagem não encontrada.', 404);
    }

    // Não há ON DELETE CASCADE. Se apagarmos a viagem e o delete dos eventos
    // falhar, sobram linhas soltas. A transação desfaz os dois passos juntos.
    $pdo->beginTransaction();
    try {
        $apagarEventos = $pdo->prepare('DELETE FROM eventos WHERE viagem_id = ?');
        $apagarEventos->execute([$id]);

        $apagarViagem = $pdo->prepare('DELETE FROM viagens WHERE id = ?');
        $apagarViagem->execute([$id]);

        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) {
            $pdo->rollBack();
        }
        throw $e;
    }

    responder_ok(['id' => $id]);
}
