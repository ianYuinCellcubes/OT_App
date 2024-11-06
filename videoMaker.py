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
    QHBoxLayout
)


image_folder = 'resource'
video_name = 'video.avi'

class subWindow(QMainWindow):
    def __init__(self, parent=None):
        super(subWindow, self).__init__(parent)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Second window")
        self.setGeometry(100,100, 1000, 1000)
        cap = cv2.VideoCapture(video_name)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print("w : %d, h : %d, FPS : %d" %(width,height,fps))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("end")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('tete', frame)
            if cv2.waitKey(42) == ord('q'):
                break
        # cap.release()
        # cv2.destroyAllWindows()
class MyApp(QMainWindow):
    fname = None
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Maker')
        self.setWindowIcon(QIcon('\\resource\\logo.ico'))
        self.setGeometry(200,200,300,400)

        hbox= QHBoxLayout()
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
    def findFileFrame(self):
        buttonF = QPushButton("  Find Folder  ", self)
        buttonR = QPushButton("  Run  ", self)
        buttonP = QPushButton(" Play ", self)

        buttonF.clicked.connect(self.btn_Find_Folder)
        buttonR.clicked.connect(self.btn_Run_Maker)
        buttonP.clicked.connect(self.btn_Play_Video)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(buttonF)
        vbox1.addStretch(1)
        vbox1.addWidget(buttonR)
        vbox1.addStretch(1)
        vbox1.addWidget(buttonP)

        frame01 = QWidget()
        frame01.setLayout(vbox1)
        return frame01
    def btn_Play_Video(self):
        dialog = subWindow(self)
        dialog.show()
    def btn_Find_Folder(self):
        self.fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        print(self.fname)
        return 0
    def btn_Run_Maker(self):
        images = [img for img in os.listdir(self.fname) if img.endswith(".jpg")]
        frame = cv2.imread(os.path.join(self.fname, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, 10, (width, height))

        for image in images:
            nowFrame = cv2.imread(os.path.join(self.fname, image))
            video.write(nowFrame)
            height, width, channel = nowFrame.shape
            bytesPerLine = 3 * width
            qImg = QImage(nowFrame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.img_lbl.setPixmap(QPixmap.fromImage(qImg))
            self.show()
        cv2.destroyAllWindows()
        video.release()
        print("Finish")
        return 0


if __name__ == '__main__':

    font = QFont("SF Pro Compressed Medium", 16)
    font1 = QFont("Times New Roman")
    app = QApplication(sys.argv)
    app.setFont(font)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())