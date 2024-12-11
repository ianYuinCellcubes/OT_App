# import OT_App_Pyside as main
from source.OT.mainWidnow import MyApp
from PySide6.QtGui import QIcon, QFont, QImage, QPixmap, QIntValidator
from PySide6.QtCore import QCoreApplication, Qt, QTimer
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
class viewFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.viewInit()
    def viewInit(self):
        test = QPushButton("test")
        vbox2 = QVBoxLayout()
        vbox2.addWidget(test)

        vF = QWidget()
        vF.setLayout(vbox2)
        return vF