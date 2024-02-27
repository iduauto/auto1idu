import subprocess
import time

from adb_setup import adb_setup
from logger import setup_logger

logger = setup_logger( __name__ )

class Adb:
    def __init__(self):
        adb_setup()

    def set_wifi_enable(self):
        command = ['cmd /c adb shell cmd -w wifi set-wifi-enabled disabled',
                   'adb shell cmd -w wifi status',
                   'adb shell cmd -w wifi set-wifi-enabled enabled',
                   'adb shell cmd -w wifi status']

        for i in command:
            cmd = subprocess.Popen(i, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)  # start -- cmd visible, /c -- close cmd after execution
            if 'status' in i:
                wifi_status = cmd.communicate()
                if 'Wifi is enabled' in str(wifi_status[0]):
                    print('Mobile client Wifi is Enabled')
            time.sleep(5)

    def set_wifi_disable(self):
        command = ['cmd /c adb shell cmd -w wifi set-wifi-enabled enabled',
                   'adb shell cmd -w wifi status ',
                   'adb shell cmd -w wifi set-wifi-enabled disabled',
                   'adb shell cmd -w wifi status']

        for i in command:
            cmd = subprocess.Popen(i, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)  # start -- cmd visible, /c -- close cmd after execution
            if 'status' in i:
                wifi_status = cmd.communicate()
                if 'Wifi is disabled' in str(wifi_status[0]):
                    print('Mobile client Wifi is disabled')
            time.sleep(5)

