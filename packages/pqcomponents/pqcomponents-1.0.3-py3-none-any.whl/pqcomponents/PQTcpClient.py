
import os
import platform

import socket

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

global strOS
strOS = platform.system()

EN_TEST_RUN_MODE = 0
EN_TEST_QC_MODE = 1

DEF_CLOUD_PROTOCOL_SAVE_TX_BUFFER = False

DEF_CLOUD_PROTOCOL_COMMAND_RAW_DATA_TEST = "rawdatatest/"
DEF_CLOUD_PROTOCOL_COMMAND_RAW_DATA_QC = "rawdataqc/"

DEF_CLOUD_PROTOCOL_COMMAND_IMAGE_TEST = "imagetest/"
DEF_CLOUD_PROTOCOL_COMMAND_IMAGE_QC = "imageqc/"

E201 = "[E201] No message from server"
E202 = "[E202] NACK(Step:{0}/4) from server"
E203 = "[E203] Wrong server data"

DEFAULT_SOCKET_DATA_SIZE = 1024
MAX_TIMEOUT_COUNT = 30  # 30 SEC
SHOW_POPUP_CANCEL_BUTTON_COUNT = 3  # 3 SEC

class PQTcpClient(QObject):
    status = pyqtSignal(int, object)
    message = pyqtSignal(object, object)
    ERROR = -1
    LISTEN = 1
    CONNECTED = 2
    STOP = 3
    SHOW_BTN = 4

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    DEF_STX = bytearray(b'rdt://')
    DEF_ETX = bytearray(b'#end')
    DEF_CR = 0x0D
    DEF_LF = 0x0A
    DEF_ACK = 0x06
    DEF_NAK = 0x15
    DEF_SYN = 0x16

    def __init__(self, ip, port, modelName, DEF_STX, DEF_EXT):
        QObject.__init__(self)

        self.ip = ip
        self.port = port
        self.modelName = modelName

        self.DEF_STX = DEF_STX
        self.DEF_ETX = DEF_EXT

        self.tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpClientSocket.settimeout(1)
        self.errMsg = ''
        self.signal = self.SIG_NORMAL

        self.timeoutCnt = 0

    @pyqtSlot()
    def start(self):
        try:
            self.tcpClientSocket.connect((self.ip, self.port))
        except OSError as err:
            self.status.emit(self.ERROR, str(err))
        else:
            self.status.emit(self.CONNECTED, self.ip)

            while True:
                if self.signal == self.SIG_NORMAL:
                    try:
                        data = self.tcpClientSocket.recv(DEFAULT_SOCKET_DATA_SIZE)
                    except socket.timeout as t_out:
                        if self.timeoutCnt >= MAX_TIMEOUT_COUNT - 1:
                            self.errMsg = E201
                            self.status.emit(self.ERROR, self.errMsg)
                            break
                        else:
                            if self.timeoutCnt == SHOW_POPUP_CANCEL_BUTTON_COUNT - 1:
                                self.status.emit(self.SHOW_BTN, "")
                            self.timeoutCnt += 1
                        pass
                    except Exception as e:
                        print('Exception : ' + e)
                    else:
                        if data:
                            try:
                                self.message.emit(self.ip+':'+str(self.port), data.decode())
                            except Exception as e:
                                self.errMsg = E203
                                break
                        else:
                            self.errMsg = E201
                            break
                elif self.signal == self.SIG_DISCONNECT:
                    self.signal = self.SIG_NORMAL
                    self.tcpClientSocket.close()
                    break
        finally:
            self.status.emit(self.STOP, self.errMsg)

    def send(self, msg):
        self.tcpClientSocket.sendall(msg.encode())

    def sendMsg(self, filename, dataTx):
        try:
            buffer = bytearray()
            # STX(Start of TeXt) : rdt://
            for i in range(0, len(self.DEF_STX)): buffer.append(self.DEF_STX[i])
            encodedData = dataTx.encode()
            # LEN(Length of data) : 4byte (CMD Length + Data Length)
            dataLen = len(dataTx)
            buffer.append((dataLen >> 24) & 0xFF)
            buffer.append((dataLen >> 16) & 0xFF)
            buffer.append((dataLen >> 8) & 0xFF)
            buffer.append(dataLen & 0xFF)
            # CMD : data
            for i in range(0, len(dataTx)): buffer.append(encodedData[i])
            # ETX(End of TeXt) : #end
            for i in range(0, len(self.DEF_ETX)): buffer.append(self.DEF_ETX[i])
            # CS : checksum
            chkSum = 0
            for i in range(0, len(dataTx)):
                chkSum ^= ord(dataTx[i])
            buffer.append(chkSum)
            # CR(Carriage Return) : 0x0D
            buffer.append(DEF_CR)
            # LF(Line Feed) : 0x0A
            buffer.append(DEF_LF)
            self.tcpClientSocket.sendall(buffer)
            # Save buffer to file
            self.saveBufferData(filename, buffer)
        except Exception as e:
            print('Exception : ' + e)

    def sendImg(self, filename, mode, dataTx):
        try:
            buffer = bytearray()
            # STX(Start of TeXt) : rdt://
            for i in range(0, len(self.DEF_STX)): buffer.append(self.DEF_STX[i])
            # LEN(Length of data) : 4byte (CMD Length + Data Length)
            cmdData = mode.encode()
            cmdDataLen = len(cmdData)
            dataLen = cmdDataLen + len(dataTx)
            buffer.append((dataLen >> 24) & 0xFF)
            buffer.append((dataLen >> 16) & 0xFF)
            buffer.append((dataLen >> 8) & 0xFF)
            buffer.append(dataLen & 0xFF)
            # CMD : data
            for i in range(0, cmdDataLen): buffer.append(cmdData[i])
            for i in range(0, len(dataTx)): buffer.append(dataTx[i])
            # ETX(End of TeXt) : #end
            for i in range(0, len(self.DEF_ETX)): buffer.append(self.DEF_ETX[i])
            # CS : checksum
            chkSum = 0
            for i in range(0, cmdDataLen):
                chkSum ^= ord(mode[i])
            for i in range(0, len(dataTx)):
                chkSum ^= dataTx[i]
            buffer.append(chkSum)
            # CR(Carriage Return) : 0x0D
            buffer.append(DEF_CR)
            # LF(Line Feed) : 0x0A
            buffer.append(DEF_LF)
            self.tcpClientSocket.sendall(buffer)
            # Save buffer to file
            self.saveBufferData(filename, buffer)
        except Exception as e:
            print('Exception : ' + e)

    def close(self):
        self.signal = self.SIG_DISCONNECT

    def saveBufferData(self, filename, buffer):
        if DEF_CLOUD_PROTOCOL_SAVE_TX_BUFFER:
            if strOS == "Windows":
                strPath = os.getcwd() + "\\data\\" + filename + ".dat"
            else:
                strPath = "/root/" + self.modelName + "/data/" + filename + ".dat"
            with open(strPath, "wb") as f:
                f.write(buffer)



    def sendMsgAll(self, mode, dataTxArray, filename):
        try:
            buffer = bytearray()
            dataLen = 0
            # STX(Start of TeXt) : rdt://
            for i in range(0, len(self.DEF_STX)):
                buffer.append(self.DEF_STX[i])

            # LEN + CMD
            for i in range(0, len(dataTxArray)):
                if i == 0 or i == 1:    # devinfo/, datatest/
                    encodedData = dataTxArray[i].encode()
                    # LEN(Length of data) : 4byte (CMD Length + Data Length)
                    dataLen = len(dataTxArray[i])
                    buffer.append((dataLen >> 24) & 0xFF)
                    buffer.append((dataLen >> 16) & 0xFF)
                    buffer.append((dataLen >> 8) & 0xFF)
                    buffer.append(dataLen & 0xFF)
                    # CMD : data
                    for i in range(0, len(dataTxArray[i])):
                        buffer.append(encodedData[i])
                elif i == 2:            # rawdatatest/
                    rawFilePath = dataTxArray[i]
                    if os.path.exists(rawFilePath):
                        with open(rawFilePath) as file_object:
                            contents = file_object.read()
                    if mode == EN_TEST_RUN_MODE:
                        rawdataWithCmd = DEF_CLOUD_PROTOCOL_COMMAND_RAW_DATA_TEST + contents
                    elif mode == EN_TEST_QC_MODE:
                        rawdataWithCmd = DEF_CLOUD_PROTOCOL_COMMAND_RAW_DATA_QC + contents
                    encodedData = rawdataWithCmd.encode()
                    # LEN(Length of data) : 4byte (CMD Length + Data Length)
                    dataLen = len(rawdataWithCmd)
                    buffer.append((dataLen >> 24) & 0xFF)
                    buffer.append((dataLen >> 16) & 0xFF)
                    buffer.append((dataLen >> 8) & 0xFF)
                    buffer.append(dataLen & 0xFF)
                    # CMD : data
                    for i in range(0, len(rawdataWithCmd)):
                        buffer.append(encodedData[i])
                elif i == 3:            # imagetest/
                    imageFilePath = dataTxArray[i]
                    if os.path.exists(imageFilePath):
                        fd = open(imageFilePath, "rb")
                        imageContents = fd.read()
                    if mode == EN_TEST_RUN_MODE:
                        CmdData = DEF_CLOUD_PROTOCOL_COMMAND_IMAGE_TEST
                    elif mode == EN_TEST_QC_MODE:
                        CmdData = DEF_CLOUD_PROTOCOL_COMMAND_IMAGE_QC
                    imageCmdData = CmdData.encode()
                    imageCmdDataLen = len(imageCmdData)
                    dataLen = imageCmdDataLen + len(imageContents)
                    buffer.append((dataLen >> 24) & 0xFF)
                    buffer.append((dataLen >> 16) & 0xFF)
                    buffer.append((dataLen >> 8) & 0xFF)
                    buffer.append(dataLen & 0xFF)
                    # CMD : data
                    for i in range(0, imageCmdDataLen):
                        buffer.append(imageCmdData[i])
                    for i in range(0, len(imageContents)):
                        buffer.append(imageContents[i])

            # ETX(End of TeXt) : #end
            for i in range(0, len(self.DEF_ETX)):
                buffer.append(self.DEF_ETX[i])

            # CS : checksum
            chkSum = 0
            # CS : devinfo
            for i in range(0, len(dataTxArray[0])): chkSum ^= ord(dataTxArray[0][i])
            # CS : data
            for i in range(0, len(dataTxArray[1])): chkSum ^= ord(dataTxArray[1][i])
            # CS : rawdata
            for i in range(0, len(rawdataWithCmd)): chkSum ^= ord(rawdataWithCmd[i])
            # CS : image
            for i in range(0, imageCmdDataLen): chkSum ^= ord(CmdData[i])
            for i in range(0, len(imageContents)): chkSum ^= imageContents[i]
            buffer.append(chkSum)

            # CR(Carriage Return) : 0x0D
            buffer.append(self.DEF_CR)

            # LF(Line Feed) : 0x0A
            buffer.append(self.DEF_LF)
            self.tcpClientSocket.sendall(buffer)
            # Save buffer to file
            self.saveBufferData(filename, buffer)
        except Exception as e:
            print('Exception : ' + e)

