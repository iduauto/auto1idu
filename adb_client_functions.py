git
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
# __pycache__/firewall.cpython-310.pyc
# __pycache__/functional_sanity.cpython-310.pyc
# __pycache__/health_check.cpython-310.pyc
# __pycache__/input.cpython-310.pyc
# __pycache__/locaters.cpython-310.pyc
# __pycache__/logger.cpython-310.pyc
# __pycache__/login.cpython-310.pyc
# __pycache__/maintenance_functionalities.cpython-310.pyc
# __pycache__/setup.cpython-310.pyc
# __pycache__/utils.cpython-310.pyc
# __pycache__/wireless.cpython-310.pyc
# adb_client_functions.py
# input.py
# main.py