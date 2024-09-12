import serial
import time
import signal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject


class MyError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class DefSerial():
    COM_BaudRate            = 115200    #115200

    COM_STX                 = 0x02
    COM_ETX                 = 0x03
    COM_CR                  = 0x0D
    # COM_ACK                 = 0x06
    # COM_NAK                 = 0x15
    # COM_SYN                 = 0x16

    # Def
    LimitLen                 = 5
    TimeOut                  = 5                        # time out


class threadSerialCom(QObject):
    threadReceiveEvent = pyqtSignal(int)
    threadFinished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.isRun = False

    def setSerialHandle(self, ser):
        self.ser = ser

    @pyqtSlot()
    def run(self):
        while self.isRun:
            time.sleep(1 / 1000)
            try:
                n = self.ser.inWaiting()
                if n:
                    szChar = self.ser.read(n)
            except serial.SerialException as e:
                print('SerialException : ' + e)
            else:
                if n:
                    for oneByte in szChar:
                        self.threadReceiveEvent.emit(oneByte)
        self.threadFinished.emit()

class PQSerial(QWidget):
    def __init__(self, parent, port, baud):
        super().__init__(parent)

        self.parent = parent
        self.port = port                  # USB to Serial (CP210x)
        self.baud = baud                  # 시리얼 보드레이트(통신속도)
        self.Variable_Init()

    def Variable_Init(self):
        self.szRxData = []                # 라인 단위로 데이터 가져올 리스트 변수
        self.szOldCmd = []

        self.worker = threadSerialCom()
        self.theadSerial = QThread()
        self.theadSerial.started.connect(self.worker.run)  # Init worker run() at startup (optional)
        self.worker.threadReceiveEvent.connect(self.threadEventHandler_ReceiveEvent)
        self.worker.threadFinished.connect(self.threadEventHandler_Finished)
        self.worker.moveToThread(self.theadSerial)

    # --------------------------------------------------------------------------------------------------
    # Protocol Status Thread Handler
    # --------------------------------------------------------------------------------------------------
    @pyqtSlot(int)
    def threadEventHandler_ReceiveEvent(self, szChar):
        szTemp = []
        self.szRxData.append(szChar)        # linux -> szChar(int) 값이 할당됨, [2,70,86,49,52...]
        szTemp.append(szChar)
        if szChar == DefSerial.COM_CR:  # 라인의 끝을 만나면.. 0x0D
            nLen = len(self.szRxData)
            if self.BoardSerialCheck(nLen):
                self.parent.RxDataParsing(self.szRxData, nLen)
            # ---------------------------------------------------------------------------------------------------------------------------
            del szTemp[:]
            del self.szRxData[:]

    @pyqtSlot()
    def threadEventHandler_Finished(self):
        try:
            self.ser.close()
        except serial.serialutil.SerialException as e:
            print('SerialException : ' + e)

    def SerialOpen(self):
        try:
            signal.signal(signal.SIGINT, self.handler)
            self.ser = serial.Serial(self.port, self.baud, timeout=0)
            if not self.theadSerial.isRunning():
                self.worker.setSerialHandle(self.ser)
                self.worker.isRun = True
                self.theadSerial.start()
            else:
                self.theadSerial.quit()
                self.theadSerial.wait(5000)
        except serial.serialutil.SerialException as e:
            print('SerialException : ' + e)
            return False
        return True

    @pyqtSlot()
    def SerialComStop(self):
        if self.theadSerial.isRunning():
            self.worker.isRun = False
            self.theadSerial.quit()
            self.theadSerial.wait(1000)
        if self.ser.isOpen():
            self.ser.close()


    # 쓰레드 종료용 시그널 함수
    def handler(self, signum, frame):
        print('handler')

    # 데이터 처리할 함수
    # 리스트 구조로 들어 왔기 때문에 작업하기 편하게 스트링으로 합침
    def parsing_data(self, data):
        tmp = ''.join(data)

    # --------------------------------------------------------------------------------------------------
    # Com Tx / Rx
    # --------------------------------------------------------------------------------------------------
    def MsgLog(self, header, buff):   # buff -> list
        szMsg = ""
        for item in range(len(buff)):
            szMsg += "%02x " % (buff[item])
            if 1 <= item <= 2:  # cmd
                szMsg += "(" + chr(buff[item]) + ")"

    def BoardSerialCheck(self, nLen):
        if nLen < DefSerial.LimitLen: return False
        elif self.szRxData[0] != DefSerial.COM_STX: return False
        elif self.szRxData[nLen - 4] != DefSerial.COM_ETX: return False
        elif self.szRxData[nLen - 1] != DefSerial.COM_CR: return False

        ckSum = []
        self.CheckSum(self.szRxData[1:], nLen - DefSerial.LimitLen, ckSum)
        if ckSum[0] != self.szRxData[nLen - 3] or ckSum[1] != self.szRxData[nLen - 2]: return False
        return True

    def SerialWrite(self, data, len):
        if len >= 2:  # Recent Command Register
            del self.szOldCmd[:]
            self.szOldCmd.append(data[0])
            self.szOldCmd.append(data[1])

        ckSum = []
        buffer = bytearray()
        buffer.append(DefSerial.COM_STX)
        for i in range(0, len): buffer.append(data[i])
        buffer.append(DefSerial.COM_ETX)
        self.CheckSum(data, len, ckSum)
        buffer.append(ckSum[0])
        buffer.append(ckSum[1])
        buffer.append(DefSerial.COM_CR)
        self.ser.write(buffer)
        time.sleep(0.1)
        self.MsgLog("Tx : ", buffer)

    def CheckSum(self, data, len, ckSum):
        nSum = 0
        for i in range(0, len): nSum = nSum + data[i]
        ckSum.append(self.Hex2Char((nSum & 0xF0) >> 4))
        ckSum.append(self.Hex2Char((nSum & 0x0F) >> 0))
        return ckSum

    def Hex2Char(self, nHex):
        if nHex < 10: szChar = nHex + ord('0')          # 48('0')
        elif nHex < 16: szChar = nHex - 10 + ord('A')   # 65('A')
        else: szChar = 0                                # Error
        return szChar
