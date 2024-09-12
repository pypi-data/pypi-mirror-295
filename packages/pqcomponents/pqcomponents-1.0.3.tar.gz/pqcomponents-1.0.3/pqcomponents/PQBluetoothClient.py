from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

import bluetooth
import time

DEFAULT_SOCKET_DATA_SIZE = 1024

class PQBluetoothClient(QThread):
    ConnectingCheck = pyqtSignal(bool)
    PrinterStates = pyqtSignal(bool)
    def __init__(self, mac=None, port=None):
        QThread.__init__(self)
        self.mac = mac
        self.port = port
        self.cnt = 0
        self.bluetoothClientSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.clientCloseOnOff = False
        self.PopupFlag = False
        self.retryCnt = 0

    def init(self, mac, port):
        self.mac = mac
        self.port = port

    @pyqtSlot()
    def start(self):
        for self.retryCnt in range(0,3):
            try:
                if self.clientCloseOnOff == True:
                    self.close()
                self.bluetoothClientSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                try:
                    self.bluetoothClientSocket.connect((self.mac, self.port))
                    self.bluetoothClientSocket.settimeout(1)
                    time.sleep(0.1)
                except Exception as e:
                    if str(e).__contains__("timed out"):
                         pass
                    else:
                        if self.retryCnt == 2:
                            self.ConnectingCheck.emit(False)
                else:
                    self.ConnectingCheck.emit(True)
                    break
            except Exception as e:
                print('Exception : ' + e)
                if self.retryCnt == 2:
                    self.ConnectingCheck.emit(False)

    def SendSocketBuffer(self, buffer):
        try:
            self.bluetoothClientSocket.sendall(buffer)
        except Exception as e:
            print('Exception : ' + e)
        else:
           print('PQBluetoothClient sendMsg OK')

    def Retry_Connect(self):
        try:
            for item in range(0, 2):
                self.bluetoothClientSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                try:
                    self.bluetoothClientSocket.connect((self.mac, int(self.port)))
                    self.bluetoothClientSocket.settimeout(1)
                except Exception as e:
                    if str(e).__contains__("timed out"):
                         pass
                else:
                    self.PopupFlag = True
                    self.ConnectingCheck.emit(True)
                    break
        except Exception as e:
            self.PopupFlag = True
            self.ConnectingCheck.emit(False)


    def close(self):
        print('ComBluetoothClient close')
        self.bluetoothClientSocket.close()

