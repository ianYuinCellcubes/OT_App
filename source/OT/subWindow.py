import os
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QMainWindow,
    QHBoxLayout
)
from source.OT.ScreenReader import ScreenReader
class subWindow(QMainWindow):
    dataFolder = None
    counter = 0
    filelist = [0]
    frameOnOff = 0
    monitorSelect = 0
    rslX = 3840
    rslY = 3840
    def __init__(self, parent=None):
        super(subWindow, self).__init__(parent)
        self.m = ScreenReader.monitor
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Projector')

        self.lbl_dir_fileName = QLabel("test")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.lbl_dir_fileName)

        widget = QWidget()
        widget.setLayout(hbox1)
        self.setCentralWidget(widget)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(0,0, 4095,4095)
        self.setWindowFlag(Qt.FramelessWindowHint, True)

        self.show()
    def timerChange(self, index):
        self.timer.stop()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(index)
    def keyPressEvent(self, event):
        key = event.key()
        print(key)
            # self.FramelessOption()
        if key == Qt.Key_H:
            self.hideOption()
    def hideOption(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
    # def FramelessOption(self):
    #     if self.frameOnOff == 1:
    #         self.setWindowFlag(Qt.FramelessWindowHint, False)
    #         self.show()
    #         self.frameOnOff = 0
    #     else:
    #         self.setWindowFlag(Qt.FramelessWindowHint, True)
    #         self.show()
    #         self.frameOnOff = 1
    def update(self):
        if len(self.filelist) == self.counter:
            self.display(0)
            self.counter = 0
        else:
            self.display(self.counter)
            self.counter += 1
    def display(self, i):
        print(self.filelist[i])
        if len(self.filelist) != 0:
            print(str(self.dataFolder)+"/"+str(self.filelist[i]))
            self.lbl_dir_fileName.setPixmap(QPixmap(str(self.dataFolder)+"/"+str(self.filelist[i])))
    def setDir(self, dir_Name):
        self.dataFolder = dir_Name
        self.filelist = [os.path.basename(f)
                    for f in os.listdir(self.dataFolder)
                    if f.endswith('.png')]
        self.display(self.counter)
    def windowMove(self, index):
        self.move(self.m.xPos(index), self.m.yPos(index))
    def rslXChange(self, index):
        self.rslX = index
        self.setGeometry(self.m.xPos(self.monitorSelect), self.m.yPos(self.monitorSelect),self.rslX, self.rslY)

    def rslYChange(self, index):
        self.rslY = index
        self.setGeometry(self.m.xPos(self.monitorSelect), self.m.yPos(self.monitorSelect),self.rslX, self.rslY)