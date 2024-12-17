from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont, QIntValidator
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
    QLineEdit,
    QFrame
)
from source.player.View.moniter_search_frame import moniterSearch
from source.player.View.folder_search_frame import folderSearch
from source.player.View.streaming_info_frame import streamingInfo
from source.player.View.Liner import *
from source.player.View.streaming_Control_frame import streamingControl
from source.player.View.streaming_button_frame import streamingButton
class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Video Maker')
        # self.setWindowIcon(QIcon('../../resource/logo.ico'))
        self.setGeometry(200, 200, 200, 300)

        vbox = QVBoxLayout()
        # vbox.setContentsMargins(0,0,0,0)
        self.mS = moniterSearch(self)
        vbox.addWidget(self.mS) # moniter searching frame
        vbox.addWidget(QHLine())
        self.fS = folderSearch(self)
        vbox.addWidget(self.fS)
        vbox.addWidget(QHLine())
        self.sI = streamingInfo(self)
        vbox.addWidget(self.sI)
        vbox.addWidget(QHLine())
        self.sC = streamingControl(self)
        vbox.addWidget(self.sC)
        vbox.addWidget(QHLine())
        self.sB = streamingButton(self)
        vbox.addWidget(self.sB)

        # vbox.addWidget(self.mainFrame())
        # vbox.addWidget(self.findFileFrame())

        widget = QWidget()
        widget.setLayout(vbox)

        self.setCentralWidget(widget)
    def update_moniterSearch(self, data):
        self.mS.cb_update(data)
    def search_monitor(self):
        self.controller.search_monitor()
    def set_monitor_index(self, i):
        self.controller.set_monitor_index(i)
    def update_lbl_root(self, data):
        self.fS.update_lbl_root(data)
    def find_Folder(self, data):
        self.controller.find_Folder(data)
    def set_rsl_x(self, rsl_x):
        self.controller.set_rsl_x(rsl_x)
    def set_rsl_y(self, rsl_y):
        self.controller.set_rsl_y(rsl_y)
    def set_le_millisec(self, text):
        self.controller.set_le_millisec(text)
    def update_hide(self):
        self.controller.update_hide()
    def set_streaming_run(self):
            self.controller.set_streaming_run()
    def closeEvent(self, event):
        self.controller.ClosedWindow()
    # def btn_onHide_Down(self):
    #     print("hide")
    # def btn_onHide_Up(self):
    #     print("show")
