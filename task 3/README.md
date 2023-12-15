# Artemiy_Saenko_20220_OOPR

Task_3: TCP Client-streaming (Клиент, например, раз в 1 секунду отправляет данные на сервер), используя встроенный в Python модуль socket. Task_3_1_server.py Task_3_1_client.py Используя encode() и decode() Task_3_2_server.py Task_3_2_client.py Используя pickle - де/сериализация произвольных объектов. Task_3_3_server.py Task_3_3_client.py Используя Google Protocol Buffers - де/сериализация определенных структурированных данных, а не произвольных объектов Python

Task_3_1_client.py

```python
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
```

![client 3.1](https://github.com/FLEKSE/Artemiy_Saenko_20220_OOPR/blob/main/task%203/img/client%203.1.png)

Task_3_1_server.py

```python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print('Подключено к {} порт {}'.format(*server_address))
sock.connect(server_address)

while True:
    mess ="Hello World"
    print(f'Отправка: {mess}')
    message = mess.encode()
    sock.sendall(message)
    time.sleep(1)
```

![server 3.1](https://github.com/FLEKSE/Artemiy_Saenko_20220_OOPR/blob/main/task%203/img/server%203.1.png)

Task_3_2_server.py Task_3_2_client.py Используя pickle - де/сериализация произвольных объектов.

Task_3_2_client.py

```python
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
```

![client 3.2](https://github.com/FLEKSE/Artemiy_Saenko_20220_OOPR/blob/main/task%203/img/client%203.2.png)

Task_3_2_server.py

```python
import socket
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

sock.listen()

while True:
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    try:
        print('Подключено к:', client_address)
        while True:
            data = connection.recv(4096)
            with open('3_2_server.pickle', 'wb') as f:
                f.write(data)
            with open('3_2_server.pickle', 'rb') as f:
                data = pickle.load(f)
            
            print(f'Получено: {data}')
            if data:
                print('Обработка данных...')
            else:
                print('Нет данных от:', client_address)
                break

    finally:
        pass
```

![server 3.2](https://github.com/FLEKSE/Artemiy_Saenko_20220_OOPR/blob/main/task%203/img/server%203.2.png)

Task_3_3_server.py Task_3_3_client.py Используя Google Protocol Buffers - де/сериализация определенных структурированных данных, а не произвольных объектов Python
Task_3_3_client.py
```python
import temp_pb2
import socket
import time
import sys

HOST = '127.0.0.1'
PORT = 8888
s = None

temp = temp_pb2.TempEvent()

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

with s:
    while True:
        temp.device_id = 1
        temp.event_id = 2
        temp.humidity = 3
        temp.video_data = 4
        s.sendall(temp.SerializeToString())
        print("отправлено: \n",temp)
        time.sleep(1)    
 

```
![client 3.3](https://github.com/FLEKSE/Artemiy_Saenko_20220_OOPR/blob/main/task%203/img/client%203.3.png)
Task_3_3_server.py
```python
import socket
import temp_pb2
import sys

HOST = "127.0.0.1"
PORT = 8888
s = None

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except OSError as msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

conn, addr = s.accept()
temp = temp_pb2.TempEvent()

with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024) 
        temp.ParseFromString(data)
        print(temp.device_id, 
        temp.event_id,
        temp.humidity,
        temp.video_data)

```
![server 3.3](https://github.com/FLEKSE/Artemiy_Saenko_20220_OOPR/blob/main/task%203/img/server%203.3.png)