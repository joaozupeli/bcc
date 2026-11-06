// O app.js chama Api.*. As URLs apontam para o PHP em server/api.

async function requisitar(url, opcoes) {
  const config = opcoes || {};
  const cabecalhos = { Accept: 'application/json' };

  if (config.body) {
    cabecalhos['Content-Type'] = 'application/json; charset=utf-8';
  }

  const pedido = {
    method: config.method || 'GET',
    headers: cabecalhos,
    cache: 'no-store',
  };

  if (config.body) {
    pedido.body = JSON.stringify(config.body);
  }

  if (typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function') {
    pedido.signal = AbortSignal.timeout(20000);
  }

  let resposta;
  try {
    resposta = await fetch(url, pedido);
  } catch (erro) {
    if (erro && (erro.name === 'TimeoutError' || erro.name === 'AbortError')) {
      throw new Error('O servidor demorou para responder.');
    }
    throw new Error('Não foi possível falar com o servidor. Confira se o PHP está rodando.');
  }

  const texto = await resposta.text();
  let corpo = null;
  if (texto) {
    try {
      corpo = JSON.parse(texto);
    } catch (erro) {
      throw new Error('O servidor não respondeu em JSON. Veja o terminal do PHP.');
    }
  }

  if (!corpo || corpo.ok !== true) {
    const falha = new Error(corpo && corpo.erro ? corpo.erro : 'Não foi possível concluir a ação.');
    falha.campos = corpo && corpo.campos ? corpo.campos : null;
    throw falha;
  }

  return corpo.dados;
}

const Api = {
  listarViagens() {
    return requisitar('/server/api/viagens.php');
  },

  obterViagem(id) {
    return requisitar('/server/api/viagens.php?id=' + encodeURIComponent(id));
  },

  criarViagem(dados) {
    return requisitar('/server/api/viagens.php', { method: 'POST', body: dados });
  },

  atualizarViagem(id, dados) {
    return requisitar('/server/api/viagens.php?id=' + encodeURIComponent(id), { method: 'PUT', body: dados });
  },

  excluirViagem(id) {
    return requisitar('/server/api/viagens.php?id=' + encodeURIComponent(id), { method: 'DELETE' });
  },

  listarEventos(viagemId) {
    return requisitar('/server/api/eventos.php?viagem_id=' + encodeURIComponent(viagemId));
  },

  criarEvento(dados) {
    return requisitar('/server/api/eventos.php', { method: 'POST', body: dados });
  },

  atualizarEvento(id, dados) {
    return requisitar('/server/api/eventos.php?id=' + encodeURIComponent(id), { method: 'PUT', body: dados });
  },

  excluirEvento(id) {
    return requisitar('/server/api/eventos.php?id=' + encodeURIComponent(id), { method: 'DELETE' });
  },
};
