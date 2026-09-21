import socket
import sys

HOST = '127.0.0.1'  # localhost = esta máquina

print('Entre com a porta do servidor')
# recebe do usuario a porta do servidor
# precisa ser convertida de string para inteiro

PORT = int(input())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except Exception as e:
   print('# erro de bind')
   print(e)
   sys.exit()

s.listen(5)

# Tratamento de conexão
print('aguardando conexao na porta ', PORT)
conn, addr = s.accept()
print('recebi uma conexao de ', addr)

print('encerrar conexao conexao com', addr)
conn.close()