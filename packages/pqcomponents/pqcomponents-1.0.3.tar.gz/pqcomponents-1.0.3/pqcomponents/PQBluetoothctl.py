from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

import PQBluetooth
import time
import pexpect
import subprocess
import re
import os
import glob


class BlutoothSignal(QObject):
    status = pyqtSignal(int)
    Confirm_Code = pyqtSignal(int)
    Insert_PinCode = pyqtSignal()


class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass


class Bluetoothctl(QThread):
    """A wrapper for bluetoothctl utility."""
    status = pyqtSignal(int)
    Confirm_Code = pyqtSignal(int)
    Insert_PinCode = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.child = pexpect.spawn("bluetoothctl", echo=False)
        self.ConnectedID = ""
        self.Pin_Code = " "
        self.Confirm_code = 0
        self.Confirm_sign = True
        self.endInsertPin = True
        self.mac_address = ""

    def init(self):
        self.child = pexpect.spawn("bluetoothctl", echo=False)

    def Close(self):
        self.child.close()

    def get_output(self, command, pause=0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        time.sleep(pause)
        if self.ConnectedID == "" or self.ConnectedID == "None":
            start_failed = self.child.expect(["bluetooth", pexpect.EOF, pexpect.TIMEOUT])
            if start_failed > 0:
                raise BluetoothctlError("Bluetoothctl failed after running (ConnectedId Is Null) " + command)
        else:
            start_failed = self.child.expect([pexpect.EOF, pexpect.TIMEOUT], 0.5)
            if start_failed > 1:
                raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.decode("utf-8").split("\r\n")

    def Agent_Set(self):
        try:
            self.child.send("agent off\n")
            print("agent off")
            time.sleep(0.5)
            self.child.send("agent NoInputNoOutput\n")
            print("agent NoInputNoOutput")
            time.sleep(0.5)
            self.child.send("default-agent\n")
            print("default-agent")
            # print(out)
        except BluetoothctlError as e:
            print(e)
            return None

    def start_scan(self):
        """Start bluetooth scanning process."""
        try:
            out = self.get_output("scan on")
        except BluetoothctlError as e:
            print(e)
            return None

    def stop_scan(self):
        """Stop bluetooth scanning process."""
        try:
            out = self.get_output("scan off")
        except BluetoothctlError as e:
            print(e)
            return None

    def make_discoverable(self):
        """Make device discoverable."""
        try:
            out = self.get_output("discoverable on")
        except BluetoothctlError as e:
            print(e)
            return None

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    if len(attribute_list) == 3:  # list의 항목이 3 이하일 경우 out of range Err때문에 길이 비교가 필요함
                        device = {
                            "mac_address": attribute_list[1],
                            "name": attribute_list[2]
                        }
        return device

    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        try:
            self.init()
            out = self.get_output("devices")
            self.Close()
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            out = self.get_output("paired-devices")
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)

            return paired_devices

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            self.init()
            out = self.get_output("paired-devices")
            self.Close()
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)

            return paired_devices

    def get_discoverable_devices(self):
        """Filter paired devices out of available."""
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]

    def get_device_info(self, mac_address):
        """Get device info by mac address."""
        try:
            self.init()
            self.child.send("info " + mac_address + "\n")
            time.sleep(0.1)
            res = self.child.expect(["Icon: printer", pexpect.EOF, pexpect.TIMEOUT], 0.1)  # Icon: printer 문구가 포함되어있는지 확인 후 True/False 반환
            if res == 0:
                return True
            else:
                return False
        except BluetoothctlError as e:
            print(e)
            return False

    def get_device_info_isConnected(self, mac_address):
        try:
            cmd = "bluetoothctl info " + str(mac_address)
            try:
                ret_value = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except Exception as e:
                print('Exception : ' + e)
                return False
            connected = ret_value.split("Connected: ")[1].split("\n")[0]
            if connected == "yes":
                return True
            elif connected == "no":
                return False
            else:
                return False
        except BluetoothctlError as e:
            print(e)
            return False

    def get_connectable_devices(self):  # 디바이스 커넥팅 상태 체크
        """Get a  list of connectable devices.
        Must install 'sudo apt-get install bluez blueztools' to use this"""
        try:
            res = []
            out = subprocess.check_output(["hcitool", "scan"])  # Requires 'apt-get install bluez'
            out = out.split("\n")
            device_name_re = re.compile("^\t([0-9,:,A-F]{17})\t(.*)$")
            for line in out:
                device_name = device_name_re.match(line)
                if device_name != None:
                    res.append({
                        "mac_address": device_name.group(1),
                        "name": device_name.group(2)
                    })
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            return res

    def is_connected(self):
        """Returns True if there is a current connection to any device, otherwise returns False"""
        try:
            res = False
            out = subprocess.check_output(["hcitool", "con"])  # Requires 'apt-get install bluez'
            out = out.split("\n")
            mac_addr_re = re.compile("^.*([0-9,:,A-F]{17}).*$")
            for line in out:
                mac_addr = mac_addr_re.match(line)
                if mac_addr != None:
                    res = True
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            return res

    @pyqtSlot()
    def run(self):
        print(self.ConnectedID)
        self.init()
        if self.ConnectedID == "" or self.ConnectedID == "None":
            try:

                self.Agent_Set()
                out = self.get_output("pair " + self.mac_address, 5)
            except BluetoothctlError as e:
                print(e)
                self.status.emit(False)
            else:
                try:
                    res = self.child.expect(
                        ["Request confirmation", "Request PIN code", "Failed to pair", "Pairing successful",
                         "Paired: no", "Paired: yes", \
                         pexpect.EOF, pexpect.TIMEOUT])

                except Exception as e:
                    print(e)
                    self.status.emit(False)
                else:
                    if res == 0:
                        self.child.send("yes\n")
                        print("confirm")
                        res = self.child.expect(["(yes/no)", pexpect.EOF])
                        passkeylist = self.child.before.decode("utf-8").split(" ")
                    elif res == 1:
                        print("request PIN code")
                        self.Insert_PinCode.emit()
                        while self.endInsertPin:
                            time.sleep(0.1)
                        success = self.insertPIN()
                        self.status.emit(success)
                    elif res == 2:
                        print("Failed to pair")
                        success = False
                        self.status.emit(success)
                    elif res == 3:
                        print("Success to pair")
                        success = True
                        self.status.emit(success)
                    elif res == 4:
                        print("Failed to pair")
                        success = False
                        self.status.emit(success)
                    elif res == 5:
                        print("Success to pair")
                        success = True
                        self.status.emit(success)
                    else:
                        success = False
                        self.status.emit(success)

        else:
            try:
                print("disconnect")
                out = self.get_output("disconnect", 2)
            except BluetoothctlError as e:
                print(e)
                self.status.emit(False)
            else:
                try:
                    self.ConnectedID = ""
                    self.Agent_Set()
                    out = self.get_output("pair " + self.mac_address, 5)
                except BluetoothctlError as e:
                    print(e)
                    self.status.emit(False)
                else:
                    try:
                        res = self.child.expect(
                            ["Request confirmation", "Request PIN code", "Failed to pair", "Pairing successful", \
                             pexpect.EOF, pexpect.TIMEOUT])

                    except Exception as e:
                        print(e)
                        self.status.emit(False)
                    else:
                        if res == 0:
                            self.child.send("yes\n")
                            print("confirm")
                            res = self.child.expect(["(yes/no)", pexpect.EOF])
                            passkeylist = self.child.before.decode("utf-8").split(" ")
                        elif res == 1:
                            print("request PIN code")
                            self.Insert_PinCode.emit()
                            while self.endInsertPin:
                                time.sleep(0.1)
                            success = self.insertPIN()
                            self.status.emit(success)
                        elif res == 2:
                            print("Failed to pair")
                            success = False
                            self.status.emit(success)
                        elif res == 3:
                            print("Success to pair")
                            success = True
                            self.status.emit(success)
                        else:
                            success = False
                            self.status.emit(success)

        self.Close()

    def init_Pair(self):
        self.child = pexpect.spawn("bluetoothctl", echo=False)

    def Close_Pair(self):
        self.child.close()

    def insertPIN(self):
        try:
            print("insertPIN")
            out = self.get_output(self.Pin_Code, 4)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            print(res)
            success = True if res == 1 else False
            return success

    def confirm_code(self, bConfirm):
        try:
            print("confirm_code")
        except BluetoothctlError as e:
            print(e)
            self.SIGNALS.status.emit(False)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            print(res)
            success = True if res == 1 else False
            self.SIGNALS.status.emit(success)
            return success

    def remove(self, mac_address, timeout=2):
        """Remove paired device by mac address, return success of the operation."""
        try:
            self.init()
            out = self.get_output("remove " + mac_address, timeout)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["not available", "Device has been removed", pexpect.EOF, pexpect.TIMEOUT], 0.2)
            success = True if res == 1 else False
            self.Close()
            return success

    def remove_cache(self, mac_address):		# 페어링 실패하였을 때 페어링 목록에서는 삭제되지만 캐시에는 목록에는 남아있는 문제로 인해 캐시를 삭제하는 작업 추가
        """Remove paired device by mac address, return success of the operation."""
        try:
            self.dongle_Mac = PQBluetooth.getBluetoothMacAddress()
            dirPath = "/var/lib/bluetooth/" + self.dongle_Mac + "/"+mac_address
            cmd = "rm -rf " + dirPath
            ret = subprocess.check_output(cmd, shell=True)
        except Exception as e:
            print("Exception : " + e)

    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address, 2)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def disconnect(self):
        """Try to disconnect to a device by mac address."""
        try:
            print("disconnect")
            out = self.get_output("disconnect", 2)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def trust(self, mac_address):
        """Trust the device with the given MAC address"""
        try:
            out = self.get_output("trust " + mac_address, 4)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["not available", "trust succeeded", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def start_agent(self):
        """Start agent"""
        try:
            out = self.get_output("agent on")
        except BluetoothctlError as e:
            print(e)
            return None

    def default_agent(self):
        """Start default agent"""
        try:
            out = self.get_output("default-agent")
        except BluetoothctlError as e:
            print(e)
            return None


class BluetoothUdate_List(QThread):
    bluetoothlist = pyqtSignal(dict)
    Pairedlist = pyqtSignal(list)

    def __init__(self):
        QObject.__init__(self)
        self.btList = []
        self.TempList = []
        self.PairList = []
        self.RetryList = []
        self.ThreadStopFlag = False
        self.ConnectedID = ""
        self.parent = Bluetoothctl()
        self.totalOutTime = 0.0
        self.start_time = 0.0
        self.end_time = 0.0
        self.during_time = 0.0
        self.bStartScan = False
        self.dongle_Mac = ""

    def Scan_Stop(self):
        self.parent.stop_scan()
        self.bStartScan = True
        print("scan stop")

    @pyqtSlot()
    def run(self):
        # 기존 Bluetoothctl 내 Cmd로 Scan 리스트와 Paired 리스트를 불러오는 방식을 /var/lib/bluetooth/내 파일 검색하는 방식으로 변경
        try:
            self.parent.ConnectedID = "Exist"
            self.parent.init()
            self.parent.start_scan()
            self.dongle_Mac = PQBluetooth.getBluetoothMacAddress()
            # 이전 캐시 삭제
            files = glob.glob("/var/lib/bluetooth/" + self.dongle_Mac + "/cache/*")
            for f in files:
                try:
                    os.remove(f)
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))
            time.sleep(3)

            self.btList.clear()
            self.TempList.clear()
            self.RetryList.clear()
            # 캐시에서 디바이스 mac 획득
            path_dir = "/var/lib/bluetooth/" + str(self.dongle_Mac) + "/cache"
            available = os.listdir(path_dir)
            # print(available)
            # 캐시에서 페어된 디바이스 Mac 획듯
            path_dir = "/var/lib/bluetooth/" + str(self.dongle_Mac)
            paired = os.listdir(path_dir)
            # print(paired)
            self.TempList = [d for d in available if d not in paired]  # TempList에 페어링된 BT 리스트 제외하고 삽입

            self.parent.stop_scan()
            if self.ThreadStopFlag == False:
                self.parent.Close()
                return
            for i in range(len(self.TempList)):
                # BT Print 구분 후 printer 아닌 항목 삭제
                if self.parent.get_device_info(self.TempList[i]):
                    if self.ThreadStopFlag == False:
                        break
                    else:
                        # 프린터인 디바이스의 이름을 가져와서 리스트형식으로 변환
                        path_dir = "/var/lib/bluetooth/" + str(self.dongle_Mac) + "/cache/" + str(self.TempList[i])
                        f = open(path_dir, encoding='utf-8')
                        f.seek(15)
                        name = f.readline()
                        device_name = name.split("\n")
                        device = {"mac_address": self.TempList[i], "name": device_name[0]}
                        self.btList.append(self.TempList[i])  # retry할때 사용할 리스트
                        self.bluetoothlist.emit(device)  # 실제 리스트에 띄울 device 정보 전송
                        del f

            paired = self.parent.get_paired_devices()  # 페어링된 BT 리스트
            self.PairList = paired
            if self.ThreadStopFlag == False:
                self.parent.Close()
                return
            self.Pairedlist.emit(self.PairList)  # 페어링된 BT 디바이스 하나씩 Emit

            if self.ThreadStopFlag == False:
                self.parent.Close()
                return

            self.parent.Close()

            self.ThreadStopFlag = False
        except BluetoothctlError as e:
            print(e)


class BluetoothPairing(QThread):
    status = pyqtSignal(int)
    Confirm_Code = pyqtSignal(int)
    Insert_PinCode = pyqtSignal()

    def __init__(self):
        QObject.__init__(self, child)
        self.mac_address = ""
        self.child = child  # pexpect.spawn("bluetoothctl", echo=False)
        self.Pin_Code = " "
        self.Confirm_code = 0
        self.Confirm_sign = True
        self.endInsertPin = True
        self.parent = Bluetoothctl()

    def get_output_Pair(self, command, pause=0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.parent.child.send(command + "\n")
        time.sleep(pause)
        if self.parent.ConnectedID == "" or self.parent.ConnectedID == "None":
            start_failed = self.parent.child.expect(["bluetooth", pexpect.EOF, pexpect.TIMEOUT])
            if start_failed > 0:
                raise BluetoothctlError("Bluetoothctl failed after running " + command)
        else:
            start_failed = self.parent.child.expect([pexpect.EOF, pexpect.TIMEOUT])
        return self.parent.child.before.decode("utf-8").split("\r\n")

    def init_Pair(self):
        self.parent.child = pexpect.spawn("bluetoothctl", echo=False)

    def Close_Pair(self):
        self.parent.child.close()

    def insertPIN(self):
        try:
            print("insertPIN")
            out = self.get_output_Pair(self.Pin_Code, 4)

        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.parent.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            print(res)
            success = True if res == 1 else False
            return success

    def confirm_code(self, bConfirm):
        try:
            print("confirm_code")
        except BluetoothctlError as e:
            print(e)
            self.status.emit(False)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            print(res)
            success = True if res == 1 else False
            self.status.emit(success)
            return success

    @pyqtSlot()
    def run(self):
        try:
            self.parent.Agent_Set()
            out = self.get_output_Pair("pair " + self.mac_address, 5)
        except BluetoothctlError as e:
            print(e)
            self.status.emit(False)
        else:
            try:
                res = self.parent.child.expect(
                    ["Request confirmation", "Request PIN code", "Failed to pair", "Pairing successful", pexpect.EOF,
                     pexpect.TIMEOUT])
            except Exception as e:
                print(e)
                self.status.emit(False)
            else:
                if res == 0:
                    # success = self.confirm_code("yes")
                    self.parent.child.send("yes\n")
                    print("confirm")
                    res = self.parent.child.expect(["(yes/no)", pexpect.EOF])
                    passkeylist = self.parent.child.before.decode("utf-8").split(" ")
                elif res == 1:
                    print("request PIN code")
                    self.Insert_PinCode.emit()
                    while self.endInsertPin:
                        time.sleep(0.1)
                    success = self.insertPIN()
                    self.status.emit(success)
                elif res == 2:
                    print("Failed to pair")
                    success = False
                    self.status.emit(success)
                elif res == 3:
                    print("Success to pair")
                    success = True
                    self.status.emit(success)
                else:
                    success = False
                    self.status.emit(success)
