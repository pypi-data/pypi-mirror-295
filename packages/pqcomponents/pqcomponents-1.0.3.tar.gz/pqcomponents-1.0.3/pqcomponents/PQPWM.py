
import os
import subprocess

# PWM : Init (Not used : /etc/init.d/nbs-start.sh)
def PWM_Init():
    try:
        # IrLed(PWM3)
        listPWMExport = ["3"]
        listPWMPriod = ["1000000"]
        listPWMDutyCycle = ["500000"]
        for cnt in range(0, len(listPWMExport)):
            # export
            cmd = "echo " + listPWMExport[cnt] + " > /sys/class/pwm/pwmchip0/export"
            os.system(cmd)
            # period
            cmd = "echo " + listPWMPriod[cnt] + " > /sys/class/pwm/pwmchip0/pwm" + listPWMExport[cnt] + "/period"
            os.system(cmd)
            # duty_cycle
            cmd = "echo " + listPWMDutyCycle[cnt] + " > /sys/class/pwm/pwmchip0/pwm" + listPWMExport[cnt] + "/duty_cycle"
            os.system(cmd)
    except Exception as e:
        print('Exception : ' + e)

# PWM : enable
def set_pwm_enable_val(pwmNum, val):
    try:
        cmd = "echo  " + str(val) + " > /sys/class/pwm/pwmchip0/pwm" + str(pwmNum) + "/enable"
        os.system(cmd)
    except Exception as e:
        print('Exception : ' + e)

def get_pwm_enable_val(pwmNum):
    try:
        cmd = "cat /sys/class/pwm/pwmchip0/pwm" + str(pwmNum) + "/enable"
        ret_value = subprocess.check_output(cmd, shell=True)
        decode_value = ret_value.decode("utf-8")
        return int(decode_value)
    except Exception as e:
        print('Exception : ' + e)

# PWM : period
def set_pwm_period_val(pwmNum, val):
    try:
        cmd = "echo  " + str(val) + " > /sys/class/pwm/pwmchip0/pwm" + str(pwmNum) + "/period"
        os.system(cmd)
    except Exception as e:
        print('Exception : ' + e)

def get_pwm_period_val(pwmNum):
    try:
        cmd = "cat /sys/class/pwm/pwmchip0/pwm" + str(pwmNum) + "/period"
        ret_value = subprocess.check_output(cmd, shell=True)
        decode_value = ret_value.decode("utf-8")
        return int(decode_value)
    except Exception as e:
        print('Exception : ' + e)

# PWM : duty_cycle
def set_pwm_duty_cycle_val(pwmNum, val):
    try:
        cmd = "echo  " + str(val) + " > /sys/class/pwm/pwmchip0/pwm" + str(pwmNum) + "/duty_cycle"
        os.system(cmd)
    except Exception as e:
        print('Exception : ' + e)

def get_pwm_duty_cycle_val(pwmNum):
    try:
        cmd = "cat /sys/class/pwm/pwmchip0/pwm" + str(pwmNum) + "/duty_cycle"
        ret_value = subprocess.check_output(cmd, shell=True)
        decode_value = ret_value.decode("utf-8")
        return int(decode_value)
    except Exception as e:
        print('Exception : ' + e)


# out_voltage0_raw : enable/disable - 500(OFF) or value
# out_voltage0_raw
def set_voltage_val(val):
    try:
        cmd = "echo  " + str(val) + " > /sys/bus/i2c/drivers/mcp4725/3-0060/iio:device1/out_voltage0_raw"
        os.system(cmd)
    except Exception as e:
        print('Exception : ' + e)

def get_voltage_val():
    try:
        cmd = "cat /sys/bus/i2c/drivers/mcp4725/3-0060/iio:device1/out_voltage0_raw"
        ret_value = subprocess.check_output(cmd, shell=True)
        decode_value = ret_value.decode("utf-8")
        return int(decode_value)
    except Exception as e:
        print('Exception : ' + e)
