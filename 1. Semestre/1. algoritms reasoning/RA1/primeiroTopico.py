# Tópico 01 - Exercícios de Fixação

### 1 - Calcule a soma de dois números

def sum( a , b) :
    a = input("Digite o valor do primeiro numero: " )
    a = int(a)
    b = input("Digite o valor do segundo numero: " )
    b = int(b)
    return a + b;

print ("A soma desses 2 numeros e igual a ", sum(200,200))

### 2 - Calcule o antecessor e o sucessor de um número
def antNumber(numero):
    return numero - 1;


print("O proximo numero e ", antNumber(100))

def proxNumber(numero) :
        return numero + 1;

print ("O proximo numero e ", proxNumber(100))

### 3 - Calcular o troco de uma compra

def troco( valorCompra, valorPago) :
    return valorPago - valorCompra;

print ("O Troco da sua compra e igual a ", troco(200,400))

### 4 - Calcule a gorjeta de um garçom (10%)

def gorjeta(valorConta) :
    valorConta = int(input("Digite o valor da conta: " ))
    return (valorConta / 100) * 10;

print("A gorjeta do garcom e equivalente a ",gorjeta(234))

### 5 - Calcule a metragem quadrada de uma área qualquer (casa, terreno, quarto, sala, etc)
def calcularMetragem(largura, comprimento) :
    largura = int(input("Digite o largura da area: " ))
    comprimento = int(input("Digite o comprimento da area: " ))
    return largura * comprimento;

print("A metragem quadrada da area e igual a", calcularMetragem(20, 40))

### 6 - Calcule a metragem quadrada de uma casa com 3 pavimentos

def calcularMetragemPavimentos(l1,l2,l3,c1,c2,c3) :
    return l1 * c1 + l2 * c2 + l3 * c3;

print ("A metragem de todos os pavimentos é", calcularMetragemPavimentos(20,20,20,40,40,40))

### 7 - Calcule a média de idade de 5 pessoas

def calcularMediaIdade(idade1, idade2, idade3, idade4, idade5) :
    return (idade1 + idade2 + idade3 + idade4 + idade5) // 5;

print("A media de idade dessas 5 pessoas são", calcularMediaIdade(23,26,28,29,20))

### 8 - Calcule a idade a partir do ano de nascimento
anoAtual = 2026
## Generalização dos Exercícios #4 e #5

## 9 - Calcular a gorjeta de N%

def gorjeta(valorConta, porcentagem) :
    return (valorConta / 100) * porcentagem;

print("Estou calculando a gorjeta dinamica", gorjeta(234, 25))

## 10 - Calcule a metragem quadrada de uma casa com N pavimentos

def calcularMetragemPavimentoDinamico(largura, comprimento, pavimentos) :
    while pavimentos > 0:
        return largura * comprimento * pavimentos;

print ("A metragem de todos os pavimentos é", calcularMetragemPavimentoDinamico(20,40,7))