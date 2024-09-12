import serial
import time
import signal

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from serial import SerialException

class threadBarcodeTimer(QThread):
    threadReceiveEvent = pyqtSignal(object)
    threadFinished = pyqtSignal()
    threadTimeout = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.isRun = False
        self.timeoutCnt = 0
        self.timeout = 0

    def setBarcodeTimerHandle(self, handle):
        self.BarcodeHandle = handle

    def run(self):
        while self.isRun:
            try:
                time.sleep(1 / 1500)
                readLine = self.BarcodeHandle.readline()
                strData = readLine.decode('utf-8')
                if strData:
                    strData = strData.rstrip()
                    self.isRun = False
                    self.threadReceiveEvent.emit(strData)
                else:
                    self.timeoutCnt += 1

                if self.timeoutCnt >= int(self.timeout):
                    self.isRun = False
                    self.threadTimeout.emit()
            except Exception as e:
                print("Exception : " + e)

class PQBarcode(QWidget):
    def __init__(self, parent, port="/dev/ttyS1", baudrate=115200, timeout=15000):
        super().__init__(parent)

        self.parent = parent
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.Variable_Init()

    def Variable_Init(self):
        self.theadBarcode = threadBarcodeTimer(parent=self)
        self.theadBarcode.threadReceiveEvent.connect(self.threadEventHandler_ReceiveEvent)
        self.theadBarcode.threadFinished.connect(self.threadEventHandler_Finished)
        self.theadBarcode.threadTimeout.connect(self.threadEventHandler_Timeout)

    # --------------------------------------------------------------------------------------------------
    # Protocol Status Thread Handler
    # --------------------------------------------------------------------------------------------------
    @pyqtSlot(object)
    def threadEventHandler_ReceiveEvent(self, readData):
        self.parent.RxSetBarcodeInfoData(readData)

    @pyqtSlot()
    def threadEventHandler_Finished(self):
        try:
            self.BarcodeHandle.close()
        except SerialException as e:
            print("SerialException : " + e)
        except Exception as e:
            print("Exception : " + e)

    @pyqtSlot()
    def threadEventHandler_Timeout(self):
        try:
            self.BarcodeHandle.close()
            self.parent.RxSetBarcodeTimeout()
        except SerialException as e:
            print("SerialException : " + e)
        except Exception as e:
            print("Exception : " + e)

    def start(self):
        try:
            signal.signal(signal.SIGINT, self.handler)
            self.BarcodeHandle = serial.Serial(self.port, self.baudrate, timeout=0)
            if not self.theadBarcode.isRun:
                self.theadBarcode.setBarcodeTimerHandle(self.BarcodeHandle)
                self.theadBarcode.isRun = True
                self.theadBarcode.timeoutCnt = 0
                self.theadBarcode.timeout = self.timeout
                self.theadBarcode.start()
            else:
                self.stop()
        except SerialException as e:
            print("SerialException : " + e)
            return False
        return True

    @pyqtSlot()
    def stop(self):
        if self.theadBarcode.isRun:
            self.theadBarcode.isRun = False

    def checkBarcode(self):
        try:
            ret = serial.Serial(self.port, self.baudrate, timeout=0)
        except SerialException as e:
            print("SerialException : " + e)
            return False
        return True

