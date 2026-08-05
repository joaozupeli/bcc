# Lista de Exercícios - Recursividade

## 1. Imprimir números de N até 0

# Implemente uma função recursiva que imprime todos os números de `N` até `0`.

# def decrescente(n):
#   if n < 0:
#     return 0
#   print(n)
#   decrescente(n-1)

# print(decrescente(9))
  



# Implemente uma função recursiva que imprime todos os números de `0` até `N`.

# def crescente(n):
#   if n < 0:
#     return 0
#   crescente(n-1)
#   print(n)

# print(crescente(19))

## 3. Soma dos números de N até 0

# Desenvolva uma função recursiva que retorna a soma de todos os números inteiros de `N` até `0`.

# def soma_recursiva(n):
#     if n < 0:
#         return 0
#     return n + soma_recursiva(n - 1)

# print(soma_recursiva(6))


## 4. Soma dos dígitos de um número inteiro

# Crie uma função recursiva que calcula a soma dos dígitos de um número inteiro.

# Exemplo:

4871

# Saída esperada:

20

def soma_digitos(numero):
  if numero == 0:
    return 0
  return (numero % 10) + soma_digitos(numero // 10)


print(soma_digitos(321))


## 5. Soma dos elementos de um vetor

# Implemente uma função recursiva que retorna a soma dos elementos de um vetor de inteiros.



## 6. Fatorial de N

# Escreva uma função recursiva para calcular o fatorial de `N`.

## 7. Sequência de Fibonacci

# Desenvolva uma função recursiva para calcular o `N`-ésimo termo da sequência de Fibonacci.

# Considere:

# fibo(0) = 0
# fibo(1) = 1


## 8. Selection Sort recursivo

# Implemente o algoritmo Selection Sort para ordenar um vetor de inteiros usando recursividade.

