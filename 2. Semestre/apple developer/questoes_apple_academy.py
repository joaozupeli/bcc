# ============================================================
#  TREINO PARA A PROVA DE PROGRAMAÇÃO — APPLE DEVELOPER ACADEMY
#  Para: João  |  Prova: sexta, 09/10/2026
# ============================================================
#
#  O QUE SABEMOS DA PROVA (pelo amigo que fez):
#    - 2 horas, 4 questões.
#    - Lógica básica em Python: input/print, laços, listas.
#    - 3 questões lembradas estão no BLOCO 7 (questões 19 a 25).
#    - A 4ª questão é desconhecida -> os blocos 1 a 6 treinam o resto.
#
#  COMO USAR:
#    1. Escreva seu código dentro de questao_XX() (troque o "pass").
#    2. Rode:  python3 questoes_apple_academy.py
#    3. Escolha o número da questão.
#    4. Escolha 1 (sua versão) ou 2 (solução).
#    As SOLUÇÕES estão no FIM do arquivo. Tente antes de olhar!
#
#  DICAS RÁPIDAS:
#    - Leia o enunciado 2 vezes. Sublinhe as mensagens exatas.
#    - Copie as mensagens EXATAMENTE (acento, maiúscula, espaço).
#    - Se a prova corrigir a saída automaticamente, use input()
#      sem texto dentro (o texto do input aparece na saída).
#    - Teste com o exemplo do enunciado antes de seguir.
#    - Travou 10 minutos? Pule e volte depois.
#
#  LISTAS: nas questões com lista, digite números separados por
#  espaço (ex.: 5 20 23 25) ou só aperte Enter para usar o exemplo.
# ============================================================


# ------------------------------------------------------------
# FUNÇÃO DE AJUDA (pode usar nas suas respostas)
# ------------------------------------------------------------
def ler_lista(exemplo):
    """Lê números separados por espaço. Enter vazio = usa o exemplo."""
    texto = input("Números separados por espaço (Enter = " + str(exemplo) + "): ")
    if texto.strip() == "":
        return exemplo
    numeros = []
    for parte in texto.split():
        try:
            numeros.append(int(parte))
        except ValueError:
            print("Valor inválido:", parte, "-> usando o exemplo")
            return exemplo
    return numeros


# ############################################################
#  BLOCO 1 — AQUECIMENTO (input, print, if)
# ############################################################

# ============================================================
# QUESTÃO 01 — Saudação
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia um nome.
#   Mostre: Olá, <nome>!
# Exemplo:
#   Entrada: João
#   Saída:   Olá, João!
# ============================================================
def questao_01():
    nome = input("Escreva o seu nome: ")
    print("Olá" + nome)
    

    print(questao_01())

# ============================================================
# QUESTÃO 02 — Par ou ímpar
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia um número inteiro.
#   Mostre "Par" ou "Ímpar".
#   Dica: use o resto da divisão (%).
# Exemplo:
#   Entrada: 7
#   Saída:   Ímpar
# ============================================================
def questao_02():
    numero = input(int("Digite o numero: "))
    if (numero // 2 == 0):
        print("par")
    else :
        print("impar")

    pass


# ============================================================
# QUESTÃO 03 — Maior de três números
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia 3 números inteiros (um por linha).
#   Mostre o maior. Não use max().
# Exemplo:
#   Entrada: 3
#            9
#            5
#   Saída:   Maior: 9
# ============================================================
def questao_03():
    # seu código aqui
    pass


# ############################################################
#  BLOCO 2 — STRINGS E LAÇOS SIMPLES
# ############################################################

# ============================================================
# QUESTÃO 04 — Contar vogais
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia uma frase.
#   Conte as vogais (maiúsculas e minúsculas, com ou sem acento).
# Exemplo:
#   Entrada: Apple Academy
#   Saída:   Vogais: 5
# ============================================================
def questao_04():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 05 — Palíndromo
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   Leia uma palavra ou frase.
#   Ignore espaços e maiúsculas.
#   Se lida igual de trás pra frente: "É palíndromo".
#   Senão: "Não é palíndromo".
# Exemplo:
#   Entrada: Ame a ema
#   Saída:   É palíndromo
#   Entrada: Python
#   Saída:   Não é palíndromo
# ============================================================
def questao_05():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 06 — FizzBuzz
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   Leia um número N.
#   Mostre de 1 até N, um por linha.
#   Múltiplo de 3 e de 5: "FizzBuzz".
#   Só de 3: "Fizz".  Só de 5: "Buzz".
# Exemplo:
#   Entrada: 5
#   Saída:   1
#            2
#            Fizz
#            4
#            Buzz
#   (com N = 15, a última linha é FizzBuzz)
# ============================================================
def questao_06():
    # seu código aqui
    pass


# ############################################################
#  BLOCO 3 — VALIDAR ENTRADA E LIMITE DE TENTATIVAS
#  (treino direto para a questão da SENHA)
# ############################################################

# ============================================================
# QUESTÃO 07 — Ler inteiro com segurança
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia um valor.
#   Se NÃO for inteiro: "Entrada inválida".
#   Se for: "O dobro é <dobro>".
#   Dica: try: int(...)  except ValueError:
# Exemplo:
#   Entrada: abc
#   Saída:   Entrada inválida
#   Entrada: 8
#   Saída:   O dobro é 16
# ============================================================
def questao_07():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 08 — Repetir até ser válido
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Peça um inteiro. Repita até o usuário acertar.
#   A cada valor inválido: "Tentativa inválida".
#   No final: "Número aceito: <n>".
#   Atenção: "2.5" NÃO é inteiro para int().
# Exemplo:
#   Entrada: x
#            2.5
#            7
#   Saída:   Tentativa inválida
#            Tentativa inválida
#            Número aceito: 7
# ============================================================
def questao_08():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 09 — Adivinhe o número (3 tentativas)
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   O número secreto é 7 (use NUMERO_SECRETO).
#   O usuário tem 3 tentativas.
#   Palpite menor que o secreto: "O número é maior".
#   Palpite maior: "O número é menor".
#   Acertou: "Acertou!" e para.
#   Valor não inteiro: "Tentativa inválida" (conta como tentativa).
#   Errou as 3: "Suas tentativas acabaram".
# Exemplo:
#   Entrada: 5
#            9
#            7
#   Saída:   O número é maior
#            O número é menor
#            Acertou!
# ============================================================
NUMERO_SECRETO = 7

def questao_09():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 10 — Menu da calculadora
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   Repita o menu até escolher 0.
#   1 = somar dois números.  2 = subtrair dois números.
#   0 = mostrar "Tchau!" e sair.
#   Outra opção: "Opção inválida".
#   Mostre o resultado assim: "Resultado: <valor>".
# Exemplo:
#   Entrada: 1
#            3
#            4
#            9
#            0
#   Saída:   Resultado: 7
#            Opção inválida
#            Tchau!
# ============================================================
def questao_10():
    # seu código aqui
    pass


# ############################################################
#  BLOCO 4 — LISTAS BÁSICAS
# ############################################################

# ============================================================
# QUESTÃO 11 — Soma e média
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista de números (use ler_lista).
#   Mostre a soma e a média. Não use sum().
# Exemplo:
#   Entrada: 4 8 6 2
#   Saída:   Soma: 20
#            Média: 5.0
# ============================================================
def questao_11():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 12 — Maior e menor (sem max/min)
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista. Mostre o maior e o menor.
#   Não use max() nem min().
# Exemplo:
#   Entrada: 7 2 9 4
#   Saída:   Maior: 9
#            Menor: 2
# ============================================================
def questao_12():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 13 — Contar pares e ímpares
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista. Conte os pares e os ímpares.
# Exemplo:
#   Entrada: 1 2 3 4 6
#   Saída:   Pares: 3
#            Ímpares: 2
# ============================================================
def questao_13():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 14 — Posição do maior
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista. Ache o maior número e a posição dele.
#   Posição começa em 0. Se repetir, vale o primeiro.
#   Mostre também quantos números vêm antes dele.
#   IDEIA IMPORTANTE: na posição i, existem i números antes.
#   (Isso ajuda MUITO na questão dos picos!)
# Exemplo:
#   Entrada: 3 8 1 8
#   Saída:   Maior: 8
#            Posição: 1
#            Números antes: 1
# ============================================================
def questao_14():
    # seu código aqui
    pass


# ############################################################
#  BLOCO 5 — VIZINHOS NA LISTA (lista[i] e lista[i-1])
#  (treino direto para TEMPERATURA e PICOS)
# ############################################################

# ============================================================
# QUESTÃO 15 — Diferenças entre vizinhos
# Dificuldade: Fácil
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista.
#   Para cada par de vizinhos, mostre a diferença (sempre positiva).
#   Um resultado por linha. Dica: abs().
# Exemplo:
#   Entrada: 5 20 23 25
#   Saída:   15
#            3
#            2
# ============================================================
def questao_15():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 16 — A lista é crescente?
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista.
#   Se cada número for MAIOR que o anterior: "Sim".
#   Senão: "Não".
# Exemplo:
#   Entrada: 1 3 5 9
#   Saída:   Sim
#   Entrada: 1 3 2
#   Saída:   Não
# ============================================================
def questao_16():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 17 — Contar subidas
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista.
#   Conte quantas vezes um número é maior que o anterior.
# Exemplo:
#   Entrada: 2 3 1 5 4 8
#   Saída:   Subidas: 3
#   (3>2, 5>1, 8>4)
# ============================================================
def questao_17():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 18 — Maior sequência crescente
# Dificuldade: Difícil
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista.
#   Ache o maior trecho SEGUIDO em que cada número sobe.
#   Mostre o tamanho desse trecho.
# Exemplo:
#   Entrada: 1 2 0 3 4 5 1
#   Saída:   Maior sequência: 4
#   (o trecho é 0 3 4 5)
# ============================================================
def questao_18():
    # seu código aqui
    pass


# ############################################################
#  BLOCO 6 — QUESTÕES DA PROVA (VERSÃO LEMBRADA PELO AMIGO)
#  + variantes, caso o enunciado real seja um pouco diferente
# ############################################################

# ============================================================
# QUESTÃO 19 — [PROVA] Senha com 5 tentativas
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   A senha correta é 1234 (use SENHA_CORRETA).
#   O usuário tem no MÁXIMO 5 tentativas.
#   Senha certa: "Acesso permitido" e para.
#   Senha errada: "Senha incorreta".
#   Não é inteiro: "Tentativa inválida".
#   REGRA DESTA VERSÃO: tentativa inválida TAMBÉM CONTA.
#   Gastou as 5: "Acesso bloqueado".
#   (Essa última mensagem é escolha nossa. Se a prova não
#    pedir, não mostre nada no final.)
# Exemplo 1:
#   Entrada: abc
#            1111
#            1234
#   Saída:   Tentativa inválida
#            Senha incorreta
#            Acesso permitido
# Exemplo 2 (a 6ª linha nem é lida):
#   Entrada: abc
#            1
#            2
#            3
#            4
#            1234
#   Saída:   Tentativa inválida
#            Senha incorreta
#            Senha incorreta
#            Senha incorreta
#            Senha incorreta
#            Acesso bloqueado
# ============================================================
SENHA_CORRETA = 1234

def questao_19():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 20 — [PROVA – VARIANTE] Senha: inválida NÃO conta
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   Igual à questão 19, MAS:
#   tentativa inválida mostra "Tentativa inválida"
#   e NÃO gasta tentativa.
#   Só senhas inteiras contam (máximo 5).
# Exemplo (mesma entrada do Exemplo 2 da 19):
#   Entrada: abc
#            1
#            2
#            3
#            4
#            1234
#   Saída:   Tentativa inválida
#            Senha incorreta
#            Senha incorreta
#            Senha incorreta
#            Senha incorreta
#            Acesso permitido
#   (agora 1234 é a 5ª tentativa válida)
# ============================================================
def questao_20():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 21 — [PROVA] Maior diferença de temperatura
# Dificuldade: Médio
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista de temperaturas.
#   Ache a maior diferença entre dois dias SEGUIDOS.
#   A diferença é sempre positiva (use abs).
# Exemplo:
#   Entrada: 5 20 23 25
#   Saída:   15
#   (diferenças: 15, 3, 2 -> a maior é 15)
#   Entrada: -3 4 2
#   Saída:   7
# ============================================================
def questao_21():
    # seu código aqui
    pass


# ------------------------------------------------------------
#  SOBRE OS PICOS (leia antes das questões 22 a 25)
#  O amigo lembrou: lista [2, 3, 1, 5, 4, 8], picos 5 e 8.
#  Ele não lembrou a regra exata. Então treinamos 4 versões.
#  O SEGREDO: todas são 1 laço + 1 if. Só muda a condição do if
#  e a forma de contar.
#    Contar desde o início:     antes = i
#    Contar desde o último pico: antes = i - ultimo_pico - 1
# ------------------------------------------------------------

# ============================================================
# QUESTÃO 22 — [PROVA] Picos (versão principal: "novo recorde")
# Dificuldade: Difícil
# ------------------------------------------------------------
# Enunciado:
#   Leia uma lista.
#   PICO = número maior que TODOS os anteriores.
#   O primeiro número não conta como pico.
#   Para cada pico, mostre quantos números vêm antes dele
#   (contando desde o início da lista).
#   Sem picos: "Nenhum pico".
# Exemplo:
#   Entrada: 2 3 1 5 4 8
#   Saída:   Pico: 3 | Antes: 1
#            Pico: 5 | Antes: 3
#            Pico: 8 | Antes: 5
#   (5 e 8 batem com o amigo. Nesta regra, 3 também é pico.)
# ============================================================
def questao_22():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 23 — [PROVA – VARIANTE A] Picos, contando desde o último pico
# Dificuldade: Difícil
# ------------------------------------------------------------
# Enunciado:
#   Mesma regra de pico da questão 22 (novo recorde).
#   MAS conte só os números ENTRE o pico anterior e este.
#   No primeiro pico, conte desde o início.
# Exemplo:
#   Entrada: 2 3 1 5 4 8
#   Saída:   Pico: 3 | Antes: 1
#            Pico: 5 | Antes: 1
#            Pico: 8 | Antes: 1
#   (entre 5 e 8 só existe o 4 -> 1)
# ============================================================
def questao_23():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 24 — [PROVA – VARIANTE B] Pico local (maior que os 2 vizinhos)
# Dificuldade: Difícil
# ------------------------------------------------------------
# Enunciado:
#   PICO = maior que o vizinho da esquerda E da direita.
#   O primeiro e o último NÃO podem ser pico (falta vizinho).
#   Conte desde o início da lista.
#   Sem picos: "Nenhum pico".
# Exemplo:
#   Entrada: 2 3 1 5 4 8
#   Saída:   Pico: 3 | Antes: 1
#            Pico: 5 | Antes: 3
#   (8 é o último, então não entra)
#   Se pedirem "desde o último pico": 3 -> 1, 5 -> 1.
# ============================================================
def questao_24():
    # seu código aqui
    pass


# ============================================================
# QUESTÃO 25 — [PROVA – VARIANTE C] Maior que os 2 anteriores
# Dificuldade: Difícil
# ------------------------------------------------------------
# Enunciado:
#   PICO = maior que os DOIS números logo antes dele.
#   Os dois primeiros não podem ser pico.
#   Mostre os dois jeitos de contar, nesta ordem:
#   desde o início e desde o último pico.
#   Sem picos: "Nenhum pico".
# Exemplo:
#   Entrada: 2 3 1 5 4 8
#   Saída:   Pico: 5 | Desde o início: 3 | Desde o último pico: 3
#            Pico: 8 | Desde o início: 5 | Desde o último pico: 1
#   (Esta regra dá EXATAMENTE 5 e 8, como o amigo lembrou.
#    A regra "subiu logo depois de uma descida" também dá 5 e 8.)
# ============================================================
def questao_25():
    # seu código aqui
    pass


# ############################################################
# ############################################################
# ##                                                        ##
# ##          SOLUÇÕES — SÓ OLHE DEPOIS DE TENTAR!          ##
# ##                                                        ##
# ############################################################
# ############################################################


def solucao_01():
    nome = input("Nome: ")
    print("Olá, " + nome + "!")


def solucao_02():
    numero = int(input("Número: "))
    if numero % 2 == 0:      # resto 0 na divisão por 2 = par
        print("Par")
    else:
        print("Ímpar")


def solucao_03():
    a = int(input("Número 1: "))
    b = int(input("Número 2: "))
    c = int(input("Número 3: "))
    maior = a                # começa achando que o primeiro é o maior
    if b > maior:
        maior = b
    if c > maior:
        maior = c
    print("Maior:", maior)


def solucao_04():
    frase = input("Frase: ")
    vogais = "aeiouáéíóúâêôãõà"
    contador = 0
    for letra in frase.lower():   # lower() deixa tudo minúsculo
        if letra in vogais:
            contador = contador + 1
    print("Vogais:", contador)


def solucao_05():
    texto = input("Texto: ")
    # 1) tira espaços e deixa minúsculo
    limpo = ""
    for letra in texto.lower():
        if letra != " ":
            limpo = limpo + letra
    # 2) monta o texto ao contrário (atalho: limpo[::-1])
    invertido = ""
    for letra in limpo:
        invertido = letra + invertido
    # 3) compara
    if limpo == invertido:
        print("É palíndromo")
    else:
        print("Não é palíndromo")


def solucao_06():
    n = int(input("N: "))
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:   # testa o caso duplo PRIMEIRO
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


def solucao_07():
    texto = input("Valor: ")
    try:
        numero = int(texto)          # se não for inteiro, pula pro except
        print("O dobro é", numero * 2)
    except ValueError:
        print("Entrada inválida")


def solucao_08():
    while True:
        texto = input("Inteiro: ")
        try:
            numero = int(texto)
            break                    # deu certo: sai do laço
        except ValueError:
            print("Tentativa inválida")
    print("Número aceito:", numero)


def solucao_09():
    for tentativa in range(3):       # 3 tentativas
        texto = input("Palpite: ")
        try:
            palpite = int(texto)
        except ValueError:
            print("Tentativa inválida")
            continue                 # gasta a tentativa e vai pra próxima
        if palpite == NUMERO_SECRETO:
            print("Acertou!")
            return                   # sai da função
        elif palpite < NUMERO_SECRETO:
            print("O número é maior")
        else:
            print("O número é menor")
    print("Suas tentativas acabaram")


def solucao_10():
    while True:
        opcao = input("Opção (1=somar, 2=subtrair, 0=sair): ")
        if opcao == "0":
            print("Tchau!")
            break
        elif opcao == "1" or opcao == "2":
            try:
                a = int(input("Primeiro número: "))
                b = int(input("Segundo número: "))
            except ValueError:
                print("Entrada inválida")
                continue
            if opcao == "1":
                print("Resultado:", a + b)
            else:
                print("Resultado:", a - b)
        else:
            print("Opção inválida")


def solucao_11():
    lista = ler_lista([4, 8, 6, 2])
    if len(lista) == 0:
        print("Lista vazia")
        return
    soma = 0
    for numero in lista:
        soma = soma + numero
    media = soma / len(lista)
    print("Soma:", soma)
    print("Média:", media)


def solucao_12():
    lista = ler_lista([7, 2, 9, 4])
    maior = lista[0]                 # começa com o primeiro
    menor = lista[0]
    for numero in lista:
        if numero > maior:
            maior = numero
        if numero < menor:
            menor = numero
    print("Maior:", maior)
    print("Menor:", menor)


def solucao_13():
    lista = ler_lista([1, 2, 3, 4, 6])
    pares = 0
    impares = 0
    for numero in lista:
        if numero % 2 == 0:
            pares = pares + 1
        else:
            impares = impares + 1
    print("Pares:", pares)
    print("Ímpares:", impares)


def solucao_14():
    lista = ler_lista([3, 8, 1, 8])
    posicao = 0
    for i in range(len(lista)):      # i = 0, 1, 2, ...
        if lista[i] > lista[posicao]:    # ">" mantém o primeiro em empate
            posicao = i
    print("Maior:", lista[posicao])
    print("Posição:", posicao)
    print("Números antes:", posicao) # na posição i há i números antes


def solucao_15():
    lista = ler_lista([5, 20, 23, 25])
    for i in range(1, len(lista)):   # começa em 1 para ter lista[i-1]
        diferenca = abs(lista[i] - lista[i - 1])
        print(diferenca)


def solucao_16():
    lista = ler_lista([1, 3, 5, 9])
    crescente = True                 # "bandeira": começa verdadeira
    for i in range(1, len(lista)):
        if lista[i] <= lista[i - 1]:
            crescente = False        # achou um problema
    if crescente:
        print("Sim")
    else:
        print("Não")


def solucao_17():
    lista = ler_lista([2, 3, 1, 5, 4, 8])
    subidas = 0
    for i in range(1, len(lista)):
        if lista[i] > lista[i - 1]:
            subidas = subidas + 1
    print("Subidas:", subidas)


def solucao_18():
    lista = ler_lista([1, 2, 0, 3, 4, 5, 1])
    if len(lista) == 0:
        print("Maior sequência: 0")
        return
    atual = 1                        # tamanho do trecho de agora
    melhor = 1                       # maior trecho até agora
    for i in range(1, len(lista)):
        if lista[i] > lista[i - 1]:
            atual = atual + 1        # continua subindo
        else:
            atual = 1                # quebrou: recomeça
        if atual > melhor:
            melhor = atual
    print("Maior sequência:", melhor)


def solucao_19():
    # Versão principal: TODA tentativa conta, até a inválida.
    tentativas = 0
    while tentativas < 5:
        texto = input("Senha: ")
        tentativas = tentativas + 1  # conta ANTES de testar
        try:
            senha = int(texto)
        except ValueError:
            print("Tentativa inválida")
            continue
        if senha == SENHA_CORRETA:
            print("Acesso permitido")
            return                   # acertou: acaba
        else:
            print("Senha incorreta")
    print("Acesso bloqueado")        # tire se a prova não pedir


def solucao_20():
    # Variante: inválida NÃO gasta tentativa.
    tentativas = 0
    while tentativas < 5:
        texto = input("Senha: ")
        try:
            senha = int(texto)
        except ValueError:
            print("Tentativa inválida")
            continue                 # volta sem somar
        tentativas = tentativas + 1  # só conta senha inteira
        if senha == SENHA_CORRETA:
            print("Acesso permitido")
            return
        else:
            print("Senha incorreta")
    print("Acesso bloqueado")


def solucao_21():
    temperaturas = ler_lista([5, 20, 23, 25])
    maior = 0
    for i in range(1, len(temperaturas)):
        diferenca = abs(temperaturas[i] - temperaturas[i - 1])
        if diferenca > maior:
            maior = diferenca
    print(maior)


def solucao_22():
    # Pico = novo recorde. Conta desde o início (antes = i).
    lista = ler_lista([2, 3, 1, 5, 4, 8])
    if len(lista) == 0:
        print("Nenhum pico")
        return
    recorde = lista[0]               # o primeiro é o recorde inicial
    achou = False
    for i in range(1, len(lista)):
        if lista[i] > recorde:
            print("Pico:", lista[i], "| Antes:", i)
            recorde = lista[i]
            achou = True
    if not achou:
        print("Nenhum pico")


def solucao_23():
    # Pico = novo recorde. Conta desde o último pico.
    lista = ler_lista([2, 3, 1, 5, 4, 8])
    if len(lista) == 0:
        print("Nenhum pico")
        return
    recorde = lista[0]
    ultimo_pico = -1                 # -1 faz o 1º pico contar desde o início
    for i in range(1, len(lista)):
        if lista[i] > recorde:
            antes = i - ultimo_pico - 1
            print("Pico:", lista[i], "| Antes:", antes)
            recorde = lista[i]
            ultimo_pico = i
    if ultimo_pico == -1:
        print("Nenhum pico")


def solucao_24():
    # Pico local: maior que os dois vizinhos. Pontas não contam.
    lista = ler_lista([2, 3, 1, 5, 4, 8])
    achou = False
    for i in range(1, len(lista) - 1):   # pula o primeiro e o último
        if lista[i] > lista[i - 1] and lista[i] > lista[i + 1]:
            print("Pico:", lista[i], "| Antes:", i)
            achou = True
    if not achou:
        print("Nenhum pico")


def solucao_25():
    # Pico = maior que os 2 anteriores. Mostra os dois jeitos de contar.
    lista = ler_lista([2, 3, 1, 5, 4, 8])
    ultimo_pico = -1
    for i in range(2, len(lista)):   # começa em 2: precisa de 2 antes
        if lista[i] > lista[i - 1] and lista[i] > lista[i - 2]:
            desde_ultimo = i - ultimo_pico - 1
            print("Pico:", lista[i], "| Desde o início:", i,
                  "| Desde o último pico:", desde_ultimo)
            ultimo_pico = i
    if ultimo_pico == -1:
        print("Nenhum pico")
    # Regra alternativa "subiu logo depois de uma descida":
    # troque o if por:
    #   lista[i] > lista[i - 1] and lista[i - 1] < lista[i - 2]


# ############################################################
#  MENU — escolha a questão e rode sua versão ou a solução
# ############################################################

QUESTOES = [
    questao_01, questao_02, questao_03, questao_04, questao_05,
    questao_06, questao_07, questao_08, questao_09, questao_10,
    questao_11, questao_12, questao_13, questao_14, questao_15,
    questao_16, questao_17, questao_18, questao_19, questao_20,
    questao_21, questao_22, questao_23, questao_24, questao_25,
]

SOLUCOES = [
    solucao_01, solucao_02, solucao_03, solucao_04, solucao_05,
    solucao_06, solucao_07, solucao_08, solucao_09, solucao_10,
    solucao_11, solucao_12, solucao_13, solucao_14, solucao_15,
    solucao_16, solucao_17, solucao_18, solucao_19, solucao_20,
    solucao_21, solucao_22, solucao_23, solucao_24, solucao_25,
]


def menu():
    total = len(QUESTOES)
    while True:
        try:
            texto = input("\nQuestão (1-" + str(total) + ", 0 = sair): ")
            try:
                numero = int(texto)
            except ValueError:
                print("Digite um número.")
                continue
            if numero == 0:
                print("Bons estudos, João!")
                break
            if numero < 1 or numero > total:
                print("Essa questão não existe.")
                continue
            escolha = input("1 = minha versão | 2 = solução: ")
            print("-" * 40)
            if escolha == "2":
                SOLUCOES[numero - 1]()
            else:
                QUESTOES[numero - 1]()
                print("(Se nada apareceu, sua função ainda está vazia.)")
            print("-" * 40)
        except EOFError:             # fim da entrada (ex.: Ctrl+D)
            print()
            break


if __name__ == '__main__':
    menu()
