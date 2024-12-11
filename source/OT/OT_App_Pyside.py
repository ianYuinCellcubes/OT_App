import sys

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

import mainWidnow as mW

if __name__ == '__main__':

    font = QFont("SF Pro Compressed Medium", 16)
    font1 = QFont("Times New Roman")
    app = QApplication(sys.argv)
    app.setFont(font)
    ex = mW.MyApp()
    ex.show()
    sys.exit(app.exec_())