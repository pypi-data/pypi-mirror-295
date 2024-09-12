from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import bluetooth

DEFAULT_SOCKET_DATA_SIZE = 1024

class PQBluetoothServer(QObject):
    status = pyqtSignal(int, object)
    message = pyqtSignal(object, object)

    ERROR = -1
    LISTEN = 1
    CONNECTED = 2
    STOP = 3

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    def __init__(self, name, uuid, mac, port):
        QObject.__init__(self)
        self.name = name
        self.uuid = uuid
        self.mac = mac
        self.port = port
        self.signal = self.SIG_NORMAL
        try:
            self.bluetoothServerSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.bluetoothServerSocket.settimeout(1)
        except OSError as err:
            print('ComBluetoothServer OSError:', err)
            self.status.emit(self.STOP, 'OSError')

    @pyqtSlot()
    def start(self):
        try:
            print('ComBluetoothServer start bind mac:', self.mac + ", port:", self.port)
            self.bluetoothServerSocket.bind((self.mac, int(self.port)))  # bluetooth.PORT_ANY
            print('ComBluetoothServer start listen')
            self.bluetoothServerSocket.listen(1)
            print('ComBluetoothServer start advertise_service')
            bluetooth.advertise_service(self.bluetoothServerSocket, self.name, self.uuid)
        except OSError as err:
            print('ComBluetoothServer OSError:', err)
            self.status.emit(self.STOP, 'OSError')
        else:
            print('ComBluetoothServer start')
            self.status.emit(self.LISTEN, 'Start')
            while True:
                # Wait for a connection
                if self.signal == self.SIG_NORMAL:
                    print('wait for a connection')
                    try:
                        self.connection, addr = self.bluetoothServerSocket.accept()
                        self.connection.settimeout(1)
                    except Exception as e:
                        if str(e).__contains__("timed out"):
                            pass
                    else:
                        self.status.emit(self.CONNECTED, addr[0])
                        while True:
                            print('[waiting for data] self.signal:', self.signal)
                            if self.signal == self.SIG_NORMAL:
                                try:
                                    data = self.connection.recv(DEFAULT_SOCKET_DATA_SIZE)
                                except Exception as e:
                                    if str(e).__contains__("timed out"):
                                        pass
                                    else:
                                        self.signal = self.SIG_NORMAL
                                        self.connection.close()
                                        self.status.emit(self.LISTEN, 'Exception')
                                        break
                                else:
                                    if data:
                                        self.message.emit(addr[0], data.decode())
                                    else:
                                        self.status.emit(self.LISTEN, 'Normal')
                                        break
                            elif self.signal == self.SIG_DISCONNECT:
                                print('ComBluetoothServer disconnect')
                                self.signal = self.SIG_NORMAL
                                self.connection.close()
                                self.status.emit(self.LISTEN, 'Disconnect')
                                break
                else:
                    print('ComBluetoothServer close self.signal:', str(self.signal))
                    self.bluetoothServerSocket.close()
                    break
        finally:
            print('ComBluetoothServer stop')
            self.status.emit(self.STOP, 'finally')

    def sendMsg(self, msg):
        try:
            self.connection.sendall(msg.encode())
            print('ComBluetoothServer sendMsg OK')
        except Exception as e:
            print('Exception : ' + e)

    def sendFile(self, filePath):
        print('ComBluetoothServer file path:', filePath)
        try:
            fileToSend = open(str(filePath), 'rb')
            while True:
                data = fileToSend.readline()
                if data:
                    self.connection.send(data)
                else:
                    break
            fileToSend.close()
            print('sendFile OK')
        except Exception as e:
            print('Exception : ' + e)

    def disconnect(self):
        print('ComBluetoothServer disconnect')
        self.signal = self.SIG_DISCONNECT

    def close(self):
        print('ComBluetoothServer close')
        self.signal = self.SIG_STOP
