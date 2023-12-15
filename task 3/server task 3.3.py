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
