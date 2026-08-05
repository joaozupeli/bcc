## TRABALHO SISTEMA DE UM BANCO - BY: @GustavoVilela - @JoãoZupeli - @JoãoBaby - @VicenteKolrooss

import pickle
import os
from datetime import datetime
import time

db = "4. bank system/database.pkl"

gerente = {
  "login": "admin",
  "senha": "123"
}

tentativa = 0
tempo_bloqueio = 0

if not os.path.exists(db):
    with open(db, 'wb') as f:
        dados = pickle.dump({}, f)
else:
    try:
        with open(db, 'rb') as f:
            dados = pickle.load(f)
        if not isinstance(dados, dict):
            raise ValueError("Banco de dados não é um dicionário!")
    except Exception:
        with open(db, 'wb') as f:
            dados = pickle.dump({}, f)

print ("Bem-vindo ao sistema bancario")

while True:

  escolha = input("Selecione uma opcao:\n1 - Cliente\n2 - Gerente\n3 - Salvar alteracoes em disco\n0 - Sair\n")

## ------------ MODO CLIENTE ------------ ##
  
  if escolha == "1": 
    login_cliente = input("Informe o login:\t")

    while True:
      
      if login_cliente not in dados:
          print("Cliente não encontrado!")
          break
      else:
        print(f"\nBem-vindo(a), {login_cliente}!")
        nome_cliente = login_cliente
        
        cliente_opcoes = input("Selecione uma opcao:\n1 - Consultar saldo\n2 - Depositar valor\n3 - Sacar valor\n4 - Simular rendimento\n5 - Listar ultimas transacoes (extrato)\n0 - Sair\n")
        
        if cliente_opcoes == "1": 
          print(f"\nSaldo atual: R$ {dados[nome_cliente]['saldo']:.2f}\n")
          
        elif cliente_opcoes == "2":
            valor_deposito = float(input("Informe o valor a ser depositado: "))
            if valor_deposito > 0:
                  dados[nome_cliente]['saldo'] += valor_deposito
                  data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                  dados[nome_cliente]['extrato'].append(f"{data_hora} - Deposito: R$ {valor_deposito:.2f}")
                  
                  print("Depósito realizado com sucesso!")
            else:
                  print("Valor de depósito inválido.")
        elif cliente_opcoes == "3":
          valor_saque = float(input("Informe o valor a ser sacado: "))
          if 0 < valor_saque <= dados[nome_cliente]['saldo']:
              dados[nome_cliente]['saldo'] -= valor_saque
              data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
              dados[nome_cliente]['extrato'].append(f"{data_hora} - Saque: R$ {valor_saque:.2f}")
              print("Saque realizado com sucesso!")
          elif valor_saque <= 0 or valor_saque > dados[nome_cliente]['saldo']:
              print("Saldo insuficiente ou valor inválido.")
          
        elif cliente_opcoes == "4":
          print("SIMULAÇÃO DE RENDIMENTO (JUROS SIMPLES)\nPeríodo: 12 meses | Taxa: 1,1% ao mês\n")
          
          entrada = input("Informe o valor que você quer simular o investimento:\n")
          valor_inv = float(entrada)
          saldo_atual = dados[nome_cliente]['saldo']

          if valor_inv <= saldo_atual:
              taxa = 0.011
              rendimento_mensal = valor_inv * taxa
              
              print(f"{'Mês'} | {'Rendimento'} | {'Montante'}")
              print("-" * 35)
              
              for mes in range(1, 13):
                  lucro_total = valor_inv + (rendimento_mensal * mes)
                  print(f"{mes} | R$ {rendimento_mensal:.2f} | R$ {lucro_total:.2f}")
                  
              lucro_total = rendimento_mensal * 12
              print("-" * 35)
              print(f"Rendimento total: R$ {lucro_total:.2f}")
              print(f"Total final: R$ {valor_inv + lucro_total:.2f}")
          else:
              print("Erro: Saldo insuficiente.")
                
        elif cliente_opcoes == "5":
          print("--- EXTRATO ---")
          for transacao in dados[nome_cliente]['extrato']:
            print(transacao)

        elif cliente_opcoes == "0":
          with open(db, 'wb') as f:
            pickle.dump(dados, f)
          break
        
        else:
          print("Opcao invalida")

## ------------ MODO GERENTE ------------ ##

  elif escolha == "2":

    if tempo_bloqueio > time.time():
       restante = int(tempo_bloqueio - time.time())
       print(f"Espere mais {restante} segundos para tentar novamente")

    else:
      login_gerente = input("Informe o login:\t")
      senha_gerente = input("Informe a senha:\t")

      while login_gerente != gerente["login"] or senha_gerente != gerente["senha"]:
        print("Senha incorreta")
        login_gerente = input("Informe o login:\t")
        senha_gerente = input("Informe a senha:\t")
        tentativa += 1

        if tentativa == 3:
          print("Senha inválida...\tTente Novamente mais tarde")
          tempo_bloqueio = time.time() + 15
          tentativa = 0
          break
        
      if login_gerente == gerente["login"] and senha_gerente == gerente["senha"]:
        print("Login bem-sucedido!")

        while True:
          gerente_opcoes = input("Selecione uma opcao:\n1 - Cadastrar ou alterar o nome de um cliente\n2 - Corrigir Saldo\n3 - Consultar Dados de um Cliente\n4 - Listar ultimas transacoes (extrato)\n0 - Sair\n")
          
          if gerente_opcoes == "1":
              nome_cliente = input("Informe o nome do cliente:\t")

              if nome_cliente not in dados:

                print("Cliente ainda não existente! Cadastrando novo cliente...")
                nome_cliente = input("Informe o nome do cliente a ser cadastrado:\t")
                dados[nome_cliente] = {
                    "nome": nome_cliente,
                    "saldo": 0,
                    "extrato": [] 
                }
                print(f"Cliente {nome_cliente} cadastrado com sucesso!")
              else:
                print(f"Cliente {nome_cliente} encontrado!")
                novo_nome = input("Informe o novo nome do cliente:\t")
                dados[novo_nome] = dados.pop(nome_cliente)
                dados[novo_nome]['nome'] = novo_nome
                with open(db, 'wb') as f:
                  pickle.dump(dados, f)
                print(f"Cliente {nome_cliente} alterado para {novo_nome} com sucesso!")
                  
          elif gerente_opcoes == "2":
            nome_cliente = input("Informe o nome do cliente:\t")
            if nome_cliente not in dados:
              print("Cliente não encontrado!")
              break
            else:
              print(f"Cliente {nome_cliente} encontrado!")
              saldo_cliente = float(input("Informe o novo saldo do cliente:\t"))
              dados[nome_cliente]['saldo'] = saldo_cliente
              dados[nome_cliente]['extrato'].append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Correção de Saldo: R$ {saldo_cliente:.2f}")

              print(f"Saldo do cliente {nome_cliente} alterado com sucesso!")
          elif gerente_opcoes == "3":
            nome_cliente = input("Informe o nome do cliente a ser consultado:\t")
            if nome_cliente not in dados:
              print("Cliente não encontrado! Cadastre-o antes de consultá-lo.")
              break
            else:
              print(f"Cliente {nome_cliente} encontrado!")
              print(f"Saldo: {dados[nome_cliente]['saldo']}")

          elif gerente_opcoes == "4":
            nome_cliente = input("Informe o nome do cliente:\t")
            if nome_cliente not in dados:
              print("Cliente não encontrado! Cadastre-o antes de listar o extrato.")
              break
            else:
              print("--- EXTRATO ---")
              for i in dados[nome_cliente]['extrato']:
                print(i)
            
          elif gerente_opcoes == "0":
              with open(db, 'wb') as f:
                pickle.dump(dados, f)
              break
          else:
              print("Opcao inválida")

## ------------ SALVAR OS DADOS, GARANTINDO A PERSISTÊNCIA DOS DADOS ------------ ##

  elif escolha == "3": 
    salvar_alteracoes = input("Deseja salvar as alteracoes em disco? (s/n)")
    if salvar_alteracoes == "s":
      with open(db, 'wb') as f:
        pickle.dump(dados, f)
      print("Alteracoes salvas com sucesso")
    else:
      print("Alteracoes nao salvas")
  elif escolha == "0": ## SAIR
    with open(db, 'wb') as f:
        pickle.dump(dados, f)
    break
  else:
    print("Opcao invalida")
