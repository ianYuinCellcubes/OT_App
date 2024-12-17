from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QMainWindow, QHBoxLayout

class SubView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("View")

        self.lbl_pixmap = QLabel("test")

        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_pixmap)

        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(0,0, 3000,3000)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
    def set_monitor(self, data):
        self.move(data[3][0],data[3][1])
    def update_lbl_pixmap(self, root_data):
        self.lbl_pixmap.setPixmap(root_data)
