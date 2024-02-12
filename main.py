import time

import setup
from health_check import HealthCheck
from maintenance_functionalities import Maintenance

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



maintenance = Maintenance(driver)
maintenance.reboot()
time.sleep(10)
login.WebGUI_login()
time.sleep(10)

maintenance.reset()
time.sleep(10)
login.WebGUI_login()
driver.quit()

