import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print('Подключено к {} порт {}'.format(*server_address))
sock.connect(server_address)

for i in range(10):
    mess ="Hello World"
    print(f'Отправка: {mess}')
    message = mess.encode()
    sock.sendall(message)
    time.sleep(1)
    