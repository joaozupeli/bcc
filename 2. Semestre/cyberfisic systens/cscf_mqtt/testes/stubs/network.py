import os
HW = os.getenv("HW_DIR", "/tmp/hw")
STA_IF = 0
class WLAN:
    def __init__(self, tipo):
        pass
    def active(self, x=None):
        return True
    def connect(self, ssid, senha):
        pass
    def isconnected(self):
        try:
            open(HW + "/wifi_down").close()
            return False
        except OSError:
            return True
