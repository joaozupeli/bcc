def separar_simbolos(texto_digitado):
    texto_com_espacos = texto_digitado.replace('(', ' ( ')
    texto_com_espacos = texto_com_espacos.replace(')', ' ) ')

    lista_de_pedacos = texto_com_espacos.split()

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

                if peso_atual < peso_do_melhor_operador:
                    posicao_do_melhor_operador = i
                    peso_do_melhor_operador = peso_atual

    if posicao_do_melhor_operador != -1:
        return posicao_do_melhor_operador

    return posicao_do_not


def tirar_parenteses(pedacos):
    while pedacos[0] == '(' and pedacos[-1] == ')':
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


def calcular(pedacos, valores):
    pedacos = tirar_parenteses(pedacos)

    if len(pedacos) == 1:
        letra = pedacos[0]
        return valores[letra]

    posicao_do_operador = operador_principal(pedacos)
    operador = pedacos[posicao_do_operador]

    lado_direito_pedacos = pedacos[posicao_do_operador + 1:]

    if operador == 'not':
        valor_direito = calcular(lado_direito_pedacos, valores)
        return not valor_direito

    lado_esquerdo_pedacos = pedacos[:posicao_do_operador]

    valor_esquerdo = calcular(lado_esquerdo_pedacos, valores)
    valor_direito = calcular(lado_direito_pedacos, valores)

    if operador == 'and':
        return valor_esquerdo and valor_direito

    if operador == 'or':
        return valor_esquerdo or valor_direito

    if operador == '->':
        return (not valor_esquerdo) or valor_direito

    if operador == 'XOR':
        return valor_esquerdo != valor_direito

    if operador == '<->':
        return valor_esquerdo == valor_direito


def rodar():
    print("\nOperadores: not | and | or | -> | XOR | <->")
    formula = input("Formula: ")

    pedacos = separar_simbolos(formula)

    letras_encontradas = []
    for pedaco in pedacos:
        if len(pedaco) == 1 and pedaco.isupper():
            letras_encontradas.append(pedaco)

    letras = sorted(set(letras_encontradas))

    combinacoes = [[]]

    for letra in letras:
        novas_combinacoes = []
        for combinacao_atual in combinacoes:
            novas_combinacoes.append(combinacao_atual + [True])
            novas_combinacoes.append(combinacao_atual + [False])
        combinacoes = novas_combinacoes

    print()

    for combinacao in combinacoes:
        valores = {}
        for indice in range(len(letras)):
            letra_atual = letras[indice]
            valor_dessa_letra = combinacao[indice]
            valores[letra_atual] = valor_dessa_letra

        resultado = calcular(pedacos, valores)

        if resultado:
            print("V")
        else:
            print("F")


while True:
    rodar()
    resposta = input("\nOutra? (s/n): ")
    if resposta != 's':
        break
