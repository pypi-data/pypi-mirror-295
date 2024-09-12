
import platform
import wifi
import os
import subprocess

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

global strOS
strOS = platform.system()
if strOS == "Linux":
    NETWORK_INTERFACE_WIFI = 'wlan0'
else:
    NETWORK_INTERFACE_WIFI = 'Wi-Fi'    # Need to check

WIFI_CMD_RETURN_OK = 0
WIFI_CMD_RETURN_EXIST = 256

class PQWifi(QObject):
    status = pyqtSignal(int, object)
    message = pyqtSignal(object, object)
    ERROR = -1
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTING = 3
    DISCONNECTED = 4
    COMPLETED = 5
    STOP = 6

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    def __init__(self, mode, ssid, password):
        QObject.__init__(self)
        self.mode = mode
        self.ssid = ssid
        self.password = password
        self.signal = self.SIG_NORMAL

    @pyqtSlot()
    def start(self):
        if self.mode:   # Connect
            try:
                cell = self.findFromNetworkList(self.ssid)
            except OSError as err:
                self.status.emit(self.STOP, '')
            else:
                self.status.emit(self.CONNECTING, '')
                if self.signal == self.SIG_NORMAL and cell:
                    res = self.connectWifi(self.ssid, self.password)
                    if res:
                        self.status.emit(self.CONNECTED, self.ssid)
                        while True:
                            if self.signal == self.COMPLETED:
                                self.status.emit(self.STOP, 'Connected')
                                break
                    else:
                        self.status.emit(self.STOP, 'FailToConnect')
            finally:
                self.status.emit(self.STOP, '')
        else:   # Disconnect
            try:
                ret = self.disconnectWifi()
            except OSError as err:
                self.status.emit(self.STOP, '')
            else:
                self.status.emit(self.DISCONNECTING, '')
                if self.signal == self.SIG_NORMAL:
                    self.status.emit(self.DISCONNECTED, self.ssid)
                    if ret:
                        while True:
                            if self.signal == self.COMPLETED:
                                self.status.emit(self.STOP, '')
                                break
                    else:
                        self.status.emit(self.STOP, '')
            finally:
                self.status.emit(self.STOP, '')

    def findFromNetworkList(self, ssid):
        try:
            networklist = wifi.Cell.all('wlan0')
            for cell in networklist:
                if cell.ssid == ssid:
                    return cell
        except Exception as e:
            print('Exception : ' + e)
        return []

    def connectWifi(self, ssid, password=None):
        try:
            self.disconnectWifi()
            if password=="":
                # cmd = "wpa_passphrase \"" + ssid + "\" \"None\" > /etc/wpa_supplicant.conf"
                cmd = "echo -e \"network={\n\tkey_mgmt=NONE\n\tpriority=-999\n}\" > /etc/wpa_supplicant.conf"
            else:
                cmd = "wpa_passphrase \"" + ssid + "\" \"" + password + "\" > /etc/wpa_supplicant.conf"
            ret = os.system(cmd)
            if ret == WIFI_CMD_RETURN_OK:
                cmd = "wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant.conf"
                ret = os.system(cmd)
                if ret == WIFI_CMD_RETURN_OK:
                    return True
                else:
                    return False
        except Exception as e:
            print('Exception : ' + e)
            return False

    def disconnectWifi(self):
        try:
            cmd = "killall -9 wpa_supplicant"
            ret = os.system(cmd)
            cmd = "ifconfig wlan0 down"
            ret = os.system(cmd)
            cmd = "ifconfig wlan0 up"
            ret = os.system(cmd)
            return True
        except Exception as e:
            print('Exception : ' + e)
            return False

    def completed(self):
        self.signal = self.COMPLETED

    def close(self):
        self.signal = self.SIG_STOP


DEF_WIFI_MODULE_NAME = "0bda:8179"
def existWifiUSBModule():
    if strOS == "Windows":
        return True

    try:
        cmd = "lsusb"
        ret_value = subprocess.check_output(cmd, shell=True).decode('utf-8')
        if ret_value.__contains__(DEF_WIFI_MODULE_NAME):
            return True
        else:
            return False
    except Exception as e:
        print('Exception : ' + e)
        return False

def InsertWlanModule():
    try:
        # Insert a module into the Linux kernel
        cmd = "insmod /usr/bin/wlan.ko"
        ret = os.system(cmd)
    except Exception as e:
        print('Exception ' + e)
        return False
    return True

def FindFromNetworkList(ssid):
    networklist = wifi.Cell.all('wlan0')
    for cell in networklist:
        if cell.ssid == ssid:
            return cell
    return []

def UpdateNetworkList():
    networklist = []
    try:
        cells = wifi.Cell.all(NETWORK_INTERFACE_WIFI)
        for cell in cells:
            networklist.append([cell.signal, cell.ssid, cell.encrypted])

    except Exception as e:
        print('Exception : ' + e)
    except UnboundLocalError as e:
        print('UnboundLocalError : ' + e)
    except:
        print('Except')
    return networklist

def UpdateNetworkListWithoutSsid(ssid):
    networklist = []
    try:
        cells = wifi.Cell.all(NETWORK_INTERFACE_WIFI)
        for cell in cells:
            if ssid != cell.ssid:
                duplicate = False
                for value in networklist:
                    if value[1] == cell.ssid:
                        duplicate = True
                if not duplicate:
                    networklist.append([cell.signal, cell.ssid, cell.encrypted])

    except Exception as e:
        print('Exception : ' + e)
    except UnboundLocalError as e:
        print('UnboundLocalError : ' + e)
    except:
        print('Except')
    return networklist

def GetCurrentNetwork():
    try:
        output = subprocess.check_output(['iwgetid'])
        currentSsid = output.decode().split('"')[1]
        return currentSsid
    except Exception as e:
        print('Exception : ' + e)
        return None

def GetCellInfo(ssid):
    try:
        cells = wifi.Cell.all(NETWORK_INTERFACE_WIFI)
        for cell in cells:
            if cell.ssid == ssid:
                return cell
    except Exception as e:
        print('Exception : ' + e)
    except UnboundLocalError as e:
        print('UnboundLocalError : ' + e)
    except:
        print('Except')
    return None

def Connect(ssid, password=None):
    try:
        cmd = "wpa_passphrase \"" + ssid + "\" \"" + password + "\" > /etc/wpa_supplicant.conf"
        ret = os.system(cmd)
        if ret == WIFI_CMD_RETURN_OK:
            cmd = "wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant.conf"
            ret = os.system(cmd)
            return True
    except Exception as e:
        print('Exception : ' + e)
        return False

def Disconnect():
    try:
        cmd = "killall -9 wpa_supplicant"
        ret = os.system(cmd)
        cmd = "ifconfig wlan0 down"
        ret = os.system(cmd)
        cmd = "ifconfig wlan0 up"
        ret = os.system(cmd)
        return True
    except Exception as e:
        print('Exception : ' + e)
        return False

def AutoConnection():
    try:
        cmd = "wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant.conf"
        ret = os.system(cmd)
        return True
    except Exception as e:
        print('Exception : ' + e)
    return False

def GetQualityLevel():
    signal = -9999
    try:
        cmd = "cat /proc/net/wireless | grep wlan0"
        ret_value = subprocess.check_output(cmd, shell=True).decode("utf-8")
        signal = int(ret_value.split(".")[1])
    except Exception as e:
        print('Exception : ' + e)
    return signal
