###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

from PyQt5.QtCore import Qt
from PyQt5.Qt import QTableWidgetItem, QAbstractItemView
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QFileDialog, QTableWidget, QHeaderView, QFrame
from PyQt5.QtGui import QPixmap, QBrush, QColor, QFont
import os


class ImageViewerWidget(QWidget):

    def __init__(self, parent):
        super(ImageViewerWidget, self).__init__(parent)
        self.images_dir = None
        self.folders_list = []
        self.list_of_images = []
        self.image_idx = 0

        layout = QGridLayout()

        self.labels = []
        self.layout_pos = [[0, 0], [0, 1], [1, 0], [1, 1]]
        for p in self.layout_pos:
            label = QLabel()
            label.setMinimumSize(200, 200)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label, p[0], p[1], 1, 1)
            self.labels.append(label)
        self.setLayout(layout)

    def open_directory_callback(self):
        # Open a File Dialog and select the folder path
        dialog = QFileDialog()
        self.images_dir = dialog.getExistingDirectory(None, "Select Folder")
        self.folders_list = [self.images_dir + '/' + folder for folder in os.listdir(self.images_dir)]

        # Get the list of images in the folder and read using matplotlib and print its shape
        self.list_of_images = os.listdir(self.folders_list[0])
        self.list_of_images = sorted(self.list_of_images)

        # Length of Images
        print('Number of Images in the selected folder: {}'.format(len(self.list_of_images)))

        # Show the first four Images in the same window.
        for i in range(4):
            pixmap = QPixmap('{}\\{}'.format(self.folders_list[i], self.list_of_images[0]))
            pixmap = pixmap.scaled(self.labels[i].width(), self.labels[i].height(), Qt.KeepAspectRatio)
            self.labels[i].setPixmap(pixmap)
            self.labels[i].show()

        self.image_idx = 0

    def show_selected_image(self, row):
        if self.list_of_images is None:
            return

        total_images = len(self.list_of_images)
        row = row % total_images
        for i in range(4):
            pixmap = QPixmap('{}\\{}'.format(self.folders_list[i], self.list_of_images[row]))
            pixmap = pixmap.scaled(self.labels[i].width(), self.labels[i].height(), Qt.KeepAspectRatio)
            self.labels[i].setPixmap(pixmap)
            self.labels[i].show()

        self.image_idx = row

    def next_button_callback(self):
        # Total Images in List
        total_images = len(self.list_of_images)

        if self.list_of_images:
            try:
                self.image_idx = (self.image_idx + 1) % total_images
                img = self.list_of_images[self.image_idx]
                for i in range(4):
                    pixmap = QPixmap('{}\\{}'.format(self.folders_list[i], img))
                    pixmap = pixmap.scaled(self.labels[i].width(), self.labels[i].height(), Qt.KeepAspectRatio)
                    self.labels[i].setPixmap(pixmap)
                    self.labels[i].show()

            except ValueError as e:
                print('The selected folder does not contain any images')


class ImageTable(QWidget):
    def __init__(self, parent):
        super(ImageTable, self).__init__(parent)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)
        font10 = QFont()
        font10.setFamily(u"Segoe UI Regular")
        font10.setPointSize(10)
        self.tableWidget.setFont(font10)
        self.tableWidget.horizontalHeader().setFont(font10)
        self.tableWidget.verticalHeader().setFont(font10)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setStyleSheet(u"QScrollBar:vertical {background:rgb(51,51,51);width:20px;margin: 0px 0px 0px 0px;}\n"
                                       "QScrollBar::handle:vertical {background:rgb(0,143,150);}\n"
                                       "QTableWidget QTableCornerButton::section {background-color:rgb(51,51,51); }\n"
                                       "QScrollBar::add-page:vertical {background:rgb(51,51,51);}\n"
                                       "QScrollBar::sub-page:vertical {background:rgb(51,51,51);}")
        self.tableWidget.setFrameStyle(QFrame.NoFrame)
        stylesheet = "::section{Background-color:rgb(51,51,51);color:rgb(255,255,255)}"
        self.tableWidget.verticalHeader().setStyleSheet(stylesheet)
        self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget.setHorizontalHeaderLabels('Cam 1;Cam 2;Cam 3;Cam 4'.split(';'))
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        self.tableWidget.setCornerButtonEnabled(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.tableWidget.resize(self.parent().size().width() - 10, self.parent().size().height() - 80)

    def updateTable(self, imageList):
        self.tableWidget.setRowCount(len(imageList))
        for row, name in enumerate(imageList):
            for col in range(4):
                item = QTableWidgetItem()
                item.setText(name.split('.')[0])
                item.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(row, col, item)

    def update_selection(self, row):
        self.tableWidget.selectRow(row)

    def remove_row(self, row):
        self.tableWidget.removeRow(row)
