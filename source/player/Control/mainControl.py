from source.player.Model.mainModel import DataModel
from source.player.View.mainView import MainView
from source.player.View.subView import SubView
from source.player.ScreenReader import ScreenReader
import os
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap

class MainController():
    def __init__(self):
        self.model = DataModel()
        self.view = MainView(self)
        self.subView = SubView()
        # self.init()
    def show_main_view(self):
        self.view.show()
    def show_sub_view(self):
        self.subView.show()
    def update_model(self, data):
        self.model.set_data(data)
        self.view.updata_view(data)
    def get_data_from_model(self):
        return self.model.get_data()
    def set_monitor_index(self, data):
        self.model.set_monitor_index(data)
        self.subView.set_monitor(self.model.get_monitor_info(data))
    def search_monitor(self):
        self.SR = ScreenReader.monitor
        self.model.set_monitor_list(self.SR.scanning(self.SR))
        self.model.set_monitor_count(self.SR.countMonitor())
        self.view.update_moniterSearch(self.model.get_monitor_list())
    def find_Folder(self, root):
        self.model.set_root(root)
        self.view.update_lbl_root(self.model.get_root())
        data = [os.path.basename(f)
                    for f in os.listdir(self.model.get_root())
                    if f.endswith('.png')]
        self.model.set_fileList(data)
        self.model.set_isRun(True)
        self.set_timer(1000)
        # self.subView.update_lbl_pixmap(self.model.get_root())
        # def update_combobox(self):
    def update(self):
        root = self.model.get_root()
        if len(self.model.get_fileList()) == (self.model.get_index()):
            self.model.set_index(0)
        root_data = str(root) + "/" + str(self.model.get_file(self.model.get_index()))
        data = QPixmap(root_data)
        scale_data = data.scaled(self.model.get_rsl_x(),self.model.get_rsl_y())
        self.subView.update_lbl_pixmap(scale_data)
        if len(self.model.get_fileList()) == (self.model.get_index()+1):
            self.model.set_index(0)
        else:
            self.model.set_index(self.model.get_index()+1)
    def set_timer(self, millisec):
        self.timer = QTimer()
        if self.timer.isActive():
            self.timer.stop()
        self.timer.timeout.connect(self.update)
        self.timer.start(millisec)
    def set_le_millisec(self, text):
        millisec = int(text)
        self.model.set_millisec(millisec)
        self.set_timer(self.model.get_millisec())
    def set_rsl_x(self, x):
        self.model.set_rsl_x(x)
        self.update_rsl()
    def update_rsl(self):
        info = self.model.get_monitor_info(self.model.get_monitor_index())
        self.subView.setGeometry(info[3][0], info[3][1], self.model.get_rsl_x(), self.model.get_rsl_y())
    def set_rsl_y(self, y):
        self.model.set_rsl_y(y)
        self.update_rsl()
    def update_hide(self):
        self.model.set_Hide()
        if self.model.get_Hide():
            self.subView.hide()
        else:
            self.subView.show()
    def set_streaming_run(self):
        # if self.timer.isActive():
        print(self.model.get_isRun())
        if self.model.get_isRun():
            self.model.set_isRun(False)
            self.timer.stop()
        else:
            self.set_timer(self.model.get_millisec())
            self.model.set_isRun(True)
    def ClosedWindow(self):
        self.subView.close()
        # else:
        #     self.set_timer(self.model.get_millisec())

    # def update(self, fileList):


    # def init(self):
    #     return 0
