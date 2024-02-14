
class Adb:

    def set_wifi_enable():
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
