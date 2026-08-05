# # Tópico 04 - Exercícios de Fixação

# ### 1. Escreva um programa que exiba os múltiplos de 3 de 0 a 100.

def multiplos_de_3() :
    for i in range(0, 100) :
        if(i % 3 == 0) :
            print(i)

print(multiplos_de_3())

# # ### 2. Escreva um programa que faça a contagem regressiva de 10 a 0.

def contagem_regressiva() :
  for i in range(10,0) :
    print(i)

print(contagem_regressiva())

# # ### 3. Escreva um programa que calcule a soma dos números ímpares de 1 a 100.

def soma_impar() :
  for i in range(0,100):
    if(i % 2 != 0) :
      print(i + i)

print(soma_impar())


# # ### 4. Escreva um programa que gere um número aleatório entre 1 e 100 e peça para o usuário adivinhá-lo.
import random

def adivinhar_numero() :
    chute = int(input("Me diga o número que será impresso ?"))
    numero_aleatorio = random.randint(1, 100)
    if(chute == numero_aleatorio) :
        print("Você acertou!")
    else:
        print("Você errou!")

print(adivinhar_numero())

# ### 5. Escreva um programa que peça um número inteiro e exiba a sua tabuada de multiplicação de 1 a 10.

def number_mult():
  numero_solicitado = int(input("Digite um número para visualizar a sua tabuada: "))
  for i in range(1,10):
    print(numero_solicitado * i)

print(number_mult())

# ### 6. Escreva um programa que solicite um número inteiro e calcule a soma de seus dígitos.

def number_int() :
  numero = int(input("Digite um numero inteiro: "))
  soma = 0
  while numero > 0:
    soma += numero % 10
    numero //= 10 # //= esse sinal apenas tenta entendender se exite 10 ainda  dentro e numero ou tambem eu poderia ver se numero ainda é divisiel por 10
  return soma


print(number_int())

### 7. Escreva um programa que imprima os n primeiros números da sequência de Fibonacci.

# contador = 2
# a = 0
# b = 1
# n = int(input("Digite a quantidade de numeros da sequencia de Fibonacci: "))

# while contador < n:
#   c = a + b 
#   print(c)
#   a = b
#   b = c

#   contador += 1



### 8. Escreva um programa que solicite um número inteiro e informe se ele é primo ou não.

eh_primo = "Esse numero é primo"
primo = int(input("Digite o numero para saber se ele é primo ou nao: "))
div = primo - 1

while div > 1:
  if(primo % div == 0):
    eh_primo = "Esse numero não é primo"
    div -= 1
    break

print(eh_primo)

### 9. Escreva um programa que exiba uma tabela de conversão de graus Celsius para Fahrenheit, de -10 até 100 celsius.

### 10. Escreva um programa que gere um número aleatório entre 1 e 100 e peça para o usuário adivinhá-lo em até 5 tentativas. (Dê dicas de se está proximo ou não (quente e frio))

### 11. Você deve implementar um sistema de votação. A eleição deve ser decidida entre dois candidatos:

# - "Joao da Silva - 28765"
# - "Carlos Alberto - 32928"

# Faça um algoritmo que fique computando os votos até que a opção "ENCERRAR" seja digitada.
# Apresente também a opção de mostrar resultados parciais.





