# Simulado de Prova - Vetores, Matrizes e Funções

# Este simulado contém questões similares às que serão cobradas na avaliação individual a ser realizada em sala de aula. Durante a avaliação, você deverá escrever suas respostas à mão, sem consultar ou receber ajuda do computador. O objetivo é avaliar suas habilidades e conhecimentos em lógica de programação.

# Por isso, para que o simulado seja eficaz, recomendamos que você resolva as questões diretamente em uma folha de papel.

# As listas de exercícios realizadas ao longo das aulas também é uma excelente base de estudo.

# ### 1. Testes de Mesa

# a. Qual valor será impresso na tela?
# vet = [1,2,3,4,5,6]

# vet[0] = vet[3]
# vet[3] = vet[0]
# vet[2] = vet[4]
# vet[5] += vet[1] + vet[3]
# print(vet)

# [4,2,5,4,5,12]

# b. Qual valor será impresso na tela?
# vet = [0,1]
# for i in range(2,8):
#     vet.append(vet[i-1] + vet[i-2])

# [0,1] 
# [0,1,1] # Primeira volta do for i = 2 2-1 + 2-2
# [0,1,1,2] # Segunda volta do for i = 3 3-1 + 3-2
# [0,1,1,2] # Terceira volta do for i = 4-1 + 4-2
# [0,1,1,2,3,5] # Quarta volta do for i = 5-1 + 5-2
# [0,1,1,2,3,5,8] # Quinta volta do for i = 6-1 + 6-2
# [0,1,1,2,3,5,13] # Sexta volta do for i = 7-1 + 7-2
# [0,1,1,2,3,5,13,18] # Setima volta do for i = 8-1 + 8-2


# c. Qual valor será impresso na tela?
# vet = [4,6,4,1,2,9,13]
# tam = len(vet)
# a = 0

# for i in range(tam):    # 7 vezes rodando
#     if(vet[i] % 2 == 0): 
#         a += vet[i] 
# print(a)

[4,6,4,2]


# d. Qual valor será impresso na tela?
# vet = [4,6,4,1,2,9,13]
# tam = len(vet)
# b = 0

# for i in range(tam):    
#     if((vet[i] + vet[tam-1-i]) % 2 == 0): 9 + 7-1-7 = 
#         b += vet[i]
# print(b)

[4,] # 0 Add porque é par
[4] # 1 Não add porque deu impar
[4,4] # 2 Add porque deu par
[4,4,1] # 3 Adicionar porque a soma é par
[4,4,1,2] # 4 Adiciona porque a soma é par
[4,4,1,2] # 5 Não adiciona porque a soma é 3
[4,4,1,2] # 6 Não adiciona porque a soma é 9


# e. Qual valor será impresso na tela?

# def altera(a,b):    
#     temp = a
#     a = b
#     b = temp

#     return a,b

# vet = [4,6,4,1,2,9,13]
# tam = len(vet) -- 7 -- 
# for i in range(tam):    
#     m = i        
#     for j in range(i,tam): 0 até 7
#         if vet[j] > vet[m]: 0 é maior que 0 ? 
#             m = j não então isso continua sendo 0

#     vet[i],vet[m] = altera(vet[i],vet[m])

# print(vet)

# essa merda é muito chata 


# f. Qual valor será impresso na tela?
# def func(n,vet):    
#     ret = False    
#     for i in range(len(vet)):
#         if n == vet[i]:
#             ret = True
#     return ret        

# vet = [1,2,3,1,3,5,8,9,10,5]
# r = func(3,vet)
# print(r)


# g. Qual valor será impresso na tela?
# def func_3(vetor):    
#     temp = vetor[0]
#     tam = len(vetor)
#     vetor[0] = vetor[tam-1]
#     vetor[tam-1] = temp        
#     return vetor

# def func_2(a):
#     a += 1
#     b = a*2    
#     return b

# def func_1(vet):    
#     for i in range(len(vet)):
#         vet[i] = func_2(vet[i])        
#     return vet    

# vet = [1,2,3,4,5]
# print(vet)

# vet = func_11([4,5,6,7,8]) #ERRO QUE JA ESTA MOSTRANDO EXEMPLO
# print(vet)

# vet = func_3(vet)
# print(vet)


# h. Qual valor será impresso na tela?
# vet = [66,111,109,32,100,105,97]

# for i in range(len(vet)):
#     print(chr(vet[i]), end='')

# print()


# i. Qual valor será impresso na tela?
# def avalia(string):
#     count = 0
#     for char in string:
#         ascii_value = ord(char)
#         if 65 <= ascii_value <= 90 or 97 <= ascii_value <= 122:
#             count += 1
#     return count

# texto = "aB@c@dabra1234"
# resultado = avalia(texto)
# print(resultado)


# j. Qual valor será impresso na tela?
# def modifica(string):
#     count = 0
#     new_str = ''
#     for char in string:
#         ascii_value = ord(char)
#         if 65 <= ascii_value <= 90:
#             new_str += chr(ascii_value + 32)
#         elif 97 <= ascii_value <= 122:
#             new_str += chr(ascii_value - 32)            
#         else:
#             new_str += char

#     return new_str

# texto = "Em 24/06/2023 fez UM belo DIA de Sol"
# resultado = modifica(texto)
# print(resultado)

# **OBS**: Em teste de mesa, podem existir variações destes exercícios, no qual se pede para corrigir o código apresentado.

# 2. Implemente o que se pede

# a. Crie um vetor com 1000 números aleatórios, no entanto pares . (Dica: fique sorteando números e so incluia se for par. Facilita utilizar um while() ao invés do for)

import random

# vetor = []

# while len(vetor) < 1000:
#     numero = random.randint(0,100)
#     if numero % 2 == 0:
#         vetor.append(numero)

# print(vetor)

# b. Adicione números ao vetor, até que a soma deles ultrapasse 100mil.

# while sum(vetor) < 100000:
#     numero = random.randint(100,1000)
#     vetor.append(numero)

# print(sum(vetor))

# c. Dado um vetor de 100 posições, calcule a média dos elementos múltiplos de 5

# multiplos_cinco = []
# media = 0
# vetor = [random.randint(10, 1000) for _ in range(100)]

# for i in range(len(vetor)):
#     if vetor[i] % 5 == 0:
#         multiplos_cinco.append(vetor[i])
#     media = sum(multiplos_cinco) / len(multiplos_cinco)

# print(multiplos_cinco)
# print(sum(multiplos_cinco))
# print(len(multiplos_cinco))
# print(media) # PERFEITO RODOU

# d. Dado um vetor de N posições, cálcule a soma dos produtos, sendo o índice o fato de multiplicação. Exemplo:

#     [9,2,3,7,19,.....] = 9x0 + 2x1 + 3x2, 7x3, 19x4 .....

# posicoes = int(input(""))
# vetor = [random.randint(0,100) for _ in range(posicoes)]
# soma = 0

# for i in range(len(vetor)):
#     soma += vetor[i] * i

# print(vetor)
# print(soma)


# e. Determine uma função que recebe um valor N e cria um vetor contendo a série de fibonacci até N.

# def fibonacci_(n):
#     fibonacci = []
#     fibonacci.append(0)
#     fibonacci.append(1)
#     for i in range(2,n+1):
#         fibonacci.append(fibonacci[i-1] + fibonacci[i-2])
#     print(fibonacci)

# print(fibonacci_(5))
        


# f. Converta números binários em decimais. Considere a entrada do binário em formato texto.
#
# Se você está meio perdido, vamos entender passo a passo!
#
# Um número binário é um número usando apenas os dígitos 0 e 1, e cada posição (da direita pra esquerda) representa uma potência de 2.
# Por exemplo, o número binário "1011" significa:
#
#   Posições:    3    2    1    0   (da esquerda para a direita)
#   Dígitos:     1    0    1    1
#                |    |    |    |
#       1 * 2³ + 0 * 2² + 1 * 2¹ + 1 * 2⁰
#
# Agora vamos calcular cada termo:
#   1 * 2³ = 1 * 8 = 8
#   0 * 2² = 0 * 4 = 0
#   1 * 2¹ = 1 * 2 = 2
#   1 * 2⁰ = 1 * 1 = 1
# Some tudo: 8 + 0 + 2 + 1 = 11
#
# Resultado: "1011" em decimal é 11.
#
# Outro exemplo: "10101"
#   Posições:    4    3    2    1    0   
#   Dígitos:     1    0    1    0    1
#
#       1 * 2⁴ = 16
#       0 * 2³ = 0
#       1 * 2² = 4
#       0 * 2¹ = 0
#       1 * 2⁰ = 1
# Soma: 16 + 0 + 4 + 0 + 1 = 21
#
# RESUMINDO:
# 1. Escreva o número binário.
# 2. Comece da direita para a esquerda: a última casa vale 2⁰, depois 2¹, depois 2², e assim por diante.
# 3. Multiplique cada dígito (0 ou 1) pela potência de 2 correspondente.
# 4. Some todos esses valores, esse é o número decimal final!
#
# # Exemplo de função para converter:
# def binario_para_decimal(binario):
#     decimal = 0
#     potencia = 0
#     for digito in binario[::-1]:
#         decimal += int(digito) * (2 ** potencia)
#         potencia += 1
#     return decimal

# # Testando:
# print(binario_para_decimal("1011"))   # Deve dar 11
# print(binario_para_decimal("10101"))  # Deve dar 21

# Se ficou dúvida, peça exemplos e teste outros números!





# g. Encontre o maior elemento de um vetor. 
# vetor = [2,4,34,53,63,67,7,47,8,4,7467775,745,7,48,74,8]
# maior_elemento = 0

# for i in range(len(vetor)):
#     if vetor[i] > maior_elemento:
#         maior_elemento = vetor[i]
# print(maior_elemento)


# h. Ordene um vetor númerico


# vet = [1,7,8,4,3,9,10,5,2,6]

# def ordenar(vet):
#     for i in range(len(vet)):
#         for j in range(i+1,len(vet)):
#             if(vet[j] < vet[i]):
#                 vet[j], vet[i] = vet[i], vet[j]
#     return vet

# print(ordenar(vet))


# i. Ordene uma string qualquer: "casario" -> "aaciors"

# def ordena_string(palavra):
#     ascii_ = []
#     ordenada = str()

#     for i in palavra:
#         ascii_.append(ord(i))

#     for i in range(len(ascii_)):
#         for j in range(i+1, len(ascii_)):
#             if ascii_[j] < ascii_[i]:
#                 ascii_[j],ascii_[i] = ascii_[i], ascii_[j]

#     for i in range(len(ascii_)):
#         ordenada += chr(ascii_[i])

#     return ordenada


# print(ordena_string("gustavo"))

# j. Crie uma função que conta quantos digitos tem uma string

# def contagem_string(string):
#     vet = list(string)
#     return len(vet)

# print(contagem_string("gustavo"))

# k. Imprima uma string em ordem crescente, exemplo : "casaco"

# ```
# c
# ca
# cas
# casa
# casac
# casaco
# ```

palavra = list("casaco")
crescente = ""

for i in range(len(palavra)):
    crescente += str(palavra[i])
    print(crescente)


vet = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
crescente = []
for i in range(len(vet)):
    crescente.append(vet[i])
    print(crescente)

for i in range(len(crescente)-1,-1,-1):
    print(crescente)
    crescente.remove(crescente[i])


# l. Crie um validador de senha, considerando que a senha deve ter 8 dígitos, sendo ao menos 3 caracteres maiusculos e três númericos
# m. Uma senha númerica não pode conter sequências de três digitos, determine se a senha é válida:

#     4578218 -> válido

#     4568218 -> inválida (456)

#     4587618-> inválida (876)

#     Neste caso, implemente uma função que recebe três números e determine se estão em sequência.

# n. Determine uma função que recebe um vetor e verifica se o vetor é ordenado (return 1) ou não (return 1). Na função principal, chame a função e avalie o retorno, imprimindo na tela ou não ordenado.


#     

# **OBS**: Para os casos de implementação, reveja também as listas de exercícios.




# novo_registro = [230, 20, 5, 430]

# base_registro = [200, 25, 5, 400, 'P2']

# def distancia(novo, base):
#     soma = 0
#     for i in range(len(novo)):
#             soma += (novo[i] - base[i]) ** 2
#             raiz = soma ** 0.5 

#     return raiz

# print(distancia(novo_registro,base_registro))



