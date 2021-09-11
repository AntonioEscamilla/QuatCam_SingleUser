###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QFrame
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime
import numpy as np
import mediapipe as mp
from BodyPoseDraw import *
import time
import glob
import os
import cv2
import imutils
import ntpath


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.paths = []
        self.names = []
        self.caps = []
        self.n_cams = 4

    def set_video_path(self, videos_dir):
        paths_list = glob.glob(os.path.join(videos_dir, '*.mov'))
        self.paths = [p for idx, p in enumerate(paths_list) if idx < self.n_cams]
        self.names = [ntpath.basename(p).split('.')[0] for idx, p in enumerate(paths_list) if idx < self.n_cams]
        print(f'Names of cameras in video files: {self.names}')

    def run(self):
        self.caps = []
        for i in range(len(self.names)):
            cap = cv2.VideoCapture(self.paths[i])
            self.caps.append(cap)

        while self.caps[0].isOpened() and self.caps[1].isOpened() and self.caps[2].isOpened() and self.caps[3].isOpened():
            start_t = time.perf_counter()
            result = [cap.read() for cap in self.caps]

            if not (result[0][0] or result[1][0] or result[2][0] or result[3][0]):
                break

            cv_images = np.asarray([r[1] for r in result])
            self.change_pixmap_signal.emit(cv_images)
            elapsed_t = time.perf_counter() - start_t
            self.spin(0.0333 - elapsed_t)
        cap.release()
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


class MultiVideoWidget(QWidget):
    frame_counter_signal = pyqtSignal(bool)

    def __init__(self, parent=None, aspect_ratio=False):
        super(MultiVideoWidget, self).__init__(parent)
        self.frame_counter = 0
        self.maintain_aspect_ratio = aspect_ratio
        self.n_videos = 4
        self.metadata = []
        self.detections = []

        self.mp_pose = mp.solutions.pose
        self.pose_drawer = BodyPoseDraw()

        self.gridlayout = QGridLayout(self)
        self.imageLabels = []
        for i in range(self.n_videos):
            self.imageLabels.append(QLabel(self))                       # create the labels that holds the images

        self.gridlayout.addWidget(self.imageLabels[0], 0, 0)
        self.gridlayout.addWidget(self.imageLabels[1], 1, 0)
        self.gridlayout.addWidget(self.imageLabels[2], 2, 0)
        self.gridlayout.addWidget(self.imageLabels[3], 3, 0)
        self.setLayout(self.gridlayout)

        self.thread = VideoThread()                                     # create the video capture thread
        self.thread.change_pixmap_signal.connect(self.UpdateImage)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.screen_width = self.parent().size().width() // 4
        self.screen_height = self.parent().size().height() // 4
        if self.screen_width % 2 == 1:
            self.screen_width -= 1
        if self.screen_height % 2 == 1:
            self.screen_height -= 1

    @pyqtSlot(np.ndarray)
    def UpdateImage(self, cv_images):
        self.frame_counter += 1

        for i in range(self.n_videos):
            qt_img = self.toQPix(cv_images[i], idx=i)
            self.imageLabels[i].setPixmap(qt_img)

        self.frame_counter_signal.emit(True)

    def toQPix(self, frame, idx):
        """Convert from an opencv image to QPixmap"""
        # Keep frame aspect ratio or force resize
        if self.maintain_aspect_ratio:
            frame = imutils.resize(frame, width=self.screen_width)
        else:
            frame = cv2.resize(frame, (self.screen_width, self.screen_height))

        # Add detections to camera view
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        body_landmarks = self.detections[idx][self.frame_counter-1]
        self.pose_drawer.draw_landmarks(frame, body_landmarks, self.mp_pose.POSE_CONNECTIONS)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Add timestamp to camera
        cv2.rectangle(frame, (self.screen_width - 115, 25), (self.screen_width, 50), color=(0, 0, 0), thickness=-1)
        cv2.putText(frame, datetime.now().strftime('%H:%M:%S'), (self.screen_width - 110, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), lineType=cv2.LINE_AA)

        # Convert to pixmap and set to video frame
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(img)

    def get_image_label(self, idx):
        return self.imageLabels[idx]

    def set_metadata(self, data_dir):
        self.metadata = []
        self.detections = []
        paths_list = glob.glob(os.path.join(data_dir, '*.npz'))
        paths_list = [p for idx, p in enumerate(paths_list) if idx < self.n_videos]
        for idx, path in enumerate(paths_list):
            with np.load(path, allow_pickle=True) as data:
                self.detections.append(data['landmarks_dataset'])
                self.metadata.append(data['metadata'].item())
        self.frame_counter = 0

        self.detections_length = np.asarray([d.shape[0] for d in self.detections]).min()
        print(f'Reading detections for {len(self.detections)} videos. Each detection of shape = {self.detections[0].shape}')

    def get_metadata(self):
        return self.metadata

    def get_detections(self):
        return self.detections

    def get_detections_in_frame(self, frame_as_idx):
        return [detection[frame_as_idx, :, :] for detection in self.detections]

    def get_detections_length(self):
        return self.detections_length
