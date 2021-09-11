###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                        PURPOSE:    WINDOWS/LINUX/MACOS FLAT MODERN UI               ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import *

from ui_main import Ui_MainWindow
from ui_function import UIFunction


# APPLICATION MAIN WINDOW :
# -----> MAIN APPLICATION CLASS
class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ----> SET WINDOW TITLE AND ICON
        application_name = "QuatCam: Single-user 3D Pose Estimator"
        self.setWindowTitle(application_name)  
        UIFunction.labelTitle(self, application_name)  
        ###############################

        # -----> INITIAL STACKED WIDGET PAGE WIDGET AND TAB
        # THIS MAKE THE INITIAL WINDOW OF OUR APPLICATION, I.E. THE FIRST PAGE OR THE WELCOME PAGE/SCREEN            ---------(C5)
        # IN OUR APPLICATION THIS IS THE MENU BAR, TOGGLE SWITCH, MIN, MAX, CLOSE BUTTONS, AND THE HOME PAGE.
        # ALL THIS GET INITIALISED HERE.
        # SINCE ALL THE FUNCTION RELATED STUFF IS DONE IN THE ui_function.py FILE, IT GOES THERE
        # REMEMBER THIS FUNCTION CAN ALSO BE DONE HERE, BUT DUE TO CONVENIENCE IT IS SHIFTED TO A NEW FILE.
        UIFunction.initStackTab(self)
        ############################################################

        # ----> CERTAIN TOOLS LIKE DRAG, MAXIMISE, MINIMISE, CLOSE AND HIDING OF THE WINDOWS TOP BAR
        # THIS WINDOW INITIALISES THE BUTTONS NECESSARY FOR THE MAIN WINDOW LIKE: CLOSE, MIN, MAX E.T.C.                ---------(C6)
        UIFunction.constantFunction(self)
        #############################################################

        # ----> TOGGLE THE MENU HERE
        # THIS CODE DETECTS THE BUTTON IN THE RIGHT TOP IS PRESSED OR NOT AND IF PRESSED IT CONNECT  TO A FUNCTION IN THE ui_function.py                 ---------(C7)
        # FILE, WHICH EXPANDS THE MENU BAR TO DOUBLE ITS WIDTH MAKING ROOM FOR THE ABOUT PAGES.
        # THIS EFFECT CALLED AS TOGGLE, CAN BE MADE USE IN MANY WAYS. CHECK THE FUNCTION: toggle Menu: IN THE ui_function.py
        # FILE FOR THE CLEAR WORKING
        self.ui.toggle.clicked.connect(lambda: UIFunction.toggleMenu(self, 160, True))
        #############################################################

        # ----> MENU BUTTON PRESSED EVENTS
        # NOW SINCE OUR DEMO APPLICATION HAS ONLY 4 MENU BUTTONS: Home, Bug, Android, Cloud, WHEN USER PRESSES IT THE FOLLOWING CODE             ---------(C8)
        # REDIRECTS IT TO THE ui_function.py FILE buttonPressed() FUNCTION TO MAKE THE NECESSARY RESPONSES TO THE BUTTON PRESSED.
        # IT TAKES SELF AND THE BUTTON NAME AS THE ARGUMENT, THIS IS ONLY TO RECOGNISE WHICH BUTTON IS PRESSED BY THE buttonPressed() FUNCTION.
        self.ui.bn_home.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_home'))
        self.ui.bn_bug.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_bug'))
        self.ui.bn_cloud.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_cloud'))
        #############################################################

        # -----> STACK PAGE FUNCTION
        # OUR APPLICATION CHANGES THE PAGES BY USING THE STACKED WIDGET, THIS CODE POINTS TO A FUNCTION IN ui_function.py FILE             ---------(C9)
        # WHICH GOES AND SETS THE DEFAULT IN THESE PAGES AND SEARCHES FOR THE RESPONSES MADE BY THE USER IN THE CORRESPONDING PAGES.
        UIFunction.stackPage(self)
        #############################################################

        # ---> MOVING THE WINDOW WHEN LEFT MOUSE PRESSED AND DRAGGED OVER APP NAME LABEL
        # SAME TO SAY AS IN COMMENT (C2)
        self.dragPos = self.pos()

        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunction.returnStatus() == 1:
                UIFunction.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE: WE CHOOSE THE TOPMOST FRAME WHERE THE APPLICATION NAME IS PRESENT AS THE AREA TO MOVE THE WINDOW.
        self.ui.frame_appname.mouseMoveEvent = moveWindow  # CALLING THE FUNCTION TO CHANGE THE POSITION OF THE WINDOW DURING MOUSE DRAG

    # ----> FUNCTION TO CAPTURE THE INITIAL POSITION OF THE MOUSE: NECESSARY FOR THE moveWindow FUNCTION
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    #############################################################

    def eventFilter(self, source, event):
        if source == self.ui.line_class_name and event.type() == QEvent.MouseButtonDblClick:
            self.ui.line_class_name.setEnabled(True)
            self.ui.line_class_name.setFocus()
            self.ui.bn_add_class.setEnabled(True)
        return super(MainWindow, self).eventFilter(source, event)
    #############################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

############################################################################################################################################################
