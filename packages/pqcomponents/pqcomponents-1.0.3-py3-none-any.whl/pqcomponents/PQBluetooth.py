import os
import subprocess
import platform

def bluetoothInit():
    print("bluetootInit")

def existBluetoothUSBModule(module):
    strOS = platform.system()
    if strOS == "Windows":
        return True

    try:
        cmd = "lsusb"
        ret_value = subprocess.check_output(cmd, shell=True).decode('utf-8')
        if ret_value.__contains__(module):
            return True
        else:
            return False
    except Exception as e:
        print("Exception : " + e)
        return False

def getBluetoothMacAddress():
    try:
        deviceId = "hci0"
        cmd = "hciconfig " + deviceId
        # ret = os.system(cmd + ' ' + deviceId)
        ret_value = subprocess.check_output(cmd, shell=True).decode('utf-8')
        btMac = ret_value.split("{}:".format(deviceId))[1].split("BD Address: ")[1].split(" ")[0].strip()
    except Exception as e:
        print("Exception : " + e)
        return None
    return btMac

def getBluetoothName(mac):
    try:
        if mac != "":
            cmd = "hcitool name " + mac
            ret_value = subprocess.check_output(cmd, shell=True).decode('utf-8').rstrip('\n')
            print("getBluetoothMacAddress cmd:" + cmd + ", ret_value:", ret_value)
            return ret_value
        else:
            print("getBluetoothMacAddress mac is empty!")
    except Exception as e:
        print("Exception : " + e)
    return None


def startBluetooth():
    try:
        # Step 1 : Bluetooth Demon On
        cmd = "/usr/libexec/bluetooth/bluetoothd --compat &"
        ret = os.system(cmd)
        print("setBluetoothOn cmd(1/2):" + cmd + ", ret:", ret)

        # Sleep이 없을 경우 아래 명령어 적용 안됨
        # time.sleep(0.1)
        cmd = "hciconfig hci0 down"
        ret = os.system(cmd)
        print("setBluetoothOff cmd(2/2):" + cmd + ", ret:", ret)

    except Exception as e:
        print("Exception : " + e)
        return False

# def setBluetoothOn(mac, port):
def setBluetoothOn(btName):
    try:
        # Step 1 : Serial Port Add
        cmd = "sdptool add --channel=1 SP"
        ret = os.system(cmd)
        print("setBluetoothOn cmd(1/5):" + cmd + ", ret:", ret)

        # Step 2 : BT Up
        cmd = "hciconfig hci0 up"
        ret = os.system(cmd)
        print("setBluetoothOn cmd(2/5):" + cmd + ", ret:", ret)

        # Step 3 : BT Rename
        cmd = "hciconfig hci0 name \"" + btName + "\""
        ret = os.system(cmd)
        print("setBluetoothOn cmd(3/5):" + cmd + ", ret:", ret)

        # Step 4 : BT Reset
        cmd = "hciconfig hci0 reset"
        ret = os.system(cmd)
        print("setBluetoothOn cmd(4/5):" + cmd + ", ret:", ret)

        # Step 5 : BT Scan
        cmd = "hciconfig hci0 piscan"
        ret = os.system(cmd)
        print("setBluetoothOn cmd(5/5):" + cmd + ", ret:", ret)

        return True
    except Exception as e:
        print("Exception : " + e)
        return False

def setBluetoothOff():
    try:
        # Step 1 : BT Down
        cmd = "hciconfig hci0 down"
        ret = os.system(cmd)
        print("setBluetoothOff cmd(1/3):" + cmd + ", ret:", ret)

        # Step 2 : Serial Handle Search
        cmd = "sdptool browse local"
        ret = subprocess.check_output(cmd, shell=True).decode('utf-8')
        recHandle = ret.split("Service Name: Serial Port")[1].split("Service RecHandle: ")[1].split("Service Class ID List:")[0].strip()
        print("setBluetoothOff cmd(2/3):" + cmd + ", ret:" + ret + ", RecHandle:" + recHandle)

        # Step 3 : Serial Del
        cmd = "sdptool del " + recHandle
        ret = os.system(cmd)
        print("setBluetoothOff cmd(3/3):" + cmd + ", ret:", + ret)

        return True
    except Exception as e:
        print("Exception : " + e)
        return False

def setBluetoothClear(mac):
    try:
        cmd = "rm -rf /var/lib/bluetooth/" + mac
        ret = os.system(cmd)
        print("setBluetoothClear cmd:" + cmd + ", ret:", ret)
    except Exception as e:
        print("Exception : " + e)
        return