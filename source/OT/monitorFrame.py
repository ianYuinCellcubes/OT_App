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
from source.OT.mainWidnow import *
class monitorFrame(QWidget):
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