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
    input('Tecle algo para continuar: ')
    try:
        data, addr = s.recvfrom(10)
    except Exception as e:
        print('# Exeption no recvfrom ', e)
    else:
        print('cliente ', addr, 'enviou ', data)
        if not data:
            break

print('o servidor encerrou')
s.close()

