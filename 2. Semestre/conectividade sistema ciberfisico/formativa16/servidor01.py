import socket
import sys

def mostraip():
    hostname = socket.gethostname()
    hostip = socket.gethostbyname(hostname)
    print('host: {} ip: {}'.format(hostname, hostip))

# -------------------------------------------------
HOST = '127.0.0.1'  # localhost = esta máquina
# HOST = 'XXX.XXX.XXX.XXX'  VER COM IPCONFIG
PORT = 9999         # portas abaixo de 1023 exigem permissão de root

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except:
   print('# erro de bind')
   sys.exit()
s.listen(5)

mostraip()
print('Digite algo para terminar')
input()
