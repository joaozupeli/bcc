# Tópico 02 - Exercícios de Fixação

### 1. Informe se uma pessoa tem o mesmo nome que você

def mesmo_nome(nome, nomePessoa) :
    return nome == nomePessoa

print (mesmo_nome("Joao", "Joao"))

### 2. Informe se a pessoa digitou uma vogal ou consoante

def vogal_consoante() :
    vogais = ["A", "E", "I", "O", "U"]
    consoantes = ["B", "C", "D", "F", "G", "H", "J", "K", ]
    caractere_digitado = input("Informe uma caractere: ")
    if(caractere_digitado in vogais) :
        return "O caractere digitado e uma vogal", caractere_digitado
    elif(caractere_digitado in consoantes) :
        return "O caractere digitado e uma consoante", caractere_digitado

print (vogal_consoante())


### 3. Informe o dia da semana a partir de um número entre 1 e 7. Exemplo, 1- Domingo, 2- Segunda etc. Se digitar outro valor deve aparecer “valor inválido”)

def discover_day() :
    diaSemana = int(input("Informe o dia da semana :"))
    if(diaSemana == 1) :
        return "Segunda"
    elif(diaSemana == 2) :
        return "Terca"
    elif(diaSemana == 3) :
        return "Quarta"
    elif(diaSemana == 4) :
        return "Quinta"
    elif(diaSemana == 5) :
        return "Sexta"
    elif(diaSemana == 6) :
        return "Sabado"
    elif(diaSemana == 7) :
        return "Domingo"
    elif (diaSemana > 7) :
        return "Valor Invalido, o valor que esta inserindo nao se refere a um dia da semana"

print(discover_day())

### 4. Informe o maior número entre dois números quaisquer

def high_number() :
    n1 = int(input("Informe o primeiro numero:"))
    n2 = int(input("Informe o segundo numero:"))
    if(n1 > n2) :
        return n1
    elif(n1 < n2) :
        return n2

print(high_number())

### 5. Informe o maior número e o menor número entre dois números quaisquer

def high_low_number() :
    n1 = int(input("Informe o primeiro numero:"))
    n2 = int(input("Informe o segundo numero:"))
    if(n1 > n2) :
        return "O maior numero e"
    elif(n1 < n2) :
        return n2

print(high_low_number())

### 6. Informe se um ano é bissexto ou não.

### 7. Informe se um número é par (Use o módulo da divisão (%))

def numero_par() :
    n1 = int(input("Informe o numero:"))
    if(n1 % 2 == 0) :
        return "Numero Par"
    else :
        return "Numero Impar"

print(numero_par())

    # ### 8. Informe se um número é múltiplo de um número N qualquer

def multiple_number() :
    n1 = int(input("Informe o numero:"))
    if( n1 % 2 == 0) :
        return "Numero Multiplo"
    else:
        return "Numero Näo Multiplo"

print(multiple_number())



### 9. A partir de três notas de um aluno e informe se ele passou por média (7.0 ou mais)

def depurador_nota() :
    n1 = float(input("Informe o primeira nota desse aluno:"))
    n2 = float(input("Informe o segundo nota desse aluno:"))
    n3 = float(input("Informe a terceira nota desse aluno:"))

    if((n1 + n2 + n3) / 3 >= 7.0) :
        return "Aprovado"
    else:
        return "Reprovado"



### 10. Verifique entre duas pessoas quem tem o maior nome e a mais velha. (DICA, use a função len())

        # tam = len(“Eduardo Silva”) #tam = 13
        # tam = len(“Fabio Costa”) #tam = 11

### 11. Peça o login e senha de uma pessoa e informe se o login é valido.

def login() :
    usuario = str(input("Informe o usuario:"))
    senha = str(input("Informe o senha:"))
    if(usuario == 'JOAOZUPELI' and senha == '0306') :
        return "Usuario logado com sucesso."
    else :
        return "Credenciais Invalidas"

print (login())


### 12. Informe se uma pessoa tem idade para votar a partir de seu ano de nascimento

def pode_votar() :
    anoAtual = 2026
    anoNascimento = int(input("Informe o ano de nascimento :"))
    if(anoAtual - anoNascimento >= 16) :
        return "Voce esta apto ao voto, porque tem ", anoAtual - anoNascimento ,"Anos"
    else :
        return "Voce nao pode votar porque ainda tem", anoAtual - anoNascimento ,"Anos"

print (pode_votar())


### 13. Informe se uma pessoa pode doar sangue (entre 18 e 59 anos)

def give_blood() :
    anoAtual = 2026
    anoNascimento = int(input("Informe o ano de nascimento :"))
    idade = anoAtual - anoNascimento
    if (idade >= 18 or idade <= 89) :
        return "Essa Pessoa pode doar sangue..."
    else :
        return "Essa pessoa nao pode doar sangue..."

print(give_blood())



### 14. As maçãs custam 0,30 cada se forem compradas menos do que uma dúzia, e 0,25 se forem compradas pelo menos doze. Escreva um programa que leia o número de maçãs compradas, calcule e escreva o valor total da compra