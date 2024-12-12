
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit
from PySide6.QtCore import Qt

class streamingInfo(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
    def initUI(self):
        lbl_Streaming_Setting = QLabel("Streaming Setting")

        lbl_Image_Size = QLabel("Image Size")
        lbl_Time = QLabel("Time")

        self.le_rsl_X = QLineEdit()
        self.le_rsl_X.returnPressed.connect(self.set_le_rsl_x)
        lbl_sign_X = QLabel(" X ")
        self.le_rsl_Y = QLineEdit()
        self.le_rsl_Y.returnPressed.connect(self.set_le_rsl_y)

        hbox_rsl = QHBoxLayout()
        hbox_rsl.addWidget(self.le_rsl_X)
        hbox_rsl.addWidget(lbl_sign_X)
        hbox_rsl.addWidget(self.le_rsl_Y)
        inputWidget_rsl = QWidget()
        inputWidget_rsl.setLayout(hbox_rsl)

        le_millisec = QLineEdit()
        lbl_sec = QLabel("ms/image")

        hbox_time = QHBoxLayout()
        hbox_time.addWidget(le_millisec)
        hbox_time.addWidget(lbl_sec)
        inputWidget_time = QWidget()
        inputWidget_time.setLayout(hbox_time)

        gbox = QGridLayout()
        gbox.addWidget(lbl_Image_Size, 0, 0, 1, 1)
        gbox.addWidget(lbl_Time, 1, 0, 1, 1)
        gbox.addWidget(inputWidget_rsl, 0, 1, 2, 1)
        gbox.addWidget(inputWidget_time, 1, 1, 2, 1)
        gbox.setAlignment(Qt.AlignVCenter)
        wg_gbox = QWidget()
        wg_gbox.setLayout(gbox)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_Streaming_Setting)
        vbox.addWidget(wg_gbox)
        self.setLayout(vbox)
    def set_le_rsl_x(self):
        self.controller.set_rsl_x(int(self.le_rsl_X.text()))
    def set_le_rsl_y(self):
        self.controller.set_rsl_y(int(self.le_rsl_Y.text()))