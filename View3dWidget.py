###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################
'''

pyqt==5.9.2
pyqtgraph==0.11.0
pyopengl==3.1.5
'''

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph.Qt import QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
from mediapipe.python.solutions.pose import POSE_CONNECTIONS


class View3dWidget(QWidget):

    def __init__(self, parent=None):
        super(View3dWidget, self).__init__(parent)

        self.plotter = gl.GLViewWidget()
        #self.plotter.setVisible(True)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.plotter)
        self.setLayout(self.main_layout)

        self.plotter.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.plotter.setCameraPosition(distance=50, elevation=8)    # 50 for (0.1) scale of hand
        self.plotter.setBackgroundColor('#5B5A5A')

        # ground plane
        gz = gl.GLGridItem()
        self.plotter.addItem(gz)

        # cam center
        self.cam_positions = gl.GLScatterPlotItem(pos=np.random.randint(10, size=(4, 3)), color=pg.glColor((255, 255, 255)), size=10)
        self.cam_positions.setVisible(False)
        self.plotter.addItem(self.cam_positions)

        # cameras axis
        self.axes = {}
        rgb = [pg.glColor((255, 0, 0)), pg.glColor((0, 255, 0)), pg.glColor((0, 0, 255))]
        for j in range(4):
            for i in range(3):
                n = int(4*j + i)
                self.axes[n] = gl.GLLinePlotItem(pos=np.zeros((2, 3)), color=rgb[i], width=3, antialias=True)
                self.axes[n].setVisible(False)
                self.plotter.addItem(self.axes[n])

        # cameras frames
        self.far_cam_frame = {}
        for j in range(4):
            for i in range(4):
                n = int(4 * j + i)
                self.far_cam_frame[n] = gl.GLLinePlotItem(pos=np.zeros((2, 3)), color='w', width=3, antialias=True)
                self.far_cam_frame[n].setVisible(False)
                self.plotter.addItem(self.far_cam_frame[n])

        self.near_cam_frame = {}
        for j in range(4):
            for i in range(4):
                n = int(4 * j + i)
                self.near_cam_frame[n] = gl.GLLinePlotItem(pos=np.zeros((2, 3)), color='w', width=1, antialias=True)
                self.near_cam_frame[n].setVisible(False)
                self.plotter.addItem(self.near_cam_frame[n])

        self.connectors_cam_frame = {}
        for j in range(4):
            for i in range(4):
                n = int(4 * j + i)
                self.connectors_cam_frame[n] = gl.GLLinePlotItem(pos=np.zeros((2, 3)), color='w', width=1, antialias=True)
                self.connectors_cam_frame[n].setVisible(False)
                self.plotter.addItem(self.connectors_cam_frame[n])

        # keypoints
        keypoints = np.random.randint(10, size=(33, 3))
        self.body_points = gl.GLScatterPlotItem(pos=keypoints, color=pg.glColor((0, 255, 0)), size=10)
        self.body_points.setVisible(False)
        self.plotter.addItem(self.body_points)

        # keypoints connectors
        self.body_lines = {}
        self.connections = POSE_CONNECTIONS
        for n, pts in enumerate(self.connections):
            self.body_lines[n] = gl.GLLinePlotItem(pos=np.array([keypoints[p] for p in pts]), color='b', width=5, antialias=True)
            self.body_lines[n].setVisible(False)
            self.plotter.addItem(self.body_lines[n])

    def plot_pose(self, pose):
        idx_to_coordinates = pose
        num_landmarks = 33
        landmarks = np.zeros((33, 3))
        for n, connection in enumerate(self.connections):
            start_idx = connection[0]
            end_idx = connection[1]
            if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                raise ValueError(f'Landmark index is out of range. Invalid connection '
                                 f'from landmark #{start_idx} to landmark #{end_idx}.')
            if start_idx in idx_to_coordinates and end_idx in idx_to_coordinates:
                self.body_lines[n].setData(pos=np.array([idx_to_coordinates[start_idx], idx_to_coordinates[end_idx]]))
                self.body_lines[n].setVisible(True)
            else:
                self.body_lines[n].setVisible(False)

        for idx, coords in pose.items():
            landmarks[idx, :] = coords

        self.body_points.setData(pos=landmarks)
        self.body_points.setVisible(True)


    def plot_system(self, system, **kwargs):
        self.plot_cameras(system, **kwargs)

    def plot_cameras(self, system, scale=0.2, axes_size=0.2):
        points = []
        for name, cam in system.get_camera_dict().items():
            # cam center
            cam_center = cam.get_camcenter().reshape(1, 3)
            points.append(cam_center)

            #cam frame
            cam_idx = int(name.split('cam')[1]) - 1
            world_coords = cam.project_camera_frame_to_3d([[axes_size, 0, 0], [0, axes_size, 0], [0, 0, axes_size]])
            for i in range(3):
                n = 4 * cam_idx + i
                self.axes[n].setData(pos=np.array([cam_center, world_coords[i].reshape(1, 3)]))
                self.axes[n].setVisible(True)

            #cam body
            if cam.width is None or cam.height is None:
                raise ValueError('Camera width/height must be defined to plot.')
            uv_raw = np.array([[0, 0], [0, cam.height], [cam.width, cam.height], [cam.width, 0], [0, 0]])
            pts3d_near = cam.project_pixel_to_3d_ray(uv_raw, distorted=True, distance=0.2 * scale)
            pts3d_far = cam.project_pixel_to_3d_ray(uv_raw, distorted=True, distance=scale)
            # ring at far depth
            for i in range(4):
                n = 4 * cam_idx + i
                self.far_cam_frame[n].setData(pos=np.array([pts3d_far[i], pts3d_far[i + 1]]))
                self.far_cam_frame[n].setVisible(True)

            # ring at near depth
            for i in range(4):
                n = 4 * cam_idx + i
                self.near_cam_frame[n].setData(pos=np.array([pts3d_near[i], pts3d_near[i + 1]]))
                self.near_cam_frame[n].setVisible(True)

            # connectors
            for i in range(4):
                n = 4 * cam_idx + i
                self.connectors_cam_frame[n].setData(pos=np.array([pts3d_near[i], pts3d_far[i]]))
                self.connectors_cam_frame[n].setVisible(True)

        points = np.asarray(points)
        self.cam_positions.setData(pos=points)
        self.cam_positions.setVisible(True)
