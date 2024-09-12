
import socket
import psutil

mode_Windows = 0
mode_Linux = 1

def getEthernetConnection(mode):
    ret = False

    try:
        if mode == mode_Linux:
            networkInterfaceName = "eth0"
        else:
            networkInterfaceName = "이더넷"

        net_if = psutil.net_if_addrs()
        for snicaddr in net_if[networkInterfaceName]:
            if snicaddr.family == socket.AF_INET:
                ret = True
                break
    except Exception as e:
        print('Exception : ' + e)
    return ret

def getEthernetIPAddress(mode):
    ipv4_add = '0.0.0.0'
    try:
        if mode == mode_Linux:
            networkInterfaceName = "eth0"
        else:
            networkInterfaceName = "이더넷"

        net_if = psutil.net_if_addrs()
        try:
            for snicaddr in net_if[networkInterfaceName]:
                if snicaddr.family == socket.AF_INET:
                    ipv4_add = snicaddr.address
                    break
        except Exception as e:
            print('Exception : ' + e)
    except Exception as e:
        print('Exception : ' + e)
    return ipv4_add
