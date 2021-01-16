import socket

AUTH_OPEN, AUTH_WEP, AUTH_WPA_PSK, AUTH_WPA2_PSK, AUTH_WPA_WPA2_PSK = range(5)
STA_IF, AP_IF = range(2)

class WLAN:
    ACTIVITIES = [False, True]
    def __init__(self, interface_id: STA_IF | AP_IF):
        self.__interface = interface_id

    def active(self, is_active: bool = None):
        if is_active is not None:
            WLAN.ACTIVITIES[self.__interface] = is_active
        return WLAN.ACTIVITIES[self.__interface]

    def connect(self, ssid=None, password=None, *, bssid=None):
        pass

    def config(self, ssid, authmode, password):
        pass

    def isconnected(self):
        x = True
        return x

    def ifconfig(self,params=None): #[(ip, subnet, gateway, dns)])
        return (
            socket.gethostbyname(socket.gethostname()),
            '255.255.255.0', '10.0.0.1', '8.8.8.8'
        )
