# Tópico 03 - Exercícios de Fixação

### 1. Implemente um seletor de canais para informar que canal a pessoa está assistindo, sendo: -->

def search_channel() :
    canal = int(input("Digite o canal que deseja assistir:"))
    if (canal == 2) :
        return "Você esta assistindo o canal BANDEIRANTES"
    elif (canal == 4) :
        return "Você esta assistindo o canal SBT"
    elif (canal == 6) :
        return "Você esta assistindo o canal CNT"
    elif (canal == 7) :
        return "Você esta assistindo o canal RECORD"
    elif (canal == 9) :
        return "Você esta assistindo o canal CULTURA"
    elif (canal == 12) :
        return "Você esta assistindo o canal GLOBO"
    else:
        return "O numero informado não se refere a um canal válido..."

print (search_channel())

# 2. Um estabelecimento, fornece uma comissão progressiva aos seus vendedores:
#
#     a. 5%, para vendas até R$ 100,00
#     b. 6% para vendas até R$ 500,00
#     c. 7% para vendas até R$ 1000,00
#     d. 8% para vendas acima de R$ 1000,00
#
# Implemente um algoritmo que calcule a comissão do vendedor.

def calcular_comissao() :
    valor_vendido = float(input("Digite o valor da comissao: "))
    if(valor_vendido <= 100) :

        return "O valor de comissão para esse funcionario sera no valor de R$" + str(valor_vendido * 0.05)
    elif(valor_vendido <= 500) :
        return "O valor de comissão para esse funcionario sera no valor de R$" + str(valor_vendido * 0.06)
    elif(valor_vendido <= 1000) :
        return "O valor de comissão para esse funcionario sera no valor de R$" + str(valor_vendido * 0.07)
    elif(valor_vendido > 1000) :
        return "O valor de comissão para esse funcionario sera no valor de R$" + str(valor_vendido * 0.08)
    else:
        return "Valor inválido!"

print(calcular_comissao())

### 3. A partir de três notas de um aluno e informe o conceito a partir da média:

#     <!-- Média de aproveitamento Conceito
#     Entre 9.0 e 10.0                A
#     Entre 7.5 e 9.0                 B
#     Entre 6.0 e 7.5                 C
#     Entre 4.0 e 6.0                 D
#     Entre 4.0 e zero                E

#     Caso, o conceito seja abaixo de C, indique reprovado, caso contrário aprovado. -->

def conceito_nota() :
    nota_aluno = float(input("Digite a nota do aluno: "))
    if (nota_aluno >= 9.0 and nota_aluno <= 10.0 ) :
        return "A | Aluno Aprovado"
    elif (nota_aluno >= 7.5 and nota_aluno <= 9.0 ) :
        return "B | Aluno Aprovado"
    elif (nota_aluno >= 6.0 and nota_aluno <= 7.5 ) :
        return "C | Aluno Reprovado"
    elif (nota_aluno >= 4.0 and nota_aluno <= 6.0 ) :
        return "D | Aluno Reprovado"
    elif (nota_aluno >= 4.0 and nota_aluno <= 0 ) :
        return "E | Aluno Reprovado"
    else :
        return "Nota Inválida! "

print(conceito_nota())

# ### 4. Informe o imposto a recolher de um salário, seguindo a tabela abaixo:

#           Salário             IRPF
#     Até R$1.903,98            Isento
#     De R$1.903,99 até R$2.826,65    7,5%
#     De R$2.826,66 até R$3.751,05    15%
#     De R$3.751,06 até R$4.664,68    22,5%

def calcular_imposto() :
    valor_declarado = float(input("Digite o valor de declarado: "))
    if(valor_declarado < 1.903,98) :
        return "Você esta ausento ao pagamento do imposto de renda"
    elif (valor_declarado >= 1.903,99 and valor_declarado <= 2.826,65):
        return "Voce deve realizar o pagamento de R$", str(valor_declarado * 0.05)
    elif (valor_declarado >= 1.903,99 and valor_declarado <= 2.826,65) :
        return "Você esta ausento ao pagamento do imposto de renda"
    elif (valor_declarado >= 1.903,99 and valor_declarado <= 2.826,65) :
        return "Você esta ausento ao pagamento do imposto de renda"
    elif (valor_declarado >= 1.903,99 and valor_declarado <= 2.826,65) :
        return "Você esta ausento ao pagamento do imposto de renda"
    else:
        return "Valor inválido para definição do IR"

# ### 5. Escreva um programa Python que ordena três números em ordem crescente.

def ordenar_numeros() :
    n1 = int(input("Informe o primeiro numero:"))
    n2 = int(input("Informe o segundo numero:"))
    n3 = int(input("Informe o terceiro numero:"))
    if(n1 > n2 and n1 > n3 and n1 < n3) :
        return n1 , n2 , n3
    elif(n2 > n1 and n2 > n3 and n2 < n1) :
        return n2 , n1 , n3
    elif(n3 > n1 and n3 > n2) :
        return n3 , n1 , n2
    else:
        return n1 , n2 , n3

print(ordenar_numeros())

# ### 6. Escreva um programa Python que simula um jogo de pedra-papel-tesoura entre dois jogadores.

def pedra_papel_tesoura() :
    primeira_jogada = input("Informe a primeira jogada: ")
    segunda_jogada = input("Informe a segunda jogada: ")
    if(primeira_jogada == segunda_jogada) :
        return "Ocorreu Empate...Jogue novamente"
    elif(primeira_jogada == "papel" and segunda_jogada == "pedra") \
        or (primeira_jogada == "tesoura" and segunda_jogada == "papel") \
        or (primeira_jogada == "pedra" and segunda_jogada == "tesoura") :
        return "Jogador A venceu esta rodada"
    else : 
        return "Jogador B venceu esta rodada"

print(pedra_papel_tesoura())

# ### 7. Detetive: Faça um programa que faça 5 perguntas para uma pessoa sobre um crime. As perguntas são:

#     • Telefonou para a vítima? [S/N]
#     • Esteve no local do crime? [S/N]
#     • Mora perto da vítima? [S/N]
#     • Tinha algum dívida com a vítima? [S/N]
#     • Já trabalhou com a vítima? [S/N]

#%%

def crime_answers() :
    perguntas = ["Telefonou para a vítima? [S/N]"
    ,"Esteve no local do crime? [S/N]"
    ," Mora perto da vítima? [S/N]"
    ,"Tinha algum dívida com a vítima? [S/N]"
    ,"Já trabalhou com a vítima? [S/N]"]

    sim = 0
    for pergunta in perguntas:
        if(input(pergunta) == "S") :
            sim += 1

    if(sim == 1):
        return "Inocente"
    elif(sim == 2):
        return "Suspeito"
    elif(sim == (3 or 4)):
        return "Cumplice"
    elif(sim >= 5):
        return "Assassino"
    else :
        return "Inocente"


print(crime_answers())
        


#     O programa deve no final emitir uma classificação sobre a participação da pessoa no crime.
#     Se a pessoa responder positivamente a 2 questões ela deve ser classificada como “Suspeita”.
#     Entre 3 e 4 como “Cúmplice” e 5 como “Assassino“.
#     Caso contrário, ele será classificado como “Inocente“.

# ### 8. Elabore um sistema que recomende o tipo de roupa para um evento:

#     • O evento é profissional ou lazer?
#     • É com amigos ou família?
#     • Faz calor ou frio?
#     • O evento é em uma cachara, cidade ?
#     • O local fechado ou aberto?

#     Baseado nestas respostas, criar uma estrutura de seleção capaz de indicar desde um terno até bermuda e calção.
#     Fique livre para propor mais perguntas ou até mesmo outro sistema de recomendação (viagem, esporte, filme, musica, etc)


# QUESTOES DA SALA 
# CALCULO MEDIA DE 5 NUMEROS COM WHILE
#CALCULO DE MEDIA COM N NUMEROS 


# ENTRE 0 A 100 PARA IMPRIMIR ( NUMEROS PARES ) (INFORMAR SE O NUMERO É PAR OU NAO ) (APRESENTAR A SOMA DOS NUMEROS PARES) ( A SOMA DE TODOS OS MULTIPLOS DE 5)
# i = 0
# soma_p = 0
# soma_i = 0

# while i <= 100 :
#   if(i / 2 == 0):
#       print(str(i) + " Esse numero é par")
#       soma_p += i
#       print(soma_p)
#   else :
#     print(str(i) + " Esse numero é impar")
#     soma_i += i
#     print(soma_i)

  
#   i += 1


#LOGIN UTILIZANDO WHILE PARA LIMITAR O NUMERO DE TENTATIVAS DO USUARIO

# usuario = "zupeli"
# senha = int(0306)
# contador = 0

# login = input("Digite o seu nome de usuario: ")
# password = int(input("Digite a sua senha: "))

# while(login == usuario and password == senha):
#   print("Login suceed")
# else:
#   contador += 1

# if(contador = 5):
#   print("Limite de tentativas excedida")




