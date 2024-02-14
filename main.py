import time

import input
import setup

from health_check import HealthCheck
from maintenance_functionalities import Maintenance

from functional_sanity import FunctionalSanity
from wireless import Wireless
from login import Login

from logger import setup_logger
from login import Login
from utils import Utils

logger = setup_logger(__name__)

driver=setup.get_driver()

#
# health_check = HealthCheck(driver)
# health_check.health_check_webgui()

login=Login(driver)
# utils=Utils(driver)
#
# print('him')
#
login.WebGUI_login()
# print(utils.get_DBGLogs())
login = Login(driver)
wireless = Wireless(driver)
# functional_sanity=FunctionalSanity(driver)
#
# print( functional_sanity.functional_sanity_01())
# print( functional_sanity.functional_sanity_01())

login.WebGUI_login()
# wireless.set_ssid_password_from_gui('India', 'ilovemyindia')
ssid = wireless.get_ssid_from_gui()
print(f'SSID value returned from gui is {ssid}')

driver.quit()






maintenance = Maintenance(driver)
maintenance.firmware_upgrade(input.downgrade_image_path,input.downgrade_sign_path)
#maintenance.restore(r"C:\Users\ontvi\Downloads\backup-jio-2024-02-13_enc.tar.gz")

time.sleep(10)
# login.WebGUI_login()
# time.sleep(10)C:\Users\ontvi\Downloads\Firmware\idu\ARCNJIO_JIDU6101_D1.8.5.img
# C:\Users\ontvi\Downloads\Firmware\idu\ARCNJIO_JIDU6101_D1.8.5.sig

#



# time.sleep(10)
# login.WebGUI_login()
driver.quit()


