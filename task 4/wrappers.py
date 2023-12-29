import video_pb2
import numpy as np


class ImageWrapper(object):
    def __init__(self, input_image=None):
        self.image_pb = video_pb2.Image()

    def copy_from_cv_image(self, input_image, timestamp=0, fmt='bgr'):

        self.image_pb.timestamp = timestamp

        shape = input_image.shape

        self.image_pb.cols = shape[1]
        self.image_pb.rows = shape[0]
        if len(shape) > 2:
            self.image_pb.channels = shape[2]
        else:
            self.image_pb.channels = 1

        self.image_pb.format = fmt

        self.image_pb.image_bytes = input_image.tobytes()
        
    def get_open_cv_image(self):
        if self.image_pb.IsInitialized():
            image_cv = np.fromstring(self.image_pb.image_bytes, dtype='uint8')
            image_cv = np.reshape(image_cv, (self.image_pb.rows, self.image_pb.cols, self.image_pb.channels))
            return True, image_cv
        else:
            return False, None