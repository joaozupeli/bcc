<?php
// Copie este arquivo para config.local.php e preencha com a janela "Connect" do TiDB Cloud.
// O config.local.php fica de fora do Git para a senha não ser publicada.

return [
    // Host parecido com gateway01.sa-east-1.prod.aws.tidbcloud.com
    'host' => 'gateway01.sa-east-1.prod.aws.tidbcloud.com',

    // A porta do TiDB Cloud é 4000, não 3306.
    'porta' => 4000,

    // No cluster novo o banco padrão costuma se chamar test.
    'banco' => 'test',

    // Usuário no formato <prefixo>.root
    'usuario' => '3AbCDefGhIJk.root',

    'senha' => 'troque_esta_senha',

    // Caminho do certificado CA (TLS). O TiDB recusa conexão sem isso.
    // A janela Connect mostra o caminho ou um botão para baixar o arquivo.
    //
    // Windows: o PHP não usa o cofre de certificados do sistema.
    //          Baixe o CA pela janela Connect e use barras normais, por exemplo
    //          C:/Users/seu-usuario/Downloads/ca.pem
    // macOS:   /etc/ssl/cert.pem
    // Linux:   /etc/ssl/certs/ca-certificates.crt
    //          (no CentOS/Fedora: /etc/pki/tls/certs/ca-bundle.crt)
    'ssl_ca' => 'C:/Users/seu-usuario/Downloads/ca.pem',

    // true confere se o certificado pertence ao servidor.
    // Se o caminho do CA estiver certo e ainda aparecer "certificate verify failed",
    // mude para false (sem aspas) só para conseguir apresentar o trabalho.
    'ssl_verificar' => true,
];
