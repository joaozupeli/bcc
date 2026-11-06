<?php
declare(strict_types=1);

// Única função deste arquivo: devolver uma conexão PDO com o TiDB Cloud.
// Os arquivos da API chamam obter_conexao() e não conhecem senha nem host.

function obter_conexao(): PDO
{
    // No mesmo pedido HTTP reutilizamos a conexão.
    // O PHP do servidor embutido não guarda isso entre um clique e outro.
    static $pdo = null;
    if ($pdo instanceof PDO) {
        return $pdo;
    }

    if (!extension_loaded('pdo_mysql')) {
        throw new RuntimeException(
            'A extensão pdo_mysql não está habilitada. Abra o php.ini (php --ini), ative extension=pdo_mysql e reinicie o php -S.'
        );
    }

    $config = ler_config_local();

    $host = trim((string)($config['host'] ?? ''));
    $banco = trim((string)($config['banco'] ?? ''));
    $usuario = trim((string)($config['usuario'] ?? ''));
    $senha = (string)($config['senha'] ?? '');
    $porta = isset($config['porta']) ? (int)$config['porta'] : 4000;

    if ($host === '' || $usuario === '' || $senha === '' || $banco === '') {
        throw new RuntimeException(
            'Preencha server/config/config.local.php com os dados da janela Connect do TiDB Cloud (host, usuário, senha e banco).'
        );
    }

    // O DSN junta host e banco na mesma string. Ponto e vírgula mudaria o sentido dessa string.
    if (preg_match('/[;\r\n]/', $host) || preg_match('/[;\r\n]/', $banco)) {
        throw new RuntimeException('Host ou nome do banco contém um caractere inválido.');
    }

    if ($porta <= 0) {
        throw new RuntimeException('A porta do banco está inválida. No TiDB Cloud use 4000.');
    }

    $certificado = caminho_certificado($config);

    if (!is_readable($certificado)) {
        throw new RuntimeException(
            'Não encontrei o certificado CA dentro de server/. Coloque o arquivo isrgrootx1.pem nessa pasta. Caminho procurado: ' . $certificado
        );
    }

    // A senha vai no argumento separado, não dentro do DSN, para não parar no meio de um log de conexão.
    $dsn = 'mysql:host=' . $host . ';port=' . $porta . ';dbname=' . $banco . ';charset=utf8mb4';

    $opcoes = [
        // Erro de SQL vira exceção. O catch da API esconde o detalhe e responde JSON.
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        // fetch() devolve array associativo: $linha['destino'], não $linha[0].
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        // false usa o prepared statement de verdade do MySQL/TiDB, não uma concatenação escondida.
        PDO::ATTR_EMULATE_PREPARES => false,
    ];

    $verificar = true;
    if (array_key_exists('ssl_verificar', $config)) {
        $verificar = (bool)$config['ssl_verificar'];
    }

    // O certificado CA é obrigatório no TiDB Cloud.
    // No PHP 8.4 a constante antiga PDO::MYSQL_ATTR_SSL_CA gera aviso.
    // Se esse aviso fosse para a tela, o JSON quebraria. Por isso preferimos Pdo\Mysql.
    if (class_exists('Pdo\\Mysql') && defined('Pdo\\Mysql::ATTR_SSL_CA')) {
        $opcoes[constant('Pdo\\Mysql::ATTR_SSL_CA')] = $certificado;
        if (defined('Pdo\\Mysql::ATTR_SSL_VERIFY_SERVER_CERT')) {
            $opcoes[constant('Pdo\\Mysql::ATTR_SSL_VERIFY_SERVER_CERT')] = $verificar;
        }
    } else {
        $opcoes[PDO::MYSQL_ATTR_SSL_CA] = $certificado;
        if (defined('PDO::MYSQL_ATTR_SSL_VERIFY_SERVER_CERT')) {
            $opcoes[PDO::MYSQL_ATTR_SSL_VERIFY_SERVER_CERT] = $verificar;
        }
    }

    $pdo = new PDO($dsn, $usuario, $senha, $opcoes);
    return $pdo;
}

function caminho_certificado(array $config): string
{
    $pastaServer = dirname(__DIR__);
    $padrao = $pastaServer . '/isrgrootx1.pem';

    $informado = trim((string)($config['ssl_ca'] ?? ''));
    if ($informado === '') {
        return $padrao;
    }

    $normalizado = str_replace('\\', '/', $informado);
    $absoluto = str_starts_with($normalizado, '/') || preg_match('/^[A-Za-z]:\//', $normalizado) === 1;

    if ($absoluto && is_file($informado)) {
        return $informado;
    }

    $relativo = ltrim($normalizado, '/');
    if (str_starts_with($relativo, 'server/')) {
        $relativo = substr($relativo, strlen('server/'));
    }

    $dentroDoServer = $pastaServer . '/' . $relativo;
    if (is_file($dentroDoServer)) {
        return $dentroDoServer;
    }

    $peloNome = $pastaServer . '/' . basename($relativo);
    if (is_file($peloNome)) {
        return $peloNome;
    }

    if (is_file($padrao)) {
        return $padrao;
    }

    return $absoluto ? $informado : $dentroDoServer;
}

function ler_config_local(): array
{
    $arquivo = __DIR__ . '/config.local.php';
    if (!is_file($arquivo)) {
        throw new RuntimeException(
            'Arquivo server/config/config.local.php não encontrado. Copie config.example.php para config.local.php e preencha.'
        );
    }

    $config = require $arquivo;
    if (!is_array($config)) {
        throw new RuntimeException('server/config/config.local.php precisa dar return em um array.');
    }

    return $config;
}
