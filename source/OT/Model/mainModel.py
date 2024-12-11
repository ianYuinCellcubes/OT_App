class DataModel:
    def __init__(self):
        self.data = None
        self.monitor_index = 0
        self.monitor_count = 1
    def set_data(self, data):
        self.data = data
    def get_data(self):
        return self.data
    def set_monitor_index(self, data):
        self.monitor_index = data
    def get_monitor_index(self):
        return self.monitor_index
    def set_monitor_count(self, data):
        self.monitor_count = data
    def get_monitor_count(self):
        return self.monitor_count