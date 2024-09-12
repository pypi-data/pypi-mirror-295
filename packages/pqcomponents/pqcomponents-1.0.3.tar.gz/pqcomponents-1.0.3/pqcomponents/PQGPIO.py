
import os
import subprocess

LIST_GPIO = [["GPIO1_D5", "high", 1],
             ["GPIO2_A0", "out", 0],
             ["GPIO1_D6", "out", 0]]

EN_GPIO_BARCODE_READER_CONTROL = ["GPIO0_A4", "high", 1]

def GPIO_Init():
    try:
        for cnt in range(0, len(LIST_GPIO)):
            LIST_GPIO[cnt][2] = calculate_gpio_pin(LIST_GPIO[cnt][0])
            cmd = "echo " + LIST_GPIO[cnt][2] + " > /sys/class/gpio/export"
            print("GPIO_Init : {0}" + cmd)
            os.system(cmd)
            cmd = "echo " + LIST_GPIO[cnt][1] + " > /sys/class/gpio/gpio" + LIST_GPIO[cnt][2] + "/direction"
            print("GPIO_Init : {0}" + cmd)
            os.system(cmd)

        EN_GPIO_BARCODE_READER_CONTROL[2] = calculate_gpio_pin(EN_GPIO_BARCODE_READER_CONTROL[0])
        cmd = "echo " + EN_GPIO_BARCODE_READER_CONTROL[2] + " > /sys/class/gpio/export"
        print("GPIO_Init : {0}" + cmd)
        os.system(cmd)
        cmd = "echo " + EN_GPIO_BARCODE_READER_CONTROL[1] + " > /sys/class/gpio/gpio" + EN_GPIO_BARCODE_READER_CONTROL[2] + "/direction"
        print("GPIO_Init : {0}" + cmd)
        os.system(cmd)

    except Exception as e:
        print("Exception" + e)


# ROC-RK3566-PC GPIO Pin to calculate
# ex> GPIO4_D5
# bank  : GPIO0=0, GPIO1=1, GPIO2=2, GPIO3=3, GPIO4=4
# group : A=0, B=1, C=2, D=3
# X     = 0, 1, 2, 3, 4, 5, 6, 7
# pin = (bank * 32) + (group * 8) + X = (4 * 32) + (3 * 8) + 5 = 157
def calculate_gpio_pin(gpio):
    gpioTmp = gpio.replace("GPIO", "").replace("_", "")
    bank = int(gpioTmp[0])
    group = int(ord(gpioTmp[1]) - 0x41)
    x = int(gpioTmp[2])
    pin = (bank * 32) + (group * 8) + x
    return str(pin)


def set_gpio_control_val(gpioNum, val):
    try:
        cmd = "echo  " + str(val) + " > /sys/class/gpio/gpio" + str(gpioNum) + "/value"
        os.system(cmd)
    except Exception as e:
        print("Exception" + e)


def get_gpio_control_val(gpioNum):
    try:
        cmd = "cat /sys/class/gpio/gpio" + str(gpioNum) + "/value"
        ret_value = subprocess.check_output(cmd, shell=True)
        decode_value = ret_value.decode("utf-8")
        return int(decode_value)
    except Exception as e:
        print("Exception" + e)

