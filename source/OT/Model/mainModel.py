class monitor_info:
    mIndex: int = 0     #  monitor select
    mCount: int = 1     #  How many moniter detect
    mlist: list = []    #  monitor list(data)
class DataModel:
    def __init__(self):
        self.data = None
        self.monitor = monitor_info
        self.root = None
        self.index = 0
        self.rsl_x = 3840
        self.rsl_y = 3840
    def set_data(self, data):
        self.data = data
    def get_data(self):
        return self.data
    def set_monitor_index(self, data):
        self.monitor.mIndex = data
    def get_monitor_index(self):
        print(self.monitor.mIndex)
        return self.monitor.mIndex
    def set_monitor_count(self, data):
        self.monitor.mCount = data
    def get_monitor_count(self):
        return self.monitor.mCount
    def set_monitor_list(self, data):
        self.monitor.mlist = data
    def get_monitor_list(self):
        return self.monitor.mlist
    def get_monitor_info(self, index):
        return self.monitor.mlist[index]
    def set_root(self, root):
        self.root = root
    def get_root(self):
        return self.root
    def set_fileList(self, data):
        self.fileList = []
        self.fileList = data
    def get_fileList(self):
        return self.fileList
    def get_file(self, index):
        return self.fileList[index]
    def get_index(self):
        return self.index
    def set_index(self, index):
        self.index = index
    def set_rsl_x(self, x):
        self.rsl_x = x
    def get_rsl_x(self):
        return self.rsl_x
    def set_rsl_y(self, y):
        self.rsl_y = y
    def get_rsl_y(self):
        return self.rsl_y