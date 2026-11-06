// Regras da tela. A validação que vale é a do PHP em server/api.
const CATEGORIAS = [
  { valor: 'voo', nome: 'Voo' },
  { valor: 'hospedagem', nome: 'Hospedagem' },
  { valor: 'comida', nome: 'Comida' },
  { valor: 'passeio', nome: 'Passeio' },
  { valor: 'transporte', nome: 'Transporte' },
  { valor: 'outro', nome: 'Outro' },
];

const STATUS = [
  { valor: 'pendente', nome: 'Pendente' },
  { valor: 'confirmado', nome: 'Confirmado' },
];

const LIMITE_DIAS = 366;

const estado = {
  viagens: [],
  busca: '',
  viagemAtual: null,
  eventos: [],
  diaAtivo: null,
  filtroCategoria: '',
  filtroStatus: '',
};

function iniciar() {
  iniciarUi();
  aplicarTemaNaTela(temaSalvo());

  document.getElementById('btn-tema').addEventListener('click', () => {
    const atual = document.documentElement.getAttribute('data-tema');
    aplicarTemaNaTela(atual === 'escuro' ? 'claro' : 'escuro');
  });

  document.getElementById('busca').addEventListener('input', (evento) => {
    // A busca filtra a lista que já está na memória. Não chama o PHP a cada tecla.
    estado.busca = evento.target.value;
    renderizarLista();
  });

  document.getElementById('btn-nova-viagem').addEventListener('click', () => {
    abrirFormularioViagem(null);
  });

  // A tela é redesenhada com innerHTML. O clique fica no pai
  // para não precisar recolocar o ouvinte em cada botão novo.
  document.getElementById('app').addEventListener('click', aoClicar);
  document.getElementById('app').addEventListener('change', aoMudarFiltro);

  window.addEventListener('beforeprint', () => {
    const detalhe = document.getElementById('tela-viagem');
    if (detalhe && !detalhe.hidden) {
      document.body.classList.add('imprimindo');
    }
  });
  window.addEventListener('afterprint', () => {
    document.body.classList.remove('imprimindo');
  });

  carregarViagens();
}

function temaSalvo() {
  const salvo = localStorage.getItem(CHAVE_TEMA);
  if (salvo === 'claro' || salvo === 'escuro') {
    return salvo;
  }
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return 'escuro';
  }
  return 'claro';
}

function aplicarTemaNaTela(tema) {
  document.documentElement.setAttribute('data-tema', tema);
  localStorage.setItem(CHAVE_TEMA, tema);
  const botao = document.getElementById('btn-tema');
  const escuro = tema === 'escuro';
  botao.textContent = escuro ? 'Tema claro' : 'Tema escuro';
  botao.setAttribute('aria-pressed', escuro ? 'true' : 'false');
}

function aoClicar(evento) {
  const alvo = evento.target.closest('[data-acao]');
  if (!alvo) {
    return;
  }

  const acao = alvo.dataset.acao;
  const id = alvo.dataset.id;

  if (acao === 'abrir-viagem') {
    abrirViagem(id, { manter: false }).catch((erro) => console.log(erro.message));
    return;
  }
  if (acao === 'editar-viagem') {
    const viagem = obterViagemLocal(id);
    if (viagem) {
      abrirFormularioViagem(viagem);
    }
    return;
  }
  if (acao === 'excluir-viagem') {
    const viagem = obterViagemLocal(id);
    if (viagem) {
      pedirExclusaoViagem(viagem);
    }
    return;
  }
  if (acao === 'voltar') {
    voltarParaLista();
    return;
  }
  if (acao === 'imprimir') {
    window.print();
    return;
  }
  if (acao === 'selecionar-dia') {
    estado.diaAtivo = alvo.dataset.dia;
    atualizarAbas();
    return;
  }
  if (acao === 'novo-evento') {
    abrirFormularioEvento(null);
    return;
  }
  if (acao === 'editar-evento') {
    const item = eventoPorId(id);
    if (item) {
      abrirFormularioEvento(item);
    }
    return;
  }
  if (acao === 'excluir-evento') {
    const item = eventoPorId(id);
    if (item) {
      pedirExclusaoEvento(item);
    }
    return;
  }
  if (acao === 'alternar-status') {
    const item = eventoPorId(id);
    if (item) {
      alternarStatus(item, alvo);
    }
  }
}

function aoMudarFiltro(evento) {
  if (evento.target.id === 'filtro-categoria') {
    estado.filtroCategoria = evento.target.value;
    renderizarPaineis();
  }
  if (evento.target.id === 'filtro-status') {
    estado.filtroStatus = evento.target.value;
    renderizarPaineis();
  }
}

async function carregarViagens() {
  const alvo = document.getElementById('lista-viagens');
  if (estado.viagens.length === 0) {
    alvo.innerHTML = htmlVazio('Carregando viagens...');
  }

  try {
    estado.viagens = await Api.listarViagens();
    renderizarLista();
  } catch (erro) {
    estado.viagens = [];
    alvo.innerHTML = htmlVazio('Não foi possível carregar as viagens.');
    console.log(erro.message);
  }
}

function renderizarLista() {
  const alvo = document.getElementById('lista-viagens');
  const busca = normalizarBusca(estado.busca);
  const filtradas = estado.viagens
    .filter((viagem) => normalizarBusca(viagem.destino).includes(busca))
    .sort(compararViagens);

  if (estado.viagens.length === 0) {
    alvo.innerHTML = htmlVazio('Nenhuma viagem ainda. Crie a primeira.', true);
    return;
  }
  if (filtradas.length === 0) {
    alvo.innerHTML = htmlVazio('Nenhuma viagem encontrada para essa busca.');
    return;
  }

  alvo.innerHTML = '<div class="grade-viagens">' + filtradas.map(htmlCartaoViagem).join('') + '</div>';
}

function htmlCartaoViagem(viagem) {
  const contagem = textoContagem(viagem.data_ida, viagem.data_volta);
  const dias = listarDias(viagem.data_ida, viagem.data_volta).length;
  const obs = viagem.observacoes
    ? '<p class="cartao-obs">' + escapeHtml(viagem.observacoes) + '</p>'
    : '';

  return (
    '<article class="cartao">' +
      '<div class="cartao-topo">' +
        '<h3>' + escapeHtml(viagem.destino) + '</h3>' +
        '<span class="selo selo-' + contagem.tipo + '">' + escapeHtml(contagem.texto) + '</span>' +
      '</div>' +
      '<p class="cartao-periodo">' + escapeHtml(formatarDataBR(viagem.data_ida)) + ' — ' + escapeHtml(formatarDataBR(viagem.data_volta)) + '</p>' +
      '<p class="cartao-dias">' + escapeHtml(textoQuantidade(dias, 'dia', 'dias')) + '</p>' +
      obs +
      '<div class="cartao-acoes">' +
        '<button type="button" class="btn btn-pequeno btn-primario" data-acao="abrir-viagem" data-id="' + escapeHtml(viagem.id) + '">Abrir</button>' +
        '<button type="button" class="btn btn-pequeno btn-fantasma" data-acao="editar-viagem" data-id="' + escapeHtml(viagem.id) + '">Editar</button>' +
        '<button type="button" class="btn btn-pequeno btn-perigo" data-acao="excluir-viagem" data-id="' + escapeHtml(viagem.id) + '">Excluir</button>' +
      '</div>' +
    '</article>'
  );
}

function compararViagens(a, b) {
  const peso = { andamento: 0, futura: 1, concluida: 2 };
  const pa = peso[textoContagem(a.data_ida, a.data_volta).tipo];
  const pb = peso[textoContagem(b.data_ida, b.data_volta).tipo];
  if (pa !== pb) {
    return pa - pb;
  }
  if (pa === 2) {
    return String(b.data_ida).localeCompare(String(a.data_ida));
  }
  return String(a.data_ida).localeCompare(String(b.data_ida));
}

function obterViagemLocal(id) {
  if (estado.viagemAtual && String(estado.viagemAtual.id) === String(id)) {
    return estado.viagemAtual;
  }
  return estado.viagens.find((viagem) => String(viagem.id) === String(id)) || null;
}

function abrirFormularioViagem(viagem) {
  const form = criarFormularioViagem(viagem);
  const cancelar = botaoSimples('Cancelar', 'btn btn-fantasma', fecharModal);
  const salvar = botaoSimples(viagem ? 'Salvar alterações' : 'Criar viagem', 'btn btn-primario', () => {
    enviarFormulario(form);
  });

  abrirModal({
    titulo: viagem ? 'Editar viagem' : 'Nova viagem',
    corpo: form,
    rodape: [cancelar, salvar],
    fecharNoFundo: false,
  });
}

function criarFormularioViagem(viagem) {
  const form = document.createElement('form');
  form.className = 'formulario';
  form.noValidate = true;
  form.autocomplete = 'off';

  const destino = inputTexto('text', viagem ? viagem.destino : '', 120);
  destino.required = true;
  destino.setAttribute('aria-required', 'true');

  const dataIda = inputTexto('date', viagem ? viagem.data_ida : '');
  dataIda.required = true;
  const dataVolta = inputTexto('date', viagem ? viagem.data_volta : '');
  dataVolta.required = true;

  const orcamento = inputTexto('number', viagem ? String(viagem.orcamento) : '');
  orcamento.min = '0';
  orcamento.step = '0.01';
  orcamento.placeholder = '0.00';
  orcamento.required = true;

  const observacoes = document.createElement('textarea');
  observacoes.rows = 3;
  observacoes.value = viagem && viagem.observacoes ? viagem.observacoes : '';

  const grade = document.createElement('div');
  grade.className = 'grade-2';
  grade.append(
    criarGrupo('data_ida', 'Data de ida', dataIda),
    criarGrupo('data_volta', 'Data de volta', dataVolta)
  );

  const erroGeral = document.createElement('p');
  erroGeral.className = 'erro-geral';

  form.append(
    erroGeral,
    criarGrupo('destino', 'Destino', destino),
    grade,
    criarGrupo('orcamento', 'Orçamento total (R$)', orcamento),
    criarGrupo('observacoes', 'Observações', observacoes)
  );

  dataIda.addEventListener('change', () => {
    if (dataIda.value) {
      dataVolta.min = dataIda.value;
    }
  });
  if (dataIda.value) {
    dataVolta.min = dataIda.value;
  }

  form.addEventListener('submit', (evento) => {
    evento.preventDefault();
    salvarViagem(form, viagem ? viagem.id : null);
  });

  return form;
}

async function salvarViagem(form, id) {
  const dados = {
    destino: valorCampo(form, 'destino'),
    data_ida: valorCampo(form, 'data_ida'),
    data_volta: valorCampo(form, 'data_volta'),
    orcamento: valorCampo(form, 'orcamento'),
    observacoes: valorCampo(form, 'observacoes'),
  };

  const erros = validarViagem(dados);
  if (Object.keys(erros).length > 0) {
    mostrarErros(form, erros);
    console.log('Verifique os campos destacados.');
    return;
  }

  limparErros(form);
  const botoes = travarBotoesModal(true);

  try {
    if (id) {
      await Api.atualizarViagem(id, dados);
      mostrarToast('Viagem atualizada.', 'sucesso');
    } else {
      await Api.criarViagem(dados);
      mostrarToast('Viagem criada.', 'sucesso');
    }
    fecharModal();
    if (id && estado.viagemAtual && String(estado.viagemAtual.id) === String(id)) {
      await abrirViagem(id, { manter: true });
    }
    await carregarViagens();
  } catch (erro) {
    if (erro.campos) {
      mostrarErros(form, erro.campos);
    } else {
      const geral = form.querySelector('.erro-geral');
      if (geral) {
        geral.textContent = erro.message;
      }
    }
    console.log(erro.message);
  } finally {
    travarBotoesModal(false, botoes);
  }
}

async function pedirExclusaoViagem(viagem) {
  const certo = await confirmar({
    titulo: 'Excluir viagem',
    mensagem: 'Excluir a viagem para ' + viagem.destino + '? Todos os eventos dessa viagem também serão apagados. Essa ação não pode ser desfeita.',
    textoConfirmar: 'Excluir viagem',
  });
  if (!certo) {
    return;
  }

  try {
    await Api.excluirViagem(viagem.id);
    mostrarToast('Viagem excluída.', 'sucesso');
    if (estado.viagemAtual && String(estado.viagemAtual.id) === String(viagem.id)) {
      estado.viagemAtual = null;
      estado.eventos = [];
      document.title = 'Itinera';
      mostrarTela('lista');
    }
    await carregarViagens();
  } catch (erro) {
    console.log(erro.message);
  }
}

async function abrirViagem(id, opcoes) {
  const manter = opcoes && opcoes.manter === true;
  const diaAntes = estado.diaAtivo;
  const filtroCategoria = estado.filtroCategoria;
  const filtroStatus = estado.filtroStatus;

  const [viagem, eventos] = await Promise.all([
    Api.obterViagem(id),
    Api.listarEventos(id),
  ]);

  estado.viagemAtual = viagem;
  estado.eventos = eventos;
  estado.filtroCategoria = manter ? filtroCategoria : '';
  estado.filtroStatus = manter ? filtroStatus : '';

  const dias = listarDias(viagem.data_ida, viagem.data_volta);
  if (manter && dias.includes(diaAntes)) {
    estado.diaAtivo = diaAntes;
  } else {
    estado.diaAtivo = diaInicial(dias);
  }

  document.title = viagem.destino + ' · Itinera';
  mostrarTela('viagem');
  renderizarDetalhe();
}

function voltarParaLista() {
  estado.viagemAtual = null;
  estado.eventos = [];
  estado.diaAtivo = null;
  document.title = 'Itinera';
  mostrarTela('lista');
  carregarViagens();
}

function mostrarTela(nome) {
  document.getElementById('tela-lista').hidden = nome !== 'lista';
  document.getElementById('tela-viagem').hidden = nome !== 'viagem';
}

function renderizarDetalhe() {
  const viagem = estado.viagemAtual;
  if (!viagem) {
    return;
  }
  document.getElementById('viagem-conteudo').innerHTML = htmlDetalhe(viagem, estado.eventos);
  atualizarAbas();
}

function htmlDetalhe(viagem, eventos) {
  const contagem = textoContagem(viagem.data_ida, viagem.data_volta);
  const dias = listarDias(viagem.data_ida, viagem.data_volta);
  const obs = viagem.observacoes
    ? '<p class="obs-viagem">' + escapeHtmlMultilinha(viagem.observacoes) + '</p>'
    : '';

  return (
    '<div class="detalhe-topo no-print">' +
      '<button type="button" class="btn btn-fantasma" data-acao="voltar">← Voltar</button>' +
      '<div class="detalhe-acoes">' +
        '<button type="button" class="btn btn-fantasma" data-acao="imprimir">Imprimir roteiro</button>' +
        '<button type="button" class="btn btn-fantasma" data-acao="editar-viagem" data-id="' + escapeHtml(viagem.id) + '">Editar</button>' +
        '<button type="button" class="btn btn-perigo" data-acao="excluir-viagem" data-id="' + escapeHtml(viagem.id) + '">Excluir</button>' +
      '</div>' +
    '</div>' +
    '<header class="detalhe-cabecalho">' +
      '<h2>' + escapeHtml(viagem.destino) + '</h2>' +
      '<p class="detalhe-periodo">' +
        escapeHtml(formatarDataBR(viagem.data_ida)) + ' — ' + escapeHtml(formatarDataBR(viagem.data_volta)) +
        ' · ' + escapeHtml(textoQuantidade(dias.length, 'dia', 'dias')) +
        ' · ' + escapeHtml(contagem.texto) +
      '</p>' +
      obs +
    '</header>' +
    htmlResumo(viagem, eventos) +
    '<div class="filtros no-print">' +
      '<div class="campo campo-inline">' +
        '<label for="filtro-categoria">Categoria</label>' +
        htmlOpcoesFiltro('filtro-categoria', CATEGORIAS, estado.filtroCategoria, 'Todas') +
      '</div>' +
      '<div class="campo campo-inline">' +
        '<label for="filtro-status">Status</label>' +
        htmlOpcoesFiltro('filtro-status', STATUS, estado.filtroStatus, 'Todos') +
      '</div>' +
      '<button type="button" class="btn btn-primario" data-acao="novo-evento">Novo evento</button>' +
    '</div>' +
    '<div class="abas no-print" role="tablist">' + dias.map((dia) => htmlAba(dia, eventos)).join('') + '</div>' +
    '<div id="paineis-dias">' + htmlPaineis(dias, eventos) + '</div>'
  );
}

function htmlResumo(viagem, eventos) {
  const dias = listarDias(viagem.data_ida, viagem.data_volta).length;
  const total = eventos.length;
  const confirmados = eventos.filter((evento) => evento.status === 'confirmado').length;
  const gasto = somarValores(eventos);
  const orcamento = Number(viagem.orcamento);
  const estourou = Number.isFinite(orcamento) && gasto > orcamento;
  const percentual = orcamento > 0 ? Math.round((gasto / orcamento) * 100) : (gasto > 0 ? 100 : 0);
  const largura = Math.max(0, Math.min(percentual, 100));
  const aviso = estourou
    ? '<p class="aviso-orcamento">O gasto passou do orçamento em ' + escapeHtml(formatarMoeda(gasto - orcamento)) + '.</p>'
    : '';

  return (
    '<section class="resumo">' +
      '<article class="cartao-resumo"><p class="resumo-rotulo">Dias</p><p class="resumo-valor">' + dias + '</p></article>' +
      '<article class="cartao-resumo"><p class="resumo-rotulo">Eventos</p><p class="resumo-valor">' + total + '</p></article>' +
      '<article class="cartao-resumo' + (estourou ? ' estourou' : '') + '">' +
        '<p class="resumo-rotulo">Gasto previsto</p>' +
        '<p class="resumo-valor">' + escapeHtml(formatarMoeda(gasto)) + '</p>' +
        '<p class="resumo-sub">de ' + escapeHtml(formatarMoeda(orcamento)) + '</p>' +
      '</article>' +
      '<article class="cartao-resumo"><p class="resumo-rotulo">Confirmados</p><p class="resumo-valor">' + confirmados + ' de ' + total + '</p></article>' +
    '</section>' +
    '<div class="bloco-orcamento">' +
      '<div class="progresso' + (estourou ? ' estourou' : '') + '" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + largura + '" aria-label="Uso do orçamento">' +
        '<div class="progresso-barra" style="width: ' + largura + '%"></div>' +
      '</div>' +
      '<p class="progresso-texto">' + escapeHtml(formatarMoeda(gasto)) + ' de ' + escapeHtml(formatarMoeda(orcamento)) + ' (' + percentual + '%)</p>' +
      aviso +
    '</div>'
  );
}

function htmlAba(dia, eventos) {
  const data = parseDataISO(dia);
  const curto = data ? DIAS_CURTOS[data.getDay()] : '';
  const qtd = eventos.filter((evento) => evento.data === dia).length;
  const ativa = dia === estado.diaAtivo;
  return (
    '<button type="button" class="aba' + (ativa ? ' ativa' : '') + '" role="tab" aria-selected="' + (ativa ? 'true' : 'false') + '" data-acao="selecionar-dia" data-dia="' + escapeHtml(dia) + '">' +
      '<span>' + escapeHtml(formatarDataCurta(dia)) + '</span>' +
      '<small>' + escapeHtml(curto) + (qtd ? ' · ' + qtd : '') + '</small>' +
    '</button>'
  );
}

function htmlOpcoesFiltro(id, lista, selecionado, primeira) {
  const opcoes = ['<option value="">' + escapeHtml(primeira) + '</option>']
    .concat(lista.map((item) => {
      const marca = item.valor === selecionado ? ' selected' : '';
      return '<option value="' + escapeHtml(item.valor) + '"' + marca + '>' + escapeHtml(item.nome) + '</option>';
    }));
  return '<select id="' + id + '">' + opcoes.join('') + '</select>';
}

function renderizarPaineis() {
  const raiz = document.getElementById('paineis-dias');
  const viagem = estado.viagemAtual;
  if (!raiz || !viagem) {
    return;
  }
  const dias = listarDias(viagem.data_ida, viagem.data_volta);
  raiz.innerHTML = htmlPaineis(dias, estado.eventos);
  atualizarAbas();
}

function htmlPaineis(dias, eventos) {
  return dias.map((dia) => {
    const doDia = eventos.filter((evento) => evento.data === dia);
    const conflitos = mapaConflitos(doDia);
    const ativos = dia === estado.diaAtivo;
    let miolo;

    if (doDia.length === 0) {
      miolo = htmlVazio('Nenhum evento neste dia. Adicione o primeiro.');
    } else {
      miolo = doDia.map((evento) => htmlEvento(evento, conflitos)).join('');
      const visiveis = doDia.filter(passaFiltro);
      if (visiveis.length === 0) {
        miolo += htmlVazio('Nenhum evento com esse filtro neste dia.', false, true);
      }
    }

    return (
      '<section class="dia-painel' + (ativos ? ' ativo' : '') + '" data-dia="' + escapeHtml(dia) + '">' +
        '<h3 class="dia-titulo">' + escapeHtml(formatarDataLonga(dia)) + '</h3>' +
        miolo +
      '</section>'
    );
  }).join('');
}

function htmlEvento(evento, conflitos) {
  const hora = String(evento.horario || '').slice(0, 5);
  const conflito = (conflitos[hora] || 0) > 1;
  const cat = classeCategoria(evento.categoria);
  const fora = passaFiltro(evento) ? '' : ' fora-filtro';
  const local = evento.local ? evento.local : 'Local não informado';
  const obs = evento.observacoes
    ? '<p class="evento-obs">' + escapeHtmlMultilinha(evento.observacoes) + '</p>'
    : '';
  const alerta = conflito
    ? '<p class="alerta-conflito">Conflito: outro evento deste dia está no mesmo horário.</p>'
    : '';
  const textoStatus = evento.status === 'confirmado' ? 'Marcar pendente' : 'Confirmar';
  const classeStatus = evento.status === 'confirmado' ? 'selo-confirmado' : 'selo-pendente';

  return (
    '<article class="evento' + (conflito ? ' conflito' : '') + fora + '">' +
      '<div class="icone-cat ' + cat + '">' + iconeCategoria(evento.categoria) + '</div>' +
      '<div class="evento-corpo">' +
        '<div class="evento-linha">' +
          '<h4>' + escapeHtml(evento.titulo) + '</h4>' +
          '<strong class="evento-valor">' + escapeHtml(formatarMoeda(evento.valor)) + '</strong>' +
        '</div>' +
        '<p class="evento-meta">' +
          '<span>' + escapeHtml(hora) + '</span>' +
          '<span>' + escapeHtml(local) + '</span>' +
          '<span class="etiqueta ' + cat + '">' + escapeHtml(nomeCategoria(evento.categoria)) + '</span>' +
          '<span class="selo ' + classeStatus + '">' + escapeHtml(nomeStatus(evento.status)) + '</span>' +
        '</p>' +
        obs +
        alerta +
        '<div class="evento-acoes no-print">' +
          '<button type="button" class="btn btn-pequeno btn-fantasma" data-acao="alternar-status" data-id="' + escapeHtml(evento.id) + '">' + textoStatus + '</button>' +
          '<button type="button" class="btn btn-pequeno btn-fantasma" data-acao="editar-evento" data-id="' + escapeHtml(evento.id) + '">Editar</button>' +
          '<button type="button" class="btn btn-pequeno btn-perigo" data-acao="excluir-evento" data-id="' + escapeHtml(evento.id) + '">Excluir</button>' +
        '</div>' +
      '</div>' +
    '</article>'
  );
}

function atualizarAbas() {
  document.querySelectorAll('#viagem-conteudo .aba').forEach((aba) => {
    const ativa = aba.getAttribute('data-dia') === estado.diaAtivo;
    aba.classList.toggle('ativa', ativa);
    aba.setAttribute('aria-selected', ativa ? 'true' : 'false');
  });
  document.querySelectorAll('#viagem-conteudo .dia-painel').forEach((painel) => {
    painel.classList.toggle('ativo', painel.getAttribute('data-dia') === estado.diaAtivo);
  });
  const abaAtiva = document.querySelector('#viagem-conteudo .aba.ativa');
  if (abaAtiva && abaAtiva.scrollIntoView) {
    abaAtiva.scrollIntoView({ inline: 'nearest', block: 'nearest' });
  }
}

function diaInicial(dias) {
  const hoje = hojeISO();
  if (dias.includes(hoje)) {
    return hoje;
  }
  return dias[0] || null;
}

function passaFiltro(evento) {
  if (estado.filtroCategoria && evento.categoria !== estado.filtroCategoria) {
    return false;
  }
  if (estado.filtroStatus && evento.status !== estado.filtroStatus) {
    return false;
  }
  return true;
}

function mapaConflitos(eventosDoDia) {
  // O aviso olha o dia inteiro, mesmo que um dos dois esteja escondido pelo filtro.
  const contagem = {};
  eventosDoDia.forEach((evento) => {
    const hora = String(evento.horario || '').slice(0, 5);
    contagem[hora] = (contagem[hora] || 0) + 1;
  });
  return contagem;
}

function somarValores(eventos) {
  // Soma em centavos para 0,10 + 0,20 não virar 0,30000000004.
  let centavos = 0;
  eventos.forEach((evento) => {
    const numero = Number(evento.valor);
    if (!Number.isFinite(numero)) {
      return;
    }
    centavos += Math.round(numero * 100);
  });
  return centavos / 100;
}

function abrirFormularioEvento(evento) {
  if (!estado.viagemAtual) {
    return;
  }
  const form = criarFormularioEvento(evento);
  const cancelar = botaoSimples('Cancelar', 'btn btn-fantasma', fecharModal);
  const salvar = botaoSimples(evento ? 'Salvar alterações' : 'Criar evento', 'btn btn-primario', () => {
    enviarFormulario(form);
  });

  abrirModal({
    titulo: evento ? 'Editar evento' : 'Novo evento',
    corpo: form,
    rodape: [cancelar, salvar],
    fecharNoFundo: false,
  });
}

function criarFormularioEvento(evento) {
  const viagem = estado.viagemAtual;
  const form = document.createElement('form');
  form.className = 'formulario';
  form.noValidate = true;
  form.autocomplete = 'off';

  const dias = listarDias(viagem.data_ida, viagem.data_volta).map((iso) => {
    const data = parseDataISO(iso);
    const curto = data ? DIAS_CURTOS[data.getDay()] : '';
    return { valor: iso, nome: formatarDataBR(iso) + ' (' + curto + ')' };
  });

  const primeiraData = dias.length ? dias[0].valor : '';
  const dataSelecionada = evento ? evento.data : (estado.diaAtivo || primeiraData);
  const selectData = criarSelect('data', dias, dataSelecionada);
  selectData.required = true;

  const horario = inputTexto('time', evento ? String(evento.horario).slice(0, 5) : '');
  horario.required = true;

  const titulo = inputTexto('text', evento ? evento.titulo : '', 150);
  titulo.required = true;

  const local = inputTexto('text', evento && evento.local ? evento.local : '', 150);

  const categoria = criarSelect(
    'categoria',
    CATEGORIAS,
    evento ? evento.categoria : '',
    'Selecione'
  );
  categoria.required = true;

  const status = criarSelect('status', STATUS, evento ? evento.status : 'pendente');
  status.required = true;

  const valor = inputTexto('number', evento ? String(evento.valor) : '0');
  valor.min = '0';
  valor.step = '0.01';
  valor.required = true;

  const observacoes = document.createElement('textarea');
  observacoes.rows = 3;
  observacoes.value = evento && evento.observacoes ? evento.observacoes : '';

  const gradeHorario = document.createElement('div');
  gradeHorario.className = 'grade-2';
  gradeHorario.append(
    criarGrupo('horario', 'Horário', horario),
    criarGrupo('valor', 'Valor (R$)', valor)
  );

  const gradeTipo = document.createElement('div');
  gradeTipo.className = 'grade-2';
  gradeTipo.append(
    criarGrupo('categoria', 'Categoria', categoria),
    criarGrupo('status', 'Status', status)
  );

  const erroGeral = document.createElement('p');
  erroGeral.className = 'erro-geral';

  // Para um campo novo: crie o controle aqui, leia em salvarEvento,
  // valide em validarEvento e também em validar_evento() no PHP,
  // e inclua a coluna no schema.sql e nas queries de server/api/eventos.php.
  form.append(
    erroGeral,
    criarGrupo('titulo', 'Título', titulo),
    criarGrupo('data', 'Data', selectData),
    gradeHorario,
    criarGrupo('local', 'Local', local),
    gradeTipo,
    criarGrupo('observacoes', 'Observações', observacoes)
  );

  form.addEventListener('submit', (eventoSubmit) => {
    eventoSubmit.preventDefault();
    salvarEvento(form, evento ? evento.id : null);
  });

  return form;
}

async function salvarEvento(form, id) {
  const dados = {
    viagem_id: estado.viagemAtual.id,
    titulo: valorCampo(form, 'titulo'),
    data: valorCampo(form, 'data'),
    horario: valorCampo(form, 'horario'),
    local: valorCampo(form, 'local'),
    categoria: valorCampo(form, 'categoria'),
    valor: valorCampo(form, 'valor'),
    status: valorCampo(form, 'status'),
    observacoes: valorCampo(form, 'observacoes'),
  };

  const erros = validarEvento(dados);
  if (Object.keys(erros).length > 0) {
    mostrarErros(form, erros);
    console.log('Verifique os campos destacados.');
    return;
  }

  limparErros(form);
  const botoes = travarBotoesModal(true);

  try {
    if (id) {
      await Api.atualizarEvento(id, dados);
      mostrarToast('Evento atualizado.', 'sucesso');
    } else {
      await Api.criarEvento(dados);
      mostrarToast('Evento criado.', 'sucesso');
    }
    fecharModal();
    estado.diaAtivo = dados.data;
    await abrirViagem(estado.viagemAtual.id, { manter: true });
  } catch (erro) {
    if (erro.campos) {
      mostrarErros(form, erro.campos);
    } else {
      const geral = form.querySelector('.erro-geral');
      if (geral) {
        geral.textContent = erro.message;
      }
    }
    console.log(erro.message);
  } finally {
    travarBotoesModal(false, botoes);
  }
}

async function alternarStatus(eventoOrigem, botao) {
  const novo = eventoOrigem.status === 'confirmado' ? 'pendente' : 'confirmado';
  const dados = {
    titulo: eventoOrigem.titulo,
    data: eventoOrigem.data,
    horario: String(eventoOrigem.horario).slice(0, 5),
    local: eventoOrigem.local || '',
    categoria: eventoOrigem.categoria,
    valor: eventoOrigem.valor,
    status: novo,
    observacoes: eventoOrigem.observacoes || '',
  };

  if (botao) {
    botao.disabled = true;
  }

  try {
    await Api.atualizarEvento(eventoOrigem.id, dados);
    mostrarToast(novo === 'confirmado' ? 'Evento confirmado.' : 'Evento marcado como pendente.', 'sucesso');
    await abrirViagem(estado.viagemAtual.id, { manter: true });
  } catch (erro) {
    console.log(erro.message);
    if (botao && botao.isConnected) {
      botao.disabled = false;
    }
  }
}

async function pedirExclusaoEvento(evento) {
  const certo = await confirmar({
    titulo: 'Excluir evento',
    mensagem: 'Excluir o evento "' + evento.titulo + '"? Essa ação não pode ser desfeita.',
    textoConfirmar: 'Excluir evento',
  });
  if (!certo) {
    return;
  }

  try {
    await Api.excluirEvento(evento.id);
    mostrarToast('Evento excluído.', 'sucesso');
    await abrirViagem(estado.viagemAtual.id, { manter: true });
  } catch (erro) {
    console.log(erro.message);
  }
}

function eventoPorId(id) {
  return estado.eventos.find((evento) => String(evento.id) === String(id)) || null;
}

function validarViagem(dados) {
  const erros = {};
  const destino = dados.destino.trim();

  if (!destino) {
    erros.destino = 'Destino é obrigatório.';
  } else if (destino.length > 120) {
    erros.destino = 'Destino deve ter no máximo 120 caracteres.';
  }

  if (!dados.data_ida) {
    erros.data_ida = 'Informe a data de ida.';
  }
  if (!dados.data_volta) {
    erros.data_volta = 'Informe a data de volta.';
  }
  if (dados.data_ida && dados.data_volta && dados.data_volta < dados.data_ida) {
    erros.data_volta = 'A data de volta não pode ser anterior à data de ida.';
  }
  if (dados.data_ida && dados.data_volta && dados.data_volta >= dados.data_ida) {
    const dias = listarDias(dados.data_ida, dados.data_volta).length;
    if (dias > LIMITE_DIAS) {
      erros.data_volta = 'A viagem pode ter no máximo ' + LIMITE_DIAS + ' dias.';
    }
  }

  const orcamento = lerDecimalJS(dados.orcamento);
  if (orcamento === null) {
    erros.orcamento = 'Informe um orçamento válido.';
  } else if (orcamento < 0) {
    erros.orcamento = 'O orçamento não pode ser negativo.';
  } else if (orcamento > 99999999.99) {
    erros.orcamento = 'Orçamento maior do que o permitido.';
  }

  return erros;
}

function validarEvento(dados) {
  const erros = {};
  const titulo = dados.titulo.trim();
  const viagem = estado.viagemAtual;
  const dias = viagem ? listarDias(viagem.data_ida, viagem.data_volta) : [];

  if (!titulo) {
    erros.titulo = 'Título é obrigatório.';
  } else if (titulo.length > 150) {
    erros.titulo = 'Título deve ter no máximo 150 caracteres.';
  }

  if (!dados.data || !dias.includes(dados.data)) {
    erros.data = 'A data do evento deve estar dentro do período da viagem.';
  }

  if (!dados.horario) {
    erros.horario = 'Informe o horário.';
  } else if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(dados.horario)) {
    erros.horario = 'Horário inválido.';
  }

  if (dados.local.trim().length > 150) {
    erros.local = 'Local deve ter no máximo 150 caracteres.';
  }

  if (!CATEGORIAS.some((item) => item.valor === dados.categoria)) {
    erros.categoria = 'Selecione uma categoria válida.';
  }
  if (!STATUS.some((item) => item.valor === dados.status)) {
    erros.status = 'Selecione um status válido.';
  }

  const valor = lerDecimalJS(dados.valor);
  if (valor === null) {
    erros.valor = 'Informe um valor válido.';
  } else if (valor < 0) {
    erros.valor = 'O valor não pode ser negativo.';
  } else if (valor > 99999999.99) {
    erros.valor = 'Valor maior do que o permitido.';
  }

  return erros;
}

function normalizarBusca(texto) {
  const base = String(texto || '').toLocaleLowerCase('pt-BR');
  if (typeof base.normalize !== 'function') {
    return base;
  }
  return base.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function classeCategoria(categoria) {
  const conhecidas = CATEGORIAS.map((item) => item.valor);
  if (conhecidas.includes(categoria)) {
    return 'cat-' + categoria;
  }
  return 'cat-outro';
}

function nomeCategoria(valor) {
  const item = CATEGORIAS.find((categoria) => categoria.valor === valor);
  return item ? item.nome : String(valor || 'Outro');
}

function nomeStatus(valor) {
  const item = STATUS.find((status) => status.valor === valor);
  return item ? item.nome : String(valor || '');
}

function textoQuantidade(qtd, singular, plural) {
  return qtd + ' ' + (qtd === 1 ? singular : plural);
}

function htmlVazio(texto, comIcone, extraClasse) {
  const icone = comIcone ? '<p class="vazio-icone" aria-hidden="true">✈</p>' : '';
  const classe = 'vazio' + (extraClasse ? ' no-print' : '');
  return '<div class="' + classe + '">' + icone + '<p>' + escapeHtml(texto) + '</p></div>';
}

function valorCampo(form, nome) {
  const campo = form.elements.namedItem(nome);
  return campo ? String(campo.value) : '';
}

function inputTexto(tipo, valor, maxLength) {
  const input = document.createElement('input');
  input.type = tipo;
  input.value = valor || '';
  if (maxLength) {
    input.maxLength = maxLength;
  }
  return input;
}

function botaoSimples(texto, classe, aoClicarBotao) {
  const botao = document.createElement('button');
  botao.type = 'button';
  botao.className = classe;
  botao.textContent = texto;
  botao.addEventListener('click', aoClicarBotao);
  return botao;
}

function enviarFormulario(form) {
  if (typeof form.requestSubmit === 'function') {
    form.requestSubmit();
    return;
  }
  form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
}

function travarBotoesModal(travar, lista) {
  const botoes = lista || Array.from(document.querySelectorAll('#modal-rodape button'));
  botoes.forEach((botao) => {
    botao.disabled = travar;
  });
  return botoes;
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', iniciar);
} else {
  iniciar();
}
