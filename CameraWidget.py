###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from datetime import datetime
import cv2
import imutils
import os


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, link):
        super().__init__()
        self.link = link
        self.run_flag = True

    def run(self):
        cap = cv2.VideoCapture(self.link, cv2.CAP_DSHOW)  # capture from web cam
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        while self.run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()  # shut down capture system

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.run_flag = False
        self.wait()


class CameraWidget(QWidget):
    frame_counter_signal = pyqtSignal(bool)
    update_image_list_signal = pyqtSignal(bool)

    def __init__(self, parent, stream_link=0, aspect_ratio=False):
        super(CameraWidget, self).__init__(parent)
        self.main_state = 0
        self.frame_counter = 0
        self.saved_img_counter = 0
        self.image_features = []

        self.screen_width = self.parent().size().width() // 2
        self.screen_height = self.parent().size().height() // 2

        self.maintain_aspect_ratio = aspect_ratio
        self.camera_stream_link = stream_link
        self.cam_name = 'cam' + str(self.camera_stream_link + 1)
        time_folder = datetime.now().strftime('%d_%H-%M') + '/'
        os.makedirs('captured/' + time_folder + self.cam_name, exist_ok=True)
        self.output_dir = os.path.join(os.getcwd(), 'captured/' + time_folder, self.cam_name, '')

        self.imageLabel = QLabel(self)  # create the label that holds the image

        self.thread = VideoThread(self.camera_stream_link)  # create the video capture thread
        self.thread.change_pixmap_signal.connect(self.UpdateImage)

    @pyqtSlot(np.ndarray)
    def UpdateImage(self, cv_img):
        self.frame = cv_img.copy()
        qt_img = self.toQPix(cv_img)
        self.imageLabel.setPixmap(qt_img)
        if not self.thread.run_flag:
            self.imageLabel.clear()
            self.imageLabel.repaint()

    def toQPix(self, frame):
        """Convert from an opencv image to QPixmap"""
        self.screen_width = self.parent().size().width() // 2
        self.screen_height = self.parent().size().height() // 2

        # Keep frame aspect ratio
        if self.maintain_aspect_ratio:
            frame = imutils.resize(frame, width=self.screen_width)
        # Force resize
        else:
            frame = cv2.resize(frame, (self.screen_width, self.screen_height))

        # Add timestamp to cameras
        cv2.rectangle(frame, (self.screen_width - 115, 25), (self.screen_width, 50), color=(0, 0, 0), thickness=-1)
        cv2.putText(frame, datetime.now().strftime('%H:%M:%S'), (self.screen_width - 110, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), lineType=cv2.LINE_AA)

        # Convert to pixmap and set to video frame
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(img)

    def get_image_label(self):
        return self.imageLabel

    def get_image(self):
        return self.frame

    def get_cam_name(self):
        return self.cam_name
