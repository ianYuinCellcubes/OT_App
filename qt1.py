import sys, miicam
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, QSignalBlocker, Qt, QRect
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QCheckBox, QMessageBox, QPushButton, QComboBox, QSlider, QGroupBox, QGridLayout, QBoxLayout, QHBoxLayout, QVBoxLayout, QMenu, QAction

class MainWidget(QWidget):
    evtCallback = pyqtSignal(int)

    @staticmethod
    def makeLayout(lbl1, sli1, val1, lbl2, sli2, val2):
        hlyt1 = QHBoxLayout()
        hlyt1.addWidget(lbl1)
        hlyt1.addStretch()
        hlyt1.addWidget(val1)
        hlyt2 = QHBoxLayout()
        hlyt2.addWidget(lbl2)
        hlyt2.addStretch()
        hlyt2.addWidget(val2)
        vlyt = QVBoxLayout()
        vlyt.addLayout(hlyt1)
        vlyt.addWidget(sli1)
        vlyt.addLayout(hlyt2)
        vlyt.addWidget(sli2)
        return vlyt

    def __init__(self):
        super().__init__()
        self.setMinimumSize(1024, 768)
        self.hcam = None
        self.timer = QTimer(self)
        self.imgWidth = 0
        self.imgHeight = 0
        self.pData = None
        self.res = 0
        self.temp = miicam.MIICAM_TEMP_DEF
        self.tint = miicam.MIICAM_TINT_DEF
        self.count = 0
        self.crop_area = None
        self.x = 50
        self.y = 50

        gboxres = QGroupBox("Resolution")
        self.cmb_res = QComboBox()
        self.cmb_res.setEnabled(False)
        vlytres = QVBoxLayout()
        vlytres.addWidget(self.cmb_res)
        gboxres.setLayout(vlytres)
        self.cmb_res.currentIndexChanged.connect(self.onResolutionChanged)

        gboxexp = QGroupBox("Exposure")
        self.cbox_auto = QCheckBox("Auto exposure")
        self.cbox_auto.setEnabled(False)
        self.lbl_expoTime = QLabel("0")
        self.lbl_expoGain = QLabel("0")
        self.slider_expoTime = QSlider(Qt.Horizontal)
        self.slider_expoGain = QSlider(Qt.Horizontal)
        self.slider_expoTime.setEnabled(False)
        self.slider_expoGain.setEnabled(False)
        self.cbox_auto.stateChanged.connect(self.onAutoExpo)
        self.slider_expoTime.valueChanged.connect(self.onExpoTime)
        self.slider_expoGain.valueChanged.connect(self.onExpoGain)
        vlytexp = QVBoxLayout()
        vlytexp.addWidget(self.cbox_auto)
        vlytexp.addLayout(self.makeLayout(QLabel("Time(us):"), self.slider_expoTime, self.lbl_expoTime, QLabel("Gain(%):"), self.slider_expoGain, self.lbl_expoGain))
        gboxexp.setLayout(vlytexp)

        gboxwb = QGroupBox("White balance")
        self.btn_autoWB = QPushButton("White balance")
        self.btn_autoWB.setEnabled(False)
        self.btn_autoWB.clicked.connect(self.onAutoWB)
        self.lbl_temp = QLabel(str(miicam.MIICAM_TEMP_DEF))
        self.lbl_tint = QLabel(str(miicam.MIICAM_TINT_DEF))
        self.slider_temp = QSlider(Qt.Horizontal)
        self.slider_tint = QSlider(Qt.Horizontal)
        self.slider_temp.setRange(miicam.MIICAM_TEMP_MIN, miicam.MIICAM_TEMP_MAX)
        self.slider_temp.setValue(miicam.MIICAM_TEMP_DEF)
        self.slider_tint.setRange(miicam.MIICAM_TINT_MIN, miicam.MIICAM_TINT_MAX)
        self.slider_tint.setValue(miicam.MIICAM_TINT_DEF)
        self.slider_temp.setEnabled(False)
        self.slider_tint.setEnabled(False)
        self.slider_temp.valueChanged.connect(self.onWBTemp)
        self.slider_tint.valueChanged.connect(self.onWBTint)
        vlytwb = QVBoxLayout()
        vlytwb.addLayout(self.makeLayout(QLabel("Temperature:"), self.slider_temp, self.lbl_temp, QLabel("Tint:"), self.slider_tint, self.lbl_tint))
        vlytwb.addWidget(self.btn_autoWB)
        gboxwb.setLayout(vlytwb)

        self.btn_open = QPushButton("Open")
        self.btn_open.clicked.connect(self.onBtnOpen)
        self.btn_snap = QPushButton("Snap")
        self.btn_snap.setEnabled(False)
        self.btn_snap.clicked.connect(self.onBtnSnap)
        self.btn_makeVideo = QPushButton("Run")
        self.btn_makeVideo.clicked.connect(self.onBtnMake)
        vlytctrl = QVBoxLayout()
        vlytctrl.addWidget(gboxres)
        vlytctrl.addWidget(gboxexp)
        vlytctrl.addWidget(gboxwb)
        vlytctrl.addWidget(self.btn_open)
        vlytctrl.addWidget(self.btn_snap)
        vlytctrl.addWidget(self.btn_makeVideo)
        vlytctrl.addStretch()
        wgctrl = QWidget()
        wgctrl.setLayout(vlytctrl)

        self.lbl_frame = QLabel()
        self.lbl_video = QLabel()

        qmap = self.lbl_video.pixmap()
        painter = QPainter(self.lbl_video)
        painter.setPen(QPen(Qt.green, 10, Qt.SolidLine))
        painter.drawRect(100, 100, 200, 200)

        vlytshow = QVBoxLayout()
        vlytshow.addWidget(self.lbl_video, 1)
        vlytshow.addWidget(self.lbl_frame)
        wgshow = QWidget()
        wgshow.setLayout(vlytshow)


        self.lbl_frame_crop = QLabel()
        self.lbl_video_crop = QLabel()
        vlytshow_crop = QVBoxLayout()
        vlytshow_crop.addWidget(self.lbl_video_crop, 1)
        vlytshow_crop.addWidget(self.lbl_frame_crop)
        wgshow1 = QWidget()
        wgshow1.setStyleSheet("background-color: #7FFFD4")
        wgshow1.setLayout(vlytshow_crop)
        wgctrl1 = QWidget()
        wgctrl1.setStyleSheet("background-color: #7FFFA4")

        self.btn_ctrl_crop_W = QPushButton(" ↑ ")
        self.btn_ctrl_crop_A = QPushButton(" ← ")
        self.btn_ctrl_crop_S = QPushButton(" ↓ ")
        self.btn_ctrl_crop_D = QPushButton(" → ")
        self.btn_ctrl_crop_W.clicked.connect(self.onBtnW)
        self.btn_ctrl_crop_A.clicked.connect(self.onBtnA)
        self.btn_ctrl_crop_S.clicked.connect(self.onBtnS)
        self.btn_ctrl_crop_D.clicked.connect(self.onBtnD)

        vlytctrlcrop = QGridLayout()
        vlytctrlcrop.addWidget(self.btn_ctrl_crop_W, 0, 1)
        vlytctrlcrop.addWidget(self.btn_ctrl_crop_A, 1, 0)
        vlytctrlcrop.addWidget(self.btn_ctrl_crop_S, 1, 1)
        vlytctrlcrop.addWidget(self.btn_ctrl_crop_D, 1, 2)
        wgshowctlcrop = QWidget()
        wgshowctlcrop.setLayout(vlytctrlcrop)
        wgshowctlcrop.setStyleSheet("background-color: #2FF1A3")

        gmain = QGridLayout()
        gmain.setColumnStretch(0, 1)
        gmain.setColumnStretch(1, 4)
        gmain.setRowStretch(0, 3)
        gmain.setRowStretch(2, 2)
        gmain.addWidget(wgctrl1, 0, 0)
        gmain.addWidget(wgshowctlcrop, 1, 0)
        gmain.addWidget(wgctrl, 2, 0)
        gmain.addWidget(wgshow1, 0, 1)
        gmain.addWidget(wgshow, 2, 1)
        self.setLayout(gmain)

        self.timer.timeout.connect(self.onTimer)
        self.evtCallback.connect(self.onevtCallback)

    def onTimer(self):
        if self.hcam:
            nFrame, nTime, nTotalFrame = self.hcam.get_FrameRate()
            self.lbl_frame.setText("{}, fps = {:.1f}".format(nTotalFrame, nFrame * 1000.0 / nTime))
    def onBtnMake(self):
        return 0
    def onBtnW(self):
        if self.hcam:
            self.y = self.y - 1
    def onBtnA(self):
        if self.hcam:
            self.x = self.x - 1
    def onBtnS(self):
        if self.hcam:
            self.y = self.y + 1
    def onBtnD(self):
        if self.hcam:
            self.x = self.x + 1
    def closeCamera(self):
        if self.hcam:
            self.hcam.Close()
        self.hcam = None
        self.pData = None

        self.btn_open.setText("Open")
        self.timer.stop()
        self.lbl_frame.clear()
        self.cbox_auto.setEnabled(False)
        self.slider_expoGain.setEnabled(False)
        self.slider_expoTime.setEnabled(False)
        self.btn_autoWB.setEnabled(False)
        self.slider_temp.setEnabled(False)
        self.slider_tint.setEnabled(False)
        self.btn_snap.setEnabled(False)
        self.cmb_res.setEnabled(False)
        self.cmb_res.clear()

    def closeEvent(self, event):
        self.closeCamera()

    def onResolutionChanged(self, index):
        if self.hcam: #step 1: stop camera
            self.hcam.Stop()

        self.res = index
        self.imgWidth = self.cur.model.res[index].width
        self.imgHeight = self.cur.model.res[index].height

        if self.hcam: #step 2: restart camera
            self.hcam.put_eSize(self.res)
            self.startCamera()

    def onAutoExpo(self, state):
        if self.hcam:
            self.hcam.put_AutoExpoEnable(1 if state else 0)
            self.slider_expoTime.setEnabled(not state)
            self.slider_expoGain.setEnabled(not state)

    def onExpoTime(self, value):
        if self.hcam:
            self.lbl_expoTime.setText(str(value))
            if not self.cbox_auto.isChecked():
                self.hcam.put_ExpoTime(value)

    def onExpoGain(self, value):
        if self.hcam:
            self.lbl_expoGain.setText(str(value))
            if not self.cbox_auto.isChecked():
                self.hcam.put_ExpoAGain(value)

    def onAutoWB(self):
        if self.hcam:
            self.hcam.AwbOnce()

    def wbCallback(nTemp, nTint, self):
        self.slider_temp.setValue(nTemp)
        self.slider_tint.setValue(nTint)

    def onWBTemp(self, value):
        if self.hcam:
            self.temp = value
            self.hcam.put_TempTint(self.temp, self.tint)
            self.lbl_temp.setText(str(value))

    def onWBTint(self, value):
        if self.hcam:
            self.tint = value
            self.hcam.put_TempTint(self.temp, self.tint)
            self.lbl_tint.setText(str(value))

    def startCamera(self):
        self.pData = bytes(miicam.TDIBWIDTHBYTES(self.imgWidth * 24) * self.imgHeight)
        uimin, uimax, uidef = self.hcam.get_ExpTimeRange()
        self.slider_expoTime.setRange(uimin, uimax)
        self.slider_expoTime.setValue(uidef)
        usmin, usmax, usdef = self.hcam.get_ExpoAGainRange()
        self.slider_expoGain.setRange(usmin, usmax)
        self.slider_expoGain.setValue(usdef)
        self.handleExpoEvent()
        if self.cur.model.flag & miicam.MIICAM_FLAG_MONO == 0:
            self.handleTempTintEvent()
        try:
            self.hcam.StartPullModeWithCallback(self.eventCallBack, self)
        except miicam.HRESULTException:
            self.closeCamera()
            QMessageBox.warning(self, "Warning", "Failed to start camera.")
        else:
            self.cmb_res.setEnabled(True)
            self.cbox_auto.setEnabled(True)
            self.btn_autoWB.setEnabled(self.cur.model.flag & miicam.MIICAM_FLAG_MONO == 0)
            self.slider_temp.setEnabled(self.cur.model.flag & miicam.MIICAM_FLAG_MONO == 0)
            self.slider_tint.setEnabled(self.cur.model.flag & miicam.MIICAM_FLAG_MONO == 0)
            self.btn_open.setText("Close")
            self.btn_snap.setEnabled(True)
            bAuto = self.hcam.get_AutoExpoEnable()
            self.cbox_auto.setChecked(1 == bAuto)
            self.timer.start(1000)

    def openCamera(self):
        self.hcam = miicam.Miicam.Open(self.cur.id)
        if self.hcam:
            self.res = self.hcam.get_eSize()
            self.imgWidth = self.cur.model.res[self.res].width
            self.imgHeight = self.cur.model.res[self.res].height
            with QSignalBlocker(self.cmb_res):
                self.cmb_res.clear()
                for i in range(0, self.cur.model.preview):
                    self.cmb_res.addItem("{}*{}".format(self.cur.model.res[i].width, self.cur.model.res[i].height))
                self.cmb_res.setCurrentIndex(self.res)
                self.cmb_res.setEnabled(True)
            self.hcam.put_Option(miicam.MIICAM_OPTION_BYTEORDER, 0) #Qimage use RGB byte order
            self.hcam.put_AutoExpoEnable(1)
            self.startCamera()

    def onBtnOpen(self):
        if self.hcam:
            self.closeCamera()
        else:
            arr = miicam.Miicam.EnumV2()
            if 0 == len(arr):
                QMessageBox.warning(self, "Warning", "No camera found.")
            elif 1 == len(arr):
                self.cur = arr[0]
                self.openCamera()
            else:
                menu = QMenu()
                for i in range(0, len(arr)):
                    action = QAction(arr[i].displayname, self)
                    action.setData(i)
                    menu.addAction(action)
                action = menu.exec(self.mapToGlobal(self.btn_open.pos()))
                if action:
                    self.cur = arr[action.data()]
                    self.openCamera()
    def onBtnCrop(self):
        if self.hcam:
            if 0 == self.cur.model.still:
                if self.pData is not None:
                    image = QImage(self.pData, self.imgWidth, self.imgHeight, QImage.Format_RGB888)
    def onBtnSnap(self):
        if self.hcam:
            if 0 == self.cur.model.still:    # not support still image capture
                if self.pData is not None:
                    image = QImage(self.pData, self.imgWidth, self.imgHeight, QImage.Format_RGB888)
                    self.count += 1
                    image.save("pyqt{}.jpg".format(self.count))
            else:
                menu = QMenu()
                for i in range(0, self.cur.model.still):
                    action = QAction("{}*{}".format(self.cur.model.res[i].width, self.cur.model.res[i].height), self)
                    action.setData(i)
                    menu.addAction(action)
                action = menu.exec(self.mapToGlobal(self.btn_snap.pos()))
                self.hcam.Snap(action.data())

    @staticmethod
    def eventCallBack(nEvent, self):
        '''callbacks come from miicam.dll/so internal threads, so we use qt signal to post this event to the UI thread'''
        self.evtCallback.emit(nEvent)

    def onevtCallback(self, nEvent):
        '''this run in the UI thread'''
        if self.hcam:
            if miicam.MIICAM_EVENT_IMAGE == nEvent:
                self.handleImageEvent()
            elif miicam.MIICAM_EVENT_EXPOSURE == nEvent:
                self.handleExpoEvent()
            elif miicam.MIICAM_EVENT_TEMPTINT == nEvent:
                self.handleTempTintEvent()
            elif miicam.MIICAM_EVENT_STILLIMAGE == nEvent:
                self.handleStillImageEvent()
            elif miicam.MIICAM_EVENT_ERROR == nEvent:
                self.closeCamera()
                QMessageBox.warning(self, "Warning", "Generic Error.")
            elif miicam.MIICAM_EVENT_STILLIMAGE == nEvent:
                self.closeCamera()
                QMessageBox.warning(self, "Warning", "Camera disconnect.")

    def handleImageEvent(self):
        try:
            self.hcam.PullImageV3(self.pData, 0, 24, 0, None)
        except miicam.HRESULTException:
            pass
        else:
            image = QImage(self.pData, self.imgWidth, self.imgHeight, QImage.Format_RGB888)
            newimage = image.scaled(self.lbl_video.width(), self.lbl_video.height(), Qt.KeepAspectRatio, Qt.FastTransformation)
            self.qmap = QPixmap.fromImage(newimage)
            self.lbl_video.setPixmap(self.qmap)

            self.crop_area = QRect(self.x, self.y, 250, 150)

            self.pixmap = self.lbl_video.pixmap()
            painter = QPainter(self.pixmap)
            painter.setPen(QPen(Qt.green, 2, Qt.DashLine))
            painter.drawRect(self.crop_area)
            self.lbl_video.setPixmap(self.pixmap)

            image2 = image.copy(self.crop_area)
            newimage2 = image2.scaled(self.lbl_video_crop.width(), self.lbl_video_crop.height(), Qt.KeepAspectRatio, Qt.FastTransformation)
            self.lbl_video_crop.setPixmap(QPixmap.fromImage(newimage2))

    def handleExpoEvent(self):
        time = self.hcam.get_ExpoTime()
        gain = self.hcam.get_ExpoAGain()
        with QSignalBlocker(self.slider_expoTime):
            self.slider_expoTime.setValue(time)
        with QSignalBlocker(self.slider_expoGain):
            self.slider_expoGain.setValue(gain)
        self.lbl_expoTime.setText(str(time))
        self.lbl_expoGain.setText(str(gain))

    def handleTempTintEvent(self):
        nTemp, nTint = self.hcam.get_TempTint()
        with QSignalBlocker(self.slider_temp):
            self.slider_temp.setValue(nTemp)
        with QSignalBlocker(self.slider_tint):
            self.slider_tint.setValue(nTint)
        self.lbl_temp.setText(str(nTemp))
        self.lbl_tint.setText(str(nTint))

    def handleStillImageEvent(self):
        info = miicam.MiicamFrameInfoV3()
        try:
            self.hcam.PullImageV3(None, 1, 24, 0, info) # peek
        except miicam.HRESULTException:
            pass
        else:
            if info.width > 0 and info.height > 0:
                buf = bytes(miicam.TDIBWIDTHBYTES(info.width * 24) * info.height)
                try:
                    self.hcam.PullImageV3(buf, 1, 24, 0, info)
                except miicam.HRESULTException:
                    pass
                else:
                    image = QImage(buf, info.width, info.height, QImage.Format_RGB888)
                    self.count += 1
                    image.save("pyqt{}.jpg".format(self.count))

if __name__ == '__main__':
    miicam.Miicam.GigeEnable(None, None)
    app = QApplication(sys.argv)
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec_())