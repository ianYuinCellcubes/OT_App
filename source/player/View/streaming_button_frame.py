from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

class streamingButton(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.btn_Run = QPushButton("Run")
        self.btn_Run.clicked.connect(self.btn_running)
        self.btn_Run.setCheckable(True)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_Run)

        self.setLayout(hbox)
    def btn_running(self, checked):
            if checked:
                self.btn_Run.setText("Run")
            else:
                self.btn_Run.setText("Stop")
            self.controller.set_streaming_run()