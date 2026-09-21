import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

IP = input('Entre com o IP de destino: ')
PORTA = int(input('Entre com a PORTA de destino: '))
while True:
   msg = input('Entre com a mensagem: ')
   print(msg.encode())

   s.sendto(msg.encode(), (IP, PORTA))

print('Cliente encerrou')
s.close()