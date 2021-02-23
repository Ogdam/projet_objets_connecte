import time

class PluginTime:
    def response(self, args=None):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return "il est "+ current_time
