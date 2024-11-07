import cv2
import os
import sys
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (
    QWidget,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QMainWindow,
    QPushButton,
    QApplication,
    QHBoxLayout,
    QComboBox,
    QSpinBox
)


image_folder = 'resource'
video_name = 'CGH'

class subWindow(QMainWindow):
    def __init__(self, parent=None):
        super(subWindow, self).__init__(parent)
        self.initUI()
    def initUI(self):
        cap = cv2.VideoCapture(video_name+".avi")
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print("w : %d, h : %d, FPS : %d" %(width,height,fps))
        frame_counter = 0
        while cap.isOpened():
            ret, frame = cap.read()
            frame_counter += 1
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if ret:
                cv2.imshow('tete', frame)
            if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES,0)
                frame_counter = 0
                continue

            if cv2.waitKey(42) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
class MyApp(QMainWindow):
    fname = None
    extensionFile = ".jpg"
    extensionVideo = ".avi"
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Maker')
        self.setWindowIcon(QIcon('\\resource\\logo.ico'))
        self.setGeometry(200,200,450,200)

        hbox= QHBoxLayout()
        hbox.addWidget(self.extensionFrame())
        hbox.addWidget(self.findFileFrame())
        hbox.addWidget(self.viewFrame())

        widget = QWidget()
        widget.setLayout(hbox)

        self.setCentralWidget(widget)
        self.show()
    def viewFrame(self):
        self.img_lbl = QLabel()
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.img_lbl)
        frame01 = QWidget()
        frame01.setLayout(vbox2)
        return frame01
    def extensionFrame(self):
        lbl_fps = QLabel("FPS(ms):")
        self.sb_fps_value = QSpinBox()
        self.sb_fps_value.setMinimum(1)
        self.sb_fps_value.setMaximum(10000)
        self.sb_fps_value.valueChanged.connect(self.fps_changed)

        cb = QComboBox(self)
        cb.addItem(".jpg")
        cb.addItem(".bmp")
        cb.addItem(".png")
        cb.activated[str].connect(self.onActivated)

        cb1 = QComboBox(self)
        cb1.addItem('.avi')
        cb1.activated[str].connect(self.onActivated2)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(lbl_fps)
        hbox2.addWidget(self.sb_fps_value)
        tmp = QWidget()
        tmp.setLayout(hbox2)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(tmp)
        vbox1.addWidget(cb)
        vbox1.addWidget(cb1)


        frame01 = QWidget()
        frame01.setLayout(vbox1)
        return frame01
    def findFileFrame(self):
        buttonF = QPushButton("  Select Folder  ", self)
        buttonR = QPushButton("  Run  ", self)
        buttonP = QPushButton(" Play ", self)
        lbl_status0 = QLabel("Status : ", self)
        self.lbl_status = QLabel(" . . . ", self)

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

        frame01 = QWidget()
        frame01.setLayout(vbox1)
        return frame01
    def fps_changed(self):
        return 0
    def onActivated(self, text):
        self.extensionFile = text
    def onActivated2(self, text):
        self.extensionVideo = text
    def btn_Play_Video(self):
        dialog = subWindow(self)
        dialog.show()
        return 0
    def btn_Find_Folder(self):
        self.fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        print(self.fname)
        self.lbl_status.setText("Load File")
        return 0
    def btn_Run_Maker(self):
        images = [img for img in os.listdir(self.fname) if img.endswith(str(self.extensionFile))]
        frame = cv2.imread(os.path.join(self.fname, images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(video_name + self.extensionVideo, 0, self.sb_fps_value.value(), (width, height))

        for image in images:
            nowFrame = cv2.imread(os.path.join(self.fname, image))
            video.write(nowFrame)
            height, width, channel = nowFrame.shape
            bytesPerLine = 3 * width
            qImg = QImage(nowFrame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # self.img_lbl.setPixmap(QPixmap.fromImage(qImg))
            # self.show()
        cv2.destroyAllWindows()
        video.release()
        print("Finish")
        self.lbl_status.setText("Finish")
        return 0


if __name__ == '__main__':

    font = QFont("SF Pro Compressed Medium", 16)
    font1 = QFont("Times New Roman")
    app = QApplication(sys.argv)
    app.setFont(font)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())