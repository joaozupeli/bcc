import socket
import sys

HOST = '127.0.0.1'  # localhost = esta máquina

print('Entre com a porta do servidor')
PORT = int(input())

# AF_INET = IPV4     SOCK_STREAM = TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conexão
try:
    s.bind((HOST, PORT))
except:
   print('# erro de bind')
   sys.exit()

s.listen(5)


##########################################################
########    Tratar conexoes - INICIO    ##################
##########################################################
while True:
    #---------------------------------------------
    # aguardar e iniciar conexao
    print('aguardando conexoes em ', PORT)
    conn, addr = s.accept()
    print('iniciando conexao com ', addr)

    ##################################################################
    #########   Tratar de dados recebidos - INICIO   #################
    ##################################################################
    while True:
        # recebe dados do cliente
        data = conn.recv(1024)
        print('recebi ', len(data), ' bytes de', addr)

        # controle para encerrar tratamento de dados recebidos
        # se cliente enviar linha vazia encerra tratamento de dados recebidos
        if not data:
            break       # linha vazia
        print(data)

    # encerrar conexao
    print('encerrando conexao em ', addr)
    conn.close()

    ##################################################################
    #########     Tratar de dados recebidos - FIM    #################
    ##################################################################

##########################################################
########      Tratar conexoes - FIM     ##################
##########################################################


print('servidor encerrado')