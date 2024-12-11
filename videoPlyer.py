from source.OT import ScreenReader
import os, sys
from PySide6.QtGui import QIcon, QFont, QPixmap, QIntValidator
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QMainWindow,
    QPushButton,
    QApplication,
    QHBoxLayout,
    QComboBox,
    QSpinBox,
    QLineEdit
)


image_folder = 'resource'

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
        self.m = monitor1
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
class MyApp(QMainWindow):
    fname = None
    extensionFile = ".jpg"
    extensionVideo = ".avi"
    def __init__(self):
        super().__init__()
        self.initUI()
        self.w = subWindow(self)

    def initUI(self):
        self.setWindowTitle('Video Maker')
        self.setWindowIcon(QIcon('\\resource\\logo.ico'))
        self.setGeometry(200,200,450,200)

        hbox= QVBoxLayout()
        hbox.addWidget(self.monitorFrame())
        hbox.addWidget(self.findFileFrame())

        widget = QWidget()
        widget.setLayout(hbox)

        self.setCentralWidget(widget)
        self.show()
    def monitorFrame(self):
        monitor1 = ScreenReader.monitor
        monitor1.scanning(monitor1)
        mNum = monitor1.countMonitor()
        self.cb = QComboBox(self)
        for i in range(mNum):
            self.cb.addItem(monitor1.monitorName(i), userData=i)
        self.cb.activated[int].connect(self.onCbActivated)
        self.cb.setFixedWidth(200)

        self.resolutionX = QLineEdit(self)
        # self.resolutionX.setText(str(self.w.rslX))
        self.resolutionX.setFixedWidth(80)
        self.resolutionX.setText("3840")
        self.resolutionX.setAlignment(Qt.AlignCenter)
        self.resolutionX.returnPressed.connect(self.rsl_X_returnPressed)
        self.resolutionX.setValidator(QIntValidator(0, 10000, self))
        subSign = QLabel(' X ')
        subSign.setFixedWidth(20)
        subSign.setAlignment(Qt.AlignCenter)

        self.resolutionY = QLineEdit(self)
        self.resolutionY.setText("3840")
        # self.resolutionY.setText(str(self.w.rslY))
        self.resolutionY.setFixedWidth(80)
        self.resolutionY.setAlignment(Qt.AlignCenter)
        self.resolutionY.returnPressed.connect(self.rsl_Y_returnPressed)
        self.resolutionY.setValidator(QIntValidator(0, 10000, self))

        btn_reUpdate = QPushButton("↻", self)
        btn_reUpdate.clicked.connect(self.btn_reUpdate)

        resolbox = QHBoxLayout()
        resolbox.addWidget(self.resolutionX)
        resolbox.addWidget(subSign)
        resolbox.addWidget(self.resolutionY)
        resolbox.addWidget(btn_reUpdate)
        resolWidget = QWidget()
        resolWidget.setLayout(resolbox)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.cb)
        vbox1.addWidget(resolWidget)

        mF = QWidget()
        mF.setLayout(vbox1)

        return mF
    def btn_reUpdate(self):
        self.w.rslXChange(int(self.resolutionX.text()))
        self.w.rslYChange(int(self.resolutionY.text()))


    def rsl_X_returnPressed(self):
        self.w.rslXChange(int(self.resolutionX.text()))

    def rsl_Y_returnPressed(self):
        self.w.rslYChange(int(self.resolutionY.text()))

    def onCbActivated(self, i):
        index = self.cb.currentIndex()
        self.w.monitorSelect = index
        self.w.windowMove(index)
    def findFileFrame(self):
        buttonF = QPushButton("  Select Folder  ", self)
        buttonR = QPushButton("  Run  ", self)
        buttonP = QPushButton(" Play ", self)
        lbl_status0 = QLabel("Status : ", self)
        self.lbl_status = QLabel(" . . . ", self)
        self.le_timer = QSpinBox()
        self.le_timer.setFixedWidth(120)
        self.le_timer.setValue(1000)
        self.le_timer.setRange(-0, 10000)
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

if __name__ == '__main__':
    monitor1 = ScreenReader.monitor
    monitor1.scanning(monitor1)

    font = QFont("SF Pro Compressed Medium", 16)
    font1 = QFont("Times New Roman")
    app = QApplication(sys.argv)
    app.setFont(font)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())