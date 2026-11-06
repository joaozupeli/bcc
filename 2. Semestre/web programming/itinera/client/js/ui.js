// Modais, toasts, datas e dinheiro.
// Tudo que o app.js desenha com texto do usuário passa por escapeHtml.

const CHAVE_TEMA = 'itinera-tema';

const DIAS_CURTOS = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
const DIAS_LONGOS = [
  'domingo',
  'segunda-feira',
  'terça-feira',
  'quarta-feira',
  'quinta-feira',
  'sexta-feira',
  'sábado',
];

const ICONES = {
  voo: '<path fill="currentColor" d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/>',
  hospedagem: '<path fill="currentColor" d="M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-5.5v-6h-3V21H5a1 1 0 0 1-1-1v-9.5z"/>',
  comida: '<path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M7 3v7a2 2 0 0 0 4 0V3M9 3v18M16 3c2 2.5 2 5 0 7v11"/>',
  passeio: '<path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" d="M3 19h18M4.5 19 9 12l3 3.5L15.5 9 20 19"/>',
  transporte: '<path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" d="M6 16V7h12v9M6 16h12M6 11h12M8.5 19.5a1.2 1.2 0 1 0 0-2.4 1.2 1.2 0 0 0 0 2.4zM15.5 19.5a1.2 1.2 0 1 0 0-2.4 1.2 1.2 0 0 0 0 2.4z"/>',
  outro: '<circle cx="12" cy="12" r="7" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="2" fill="currentColor"/>',
};

let aoFecharAtual = null;
let elementoFocadoAntes = null;
let podeFecharNoFundo = true;
let uiPronta = false;

function escapeHtml(texto) {
  return String(texto ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeHtmlMultilinha(texto) {
  // O escape vem antes do <br>. A quebra de linha é nossa, não do usuário.
  return escapeHtml(texto).replace(/\n/g, '<br>');
}

function iniciarUi() {
  if (uiPronta) {
    return;
  }
  uiPronta = true;

  document.getElementById('modal').addEventListener('click', (evento) => {
    if (evento.target.classList.contains('modal-fundo')) {
      if (podeFecharNoFundo) {
        fecharModal();
      }
      return;
    }
    if (evento.target.closest('[data-fechar-modal]')) {
      fecharModal();
    }
  });

  document.addEventListener('keydown', (evento) => {
    if (evento.key === 'Escape') {
      fecharModal();
    }
  });
}

function abrirModal(opcoes) {
  const modal = document.getElementById('modal');
  document.getElementById('modal-titulo').textContent = opcoes.titulo;

  const corpo = document.getElementById('modal-corpo');
  corpo.replaceChildren();
  if (opcoes.corpo) {
    corpo.appendChild(opcoes.corpo);
  }

  const rodape = document.getElementById('modal-rodape');
  rodape.replaceChildren();
  (opcoes.rodape || []).forEach((botao) => rodape.appendChild(botao));

  aoFecharAtual = typeof opcoes.aoFechar === 'function' ? opcoes.aoFechar : null;
  podeFecharNoFundo = opcoes.fecharNoFundo !== false;
  elementoFocadoAntes = document.activeElement;

  modal.hidden = false;
  document.body.classList.add('modal-aberto');

  const foco = corpo.querySelector('input, select, textarea') || rodape.querySelector('button');
  if (foco) {
    foco.focus();
  }
}

function fecharModal() {
  const modal = document.getElementById('modal');
  if (!modal || modal.hidden) {
    return;
  }

  modal.hidden = true;
  document.body.classList.remove('modal-aberto');

  const callback = aoFecharAtual;
  aoFecharAtual = null;
  const voltar = elementoFocadoAntes;
  elementoFocadoAntes = null;

  if (voltar && typeof voltar.focus === 'function') {
    voltar.focus();
  }
  if (callback) {
    callback();
  }
}

function confirmar(opcoes) {
  return new Promise((resolve) => {
    const corpo = document.createElement('p');
    corpo.className = 'texto-confirmacao';
    corpo.textContent = opcoes.mensagem;

    const cancelar = document.createElement('button');
    cancelar.type = 'button';
    cancelar.className = 'btn btn-fantasma';
    cancelar.textContent = 'Cancelar';

    const ok = document.createElement('button');
    ok.type = 'button';
    ok.className = 'btn btn-perigo';
    ok.textContent = opcoes.textoConfirmar || 'Excluir';

    let decidido = false;
    function decidir(valor) {
      if (decidido) {
        return;
      }
      decidido = true;
      fecharModal();
      resolve(valor);
    }

    cancelar.addEventListener('click', () => decidir(false));
    ok.addEventListener('click', () => decidir(true));

    abrirModal({
      titulo: opcoes.titulo,
      corpo: corpo,
      rodape: [cancelar, ok],
      fecharNoFundo: true,
      aoFechar: () => decidir(false),
    });
  });
}

function mostrarToast(mensagem, tipo) {
  const caixa = document.getElementById('toasts');
  if (!caixa) {
    return;
  }

  const item = document.createElement('div');
  item.className = 'toast ' + (tipo === 'erro' ? 'erro' : 'sucesso');
  item.setAttribute('role', tipo === 'erro' ? 'alert' : 'status');
  item.textContent = mensagem;
  item.addEventListener('click', () => item.remove());
  caixa.appendChild(item);

  while (caixa.children.length > 4) {
    caixa.removeChild(caixa.firstChild);
  }

  setTimeout(() => {
    item.remove();
  }, 3800);
}

function criarGrupo(id, rotulo, controle) {
  const grupo = document.createElement('div');
  grupo.className = 'campo';

  const label = document.createElement('label');
  label.htmlFor = id;
  label.textContent = rotulo;

  controle.id = id;
  controle.name = id;

  const erro = document.createElement('p');
  erro.className = 'erro-campo';
  erro.id = 'erro-' + id;
  erro.setAttribute('data-erro-para', id);

  grupo.append(label, controle, erro);
  return grupo;
}

function criarSelect(id, opcoes, selecionado, placeholder) {
  const select = document.createElement('select');
  select.id = id;
  select.name = id;

  if (placeholder) {
    const vazio = document.createElement('option');
    vazio.value = '';
    vazio.textContent = placeholder;
    select.appendChild(vazio);
  }

  opcoes.forEach((opcao) => {
    const item = document.createElement('option');
    item.value = opcao.valor;
    item.textContent = opcao.nome;
    if (opcao.valor === selecionado) {
      item.selected = true;
    }
    select.appendChild(item);
  });

  return select;
}

function seletorCampo(nome) {
  const seguro = window.CSS && CSS.escape ? CSS.escape(nome) : nome;
  return '[data-erro-para="' + seguro + '"]';
}

function limparErros(form) {
  form.querySelectorAll('.erro-campo').forEach((erro) => {
    erro.textContent = '';
  });
  form.querySelectorAll('.invalido').forEach((grupo) => grupo.classList.remove('invalido'));
  form.querySelectorAll('[aria-invalid]').forEach((campo) => campo.removeAttribute('aria-invalid'));
  const geral = form.querySelector('.erro-geral');
  if (geral) {
    geral.textContent = '';
  }
}

function mostrarErros(form, campos) {
  limparErros(form);
  Object.keys(campos).forEach((nome) => {
    const erro = form.querySelector(seletorCampo(nome));
    if (!erro) {
      return;
    }
    erro.textContent = campos[nome];
    const grupo = erro.closest('.campo');
    if (grupo) {
      grupo.classList.add('invalido');
    }
    const controle = erro.previousElementSibling;
    if (controle && controle.setAttribute) {
      controle.setAttribute('aria-invalid', 'true');
      controle.setAttribute('aria-describedby', erro.id);
    }
  });
}

function iconeCategoria(categoria) {
  const desenho = ICONES[categoria] || ICONES.outro;
  return '<svg viewBox="0 0 24 24" aria-hidden="true" class="icone">' + desenho + '</svg>';
}

// new Date('2026-12-20') é meia-noite em UTC. No Brasil isso vira o dia 19 à noite.
// Montar com ano, mês e dia usa o fuso do computador e mantém o dia certo.
function parseDataISO(iso) {
  const partes = String(iso || '').split('-');
  if (partes.length < 3) {
    return null;
  }
  const ano = Number(partes[0]);
  const mes = Number(partes[1]);
  const dia = Number(partes[2]);
  if (!ano || !mes || !dia) {
    return null;
  }
  const data = new Date(ano, mes - 1, dia);
  if (data.getFullYear() !== ano || data.getMonth() !== mes - 1 || data.getDate() !== dia) {
    return null;
  }
  return data;
}

function formatarISO(data) {
  const ano = data.getFullYear();
  const mes = String(data.getMonth() + 1).padStart(2, '0');
  const dia = String(data.getDate()).padStart(2, '0');
  return ano + '-' + mes + '-' + dia;
}

function hojeISO() {
  return formatarISO(new Date());
}

function formatarDataBR(iso) {
  const data = parseDataISO(iso);
  if (!data) {
    return String(iso || '');
  }
  const dia = String(data.getDate()).padStart(2, '0');
  const mes = String(data.getMonth() + 1).padStart(2, '0');
  return dia + '/' + mes + '/' + data.getFullYear();
}

function formatarDataCurta(iso) {
  const data = parseDataISO(iso);
  if (!data) {
    return String(iso || '');
  }
  const dia = String(data.getDate()).padStart(2, '0');
  const mes = String(data.getMonth() + 1).padStart(2, '0');
  return dia + '/' + mes;
}

function formatarDataLonga(iso) {
  const data = parseDataISO(iso);
  if (!data) {
    return String(iso || '');
  }
  const semana = DIAS_LONGOS[data.getDay()];
  const nome = semana.charAt(0).toUpperCase() + semana.slice(1);
  return nome + ', ' + formatarDataBR(iso);
}

function listarDias(inicioISO, fimISO) {
  const inicio = parseDataISO(inicioISO);
  const fim = parseDataISO(fimISO);
  if (!inicio || !fim || fim < inicio) {
    return [];
  }

  const dias = [];
  const cursor = new Date(inicio.getTime());
  // Trava de segurança. O PHP recusa acima de 366; aqui o teto é um pouco maior
  // para a validação da tela ainda enxergar que o período passou do limite.
  while (cursor <= fim && dias.length < 400) {
    dias.push(formatarISO(cursor));
    cursor.setDate(cursor.getDate() + 1);
  }
  return dias;
}

function diferencaDias(deISO, paraISO) {
  const de = parseDataISO(deISO);
  const para = parseDataISO(paraISO);
  if (!de || !para) {
    return 0;
  }
  // round, e não floor: o horário de verão pode deixar o intervalo com 23h ou 25h.
  return Math.round((para.getTime() - de.getTime()) / 86400000);
}

function textoContagem(dataIda, dataVolta) {
  const hoje = hojeISO();
  if (hoje < dataIda) {
    const dias = diferencaDias(hoje, dataIda);
    if (dias === 1) {
      return { texto: 'Falta 1 dia', tipo: 'futura' };
    }
    return { texto: 'Faltam ' + dias + ' dias', tipo: 'futura' };
  }
  if (hoje > dataVolta) {
    return { texto: 'Concluída', tipo: 'concluida' };
  }
  return { texto: 'Em andamento', tipo: 'andamento' };
}

function formatarMoeda(valor) {
  const numero = Number(valor);
  const seguro = Number.isFinite(numero) ? numero : 0;
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(seguro);
}

function lerDecimalJS(valor) {
  let texto = String(valor ?? '').trim();
  if (!texto) {
    return null;
  }
  if (texto.includes(',')) {
    texto = texto.replace(/\./g, '').replace(',', '.');
  }
  if (!/^-?\d+(\.\d+)?$/.test(texto)) {
    return null;
  }
  const numero = Number(texto);
  if (!Number.isFinite(numero)) {
    return null;
  }
  return Math.round(numero * 100) / 100;
}
