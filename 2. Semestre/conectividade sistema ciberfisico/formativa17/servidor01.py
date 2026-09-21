import socket
import sys

HOST = '127.0.0.1'
PORTA = int(input('Entre com a porta do servidor: '))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.bind((HOST, PORTA))
except:
   print('# erro de bind')
   sys.exit()

while True:
   data, addr = s.recvfrom(1024)
   print('cliente ', addr, 'enviou ', data)
   if not data:
       break

print('o servidor encerrou')
s.close()
