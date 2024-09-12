
import socket
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

DEFAULT_SOCKET_DATA_SIZE = 1024

class PQTcpServer(QObject):
    status = pyqtSignal(int, object)
    message = pyqtSignal(object, object)

    ERROR = -1
    LISTEN = 1
    CONNECTED = 2
    STOP = 3

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    TCP_SERVER_COMMAND_01 = "COMMAND01"
    TCP_SERVER_COMMAND_02 = "COMMAND02"
    TCP_SERVER_COMMAND_03 = "COMMAND03"
    TCP_SERVER_COMMAND_04 = "COMMAND04"

    def __init__(self, ip, port):
        QObject.__init__(self)
        self.ip = ip
        self.port = port
        self.tcpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServerSocket.settimeout(1)
        self.tcpServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.signal = self.SIG_NORMAL

    @pyqtSlot()
    def start(self):
        try:
            self.tcpServerSocket.bind((self.ip, self.port))
            self.tcpServerSocket.listen(1)
        except OSError as err:
            self.status.emit(self.STOP, 'OSError')
        else:
            self.status.emit(self.LISTEN, 'Start')
            while True:
                # Wait for a connection
                if self.signal == self.SIG_NORMAL:
                    try:
                        self.connection, addr = self.tcpServerSocket.accept()
                        self.connection.settimeout(1)
                    except socket.timeout as t_out:
                        pass
                    else:
                        self.status.emit(self.CONNECTED, addr[0]+':'+str(addr[1]))
                        while True:
                            if self.signal == self.SIG_NORMAL:
                                try:
                                    data = self.connection.recv(DEFAULT_SOCKET_DATA_SIZE)
                                except socket.timeout as t_out:
                                    pass
                                except Exception as e:
                                    self.signal = self.SIG_NORMAL
                                    self.connection.close()
                                    self.status.emit(self.LISTEN, 'Exception')
                                    break
                                else:
                                    if data:
                                        self.message.emit(addr[0]+':'+str(addr[1]),data.decode())
                                    else:
                                        self.status.emit(self.LISTEN, 'Normal')
                                        break
                            elif self.signal == self.SIG_DISCONNECT:
                                self.signal = self.SIG_NORMAL
                                self.connection.close()
                                self.status.emit(self.LISTEN, 'Disconnect')
                                break

                elif self.signal == self.SIG_STOP:
                    self.tcpServerSocket.close()
                    break
        finally:
            self.status.emit(self.STOP, 'finally')

    def sendMsg(self, msg):
        try:
            self.connection.sendall(msg.encode())
        except Exception as err:
            raise Exception(err)

    def sendFile(self, filePath):
        try:
            fileToSend = open(str(filePath), 'rb')
            while True:
                data = fileToSend.readline()
                if data:
                    self.connection.send(data)
                else:
                    break
            fileToSend.close()
        except Exception as err:
            raise Exception(err)

    def disconnect(self):
        self.signal = self.SIG_DISCONNECT

    def close(self):
        self.signal = self.SIG_STOP
