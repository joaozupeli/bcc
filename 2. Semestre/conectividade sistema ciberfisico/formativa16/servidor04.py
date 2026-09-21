
import socket
import sys
import time

HOST = '127.0.0.1'  # localhost = esta máquina

print('Entre com a porta do servidor')
PORT = int(input())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    #----------------------------------------------
    # parar o servidor por n_segundos
    n_segundos = 10
    print('parar o servidor por ', n_segundos, 'segundos')
    time.sleep(n_segundos)

    #----------------------------------------------
    # encerrar conexao
    print('encerrando conexao em ', addr)
    conn.close()


##########################################################
########      Tratar conexoes - FIM     ##################
##########################################################

# Sair e encerrar servidor
print('servidor encerrado')