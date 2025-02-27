import time
import network


class WifiManager:
    def __init__(self, ssid, password, hostname = "IoT Button"):
        self.ssid = ssid
        self.password = password
        self.hostname = hostname

    def connect_wifi(self):
        print("SSID to connect to: " + self.ssid)
        print("Wifi Key to use: " + 'NotGonnaTellYou')
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('Connecting to Wifi: ', end="")
            sta_if.active(True)
            time.sleep_us(100)
            sta_if.config(dhcp_hostname=self.hostname)
            sta_if.connect(self.ssid, self.password)
            while not sta_if.isconnected():
                print('.', end="")
                time.sleep(1)
        print("*")
        print('Network config:', sta_if.ifconfig())
        print('hostname:', sta_if.config('dhcp_hostname'), '\n')