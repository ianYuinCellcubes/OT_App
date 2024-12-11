from source.OT.Model.mainModel import DataModel
from source.OT.View.mainView import MainView
from source.OT.ScreenReader import ScreenReader
class MainController():
    def __init__(self):
        self.model = DataModel()
        self.view = MainView(self)
        # self.init()
    def show_main_view(self):
        self.view.show()
    def update_model(self, data):
        self.model.set_data(data)
        self.view.updata_view(data)
    def get_data_from_model(self):
        return self.model.get_data()
    def set_monitor_index(self, data):
        self.model.set_monitor_index(data)
    def search_monitor(self):
        self.SR = ScreenReader.monitor
        self.SR.scanning(self.SR)
        self.model.set_monitor_count(self.SR.countMonitor())
    # def init(self):
    #     return 0
