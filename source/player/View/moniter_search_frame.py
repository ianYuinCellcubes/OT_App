from PySide6.QtWidgets import QWidget, QComboBox, QPushButton, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
class moniterSearch(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
    def initUI(self):
        lbl_Select_Display = QLabel("Select Display")
        self.cb = QComboBox(self)
        self.cb.activated[int].connect(self.on_cb_Activated)
        self.cb.setFixedWidth(200)

        btn_monitor_search = QPushButton("🔍")
        btn_monitor_search.setFixedWidth(40)
        # btn_monitor_search.setAlignment(Qt.AlignCenter)
        btn_monitor_search.clicked.connect(self.search_monitor)

        hbox = QHBoxLayout()
        hbox.addWidget(lbl_Select_Display)
        hbox.addWidget(self.cb)
        hbox.addWidget(btn_monitor_search)

        self.setLayout(hbox)
    def reolution_tool_bar(self):
        resol_X = QLineEdit()
        resol_X.setAlignment(Qt.AlignCenter)
        resol_X.setValidator(QIntValidator(0, 10000, self))
        # resol_X.returnPressed.connect(self.resol)
        subSign = QLabel(' X ')
        subSign.setFixedWidth(20)
        subSign.setAlignment(Qt.AlignCenter)

        resol_Y = QLineEdit()
        resol_Y.setAlignment(Qt.AlignCenter)
        resol_Y.setValidator(QIntValidator(0, 10000, self))

        btn_reUpdate = QPushButton("↻", self)
        btn_reUpdate.clicked.connect(self.btn_reUpdate)

        resolbox = QHBoxLayout()
        resolbox.addWidget(resol_X)
        resolbox.addWidget(subSign)
        resolbox.addWidget(resol_Y)
        resolbox.addWidget(btn_reUpdate)
        resolWidget = QWidget()
        resolWidget.setLayout(resolbox)

        return resolWidget
        #
        # self.resolutionX = QLineEdit(self)
        # # self.resolutionX.setText(str(self.w.rslX))
        # self.resolutionX.setFixedWidth(80)
        # self.resolutionX.setText("3840")
        # self.resolutionX.setAlignment(Qt.AlignCenter)
        # self.resolutionX.returnPressed.connect(self.rsl_X_returnPressed)
        # self.resolutionX.setValidator(QIntValidator(0, 10000, self))
        # subSign = QLabel(' X ')
        # subSign.setFixedWidth(20)
        # subSign.setAlignment(Qt.AlignCenter)
        #
        # self.resolutionY = QLineEdit(self)
        # self.resolutionY.setText("3840")
        # # self.resolutionY.setText(str(self.w.rslY))
        # self.resolutionY.setFixedWidth(80)
        # self.resolutionY.setAlignment(Qt.AlignCenter)
        # self.resolutionY.returnPressed.connect(self.rsl_Y_returnPressed)
        # self.resolutionY.setValidator(QIntValidator(0, 10000, self))
        #
        # btn_reUpdate = QPushButton("↻", self)
        # btn_reUpdate.clicked.connect(self.btn_reUpdate)
        #
        # resolbox = QHBoxLayout()
        # resolbox.addWidget(self.resolutionX)
        # resolbox.addWidget(subSign)
        # resolbox.addWidget(self.resolutionY)
        # resolbox.addWidget(btn_reUpdate)
        # resolWidget = QWidget()
        # resolWidget.setLayout(resolbox)
        #
        # vbox1 = QVBoxLayout()
        # vbox1.addWidget(self.cb)
        # vbox1.addWidget(resolWidget)
        #
        # mF = QWidget()
        # mF.setLayout(vbox1)
    def on_cb_Activated(self, i):
        self.controller.set_monitor_index(i)
    def cb_update(self, data):
        self.cb.clear()
        print(data)
        for i in range(len(data)):
            self.cb.addItem(data[i][1], userData=i)
    def search_monitor(self):
        self.controller.search_monitor()
