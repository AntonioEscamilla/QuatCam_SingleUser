###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                        PURPOSE:    WINDOWS/LINUX/MACOS FLAT MODERN UI               ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################
import numpy as np
import cv2
import json
import os
import ntpath
from MultiCamSystem import build_multi_camera_system, triangulate_poses, triangulate_frame_pose
from about import *
from datetime import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QFileDialog
from PyQt5.QtCore import QTimer, QEasingCurve, QPropertyAnimation, Qt, QEvent, pyqtSlot
from ExtrinsicsTransformation import transform_rotation, transform_translation
from ExtrinsicsUtils import cam_pose

GLOBAL_STATE = 1  # NECESSARY FOR CHECKING WEATHER THE WINDOW IS FULL SCREEN OR NOT
GLOBAL_TITLE_BAR = True  # NECESSARY FOR CHECKING WEATHER THE WINDOW IS FULL SCREEN OR NOT
init = False  # NECESSARY FOR INITIATION OF THE WINDOW.


# THIS CLASS HOUSES ALL FUNCTION NECESSARY FOR OUR PROGRAMME TO RUN.
class UIFunction:

    # ----> INITIAL FUNCTION TO LOAD THE FRONT STACK WIDGET AND TAB BUTTON I.E. HOME PAGE
    # INITIALISING THE WELCOME PAGE TO: HOME PAGE IN THE STACKEDWIDGET, SETTING THE BOTTOM LABEL AS THE PAGE NAME, SETTING THE BUTTON STYLE.
    def initStackTab(self):
        global init
        if not init:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.tab.setText("Start multi-view streaming. Click on 'Capture Images' to take synchronized photos of calibration pattern")
            self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            init = True

    ################################################################################################

    # ------> SETTING THE APPLICATION NAME IN OUR CUSTOM MADE TAB, WHERE LABEL NAMED: appname()
    def labelTitle(self, appName):
        self.ui.appname.setText(appName)

    ################################################################################################

    # ----> MAXIMISE/RESTORE FUNCTION
    # THIS FUNCTION MAXIMISES OUR MAIN WINDOW WHEN THE MAXIMISE BUTTON IS PRESSED OR IF DOUBLE MOUSE LEFT PRESS IS DOES OVER THE TOP FRAME.
    # THIS MAKE THE APPLICATION TO OCCUPY THE WHOLE MONITOR.
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.bn_max.setToolTip("Restore")
            self.ui.bn_max.setIcon(QIcon("icons/1x/restore.png"))  # CHANGE THE MAXIMISE ICON TO RESTORE ICON
            self.ui.frame_drag.hide()  # HIDE DRAG AS NOT NECESSARY
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(1280, 900)
            self.ui.bn_max.setToolTip("Maximize")
            self.ui.bn_max.setIcon(QIcon("icons/1x/max.png"))  # CHANGE BACK TO MAXIMISE ICON
            self.ui.frame_drag.show()

    ################################################################################################

    # ----> RETURN STATUS MAX OR RESTORE
    # NECESSARY FOR THE MAXIMISE FUNCTION TO WORK.
    @staticmethod
    def returnStatus():
        return GLOBAL_STATE

    @staticmethod
    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # ------> TOGGLE MENU FUNCTION
    # THIS FUNCTION TOGGLES THE MENU BAR TO DOUBLE THE LENGTH OPENING A NEW ARE OF ABOUT TAB IN FRONT.
    # ALSO IT SETS THE ABOUT>HOME AS THE FIRST PAGE.
    # IF THE PAGE IS IN THE ABOUT PAGE THEN PRESSING AGAIN WILL RESULT IN UNDOING THE PROCESS AND COMING BACK TO THE
    # HOME PAGE.
    def toggleMenu(self, maxWidth, clicked):

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS : I.E. MAKING THEN NORMAL COLOR THAN LIGHTER COLOR.
        for each in self.ui.frame_izq.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if clicked:
            currentWidth = self.ui.frame_izq.width()  # Reads the current width of the frame
            minWidth = 80  # MINIMUM WIDTH OF THE BOTTOM_WEST FRAME
            if currentWidth == 80:
                extend = maxWidth
                # ----> MAKE THE STACKED WIDGET PAGE TO ABOUT HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.tab.setText("About > Multi-view Human-body 3D Landmarks Detection")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
                self.ui.bn_bug.setVisible(False)
                self.ui.bn_cloud.setVisible(False)
            else:
                extend = minWidth
                # -----> REVERT THE ABOUT HOME PAGE TO NORMAL HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.tab.setText("Start multi-view streaming. Click on 'Capture Images' to take synchronized photos of calibration pattern")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
                self.ui.bn_bug.setVisible(True)
                self.ui.bn_cloud.setVisible(True)
            # THIS ANIMATION IS RESPONSIBLE FOR THE TOGGLE TO MOVE IN A SOME FIXED STATE.
            self.animation = QPropertyAnimation(self.ui.frame_izq, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(minWidth)
            self.animation.setEndValue(extend)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    ################################################################################################

    # -----> DEFAULT ACTION FUNCTION
    def constantFunction(self):
        # -----> DOUBLE CLICK RESULT IN MAXIMISE OF WINDOW
        def maxDoubleClick(stateMouse):
            if stateMouse.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

        # ----> REMOVE NORMAL TITLE BAR
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick
        # ----> SHOW NORMAL TITLE BAR
        # self.ui.frame_close.hide()
        # self.ui.frame_max.hide()
        # self.ui.frame_min.hide()
        # self.ui.frame_drag.hide()

        # SINCE THERE IS NO WINDOWS TOP BAR, THE CLOSE MIN, MAX BUTTON ARE ABSENT AND SO THERE IS A NEED FOR THE ALTERNATIVE BUTTONS IN OUR
        # DIALOG BOX, WHICH IS CARRIED OUT BY THE BELOW CODE
        # -----> MINIMIZE BUTTON FUNCTION
        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

        # -----> MAXIMIZE/RESTORE BUTTON FUNCTION
        self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))

        # -----> CLOSE APPLICATION FUNCTION BUTTON
        self.ui.bn_close.clicked.connect(lambda: APFunction.custom_close(self))

    # ----> BUTTON IN TAB PRESSED EXECUTES THE CORRESPONDING PAGE IN STACKED WIDGET PAGES
    def buttonPressed(self, buttonName):

        index = self.ui.stackedWidget.currentIndex()

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS I.E. FROM THE LITER COLOR TO THE SAME BG COLOR I.E. TO CHANGE THE HIGHLIGHT.
        for each in self.ui.frame_izq.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if buttonName == 'bn_home':
            if self.ui.frame_izq.width() == 80 and index != 0:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.tab.setText("Start multi-view streaming. Click on 'Capture Images' to take synchronized photos of calibration pattern")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_izq.width() == 160 and index != 1:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.tab.setText("About > Multi-view Human-body 3D Landmarks Detection")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName == 'bn_bug':
            if self.ui.frame_izq.width() == 80 and index != 5:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_image_view)
                self.ui.tab.setText("Choose folder to load calibration images. Select a row in the table to delete images from calibration dataset")
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName == 'bn_cloud':
            if self.ui.frame_izq.width() == 80 and index != 6:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_cloud)
                self.ui.tab.setText("Click on 'Run Analizer' to generate detections file for a video. Click on 'Play Scene' to show Multi-view Single-user 3D Landmarks")
                self.ui.frame_cloud.setStyleSheet("background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

    ########################################################################################################################

    ########################################################################################################################

    # ----> STACK WIDGET EACH PAGE FUNCTION PAGE FUNCTIONS
    # CODE TO PERFORM THE TASK IN THE STACKED WIDGET PAGE
    # WHAT EVER WIDGET IS IN THE STACKED PAGES ITS ACTION IS EVALUATED HERE AND THEN THE REST FUNCTION IS PASSED.
    def stackPage(self):

        ######### PAGE_HOME #############
        self.ui.home_open_bn.clicked.connect(lambda: APFunction.openBtnClicked(self))
        self.ui.home_close_bn.clicked.connect(lambda: APFunction.closeBtnClicked(self))
        self.ui.home_run_bn.clicked.connect(lambda: APFunction.runBtnClicked(self))
        self.ui.time_bar.timerEnded.connect(lambda: APFunction.timerFinished(self, 'page_home'))
        self.ui.one.update_image_list_signal.connect(lambda: APFunction.updateImageStats(self))

        ######### PAGE IMAGE VIEWER ##############
        self.ui.bn_viewer_open.clicked.connect(lambda: APFunction.selectViewerFolder(self))
        self.ui.bn_viewer_next.clicked.connect(lambda: APFunction.nextViewerImage(self))
        self.ui.bn_viewer_delete.clicked.connect(lambda: APFunction.deleteViewerImage(self))
        self.ui.viewer_image_table.tableWidget.selectionModel().selectionChanged.connect(lambda: APFunction.newTableSel(self))

        #########PAGE CLOUD #############
        self.ui.bn_analizer_run.clicked.connect(lambda: APFunction.runAnalizer(self))
        self.ui.bn_cloud_save.clicked.connect(lambda: APFunction.playVideosBtn(self))
        self.ui.multi_video.frame_counter_signal.connect(lambda: APFunction.newMultiVideoFrame(self))

        ##########PAGE: ABOUT HOME #############
        self.ui.text_about_home.setVerticalScrollBar(self.ui.vsb_about_home)
        self.ui.text_about_home.setText(aboutHome)
    ################################################################################################################################

    # -----> FUNCTION TO SHOW CORRESPONDING STACK PAGE WHEN THE ANDROID BUTTONS ARE PRESSED: CONTACT, GAME, CLOUD, WORLD
    # SINCE THE ANDROID PAGE AHS A SUB STACKED WIDGET WIT FOUR MORE BUTTONS, ALL THIS 4 PAGES CONTENT: BUTTONS, TEXT, LABEL E.T.C ARE INITIALIZED OVER HERE.
    def androidStackPages(self, page):
        # ------> THIS LINE CLEARS THE BG COLOR OF PREVIOUS TABS
        for each in self.ui.frame_android_menu.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if page == "page_contact":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_contact)
            self.ui.tab.setText("OSC Settings")
            self.ui.frame_android_contact.setStyleSheet("background:rgb(91,90,90)")

        # ADD A ADDITIONAL ELIF STATEMENT WITH THE SIMILAR CODE UP ABOVE FOR YOUR NEW SUBMENU BUTTON IN THE ANDROID STACK PAGE.
    ##############################################################################################################

# ------> CLASS WHERE ALL THE ACTION OF TH SOFTWARE IS PERFORMED:
# THIS CLASS IS WHERE THE APPLICATION OF THE UI OR THE BRAIN OF THE SOFTWARE GOES
# UNTIL NOW WE SPECIFIED THE BUTTON CLICKS, SLIDERS, E.T.C WIDGET, WHOSE APPLICATION IS EXPLORED HERE. THOSE FUNCTION WHEN DONE IS
# REDIRECTED TO THIS AREA FOR THE PROCESSING AND THEN THE RESULT ARE EXPORTED.
# REMEMBER THE SOFTWARE UI HAS A FUNCTION WHOSE CODE SHOULD BE HERE
class APFunction:

    def custom_close(self):
        if self.ui.one.thread.isRunning():
            print('closing video thread')
            self.ui.one.thread.stop()

        if self.ui.two.thread.isRunning():
            print('closing video thread')
            self.ui.two.thread.stop()

        if self.ui.three.thread.isRunning():
            print('closing video thread')
            self.ui.three.thread.stop()

        if self.ui.four.thread.isRunning():
            print('closing video thread')
            self.ui.four.thread.stop()

        self.close()

    def openBtnClicked(self):
        if not self.ui.one.thread.isRunning():
            self.ui.one.thread.run_flag = True
            self.ui.one.thread.start()
        if not self.ui.two.thread.isRunning():
            self.ui.two.thread.run_flag = True
            self.ui.two.thread.start()
        if not self.ui.three.thread.isRunning():
            self.ui.three.thread.run_flag = True
            self.ui.three.thread.start()
        if not self.ui.four.thread.isRunning():
            self.ui.four.thread.run_flag = True
            self.ui.four.thread.start()

        self.ui.home_run_bn.setEnabled(True)

    def closeBtnClicked(self):
        self.ui.time_bar.thread.stop()
        self.ui.time_bar.progress_bar.setValue(0)
        self.ui.home_run_bn.setEnabled(False)

        if self.ui.one.thread.isRunning():
            self.ui.one.thread.stop()
            if self.ui.one.main_state == 1:
                self.ui.one.main_state = 0
        if self.ui.two.thread.isRunning():
            self.ui.two.thread.stop()
            if self.ui.two.main_state == 1:
                self.ui.two.main_state = 0
        if self.ui.three.thread.isRunning():
            self.ui.three.thread.stop()
            if self.ui.three.main_state == 1:
                self.ui.three.main_state = 0
        if self.ui.four.thread.isRunning():
            self.ui.four.thread.stop()
            if self.ui.four.main_state == 1:
                self.ui.four.main_state = 0

    def runBtnClicked(self):
        self.ui.time_bar.thread.run_flag = True
        self.ui.time_bar.thread.start()
        self.ui.time_bar.progress_bar.setValue(0)

        if self.ui.one.main_state == 0:
            if not self.ui.one.thread.isRunning():
                print("Starting video thread")
                self.ui.one.thread.run_flag = True
                self.ui.one.thread.start()

            self.ui.one.main_state = 1

        if self.ui.two.main_state == 0:
            if not self.ui.two.thread.isRunning():
                print("Starting video thread")
                self.ui.two.thread.run_flag = True
                self.ui.two.thread.start()

            self.ui.two.main_state = 1

        if self.ui.three.main_state == 0:
            if not self.ui.three.thread.isRunning():
                print("Starting video thread")
                self.ui.three.thread.run_flag = True
                self.ui.three.thread.start()

            self.ui.three.main_state = 1

        if self.ui.four.main_state == 0:
            if not self.ui.four.thread.isRunning():
                print("Starting video thread")
                self.ui.four.thread.run_flag = True
                self.ui.four.thread.start()

            self.ui.four.main_state = 1

    def timerFinished(self, page):
        if page == 'page_home':
            self.ui.time_bar.progress_bar.setValue(0)
            self.ui.time_bar.thread.start()
            APFunction.saveImages(self)

    def saveImages(self):
        self.ui.one.saved_img_counter += 1
        self.ui.two.saved_img_counter += 1
        self.ui.three.saved_img_counter += 1
        self.ui.four.saved_img_counter += 1

        print('saving actual frame for all cameras as image{:02d}.jpg'.format(self.ui.one.saved_img_counter))
        ts = "image{:02d}.jpg".format(self.ui.one.saved_img_counter)

        cv2.imwrite(self.ui.one.output_dir + ts, self.ui.one.get_image())
        cv2.imwrite(self.ui.two.output_dir + ts, self.ui.two.get_image())
        cv2.imwrite(self.ui.three.output_dir + ts, self.ui.three.get_image())
        cv2.imwrite(self.ui.four.output_dir + ts, self.ui.four.get_image())

        self.ui.one.image_features.append(ts)
        self.ui.one.update_image_list_signal.emit(True)

    def updateImageStats(self):
        line = ''
        for v in self.ui.one.image_features:
            line += "\n" + "file: " + v

        self.ui.image_list.setText(line)

    def selectViewerFolder(self):
        self.ui.image_visualizer.open_directory_callback()
        self.ui.bn_viewer_next.setEnabled(True)
        self.ui.bn_viewer_delete.setEnabled(True)
        self.ui.viewer_image_table.updateTable(self.ui.image_visualizer.list_of_images)

    def nextViewerImage(self):
        self.ui.image_visualizer.next_button_callback()
        self.ui.viewer_image_table.update_selection(self.ui.image_visualizer.image_idx)

    def deleteViewerImage(self):
        if not len(self.ui.viewer_image_table.tableWidget.selectedIndexes()):
            return

        row_to_del = self.ui.viewer_image_table.tableWidget.selectedIndexes()[0].row()

        # delete image from cam folders
        file_to_del = self.ui.image_visualizer.list_of_images[row_to_del]
        for folder in self.ui.image_visualizer.folders_list:
            path_to_del = os.path.join(folder, file_to_del)
            if os.path.exists(path_to_del):
                os.remove(path_to_del)
                print(f"The file {file_to_del} was deleted from folder {folder}")
            else:
                print("The file does not exist")

        # remove row from table and update image shown
        self.ui.viewer_image_table.remove_row(row_to_del)
        self.ui.image_visualizer.list_of_images.pop(row_to_del)
        if row_to_del == len(self.ui.image_visualizer.list_of_images):
            self.ui.image_visualizer.show_selected_image(row_to_del - 1)
        else:
            self.ui.image_visualizer.show_selected_image(row_to_del)

    def newTableSel(self):
        item = self.ui.viewer_image_table.tableWidget.selectedIndexes()[0]
        if len(self.ui.image_visualizer.list_of_images) > item.row():
            self.ui.image_visualizer.show_selected_image(item.row())

    def runAnalizer(self):
        path = QFileDialog.getOpenFileName()[0]
        self.ui.analizer_progress_bar.analizer.set_video_path(path)
        self.ui.analizer_progress_bar.analizer.start()

    def playVideosBtn(self):
        scene_dir = QFileDialog.getExistingDirectory(self, "Open a folder", "./", QFileDialog.ShowDirsOnly)
        self.ui.multi_video.thread.set_video_path(scene_dir + '/videos')
        self.ui.multi_video.set_metadata(scene_dir + '/detections')

        multi_cam_calibration_data = APFunction.read_calibration_data(scene_dir + '/calibration.json', self.ui.multi_video.get_metadata())
        multi_cam_calibration_data = APFunction.transform_calibration_data(multi_cam_calibration_data)
        self.camera_system = build_multi_camera_system(multi_cam_calibration_data)
        self.ui.plotter.plot_system(self.camera_system, scale=0.2, axes_size=0.4)

        # self.world_poses = triangulate_poses(self.camera_system, self.ui.multi_video.get_detections(), self.ui.multi_video.get_metadata())
        # for poses_dict in self.world_poses:
        #     print(poses_dict)
        # print(f'len of world poses = {len(self.world_poses)}')

        self.ui.multi_video.thread.start()

    @staticmethod
    def transform_calibration_data(multi_cam_calibration_data):
        # ----------- new R,T from chArUco board in ground plane -----------#
        R1w = np.asarray([[0.906657, -0.41233829, 0.08916402],
                          [-0.12746963, -0.46923809, -0.87382327],
                          [0.40214994, 0.78089228, -0.47799861]])
        T1w = np.asarray([[-0.31621033],
                          [0.99795041],
                          [2.26775274]])
        multi_cam_calibration_data[0]['translation'] = T1w
        multi_cam_calibration_data[0]['Q'] = R1w

        # ----------- new R,T based on chArUco board in ground plane -----------#
        # read calibration data: cam1 as seen from cam2
        R21 = multi_cam_calibration_data[1]['Q']
        T21 = multi_cam_calibration_data[1]['translation']
        # obtain inverse transformation: cam2 as seen from cam 1
        T12 = cam_pose(R21, T21)
        R12 = R21.T
        # transform operation: ground plane as seen from cam2
        multi_cam_calibration_data[1]['translation'] = transform_translation(T1w, R12, T12)
        multi_cam_calibration_data[1]['Q'] = transform_rotation(R1w, R12)

        # ----------- new R,T based on chArUco board in ground plane -----------#
        # read calibration data: cam1 as seen from cam3
        R31 = multi_cam_calibration_data[2]['Q']
        T31 = multi_cam_calibration_data[2]['translation']
        # obtain inverse transformation: cam2 as seen from cam 1
        T13 = cam_pose(R31, T31)
        R13 = R31.T
        # transform operation: ground plane as seen from cam3
        multi_cam_calibration_data[2]['translation'] = transform_translation(T1w, R13, T13)
        multi_cam_calibration_data[2]['Q'] = transform_rotation(R1w, R13)

        # ----------- new R,T based on chArUco board in ground plane -----------#
        R41 = multi_cam_calibration_data[3]['Q']
        T41 = multi_cam_calibration_data[3]['translation']
        # obtain inverse transformation: cam2 as seen from cam 1
        T14 = cam_pose(R41, T41)
        R14 = R41.T
        # transform operation: ground plane as seen from cam2
        multi_cam_calibration_data[3]['translation'] = transform_translation(T1w, R14, T14)
        multi_cam_calibration_data[3]['Q'] = transform_rotation(R1w, R14)

        return multi_cam_calibration_data

    @staticmethod
    def read_calibration_data(json_file, videos_metadata):
        with open(json_file) as f:
            data = json.load(f)

        multi_cam_calibration_data = []
        for metadata in videos_metadata:
            calibration_data = {}
            name = metadata['name']
            calibration_data['name'] = name
            P = np.zeros((3, 4))
            P[:3, :3] = np.asarray(data['cameras'][name]['K'])
            calibration_data['height'] = metadata['height']
            calibration_data['width'] = metadata['width']
            calibration_data['P'] = P
            calibration_data['K'] = np.asarray(data['cameras'][name]['K'])
            calibration_data['D'] = np.asarray(data['cameras'][name]['dist']).reshape((5,))
            calibration_data['R'] = np.array([[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])

            keys_list = sorted(data['camera_poses'])
            calibration_data['translation'] = np.asarray(data['camera_poses'][keys_list[int(name.split('cam')[1]) - 1]]['T'])
            calibration_data['Q'] = np.asarray(data['camera_poses'][keys_list[int(name.split('cam')[1]) - 1]]['R'])
            multi_cam_calibration_data.append(calibration_data)

        return multi_cam_calibration_data

    def newMultiVideoFrame(self):
        frame_as_idx = self.ui.multi_video.frame_counter - 1
        if frame_as_idx + 1 <= self.ui.multi_video.get_detections_length():
            self.ui.count_frames_label.setText('Frames: {} of {}'.format(frame_as_idx + 1, self.ui.multi_video.get_detections_length()))
            self.ui.plotter.plot_pose(triangulate_frame_pose(self.camera_system, self.ui.multi_video.get_detections_in_frame(frame_as_idx), self.ui.multi_video.get_metadata()))

###############################################################################################################################################################
