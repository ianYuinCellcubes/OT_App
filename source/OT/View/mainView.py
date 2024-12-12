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
from source.OT.View.moniter_search_frame import moniterSearch
from source.OT.View.folder_search_frame import folderSearch
from source.OT.View.streaming_info_frame import streamingInfo
from source.OT.View.Liner import *
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
        self.mS = moniterSearch(self)
        vbox.addWidget(self.mS) # moniter searching frame
        vbox.addWidget(QHLine())
        self.fS = folderSearch(self)
        vbox.addWidget(self.fS)
        vbox.addWidget(QHLine())
        self.sI = streamingInfo(self)
        vbox.addWidget(self.sI)
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
