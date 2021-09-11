###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QProgressBar, QHBoxLayout
import mediapipe as mp
import cv2
import os
import numpy as np
import ntpath


class VideoAnalizer(QThread):
    frame_count_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.path = None
        self.fps = 0
        self.total_frames = 0
        self.frame_counter = 0
        self.pose_solutions = mp.solutions.pose
        self.pose = self.pose_solutions.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)

    def set_video_path(self, path):
        self.path = path
        self.name = ntpath.basename(path).split('.')[0]
        print(self.name)
        self.frame_counter = 0
        self.video_metadata = {}

    def run(self):
        print('******* Video Analizer *******')
        cap = cv2.VideoCapture(self.path)  # capture from web cam
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print('CAP_PROP_FRAME_COUNT: {}'.format(self.total_frames))
        self.landmarks_dataset = np.zeros((self.total_frames, 33, 3))
        self.video_metadata['name'] = self.name
        self.video_metadata['fps'] = self.fps
        self.video_metadata['frames'] = self.total_frames
        self.video_metadata['width'] = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.video_metadata['height'] = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            self.frame_counter += 1
            self.frame_count_signal.emit(self.frame_counter)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.pose.process(image)
            if results.pose_landmarks:
                self.landmarks_dataset[self.frame_counter-1] = self.get_landmarks_2dArray(results.pose_landmarks.landmark)

        cap.release()
        print('End of Video: total frames analyzed = {}'.format(self.frame_counter))
        last_folder = ntpath.dirname(self.path).split('/')[-1]
        base_path = ntpath.dirname(self.path).split(last_folder)[0]
        os.makedirs(base_path + 'detections', exist_ok=True)
        save_path = base_path + 'detections/' + self.name
        np.savez_compressed(save_path + '.npz', landmarks_dataset=self.landmarks_dataset, metadata=self.video_metadata)
        self.wait()

    # def stop(self):
    #     """Sets run flag to False and waits for thread to finish"""
    #     self.run_flag = False
    #     self.wait()

    @staticmethod
    def get_landmarks_2dArray(landmarks):
        """ output array of size (21, 3) """
        a_list = []
        for landmark in landmarks:
            a_list.append(np.array([landmark.x, landmark.y, landmark.visibility]))
        return np.array(a_list)


class ProgressAnalizer(QWidget):

    def __init__(self, parent):
        super(ProgressAnalizer, self).__init__(parent)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setEnabled(True)
        self.progress_bar.setStyleSheet(u"QProgressBar\n"
                                           "{\n"
                                           "	color:rgb(255,255,255);\n"
                                           "	background-color :rgb(51,51,51);\n"
                                           "	border : 2px;\n"
                                           "	border-radius:4px;\n"
                                           "}\n"
                                           "\n"
                                           "QProgressBar::chunk{\n"
                                           "	border : 2px;\n"
                                           "	border-radius:4px;\n"
                                           "	background-color:rgb(0,143,150);\n"
                                           "}")
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setOrientation(Qt.Horizontal)
        self.progress_bar.setInvertedAppearance(False)
        self.progress_bar.setTextDirection(QProgressBar.TopToBottom)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.progress_bar)
        self.setLayout(self.main_layout)  # set the vbox layout as the widgets layout

        self.analizer = VideoAnalizer()
        self.analizer.frame_count_signal.connect(self.onFrameCounterChange)

    def onFrameCounterChange(self, value):
        self.progress_bar.setValue(value*100.0/self.analizer.total_frames)
