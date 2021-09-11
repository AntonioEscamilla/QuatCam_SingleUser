###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    HANDY INTERACTION                                ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

from PyQt5.QtCore import QCoreApplication, QMetaObject, QSize, pyqtSignal, Qt, QThread, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import *
from CameraWidget import CameraWidget
from VideoAnalizer import ProgressAnalizer
from MultiVideoWidget import MultiVideoWidget
from View3dWidget import View3dWidget
from ImageViewerWidget import ImageViewerWidget, ImageTable
import time
import cv2


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setMinimumSize(QSize(1280, 900))

        #print(self.returnCameraIndexes())
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background:rgb(91,90,90);")
        self.layout_central_widget = QVBoxLayout(self.centralwidget)
        self.layout_central_widget.setSpacing(0)
        self.layout_central_widget.setObjectName(u"layout_central_widget")
        self.layout_central_widget.setContentsMargins(0, 0, 0, 0)

        # -----> Frame superior: Frame Toggle + Frame Window
        self.frame_superior = QFrame(self.centralwidget)
        self.frame_superior.setObjectName(u"frame_superior")
        self.frame_superior.setMaximumSize(QSize(16777215, 55))
        self.frame_superior.setFrameShape(QFrame.NoFrame)
        self.frame_superior.setFrameShadow(QFrame.Plain)
        self.layout_frame_superior = QHBoxLayout(self.frame_superior)
        self.layout_frame_superior.setSpacing(0)
        self.layout_frame_superior.setObjectName(u"layout_frame_superior")
        self.layout_frame_superior.setContentsMargins(0, 0, 0, 0)

        # ---> Frame Toggle: Button Toggle
        self.frame_toggle = QFrame(self.frame_superior)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMinimumSize(QSize(80, 55))
        self.frame_toggle.setMaximumSize(QSize(80, 55))
        self.frame_toggle.setStyleSheet(u"background:rgb(0,143,150);")
        self.frame_toggle.setFrameShape(QFrame.NoFrame)
        self.frame_toggle.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_toggle)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toggle = QPushButton(self.frame_toggle)
        self.toggle.setObjectName(u"toggle")
        self.toggle.setMinimumSize(QSize(80, 55))
        self.toggle.setMaximumSize(QSize(80, 55))
        icon = QIcon()
        icon.addFile(u"icons/1x/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toggle.setIcon(icon)
        self.toggle.setIconSize(QSize(22, 12))
        self.toggle.setFlat(True)
        self.toggle.setStyleSheet(u"QPushButton {\n"
                                   "	border: none;\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "	background-color: rgb(0,178,178);\n"
                                   "}\n"
                                   "QPushButton:pressed {	\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}")
        self.horizontalLayout_3.addWidget(self.toggle)
        self.layout_frame_superior.addWidget(self.frame_toggle)

        # ---> Frame Window: AppName + Min + Max + Close
        self.frame_window = QFrame(self.frame_superior)
        self.frame_window.setObjectName(u"frame_window")
        self.frame_window.setMaximumSize(QSize(16777215, 55))
        self.frame_window.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_window.setFrameShape(QFrame.NoFrame)
        self.frame_window.setFrameShadow(QFrame.Plain)
        self.layout_frame_window = QHBoxLayout(self.frame_window)
        self.layout_frame_window.setSpacing(0)
        self.layout_frame_window.setObjectName(u"layout_frame_window")
        self.layout_frame_window.setContentsMargins(0, 0, 0, 0)
        # -> Frame AppName
        self.frame_appname = QFrame(self.frame_window)
        self.frame_appname.setObjectName(u"frame_appname")
        self.frame_appname.setFrameShape(QFrame.NoFrame)
        self.frame_appname.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_appname)
        self.horizontalLayout_10.setSpacing(7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.appname = QLabel(self.frame_appname)
        self.appname.setObjectName(u"appname")
        font = QFont()
        font.setFamily(u"Segoe UI Light")
        font.setPointSize(24)
        self.appname.setFont(font)
        self.appname.setStyleSheet(u"color:rgb(255,255,255);")
        self.horizontalLayout_10.addWidget(self.appname)
        self.layout_frame_window.addWidget(self.frame_appname)
        # -> Frame Min
        self.frame_min = QFrame(self.frame_window)
        self.frame_min.setObjectName(u"frame_min")
        self.frame_min.setMinimumSize(QSize(55, 55))
        self.frame_min.setMaximumSize(QSize(55, 55))
        self.frame_min.setFrameShape(QFrame.NoFrame)
        self.frame_min.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_min)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.bn_min = QPushButton(self.frame_min)
        self.bn_min.setObjectName(u"bn_min")
        self.bn_min.setMaximumSize(QSize(55, 55))
        icon1 = QIcon()
        icon1.addFile(u"icons/1x/hideAsset 53.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_min.setIcon(icon1)
        self.bn_min.setIconSize(QSize(22, 22))
        self.bn_min.setFlat(True)
        self.bn_min.setStyleSheet(u"QPushButton {\n"
                                   "	border: none;\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "	background-color: rgb(0,143,150);\n"
                                   "}\n"
                                   "QPushButton:pressed {	\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}")
        self.horizontalLayout_7.addWidget(self.bn_min)
        self.layout_frame_window.addWidget(self.frame_min)
        # -> Frame Max
        self.frame_max = QFrame(self.frame_window)
        self.frame_max.setObjectName(u"frame_max")
        self.frame_max.setMinimumSize(QSize(55, 55))
        self.frame_max.setMaximumSize(QSize(55, 55))
        self.frame_max.setFrameShape(QFrame.NoFrame)
        self.frame_max.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_max)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.bn_max = QPushButton(self.frame_max)
        self.bn_max.setObjectName(u"bn_max")
        self.bn_max.setMaximumSize(QSize(55, 55))
        icon2 = QIcon()
        icon2.addFile(u"icons/1x/max.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_max.setIcon(icon2)
        self.bn_max.setIconSize(QSize(22, 22))
        self.bn_max.setFlat(True)
        self.bn_max.setStyleSheet(u"QPushButton {\n"
                                   "	border: none;\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "	background-color: rgb(0,143,150);\n"
                                   "}\n"
                                   "QPushButton:pressed {	\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}")
        self.horizontalLayout_6.addWidget(self.bn_max)
        self.layout_frame_window.addWidget(self.frame_max)
        # -> Frame Close
        self.frame_close = QFrame(self.frame_window)
        self.frame_close.setObjectName(u"frame_close")
        self.frame_close.setMinimumSize(QSize(55, 55))
        self.frame_close.setMaximumSize(QSize(55, 55))
        self.frame_close.setFrameShape(QFrame.NoFrame)
        self.frame_close.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_close)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.bn_close = QPushButton(self.frame_close)
        self.bn_close.setObjectName(u"bn_close")
        self.bn_close.setMaximumSize(QSize(55, 55))
        icon3 = QIcon()
        icon3.addFile(u"icons/1x/closeAsset 43.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_close.setIcon(icon3)
        self.bn_close.setIconSize(QSize(22, 22))
        self.bn_close.setFlat(True)
        self.bn_close.setStyleSheet(u"QPushButton {\n"
                                    "	border: none;\n"
                                    "	background-color: rgba(0,0,0,0);\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "	background-color: rgb(0,143,150);\n"
                                    "}\n"
                                    "QPushButton:pressed {	\n"
                                    "	background-color: rgba(0,0,0,0);\n"
                                    "}")
        self.horizontalLayout_5.addWidget(self.bn_close)
        self.layout_frame_window.addWidget(self.frame_close)
        self.layout_frame_superior.addWidget(self.frame_window)
        self.layout_central_widget.addWidget(self.frame_superior)

        # -----> Frame inferior: Frame Izq + Frame Der
        self.frame_inferior = QFrame(self.centralwidget)
        self.frame_inferior.setObjectName(u"frame_inferior")
        self.frame_inferior.setFrameShape(QFrame.NoFrame)
        self.frame_inferior.setFrameShadow(QFrame.Plain)
        self.layout_frame_inferior = QHBoxLayout(self.frame_inferior)
        self.layout_frame_inferior.setSpacing(0)
        self.layout_frame_inferior.setObjectName(u"layout_frame_inferior")
        self.layout_frame_inferior.setContentsMargins(0, 0, 0, 0)

        # ---> Frame Izq: Home + Bug + Cloud + Android + Fixed
        self.frame_izq = QFrame(self.frame_inferior)
        self.frame_izq.setObjectName(u"frame_izq")
        self.frame_izq.setMinimumSize(QSize(80, 0))
        self.frame_izq.setMaximumSize(QSize(80, 16777215))
        self.frame_izq.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_izq.setFrameShape(QFrame.NoFrame)
        self.frame_izq.setFrameShadow(QFrame.Plain)
        self.layout_frame_izq = QVBoxLayout(self.frame_izq)
        self.layout_frame_izq.setSpacing(0)
        self.layout_frame_izq.setObjectName(u"layout_frame_izq")
        self.layout_frame_izq.setContentsMargins(0, 0, 0, 0)
        # -> Frame Home
        self.frame_home = QFrame(self.frame_izq)
        self.frame_home.setObjectName(u"frame_home")
        self.frame_home.setMinimumSize(QSize(80, 55))
        self.frame_home.setMaximumSize(QSize(160, 55))
        self.frame_home.setFrameShape(QFrame.NoFrame)
        self.frame_home.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_home)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.bn_home = QPushButton(self.frame_home)
        self.bn_home.setObjectName(u"bn_home")
        self.bn_home.setMinimumSize(QSize(80, 55))
        self.bn_home.setMaximumSize(QSize(160, 55))
        icon4 = QIcon()
        icon4.addFile(u"icons/1x/captureAsset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_home.setIcon(icon4)
        self.bn_home.setIconSize(QSize(40, 40))
        self.bn_home.setFlat(True)
        self.bn_home.setStyleSheet(u"QPushButton {\n"
                                   "	border: none;\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "	background-color: rgb(91,90,90);\n"
                                   "}\n"
                                   "QPushButton:pressed {	\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}")
        self.horizontalLayout_15.addWidget(self.bn_home)
        self.layout_frame_izq.addWidget(self.frame_home)
        # -> Frame Bug
        self.frame_bug = QFrame(self.frame_izq)
        self.frame_bug.setObjectName(u"frame_bug")
        self.frame_bug.setMinimumSize(QSize(80, 55))
        self.frame_bug.setMaximumSize(QSize(160, 55))
        self.frame_bug.setFrameShape(QFrame.NoFrame)
        self.frame_bug.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_bug)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.bn_bug = QPushButton(self.frame_bug)
        self.bn_bug.setObjectName(u"bn_bug")
        self.bn_bug.setMinimumSize(QSize(80, 55))
        self.bn_bug.setMaximumSize(QSize(160, 55))
        icon5 = QIcon()
        icon5.addFile(u"icons/1x/viewerAsset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_bug.setIcon(icon5)
        self.bn_bug.setIconSize(QSize(35, 35))
        self.bn_bug.setFlat(True)
        self.bn_bug.setStyleSheet(u"QPushButton {\n"
                                  "	border: none;\n"
                                  "	background-color: rgba(0,0,0,0);\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "	background-color: rgb(91,90,90);\n"
                                  "}\n"
                                  "QPushButton:pressed {	\n"
                                  "	background-color: rgba(0,0,0,0);\n"
                                  "}")
        self.horizontalLayout_16.addWidget(self.bn_bug)
        self.layout_frame_izq.addWidget(self.frame_bug)
        # -> Frame Cloud
        self.frame_cloud = QFrame(self.frame_izq)
        self.frame_cloud.setObjectName(u"frame_cloud")
        self.frame_cloud.setMinimumSize(QSize(80, 55))
        self.frame_cloud.setMaximumSize(QSize(160, 55))
        self.frame_cloud.setFrameShape(QFrame.NoFrame)
        self.frame_cloud.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_cloud)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.bn_cloud = QPushButton(self.frame_cloud)
        self.bn_cloud.setObjectName(u"bn_cloud")
        self.bn_cloud.setMinimumSize(QSize(80, 55))
        self.bn_cloud.setMaximumSize(QSize(160, 55))
        icon6 = QIcon()
        icon6.addFile(u"icons/1x/landmarkAsset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_cloud.setIcon(icon6)
        self.bn_cloud.setIconSize(QSize(40, 40))
        self.bn_cloud.setFlat(True)
        self.bn_cloud.setStyleSheet(u"QPushButton {\n"
                                    "	border: none;\n"
                                    "	background-color: rgba(0,0,0,0);\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "	background-color: rgb(91,90,90);\n"
                                    "}\n"
                                    "QPushButton:pressed {	\n"
                                    "	background-color: rgba(0,0,0,0);\n"
                                    "}")
        self.horizontalLayout_17.addWidget(self.bn_cloud)
        self.layout_frame_izq.addWidget(self.frame_cloud)
        # -> Frame Fixed
        self.frame_fixed = QFrame(self.frame_izq)
        self.frame_fixed.setObjectName(u"frame_fixed")
        self.frame_fixed.setFrameShape(QFrame.NoFrame)
        self.frame_fixed.setFrameShadow(QFrame.Plain)
        self.verticalLayout_4 = QVBoxLayout(self.frame_fixed)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_izq.addWidget(self.frame_fixed)
        self.layout_frame_inferior.addWidget(self.frame_izq)

        # ---> Frame Der: Frame Low + Frame Main
        self.frame_der = QFrame(self.frame_inferior)
        self.frame_der.setObjectName(u"frame_der")
        self.frame_der.setFrameShape(QFrame.NoFrame)
        self.frame_der.setFrameShadow(QFrame.Plain)
        self.layout_frame_der = QVBoxLayout(self.frame_der)
        self.layout_frame_der.setSpacing(0)
        self.layout_frame_der.setObjectName(u"layout_frame_der")
        self.layout_frame_der.setContentsMargins(0, 0, 0, 0)
        
        # -> FRAME MAIN: Stacked Widget
        self.frame_main = QFrame(self.frame_der)
        self.frame_main.setObjectName(u"frame")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Plain)
        self.layout_frame_main = QHBoxLayout(self.frame_main)
        self.layout_frame_main.setSpacing(0)
        self.layout_frame_main.setObjectName(u"layout_frame_main")
        self.layout_frame_main.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame_main)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 55))
        self.stackedWidget.setStyleSheet(u"")

        # *************** PAGE HOME ******************
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.page_home.setStyleSheet(u"background:rgb(91,90,90);")
        self.layout_page_home = QHBoxLayout(self.page_home)
        self.layout_page_home.setSpacing(0)
        self.layout_page_home.setObjectName(u"layout_page_home")
        self.layout_page_home.setContentsMargins(0, 5, 0, 5)
        # -> Frame Home Main: Head + Cam + Open/Close/Run
        self.frame_home_main = QFrame(self.page_home)
        self.frame_home_main.setObjectName(u"frame_home_main")
        self.frame_home_main.setFrameShape(QFrame.NoFrame)
        self.frame_home_main.setFrameShadow(QFrame.Plain)
        self.verticalLayout_5 = QVBoxLayout(self.frame_home_main)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.home_main_head = QLabel(self.frame_home_main)
        self.home_main_head.setObjectName(u"home_main_head")
        self.home_main_head.setMinimumSize(QSize(0, 55))
        self.home_main_head.setMaximumSize(QSize(16777215, 55))
        font18 = QFont()
        font18.setFamily(u"Segoe UI Semilight")
        font18.setPointSize(18)
        self.home_main_head.setFont(font18)
        self.home_main_head.setStyleSheet(u"QLabel {\n"
                                        " color:rgb(255,255,255);\n"
                                        "}")
        self.home_main_head.setTextFormat(Qt.RichText)
        self.verticalLayout_5.addWidget(self.home_main_head)
        # -> Cam
        self.one = CameraWidget(self.frame_home_main, 0)
        self.two = CameraWidget(self.frame_home_main, 1)
        self.three = CameraWidget(self.frame_home_main, 2,)
        self.four = CameraWidget(self.frame_home_main, 3)
        self.cams_gridlayout = QGridLayout()
        self.cams_gridlayout.addWidget(self.one.get_image_label(), 0, 0, 1, 1)
        self.cams_gridlayout.addWidget(self.two.get_image_label(), 0, 1, 1, 1)
        self.cams_gridlayout.addWidget(self.three.get_image_label(), 1, 0, 1, 1)
        self.cams_gridlayout.addWidget(self.four.get_image_label(), 1, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.cams_gridlayout)
        # -> Open
        font12 = QFont()
        font12.setFamily(u"Segoe UI")
        font12.setPointSize(12)
        self.home_open_bn = QPushButton(self.frame_home_main)
        self.home_open_bn.setObjectName(u"open_button")
        self.home_open_bn.setMinimumHeight(30)
        self.home_open_bn.setText("Start Streaming")
        self.home_open_bn.setFont(font12)
        self.home_open_bn.setCheckable(False)
        self.home_open_bn.setFlat(True)
        self.home_open_bn.setStyleSheet(u"QPushButton {\n"
                                      "	border: 2px solid rgb(51,51,51);\n"
                                      "	border-radius: 5px;	\n"
                                      "	color:rgb(255,255,255);\n"
                                      "	background-color: rgb(51,51,51);\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "	border: 2px solid rgb(0,143,150);\n"
                                      "	background-color: rgb(0,143,150);\n"
                                      "}\n"
                                      "QPushButton:pressed {	\n"
                                      "	border: 2px solid rgb(0,143,150);\n"
                                      "	background-color: rgb(51,51,51);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:disabled {	\n"
                                      "	border-radius: 5px;	\n"
                                      "	border: 2px solid rgb(112,112,112);\n"
                                      "	background-color: rgb(112,112,112);\n"
                                      "}")
        # -> Close
        self.home_close_bn = QPushButton(self.frame_home_main)  # create close Button
        self.home_close_bn.setText("Stop Streaming")
        self.home_close_bn.setObjectName(u"close_button")
        self.home_close_bn.setMinimumHeight(30)
        self.home_close_bn.setFont(font12)
        self.home_close_bn.setCheckable(False)
        self.home_close_bn.setFlat(True)
        self.home_close_bn.setStyleSheet(u"QPushButton {\n"
                                       "	border: 2px solid rgb(51,51,51);\n"
                                       "	border-radius: 5px;	\n"
                                       "	color:rgb(255,255,255);\n"
                                       "	background-color: rgb(51,51,51);\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "	border: 2px solid rgb(0,143,150);\n"
                                       "	background-color: rgb(0,143,150);\n"
                                       "}\n"
                                       "QPushButton:pressed {	\n"
                                       "	border: 2px solid rgb(0,143,150);\n"
                                       "	background-color: rgb(51,51,51);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:disabled {	\n"
                                       "	border-radius: 5px;	\n"
                                       "	border: 2px solid rgb(112,112,112);\n"
                                       "	background-color: rgb(112,112,112);\n"
                                       "}")
        # -> Run
        self.home_run_bn = QPushButton(self.frame_home_main)  # create inference Button
        self.home_run_bn.setText("Capture Images")
        self.home_run_bn.setObjectName(u"capture_button")
        self.home_run_bn.setMinimumHeight(30)
        self.home_run_bn.setFont(font12)
        self.home_run_bn.setCheckable(False)
        self.home_run_bn.setFlat(True)
        self.home_run_bn.setEnabled(False)
        self.home_run_bn.setStyleSheet(u"QPushButton {\n"
                                           "	border: 2px solid rgb(51,51,51);\n"
                                           "	border-radius: 5px;	\n"
                                           "	color:rgb(255,255,255);\n"
                                           "	background-color: rgb(51,51,51);\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "	border: 2px solid rgb(0,143,150);\n"
                                           "	background-color: rgb(0,143,150);\n"
                                           "}\n"
                                           "QPushButton:pressed {	\n"
                                           "	border: 2px solid rgb(0,143,150);\n"
                                           "	background-color: rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {	\n"
                                           "	border-radius: 5px;	\n"
                                           "	border: 2px solid rgb(112,112,112);\n"
                                           "	background-color: rgb(112,112,112);\n"
                                           "}")
        # -> Progress Bar
        self.time_bar = ProgressTimer(self.frame_home_main, time_limit=5.0)
        self.time_bar.setObjectName(u"time_bar")
        self.time_bar.setMinimumSize(QSize(230, 40))
        self.time_bar.setMaximumSize(QSize(230, 40))
        # -> Horizontal Layout for the 3 Buttons + Progress Bar
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.home_open_bn)
        self.h_layout.addWidget(self.home_close_bn)
        self.h_layout.addWidget(self.home_run_bn)
        self.h_layout.addWidget(self.time_bar)
        self.verticalLayout_5.addLayout(self.h_layout)
        self.layout_page_home.addWidget(self.frame_home_main)
        # -> Frame Home Division
        self.vert_divide = QFrame(self.page_home)
        self.vert_divide.setObjectName(u"vert_divide")
        self.vert_divide.setFrameShape(QFrame.VLine)
        self.vert_divide.setFrameShadow(QFrame.Sunken)
        self.layout_page_home.addWidget(self.vert_divide)
        # -> Frame Home Stat: Head + Disc
        self.frame_home_stat = QFrame(self.page_home)
        self.frame_home_stat.setObjectName(u"frame_home_stat")
        self.frame_home_stat.setMinimumSize(QSize(300, 0))
        self.frame_home_stat.setMaximumSize(QSize(300, 16777215))
        self.frame_home_stat.setFrameShape(QFrame.NoFrame)
        self.frame_home_stat.setFrameShadow(QFrame.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.frame_home_stat)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.home_stat_hed = QLabel(self.frame_home_stat)
        self.home_stat_hed.setObjectName(u"home_stat_hed")
        self.home_stat_hed.setMinimumSize(QSize(0, 55))
        self.home_stat_hed.setMaximumSize(QSize(16777215, 55))
        self.home_stat_hed.setFont(font18)
        self.home_stat_hed.setStyleSheet(u"QLabel {\n"
                                                " color:rgb(255,255,255);\n"
                                                "}")
        self.home_stat_hed.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout_6.addWidget(self.home_stat_hed)
        font11 = QFont()
        font11.setFamily(u"Segoe UI")
        font11.setPointSize(11)
        # -> Model Statistics
        self.image_list = QLabel(self.frame_home_stat)
        self.image_list.setObjectName(u"image_list")
        self.image_list.setFont(font11)
        self.image_list.setStyleSheet(u"QLabel {\n"
                                         " color:rgb(255,255,255);\n"
                                         "}")
        self.image_list.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.verticalLayout_6.addWidget(self.image_list)
        self.layout_page_home.addWidget(self.frame_home_stat)
        self.stackedWidget.addWidget(self.page_home)

        # *************** PAGE ABOUT HOME ******************
        self.page_about_home = QWidget()
        self.page_about_home.setObjectName(u"page_about_home")
        self.page_about_home.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_13 = QVBoxLayout(self.page_about_home)
        self.verticalLayout_13.setSpacing(5)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(5, 5, 5, 5)
        self.about_home = QLabel(self.page_about_home)
        self.about_home.setObjectName(u"about_home")
        self.about_home.setMinimumSize(QSize(0, 55))
        self.about_home.setMaximumSize(QSize(16777215, 55))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(24)
        self.about_home.setFont(font3)
        self.about_home.setStyleSheet(u"color:rgb(255,255,255);")
        self.verticalLayout_13.addWidget(self.about_home)

        self.frame_about_home = QFrame(self.page_about_home)
        self.frame_about_home.setObjectName(u"frame_about_home")
        self.frame_about_home.setFrameShape(QFrame.StyledPanel)
        self.frame_about_home.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_about_home)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(5, 5, 0, 5)
        self.text_about_home = QTextEdit(self.frame_about_home)
        self.text_about_home.setObjectName(u"text_about_home")
        self.text_about_home.setEnabled(True)
        font10 = QFont()
        font10.setFamily(u"Segoe UI")
        font10.setPointSize(10)
        self.text_about_home.setFont(font10)
        self.text_about_home.setStyleSheet(u"color:rgb(255,255,255);")
        self.text_about_home.setFrameShape(QFrame.NoFrame)
        self.text_about_home.setFrameShadow(QFrame.Plain)
        self.text_about_home.setReadOnly(True)
        self.text_about_home.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.horizontalLayout_28.addWidget(self.text_about_home)

        self.vsb_about_home = QScrollBar(self.frame_about_home)
        self.vsb_about_home.setObjectName(u"vsb_about_home")
        self.vsb_about_home.setStyleSheet(u"QScrollBar:vertical {\n"
                                            "	background:rgb(51,51,51);\n"
                                            "    width:20px;\n"
                                            "    margin: 0px 0px 0px 0px;\n"
                                            "}\n"
                                            "QScrollBar::handle:vertical {\n"
                                            "    background:rgb(0,143,150);\n"
                                            "}\n"
                                            "QScrollBar::add-page:vertical {\n"
                                            " 	background:rgb(51,51,51);\n"
                                            "}\n"
                                            "QScrollBar::sub-page:vertical {\n"
                                            " 	background:rgb(51,51,51);\n"
                                            "}")
        self.vsb_about_home.setOrientation(Qt.Vertical)
        self.horizontalLayout_28.addWidget(self.vsb_about_home)
        self.verticalLayout_13.addWidget(self.frame_about_home)
        self.stackedWidget.addWidget(self.page_about_home)

        # *************** PAGE IMAGE VIEWER ******************
        self.page_image_view = QWidget()
        self.page_image_view.setObjectName(u"page_image_view")
        self.page_image_view.setStyleSheet(u"background:rgb(91,90,90);")
        self.page_main_layout = QHBoxLayout(self.page_image_view)
        self.page_main_layout.setSpacing(0)
        self.page_main_layout.setObjectName(u"page_main_layout")
        self.page_main_layout.setContentsMargins(0, 5, 0, 5)

        # -> Main Frame: Visualizer + Buttons
        self.main_frame = QFrame(self.page_image_view)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFrameShape(QFrame.NoFrame)
        self.main_frame.setFrameShadow(QFrame.Plain)
        self.main_frame_v_layout = QVBoxLayout(self.main_frame)
        self.main_frame_v_layout.setSpacing(5)
        self.main_frame_v_layout.setObjectName(u"main_frame_v_layout")
        self.main_frame_v_layout.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.viewer_main_head = QLabel(self.main_frame)
        self.viewer_main_head.setObjectName(u"main_head")
        self.viewer_main_head.setMinimumSize(QSize(0, 55))
        self.viewer_main_head.setMaximumSize(QSize(16777215, 55))
        self.viewer_main_head.setFont(font18)
        self.viewer_main_head.setStyleSheet(u"color:rgb(255,255,255);")
        self.main_frame_v_layout.addWidget(self.viewer_main_head)
        # -> Image Visualizer
        self.image_visualizer = ImageViewerWidget(self.main_frame)  # create the label that holds the image
        self.image_visualizer.setObjectName(u"image_visualizer")
        self.main_frame_v_layout.addWidget(self.image_visualizer)
        # -> Horizontal Layout for 2 Buttons
        self.h_layout_2 = QHBoxLayout()
        # -> Open Folder
        self.bn_viewer_open = QPushButton(self.main_frame)
        self.bn_viewer_open.setObjectName(u"bn_viewer_open")
        self.bn_viewer_open.setMinimumSize(QSize(180, 30))
        self.bn_viewer_open.setMaximumSize(QSize(180, 30))
        self.bn_viewer_open.setFont(font12)
        self.bn_viewer_open.setStyleSheet(u"QPushButton {\n"
                                        "	border: 2px solid rgb(51,51,51);\n"
                                        "	border-radius: 5px;	\n"
                                        "	color:rgb(255,255,255);\n"
                                        "	background-color: rgb(51,51,51);\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "	border: 2px solid rgb(0,143,150);\n"
                                        "	background-color: rgb(0,143,150);\n"
                                        "}\n"
                                        "QPushButton:pressed {	\n"
                                        "	border: 2px solid rgb(0,143,150);\n"
                                        "	background-color: rgb(51,51,51);\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:disabled {	\n"
                                        "	border-radius: 5px;	\n"
                                        "	border: 2px solid rgb(112,112,112);\n"
                                        "	background-color: rgb(112,112,112);\n"
                                        "}")
        self.bn_viewer_open.setCheckable(False)
        self.bn_viewer_open.setFlat(True)
        self.bn_viewer_open.setEnabled(True)
        self.h_layout_2.addWidget(self.bn_viewer_open)
        # -> Next Image
        self.bn_viewer_next = QPushButton(self.main_frame)
        self.bn_viewer_next.setObjectName(u"bn_bug_stop")
        self.bn_viewer_next.setMinimumSize(QSize(180, 30))
        self.bn_viewer_next.setMaximumSize(QSize(180, 30))
        self.bn_viewer_next.setFont(font12)
        self.bn_viewer_next.setStyleSheet(u"QPushButton {\n"
                                       "	border: 2px solid rgb(51,51,51);\n"
                                       "	border-radius: 5px;	\n"
                                       "	color:rgb(255,255,255);\n"
                                       "	background-color: rgb(51,51,51);\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "	border: 2px solid rgb(0,143,150);\n"
                                       "	background-color: rgb(0,143,150);\n"
                                       "}\n"
                                       "QPushButton:pressed {	\n"
                                       "	border: 2px solid rgb(0,143,150);\n"
                                       "	background-color: rgb(51,51,51);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:disabled {	\n"
                                       "	border-radius: 5px;	\n"
                                       "	border: 2px solid rgb(112,112,112);\n"
                                       "	background-color: rgb(112,112,112);\n"
                                       "}")
        self.bn_viewer_next.setCheckable(False)
        self.bn_viewer_next.setFlat(True)
        self.bn_viewer_next.setEnabled(False)
        self.h_layout_2.addWidget(self.bn_viewer_next)
        # -> Delete Image
        self.bn_viewer_delete = QPushButton(self.main_frame)
        self.bn_viewer_delete.setObjectName(u"bn_viewer_delete")
        self.bn_viewer_delete.setMinimumSize(QSize(180, 30))
        self.bn_viewer_delete.setMaximumSize(QSize(180, 30))
        self.bn_viewer_delete.setFont(font12)
        self.bn_viewer_delete.setStyleSheet(u"QPushButton {\n"
                                          "	border: 2px solid rgb(51,51,51);\n"
                                          "	border-radius: 5px;	\n"
                                          "	color:rgb(255,255,255);\n"
                                          "	background-color: rgb(51,51,51);\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "	border: 2px solid rgb(0,143,150);\n"
                                          "	background-color: rgb(0,143,150);\n"
                                          "}\n"
                                          "QPushButton:pressed {	\n"
                                          "	border: 2px solid rgb(0,143,150);\n"
                                          "	background-color: rgb(51,51,51);\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:disabled {	\n"
                                          "	border-radius: 5px;	\n"
                                          "	border: 2px solid rgb(112,112,112);\n"
                                          "	background-color: rgb(112,112,112);\n"
                                          "}")
        self.bn_viewer_delete.setCheckable(False)
        self.bn_viewer_delete.setFlat(True)
        self.bn_viewer_delete.setEnabled(False)
        self.h_layout_2.addWidget(self.bn_viewer_delete)
        # -> Spacer
        self.horizontalSpacer_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.h_layout_2.addItem(self.horizontalSpacer_1)
        # -> Frame End
        self.main_frame_v_layout.addLayout(self.h_layout_2)
        self.page_main_layout.addWidget(self.main_frame)

        # -> Frame Division
        self.vert_divide_2 = QFrame(self.page_image_view)
        self.vert_divide_2.setObjectName(u"vert_divide_2")
        self.vert_divide_2.setFrameShape(QFrame.VLine)
        self.vert_divide_2.setFrameShadow(QFrame.Sunken)
        self.page_main_layout.addWidget(self.vert_divide_2)

        # -> Stat Frame: Head + Disc
        self.aux_frame = QFrame(self.page_image_view)
        self.aux_frame.setObjectName(u"aux_frame")
        self.aux_frame.setMinimumSize(QSize(400, 0))
        self.aux_frame.setMaximumSize(QSize(400, 16777215))
        self.aux_frame.setFrameShape(QFrame.NoFrame)
        self.aux_frame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_26 = QVBoxLayout(self.aux_frame)
        self.verticalLayout_26.setSpacing(5)
        self.verticalLayout_26.setObjectName(u"verticalLayout_6")
        self.verticalLayout_26.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.viewer_aux_head = QLabel(self.aux_frame)
        self.viewer_aux_head.setObjectName(u"viewer_aux_head")
        self.viewer_aux_head.setMinimumSize(QSize(0, 55))
        self.viewer_aux_head.setMaximumSize(QSize(16777215, 55))
        self.viewer_aux_head.setFont(font18)
        self.viewer_aux_head.setStyleSheet(u"QLabel {\n"
                                         " color:rgb(255,255,255);\n"
                                         "}")
        self.viewer_aux_head.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.verticalLayout_26.addWidget(self.viewer_aux_head)
        # -> Images Table
        self.viewer_image_table = ImageTable(self.aux_frame)
        self.verticalLayout_26.addWidget(self.viewer_image_table, 1)
        self.page_main_layout.addWidget(self.aux_frame)
        self.stackedWidget.addWidget(self.page_image_view)

        # *************** PAGE CLOUD ******************
        self.page_cloud = QWidget()
        self.page_cloud.setObjectName(u"page_cloud")
        self.page_cloud.setStyleSheet(u"background:rgb(91,90,90);")
        self.layout_page_cloud = QHBoxLayout(self.page_cloud)
        self.layout_page_cloud.setSpacing(0)
        self.layout_page_cloud.setObjectName(u"layout_page_cloud")
        self.layout_page_cloud.setContentsMargins(0, 5, 0, 5)
        self.frame_cloud_main = QFrame(self.page_cloud)
        self.frame_cloud_main.setObjectName(u"frame_cloud_main")
        self.frame_cloud_main.setFrameShape(QFrame.StyledPanel)
        self.frame_cloud_main.setFrameShadow(QFrame.Raised)
        self.layout_frame_cloud = QVBoxLayout(self.frame_cloud_main)
        self.layout_frame_cloud.setSpacing(5)
        self.layout_frame_cloud.setObjectName(u"layout_frame_cloud")
        self.layout_frame_cloud.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.cloud_head = QLabel(self.frame_cloud_main)
        self.cloud_head.setObjectName(u"cloud_head")
        self.cloud_head.setMinimumSize(QSize(0, 55))
        self.cloud_head.setMaximumSize(QSize(16777215, 55))
        self.cloud_head.setFont(font18)
        self.cloud_head.setStyleSheet(u"QLabel {\n"
"	color:rgb(255,255,255);\n"
"}")
        self.layout_frame_cloud.addWidget(self.cloud_head)
        # -> Multi-Video Player
        self.multi_video = MultiVideoWidget(self.frame_cloud_main)
        self.plotter = View3dWidget()
        self.vids_gridlayout = QGridLayout(self.frame_cloud_main)
        self.vids_gridlayout.addWidget(self.multi_video, 0, 0, 4, 1)
        self.vids_gridlayout.addWidget(self.plotter, 0, 1, 4, 3)
        self.layout_frame_cloud.addLayout(self.vids_gridlayout)
        # -> Grid Layout: Label + ProgressBar + 2 Buttons
        self.cloud_grid_layout = QGridLayout(self.frame_cloud_main)
        self.cloud_grid_layout.setObjectName(u"cloud_grid_layout")
        self.cloud_grid_layout.setHorizontalSpacing(5)
        self.cloud_grid_layout.setVerticalSpacing(0)
        self.cloud_grid_layout.setContentsMargins(5, 5, 5, 5)
        # -> Run Button
        self.bn_analizer_run = QPushButton(self.frame_cloud_main)
        self.bn_analizer_run.setObjectName(u"bn_analizer_run")
        self.bn_analizer_run.setEnabled(True)
        self.bn_analizer_run.setMinimumSize(QSize(120, 25))
        self.bn_analizer_run.setMaximumSize(QSize(120, 25))
        self.bn_analizer_run.setFont(font12)
        self.bn_analizer_run.setStyleSheet(u"QPushButton {\n"
                                           "	border: 2px solid rgb(51,51,51);\n"
                                           "	border-radius: 5px;	\n"
                                           "	color:rgb(255,255,255);\n"
                                           "	background-color: rgb(51,51,51);\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "	border: 2px solid rgb(112,0,0);\n"
                                           "	background-color: rgb(112,0,0);\n"
                                           "}\n"
                                           "QPushButton:pressed {	\n"
                                           "	border: 2px solid rgb(112,0,0);\n"
                                           "	background-color: rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {	\n"
                                           "	border-radius: 5px;	\n"
                                           "	border: 2px solid rgb(112,112,112);\n"
                                           "	background-color: rgb(112,112,112);\n"
                                           "}")
        self.cloud_grid_layout.addWidget(self.bn_analizer_run, 0, 0, 1, 1)
        # -> Progress Bar
        self.analizer_progress_bar = ProgressAnalizer(self.frame_cloud_main)
        self.analizer_progress_bar.setObjectName(u"analizer_progress_bar")
        self.analizer_progress_bar.setMinimumSize(QSize(150, 40))
        self.analizer_progress_bar.setMaximumSize(QSize(150, 40))
        self.cloud_grid_layout.addWidget(self.analizer_progress_bar, 0, 1, 1, 1)
        # -> Frames Counter Label
        self.count_frames_label = QLabel(self.frame_cloud_main)
        self.count_frames_label.setObjectName(u"bn_cloud_connect")
        self.count_frames_label.setMinimumSize(QSize(160, 25))
        self.count_frames_label.setMaximumSize(QSize(160, 25))
        self.count_frames_label.setFont(font12)
        self.count_frames_label.setStyleSheet(u"QLabel {\n"
                                              "	color:rgb(255,255,255);\n"
                                              "}")
        self.cloud_grid_layout.addWidget(self.count_frames_label, 0, 2, 1, 1)
        # -> Save Button
        self.bn_cloud_save = QPushButton(self.frame_cloud_main)
        self.bn_cloud_save.setObjectName(u"bn_cloud_save")
        self.bn_cloud_save.setEnabled(True)
        self.bn_cloud_save.setMinimumSize(QSize(120, 25))
        self.bn_cloud_save.setMaximumSize(QSize(120, 25))
        self.bn_cloud_save.setFont(font12)
        self.bn_cloud_save.setStyleSheet(u"QPushButton {\n"
                                         "	border: 2px solid rgb(51,51,51);\n"
                                         "	border-radius: 5px;	\n"
                                         "	color:rgb(255,255,255);\n"
                                         "	background-color: rgb(51,51,51);\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "	border: 2px solid rgb(0,143,150);\n"
                                         "	background-color: rgb(0,143,150);\n"
                                         "}\n"
                                         "QPushButton:pressed {	\n"
                                         "	border: 2px solid rgb(0,143,150);\n"
                                         "	background-color: rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:disabled {	\n"
                                         "	border-radius: 5px;	\n"
                                         "	border: 2px solid rgb(112,112,112);\n"
                                         "	background-color: rgb(112,112,112);\n"
                                         "}")
        self.cloud_grid_layout.addWidget(self.bn_cloud_save, 0, 3, 1, 1)
        # -> Spacer
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cloud_grid_layout.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)
        self.layout_frame_cloud.addLayout(self.cloud_grid_layout)

        self.layout_page_cloud.addWidget(self.frame_cloud_main)
        self.stackedWidget.addWidget(self.page_cloud)
        self.layout_frame_main.addWidget(self.stackedWidget)
        self.layout_frame_der.addWidget(self.frame_main)

        # *************** LOWER FRAME ******************
        self.frame_low = QFrame(self.frame_der)
        self.frame_low.setObjectName(u"frame_low")
        self.frame_low.setMinimumSize(QSize(0, 20))
        self.frame_low.setMaximumSize(QSize(16777215, 20))
        self.frame_low.setStyleSheet(u"")
        self.frame_low.setFrameShape(QFrame.NoFrame)
        self.frame_low.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_low)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_tab = QFrame(self.frame_low)
        self.frame_tab.setObjectName(u"frame_tab")
        font10 = QFont()
        font10.setFamily(u"Segoe UI")
        self.frame_tab.setFont(font10)
        self.frame_tab.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_tab.setFrameShape(QFrame.NoFrame)
        self.frame_tab.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_tab)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.tab = QLabel(self.frame_tab)
        self.tab.setObjectName(u"tab")
        font10 = QFont()
        font10.setFamily(u"Segoe UI Light")
        font10.setPointSize(10)
        self.tab.setFont(font10)
        self.tab.setStyleSheet(u"color:rgb(255,255,255);")
        self.horizontalLayout_12.addWidget(self.tab)
        self.horizontalLayout_11.addWidget(self.frame_tab)

        self.frame_drag = QFrame(self.frame_low)
        self.frame_drag.setObjectName(u"frame_drag")
        self.frame_drag.setMinimumSize(QSize(20, 20))
        self.frame_drag.setMaximumSize(QSize(20, 20))
        self.frame_drag.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_drag.setFrameShape(QFrame.NoFrame)
        self.frame_drag.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_drag)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.addWidget(self.frame_drag)

        # *************** ADDING FINAL FRAMES ******************
        self.layout_frame_der.addWidget(self.frame_low)
        self.layout_frame_inferior.addWidget(self.frame_der)
        self.layout_central_widget.addWidget(self.frame_inferior)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(7)
        MainWindow.showMaximized()
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toggle.setText("")
        self.appname.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))

        self.bn_min.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
        self.bn_min.setText("")
        self.bn_max.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
        self.bn_max.setText("")
        self.bn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
        self.bn_close.setText("")
        self.bn_home.setToolTip(QCoreApplication.translate("MainWindow", u"Multi-view Capture", None))
        self.bn_home.setText("")
        self.bn_bug.setToolTip(QCoreApplication.translate("MainWindow", u"Calibration Image Viewer", None))
        self.bn_bug.setText("")
        self.bn_cloud.setToolTip(QCoreApplication.translate("MainWindow", u"Landmarks Detection", None))
        self.bn_cloud.setText("")
        self.home_main_head.setText(QCoreApplication.translate("MainWindow", u"Capture of Multi-view Calibration Images", None))
        self.home_stat_hed.setText(QCoreApplication.translate("MainWindow", u"Captured Image List", None))
        self.about_home.setText(QCoreApplication.translate("MainWindow", u"About: Run Model", None))
        self.viewer_main_head.setText(QCoreApplication.translate("MainWindow", u"Calibration Image Viewer", None))
        self.viewer_aux_head.setText(QCoreApplication.translate("MainWindow", u"Select Image", None))

        self.bn_viewer_open.setText(QCoreApplication.translate("MainWindow", u"Select Folder", None))
        self.bn_viewer_next.setText(QCoreApplication.translate("MainWindow", u"Next Image", None))
        self.bn_viewer_delete.setText(QCoreApplication.translate("MainWindow", u"Delete Image", None))
        self.cloud_head.setText(QCoreApplication.translate("MainWindow", u"Multi-view Single-user Landmarks Detection", None))
        self.bn_analizer_run.setText(QCoreApplication.translate("MainWindow", u"Run Analizer", None))
        self.bn_cloud_save.setText(QCoreApplication.translate("MainWindow", u"Play Scene", None))

        self.count_frames_label.setText(QCoreApplication.translate("MainWindow", u"Frames: ", None))
        self.tab.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.frame_drag.setToolTip(QCoreApplication.translate("MainWindow", u"Drag", None))
    # retranslateUi

    def returnCameraIndexes(self):
        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr


class TimerThread(QThread):
    countChanged = pyqtSignal(float)

    def __init__(self, time_limit):
        super().__init__()
        self.run_flag = True
        self.TIME_LIMIT = time_limit

    def run(self):
        count = 0
        while count < self.TIME_LIMIT and self.run_flag:
            count += 0.01
            time.sleep(0.01)
            self.countChanged.emit(count)

    def stop(self):
        """Waits for thread to finish"""
        self.run_flag = False
        self.wait()


class ProgressTimer(QWidget):
    timerEnded = pyqtSignal(bool)

    def __init__(self, parent, time_limit):
        super(ProgressTimer, self).__init__(parent)
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

        self.TIME_LIMIT = time_limit

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.progress_bar)
        self.setLayout(self.main_layout)  # set the vbox layout as the widgets layout

        self.thread = TimerThread(self.TIME_LIMIT)
        self.thread.countChanged.connect(self.onCountChanged)

    def onCountChanged(self, value):
        if self.thread.isFinished():
            self.progress_bar.setValue(0)
        if self.thread.isRunning():
            self.progress_bar.setValue(value*100.0/self.TIME_LIMIT)
        if value >= self.TIME_LIMIT:
            self.timerEnded.emit(True)

