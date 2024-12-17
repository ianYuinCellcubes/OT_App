from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtCore import Qt

class streamingControl(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        lbl_Streaming_Control = QLabel("Streaming Control")

        lbl_Status = QLabel("Status")
        self.lbl_status_info = QLabel("Stop")

        hbox_status = QHBoxLayout()
        hbox_status.addWidget(lbl_Status)
        hbox_status.addWidget(self.lbl_status_info)
        wgt_status = QWidget()
        wgt_status.setLayout(hbox_status)

        lbl_Image_Window = QLabel("Image Window")
        self.btn_Hide = QPushButton()
        self.btn_Hide.setCheckable(True)
        self.btn_Hide.setText("Hide")
        self.btn_Hide.clicked.connect(self.btn_on_hide)

        hbox_imageWindow = QHBoxLayout()
        hbox_imageWindow.addWidget(lbl_Image_Window)
        hbox_imageWindow.addWidget(self.btn_Hide)
        wgt_imageWindow = QWidget()
        wgt_imageWindow.setLayout(hbox_imageWindow)

        vbox_sC = QVBoxLayout()
        # vbox_sC.addWidget(wgt_status)
        vbox_sC.addWidget(wgt_imageWindow)

        self.setLayout(vbox_sC)

    def btn_on_hide(self, checked):
        if checked:
            self.btn_Hide.setText("Show")
        else:
            self.btn_Hide.setText("Hide")
        self.controller.update_hide()

