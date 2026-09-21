import socket
import sys

HOST = '127.0.0.1'    # IP do servidor

print('Entre com a porta do servidor')
PORT = int(input())

# AF_INET = IPV4     SOCK_STREAM = TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conexão
try:
    s.connect((HOST, PORT))

except:
   print('# erro de conexao')
   sys.exit()

print('cliente', s.getsockname(), 'conectado com', s.getpeername())

while True:
     print('digite o texto a ser transmitido ou linha vazia para encerrar o programa')
     line = input()
     if not line:
         break

     data = bytes(line, 'utf-8')  # converte string para bytes
     tam = s.send(data)

     print('enviei ', tam, 'bytes')
     print(data)

print('cliente encerrado')