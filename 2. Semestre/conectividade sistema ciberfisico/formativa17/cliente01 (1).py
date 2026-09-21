import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
   IP = input('Entre com o IP de destino: ')
   PORTA = int(input('Entre com a PORTA de destino: '))
   msg = input('Entre com a mensagem: ')
   print(msg.encode())

   s.sendto(msg.encode(), (IP, PORTA))

print('Cliente encerrou')
s.close()