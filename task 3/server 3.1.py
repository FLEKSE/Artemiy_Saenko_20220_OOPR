import socket

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
            data = connection.recv(16)
            print(f'Получено: {data.decode()}')
            if data:
                print('Обработка данных...')
            else:
                print('Нет данных от:', client_address)
                break

    finally:
        pass
    