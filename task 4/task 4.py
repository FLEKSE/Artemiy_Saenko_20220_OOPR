from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import cv2
import numpy as np
import socket
from PySide6.QtNetwork import QTcpServer,QHostAddress

class VideoServer(QTcpServer):
    def init(self, parent=None):
        super().init(parent)
        self.new_connection.connect(self.handle_client)

    def handle_client(self):
        client_socket = self.nextPendingConnection()
        while True:
            frame=cap.read()
            if frame is None:
                break
            # display the frame in a widget

class VideoClient:
    def init(self, server_address, video_path):
        self.server_address = server_address
        self.video_path = video_path

    def send_video(self):
        cap = cv2.VideoCapture(self.video_path)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.server_address)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # send the frame to the server using client_socket
        cap.release()
        client_socket.close()

if __name__ == "__main__":
    app = QApplication([])
    server = VideoServer()
    server.listen(QHostAddress.Any, 1234)

    client = VideoClient(("localhost", 1234), "path_to_video_file")
    client.send_video()

    app.exec_()