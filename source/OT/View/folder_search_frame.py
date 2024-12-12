from PySide6.QtWidgets import QWidget, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
class folderSearch(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
    def initUI(self):
        lbl_select_folder = QLabel("Select Folder")
        self.lbl_root_folder = QLabel("root")

        btn_Searching = QPushButton(" ... ")
        btn_Searching.clicked.connect(self.btn_on_search)
        btn_Searching.setFixedWidth(100)

        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_root_folder)
        hbox.addWidget(btn_Searching)
        hWidget = QWidget()
        hWidget.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_select_folder)
        vbox.addWidget(hWidget)

        self.setLayout(vbox)
    def btn_on_search(self):
        self.controller.find_Folder(QFileDialog.getExistingDirectory(self, 'Select Directory'))
    def update_lbl_root(self, data):
        self.lbl_root_folder.setText(data)