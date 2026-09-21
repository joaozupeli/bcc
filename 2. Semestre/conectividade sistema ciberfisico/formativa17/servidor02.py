import socket
import sys

HOST = input('Entre com o IP do servidor: ')
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