def separar_simbolos(texto_digitado):
    texto = texto_digitado

    texto = texto.replace('<->', ' SETADUPLA ')
    texto = texto.replace('->', ' SETASIMPLES ')
    texto = texto.replace('↔', ' SETADUPLA ')
    texto = texto.replace('→', ' SETASIMPLES ')

    texto = texto.replace('¬', ' not ')
    texto = texto.replace('∧', ' and ')
    texto = texto.replace('∨', ' or ')
    texto = texto.replace('⊕', ' XOR ')

    texto = texto.replace('~', ' not ')
    texto = texto.replace('&', ' and ')
    texto = texto.replace('|', ' or ')

    texto = texto.replace('SETADUPLA', ' <-> ')
    texto = texto.replace('SETASIMPLES', ' -> ')

    texto = texto.replace('(', ' ( ')
    texto = texto.replace(')', ' ) ')

    lista_de_pedacos = texto.split()

    return lista_de_pedacos


def operador_principal(pedacos):
    peso_dos_operadores = {
        '<->': 0,
        '->': 1,
        'or': 2,
        'and': 3,
        'XOR': 3,
        'not': 4,
    }

    nivel_de_parenteses = 0
    posicao_do_melhor_operador = -1
    peso_do_melhor_operador = 999
    posicao_do_not = -1

    for i in range(len(pedacos)):
        pedaco_atual = pedacos[i]

        if pedaco_atual == '(':
            nivel_de_parenteses = nivel_de_parenteses + 1

        elif pedaco_atual == ')':
            nivel_de_parenteses = nivel_de_parenteses - 1

        elif nivel_de_parenteses == 0 and pedaco_atual in peso_dos_operadores:

            if pedaco_atual == 'not':
                if posicao_do_not == -1:
                    posicao_do_not = i
            else:
                peso_atual = peso_dos_operadores[pedaco_atual]

                if peso_atual <= peso_do_melhor_operador:
                    posicao_do_melhor_operador = i
                    peso_do_melhor_operador = peso_atual

    if posicao_do_melhor_operador != -1:
        return posicao_do_melhor_operador

    return posicao_do_not


def tirar_parenteses(pedacos):
    while len(pedacos) > 0 and pedacos[0] == '(' and pedacos[-1] == ')':
        nivel_de_parenteses = 0
        pode_remover = True

        for i in range(len(pedacos)):
            if pedacos[i] == '(':
                nivel_de_parenteses = nivel_de_parenteses + 1
            elif pedacos[i] == ')':
                nivel_de_parenteses = nivel_de_parenteses - 1

            if nivel_de_parenteses == 0 and i < len(pedacos) - 1:
                pode_remover = False
                break

        if pode_remover:
            pedacos = pedacos[1:-1]
        else:
            break

    return pedacos


def construir_arvore(pedacos):
    pedacos = tirar_parenteses(pedacos)

    if len(pedacos) == 1:
        token = pedacos[0]
        if token == 'V':
            return ('CONST', True)
        if token == 'F':
            return ('CONST', False)
        return ('VAR', token)

    posicao = operador_principal(pedacos)

    if posicao == -1:
        raise ValueError("Formula invalida: nao encontrei um operador valido em '" + ' '.join(pedacos) + "'")

    operador = pedacos[posicao]

    if operador == 'not':
        lado_direito = construir_arvore(pedacos[posicao + 1:])
        return ('not', lado_direito)

    lado_esquerdo = construir_arvore(pedacos[:posicao])
    lado_direito = construir_arvore(pedacos[posicao + 1:])

    return (operador, lado_esquerdo, lado_direito)


def envolver(no):
    tipo = no[0]
    if tipo == 'VAR' or tipo == 'CONST' or tipo == 'not':
        return arvore_para_texto(no)
    return '(' + arvore_para_texto(no) + ')'


def arvore_para_texto(no):
    tipo = no[0]

    if tipo == 'VAR':
        return no[1]

    if tipo == 'CONST':
        if no[1]:
            return 'V'
        return 'F'

    if tipo == 'not':
        return 'not ' + envolver(no[1])

    lado_esquerdo = envolver(no[1])
    lado_direito = envolver(no[2])

    return lado_esquerdo + ' ' + tipo + ' ' + lado_direito


def absorcao_em_or(a, b):
    if b[0] == 'and' and (a == b[1] or a == b[2]):
        return a
    if a[0] == 'and' and (b == a[1] or b == a[2]):
        return b
    return None


def absorcao_em_and(a, b):
    if b[0] == 'or' and (a == b[1] or a == b[2]):
        return a
    if a[0] == 'or' and (b == a[1] or b == a[2]):
        return b
    return None


def fatorar_em_or(a, b):
    if a[0] == 'and' and b[0] == 'and':
        a1 = a[1]
        a2 = a[2]
        b1 = b[1]
        b2 = b[2]
        if a1 == b1:
            return ('and', a1, ('or', a2, b2))
        if a1 == b2:
            return ('and', a1, ('or', a2, b1))
        if a2 == b1:
            return ('and', a2, ('or', a1, b2))
        if a2 == b2:
            return ('and', a2, ('or', a1, b1))
    return None


def fatorar_em_and(a, b):
    if a[0] == 'or' and b[0] == 'or':
        a1 = a[1]
        a2 = a[2]
        b1 = b[1]
        b2 = b[2]
        if a1 == b1:
            return ('or', a1, ('and', a2, b2))
        if a1 == b2:
            return ('or', a1, ('and', a2, b1))
        if a2 == b1:
            return ('or', a2, ('and', a1, b2))
        if a2 == b2:
            return ('or', a2, ('and', a1, b1))
    return None


def aplicar_regra_no_no(no):
    tipo = no[0]

    if tipo == 'not':
        filho = no[1]

        if filho[0] == 'CONST':
            return (('CONST', not filho[1]), 'Negacao de constante (not V = F / not F = V)')

        if filho[0] == 'not':
            return (filho[1], 'Dupla Negacao (not not A = A)')

        if filho[0] == 'and':
            novo = ('or', ('not', filho[1]), ('not', filho[2]))
            return (novo, 'De Morgan (not (A and B) = not A or not B)')

        if filho[0] == 'or':
            novo = ('and', ('not', filho[1]), ('not', filho[2]))
            return (novo, 'De Morgan (not (A or B) = not A and not B)')

        return None

    if tipo == 'and':
        a = no[1]
        b = no[2]

        if a == ('CONST', False) or b == ('CONST', False):
            return (('CONST', False), 'Elemento absorvente (A and F = F)')

        if a == ('CONST', True):
            return (b, 'Identidade (V and A = A)')
        if b == ('CONST', True):
            return (a, 'Identidade (A and V = A)')

        if a == ('not', b) or b == ('not', a):
            return (('CONST', False), 'Contradicao (A and not A = F)')

        if a == b:
            return (a, 'Idempotente (A and A = A)')

        absorvido = absorcao_em_and(a, b)
        if absorvido is not None:
            return (absorvido, 'Absorcao (A and (A or B) = A)')

        fatorado = fatorar_em_and(a, b)
        if fatorado is not None:
            return (fatorado, 'Distributiva - fator comum ((A or B) and (A or C) = A or (B and C))')

        return None

    if tipo == 'or':
        a = no[1]
        b = no[2]

        if a == ('CONST', True) or b == ('CONST', True):
            return (('CONST', True), 'Elemento absorvente (A or V = V)')

        if a == ('CONST', False):
            return (b, 'Identidade (F or A = A)')
        if b == ('CONST', False):
            return (a, 'Identidade (A or F = A)')

        if a == ('not', b) or b == ('not', a):
            return (('CONST', True), 'Tautologia (A or not A = V)')

        if a == b:
            return (a, 'Idempotente (A or A = A)')

        absorvido = absorcao_em_or(a, b)
        if absorvido is not None:
            return (absorvido, 'Absorcao (A or (A and B) = A)')

        fatorado = fatorar_em_or(a, b)
        if fatorado is not None:
            return (fatorado, 'Distributiva - fator comum ((A and B) or (A and C) = A and (B or C))')

        return None

    if tipo == '->':
        a = no[1]
        b = no[2]
        novo = ('or', ('not', a), b)
        return (novo, 'Eliminacao da Condicional (A -> B = not A or B)')

    if tipo == '<->':
        a = no[1]
        b = no[2]
        novo = ('and', ('->', a, b), ('->', b, a))
        return (novo, 'Eliminacao da Bicondicional (A <-> B = (A -> B) and (B -> A))')

    if tipo == 'XOR':
        a = no[1]
        b = no[2]
        novo = ('or', ('and', a, ('not', b)), ('and', ('not', a), b))
        return (novo, 'Definicao do XOR (A XOR B = (A and not B) or (not A and B))')

    return None


def simplificar_um_passo(no):
    tipo = no[0]

    if tipo == 'not':
        resultado = simplificar_um_passo(no[1])
        if resultado is not None:
            novo_filho, regra = resultado
            return (('not', novo_filho), regra)

    elif tipo == 'and' or tipo == 'or' or tipo == '->' or tipo == '<->' or tipo == 'XOR':
        resultado_esquerda = simplificar_um_passo(no[1])
        if resultado_esquerda is not None:
            novo_esquerdo, regra = resultado_esquerda
            return ((tipo, novo_esquerdo, no[2]), regra)

        resultado_direita = simplificar_um_passo(no[2])
        if resultado_direita is not None:
            novo_direito, regra = resultado_direita
            return ((tipo, no[1], novo_direito), regra)

    return aplicar_regra_no_no(no)


def simplificar_tudo(arvore):
    passos = []
    atual = arvore
    limite_de_seguranca = 5000
    contador = 0

    while contador < limite_de_seguranca:
        contador = contador + 1
        resultado = simplificar_um_passo(atual)

        if resultado is None:
            break

        novo, regra = resultado
        atual = novo
        passos.append((regra, arvore_para_texto(atual)))

    return atual, passos


def rodar():
    print("\nOperadores: not | and | or | -> | XOR | <->")
    print("Constantes: V (verdadeiro) | F (falso)")
    print("Exemplo: P -> Q   /   not ( A and B )   /   ( P and Q ) or ( P and not Q )")

    formula = input("\nFormula: ")

    pedacos = separar_simbolos(formula)

    if len(pedacos) == 0:
        print("\nVoce nao digitou nenhuma formula.")
        return

    try:
        arvore = construir_arvore(pedacos)
    except ValueError as erro:
        print("\n" + str(erro))
        print("Confira se escreveu os operadores certos (not, and, or, ->, <->, XOR) e os parenteses.")
        return

    texto_original = arvore_para_texto(arvore)
    final, passos = simplificar_tudo(arvore)

    print("\nFormula original:")
    print("   " + texto_original)

    print("\nPassos da simplificacao:")
    if len(passos) == 0:
        print("   (a formula ja estava o mais simples possivel)")
    else:
        numero = 1
        for regra, como_ficou in passos:
            print("   Passo " + str(numero) + ": " + regra)
            print("      => " + como_ficou)
            numero = numero + 1

    print("\nResultado final (mais simplificado):")
    print("   " + arvore_para_texto(final))


while True:
    rodar()
    resposta = input("\nOutra? (s/n): ")
    if resposta != 's':
        break
