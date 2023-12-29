import cv2
from wrappers import ImageWrapper
from PySide6.QtNetwork import QTcpSocket, QHostAddress



def main():
    video = cv2.VideoCapture('1.mp4')

    if not video.isOpened():
        video.open(0)

    socket = QTcpSocket()
    socket.connectToHost(QHostAddress('127.0.0.1'), 8080)

    read = True
    num_frames = 0
    topic = "image".encode()

    while read:
        try:
            success, image = video.read()

            if success:
                num_frames += 1
                image = cv2.resize(image, dsize=(0, 0), fx=.5, fy=.5)
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image_wrapper = ImageWrapper()
                image_wrapper.copy_from_cv_image(image_gray, fmt='g')
                msg = topic+image_wrapper.image_pb.SerializeToString()

                socket.write(msg)
                socket.waitForBytesWritten()

        except KeyboardInterrupt:
            print("Interrupt received, stopping...")
            read = False

    video.release()
    socket.close()

if __name__ == "__main__":
    main()