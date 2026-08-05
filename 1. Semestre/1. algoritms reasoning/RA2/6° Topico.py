# Tópico 05 - Exercícios de Fixação - Arrays (Vetores)

# Para estes exercícios, é importante que você não utilize funções built-in do Python, ou seja, aquelas que já vem pré-definidas na linguagem (max, mean, min, sort, etc). O objetivo é praticar a manipulação de vetores 1D em Python utilizando apenas as estruturas de controle, como laços de repetição e estruturas condicionais. Assim você irá aprimorar sua habilidade em programação

# 1. Crie um vetor de 20 elementos aleatórios

import random 

# vetor = []

# for i in range(20):
#   numero = random.randint(0,100)
#   vetor.append(numero)

# print(vetor)


# 2. Crie um vetor de 20 elementos incrementando-os de 5 em 5

# vetor = []
# numero = 0

# for i in range(20):
#   numero += 5
#   vetor.append(numero)

# print(vetor_5)
  

# 3. Crie um vetor contendo N elementos digitados pelo usuário
# n_elementos = int(input("Digite a quantidade de elementos que deseja: "))
# vetor = []

# for i in range(n_elementos):
#   numero_aleatorio = random.randint(0,100)
#   vetor_elementos.append(numero_aleatorio)

# print(vetor_elementos)


# 4. Crie um vetor contendo N elementos pares digitados pelo usuário

# vetor = []
# elementos = int(input(""))

# for i in range(elementos):
#   numero = random.randint(0,100)
#   if numero % 2 == 0:
#     vetor.append(numero)

# print(vetor)



# 5. Para cada posição [i] do vetor, imprima o valor atual, seu antecessor e sucessor

# vetor = [1,2,3,4,5,6,7,8,9,10]

# for i in range(len(vetor) - 1):
#   print(vetor[i])
#   print(vetor[i-1])
#   print(vetor[i+1])

# 6. Apresente a soma dos elementos opostos de um vetor de 100 elementos

vetor  = [927, 128, 563, 405, 812, 194, 347, 681, 529, 372, 856, 411, 238, 975, 604, 159, 783, 314, 489, 652, 911, 47, 835, 203, 674, 136, 589, 442, 981, 715, 308, 627, 182, 754, 497, 219, 876, 531, 394, 668, 117, 843, 265, 932, 581, 422, 749, 163, 905, 378, 546, 712, 284, 968, 631, 191, 475, 824, 359, 737, 246, 891, 513, 105, 693, 437, 808, 271, 954, 618, 329, 775, 462, 148, 862, 597, 225, 992, 481, 317, 728, 175, 946, 642, 385, 761, 258, 921, 572, 418, 831, 112, 688, 502, 364, 796, 292, 963, 615, 341]
tamanho = len(vetor)
soma = []

for i in range(tamanho // 2): # primeiro pego o resto de uma divisao por 2 de um vetor 
    soma.append(vetor[i] + vetor[tamanho - 1 - i]) 

print(soma)
# 7. Compute a média e o desvio padrão de um vetor

# 8. Crie um vetor aleatorio. Posteriormente apresente a soma dos pares e depois dos múltiplos de 5. Também, crie um vetor com os múltiplos de 10 do vetor original.


# 9. Crie dois vetores de 5 elementos cada, e posteriormente crie um terceiro resultante da soma deste dois

# 10. Dado um vetor de 20 elementos, divida este em dois sub-vetores de 10 elementos


# 11. Encontre o maior elemento de um vetor

# 12. Encontre os dois maiores elementos de um vetor

# 13. Dado um vetor, crie um segundo vetor rotulando os indices do primeiro que contem valores acima (-1) e abaixo da média (-1):

# 14. Dado um vetor de 20 elementos, imprima o vetor como se fosse uma piramide:

# 15. Imprima na ordem inversa o exercício 14.

# 16. Contrua e descontrua a pirâmide (dos exercícios 14 e 15)

# 17. Dado um vetor qualquer, apresente os elementos em forma de 'X'.

# 18. Dado um vetor qualquer , apresente este vetor de forma ordenada

#     [5,2,1,3,4] ==> [1,2,3,4,5]

# 19. Maior sequência de '0' em um vetor

#     [1,0,0,1,1,0,1,**0,0,0,0**,1,1,0,0,0] ==> 4

# 20. Maior sequência de um vetor

#     [64,65,12,13,14,15,21,**33,34,35,36,37**,100,91,9,93,94]

#     valores = [33,34,35,36,37]

#     idxs = [7,8,9,10,11]

# 21. Implemente um validador de CPF. Pesquise na internet como o cálculo é realizado

# Strings:

# 21.   A partir de uma frase digitada pelo usuário, determine:

#     a. Quantidade de espaços em branco

#     b. Quantidade de letras maiúsculas

#     c. Quantidade de caracteres especiais

# 22. Faça um algoritmo que converte letra maiúscula em minúscula e vice-versa.

# 23. Validador de Senha

#     a. 10 caractereses

#     b. Não contem números em sequência

#     c. 2 Caracteres Especiais

#     d. 2 Letras maiúsculas

# 24. Código Morse: Converta um string morse (' ', '.', '-') em uma string alpha-númerica

#     
