import sys, miicam
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QLabel,
    QApplication,
    QWidget,
    QCheckBox,
    QMessageBox,
    QPushButton,
    QComboBox,
    QSlider,
    QGroupBox,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QMenu,
    QAction
)
class MainWidget(QWidget):

if __name__ == '__main__':
    miicam.Miicam.GigeEnable(None, None)
    app = QApplication(sys.argv)
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec_())