###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime
import numpy as np
import mediapipe as mp
from BodyPoseDraw import *
import time
import cv2
import imutils
import ntpath
import json


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.path = None
        self.name = None


    def set_video_path(self, path):
        self.path = path
        self.name = ntpath.basename(path).split('.')[0]
        print(self.name)
        self.frame_counter = 0

    def run(self):
        cap = cv2.VideoCapture(self.path)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        while cap.isOpened():
            success, cv_img = cap.read()
            if not success:
                break

            self.change_pixmap_signal.emit(cv_img)
            self.spin(0.0333)
        cap.release()  # shut down capture system
        print('End of Video')
        self.wait()

    def stop(self):
        """Waits for thread to finish"""
        self.wait()


    def spin(self, seconds):
        """Pause for set amount of seconds, replaces time.sleep so program doesnt stall"""
        time_end = time.time() + seconds
        while time.time() < time_end:
            QApplication.processEvents()


class VideoWidget(QWidget):
    frame_counter_signal = pyqtSignal(bool)
    update_image_list_signal = pyqtSignal(bool)

    def __init__(self, parent, aspect_ratio=False):
        super(VideoWidget, self).__init__(parent)
        self.frame_counter = 0
        self.metadata = None
        self.landmarks_dataset = None
        self.frame_counter = 0
        self.calibration_data = {}

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose_drawer = BodyPoseDraw()

        self.screen_width = self.parent().size().width() // 4
        self.screen_height = self.parent().size().height() // 4
        if self.screen_width % 2 == 1:
            self.screen_width -= 1
        if self.screen_height % 2 == 1:
            self.screen_height -= 1

        self.maintain_aspect_ratio = aspect_ratio

        self.imageLabel = QLabel(self)  # create the label that holds the image
        self.thread = VideoThread()  # create the video capture thread
        self.thread.change_pixmap_signal.connect(self.UpdateImage)

    @pyqtSlot(np.ndarray)
    def UpdateImage(self, cv_img):
        qt_img = self.toQPix(cv_img)
        self.imageLabel.setPixmap(qt_img)
        # if not self.thread.run_flag:
        #     self.imageLabel.clear()
        #     self.imageLabel.repaint()

    def toQPix(self, frame):
        """Convert from an opencv image to QPixmap"""
        self.screen_width = self.parent().size().width() // 4
        self.screen_height = self.parent().size().height() // 4
        if self.screen_width % 2 == 1:
            self.screen_width -= 1
        if self.screen_height % 2 == 1:
            self.screen_height -= 1

        self.frame_counter += 1

        # Keep frame aspect ratio
        if self.maintain_aspect_ratio:
            frame = imutils.resize(frame, width=self.screen_width)
        # Force resize
        else:
            frame = cv2.resize(frame, (self.screen_width, self.screen_height))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        body_landmarks = self.landmarks_dataset[self.frame_counter-1]
        self.pose_drawer.draw_landmarks(frame, body_landmarks, self.mp_pose.POSE_CONNECTIONS)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Add timestamp to cameras
        cv2.rectangle(frame, (self.screen_width - 115, 25), (self.screen_width, 50), color=(0, 0, 0), thickness=-1)
        cv2.putText(frame, datetime.now().strftime('%H:%M:%S'), (self.screen_width - 110, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), lineType=cv2.LINE_AA)

        # Convert to pixmap and set to video frame
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(img)

    def get_image_label(self):
        return self.imageLabel

    def set_metadata(self, data_dir):
        with np.load(data_dir, allow_pickle=True) as data:
            self.landmarks_dataset = data['landmarks_dataset']
            self.metadata = data['metadata'].item()
        self.frame_counter = 0
        print(self.metadata)

    def read_calibration_data(self, json_file):
        with open(json_file) as f:
            data = json.load(f)
            name = self.metadata['name']
            self.calibration_data['name'] = name
            P = np.zeros((3, 4))
            P[:3, :3] = np.asarray(data['cameras'][name]['K'])
            self.calibration_data['height'] = self.metadata['height']
            self.calibration_data['width'] = self.metadata['width']
            self.calibration_data['P'] = P
            self.calibration_data['K'] = np.asarray(data['cameras'][name]['K'])
            self.calibration_data['D'] = np.asarray(data['cameras'][name]['dist']).reshape((5,))
            self.calibration_data['R'] = np.array([[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])

            keys_list = sorted(data['camera_poses'])
            self.calibration_data['translation'] = np.asarray(data['camera_poses'][keys_list[int(name.split('cam')[1]) - 1]]['T'])
            self.calibration_data['Q'] = np.asarray(data['camera_poses'][keys_list[int(name.split('cam')[1]) - 1]]['R'])
        print(self.calibration_data)

    def get_camera_data(self):
        return self.calibration_data
