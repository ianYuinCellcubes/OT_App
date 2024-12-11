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
    QLineEdit
)
from source.OT.View.moniter_search_frame import moniterSearch

class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Video Maker')
        # self.setWindowIcon(QIcon('../../resource/logo.ico'))
        self.setGeometry(200, 200, 650, 600)

        vbox = QVBoxLayout()
        self.mS = moniterSearch(self)
        vbox.addWidget(self.mS) # moniter searching frame
        # vbox.addWidget(self.mainFrame())
        # vbox.addWidget(self.findFileFrame())

        widget = QWidget()
        widget.setLayout(vbox)

        self.setCentralWidget(widget)