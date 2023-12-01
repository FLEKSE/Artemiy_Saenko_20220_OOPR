import socket
import time
import pickle


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('localhost', 10000) 
print('Подключено к {} порт {}'.format(*server_address))
sock.connect(server_address)

for i in range(10):

    mess = 'Hello, world!'
    print(f'Отправка: {mess}')
    with open('3_2_client.pickle', 'wb') as f:
        pickle.dump(mess, f)
    with open('3_2_client.pickle', 'rb') as f:
        sock.sendall(f.read())
    
    time.sleep(1)

