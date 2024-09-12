
import os

DEF_SOUND_PLAY_LINUX_CMD = "aplay -Dplug:default -F 800 "

DEF_SOUND_SOURCE_KIND_PATH = ["start_1.wav", "start_2.wav", "start_3.wav", "start_4.wav","","","","","","",
                              "button_1.wav", "button_2.wav", "button_3.wav", "button_4.wav","","","","","","",
                              "shutdown_1.wav", "shutdown_2.wav", "shutdown_3.wav", "shutdown_4.wav","","","","","","",
                              "Notice_1.wav", "Notice_2.wav", "Notice_3.wav", "Notice_4.wav","","","","","",""]

def play(sndPath, sndNo):
    strSndFilePath = sndPath + DEF_SOUND_SOURCE_KIND_PATH[sndNo]
    os.system("pkill -9 aplay")
    cmd = DEF_SOUND_PLAY_LINUX_CMD + strSndFilePath + " &"
    os.system(cmd)

def playBarcodeSuccess(sndPath):
    cmd = DEF_SOUND_PLAY_LINUX_CMD + sndPath + "beep.wav &"
    os.system(cmd)

def playBarcodeTimeout(sndPath):
    cmd = DEF_SOUND_PLAY_LINUX_CMD + sndPath + "beep_beep_beep.wav &"
    os.system(cmd)
