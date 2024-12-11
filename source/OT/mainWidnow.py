from source.OT.ScreenReader import ScreenReader
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtWidgets import (
    QWidget,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QSpinBox,
    QLineEdit
)

import subWindow as sb
import viewFrame
import monitorFrame
image_folder = 'resource'

class MyApp(QMainWindow):
    fname = None
    extensionFile = ".jpg"
    extensionVideo = ".avi"
    def __init__(self):
        super().__init__()
        self.w = sb.subWindow()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Video Maker')
        self.setWindowIcon(QIcon('../../resource/logo.ico'))
        self.setGeometry(200,200,650,600)

        vbox= QVBoxLayout()
        vbox.addWidget(monitorFrame.monitorFrame().monitorFrame())
        vbox.addWidget(self.mainFrame())
        vbox.addWidget(self.findFileFrame())

        widget = QWidget()
        widget.setLayout(vbox)

        self.setCentralWidget(widget)
        self.show()
        self.w.show()


    def mainFrame(self):
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.controlFrame())
        hbox1.addWidget(viewFrame.viewFrame.viewInit(viewFrame))

        widget2 = QWidget()
        widget2.setLayout(hbox1)
        return widget2
    def viewFrame(self):
        vbox2 = QVBoxLayout()
        # vbox2.addWidget()

        vF = QWidget()
        vF.setLayout(vbox2)
        return vF
    def controlFrame(self):
        vbox3 = QVBoxLayout()
        # vbox3.addWidget()

        cF = QWidget()
        cF.setLayout(vbox3)
        return cF
    def findFileFrame(self):
        buttonF = QPushButton("  Select Folder  ", self)
        buttonR = QPushButton("  Run  ", self)
        buttonP = QPushButton(" Play ", self)
        lbl_status0 = QLabel("Status : ", self)
        self.lbl_status = QLabel(" . . . ", self)
        self.le_timer = QSpinBox()
        self.le_timer.setFixedWidth(120)
        self.le_timer.setValue(1000)
        self.le_timer.setRange(0, 10000)
        self.le_timer.setAlignment(Qt.AlignCenter)

        self.le_timer.valueChanged.connect(self.onActivated3)
        buttonF.clicked.connect(self.btn_Find_Folder)
        buttonR.clicked.connect(self.btn_Run_Maker)
        buttonP.clicked.connect(self.btn_Play_Video)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(buttonF)
        vbox1.addWidget(buttonR)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(lbl_status0)
        hbox1.addWidget(self.lbl_status)
        tmpWidget = QWidget()
        tmpWidget.setLayout(hbox1)
        vbox1.addWidget(tmpWidget)
        vbox1.addWidget(buttonP)
        vbox1.addWidget(self.le_timer)

        frame01 = QWidget()
        frame01.setLayout(vbox1)
        return frame01
    def onActivated3(self, text):
        self.w.timerChange(self.le_timer.value())
    def onActivated(self, text):
        self.extensionFile = text
    def onActivated2(self, text):
        self.extensionVideo = text
    def btn_Play_Video(self):
        dialog = self.w
        dialog.show()
        return 0
    def btn_Find_Folder(self):
        self.fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        print(self.fname)
        self.lbl_status.setText("Load File")
        return 0
    def btn_Run_Maker(self):
        self.w.setDir(self.fname)
    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        if key == Qt.Key_H:
            if self.w.isHidden():
                self.w.show()
            else:
                self.w.hide()