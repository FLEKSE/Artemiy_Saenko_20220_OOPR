import cv2
import sys
from wrappers import ImageWrapper
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtNetwork import QTcpServer, QHostAddress
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout, QWidget)
import socket


class Thread(QThread):
    updateFrame = Signal(QImage)
    def __init__(self, socket, parent=None):
        QThread.__init__(self, parent)
        self.trained_file = None
        self.status = True
        self.cap = True
        self.socket = socket

    def run(self):
        g_run = True
        num_frames = 0
        topic = "image"
        len_topic = len(topic.encode())

        image_wrapper = ImageWrapper()

        while g_run:
            try:
                data = self.socket.recv()
                image_bytes = data[len_topic:]
                image_wrapper.image_pb.ParseFromString(image_bytes)

                success, image = image_wrapper.get_open_cv_image()
                if success:
                    num_frames += 1
                    
                    color_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    h, w, ch = color_frame.shape
                    img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
                    scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)

                    self.updateFrame.emit(scaled_img)
                    print(f"Image number {num_frames}")
                    key = cv2.waitKey(1)
                    if key == 'q':
                        g_run = False

            except KeyboardInterrupt:
                print("Interrupt received, stopping...")
                g_run = False



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Server")
        self.setGeometry(0, 0, 800, 500)
        self.server = QTcpServer(self)
        self.server.listen(QHostAddress('127.0.0.1'), 8080)
        self.server.newConnection.connect(self.handle_new_connection)
        

        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)
        
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)
        
        
        buttons_layout = QHBoxLayout()
        self.button1 = QPushButton("Start")
        self.button1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.button1)
        
        self.button1.clicked.connect(self.start)
        
        right_layout = QHBoxLayout()
        right_layout.addLayout(buttons_layout, 1)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(right_layout)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    @Slot()
    def start(self):
        print("Starting...")
        self.button1.setEnabled(False)
        self.th.start()
        
    @Slot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        
    @Slot()
    def handle_new_connection(self):
        socket = self.server.nextPendingConnection()
        self.th = Thread(self, socket)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)
        

    

if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())