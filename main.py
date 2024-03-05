import time

import input
import setup
from firewall import Firewall

from health_check import HealthCheck
from maintenance_functionalities import Maintenance

from functional_sanity import FunctionalSanity
from wireless import Wireless
from login import Login

from logger import setup_logger
from login import Login

from utils import Utils

logger = setup_logger(__name__)

driver = setup.get_driver()
functional_sanity = FunctionalSanity(driver)
firewall = Firewall(driver)
login = Login(driver)
maintenance = Maintenance(driver)
login.WebGUI_login()
utils = Utils(driver)
utils.search_WebGUI("Firmware Upgrade")
time.sleep(10)
utils.search_WebGUI("List of IPv4 Firewall Rules")
time.sleep(10)
utils.search_WebGUI("Wireless Configuraon")
time.sleep(10)
utils.search_WebGUI("WAN Information")
time.sleep(10)
utils.search_WebGUI("Date & Time Configuration")
time.sleep(10)
utils.search_WebGUI("Default Policy")
time.sleep(10)
utils.search_WebGUI("List of Port Forwarding")
time.sleep(10)
utils.search_WebGUI("LAN Information")
time.sleep(10)
utils.search_WebGUI("Firmware Upgrade")
time.sleep(10)
utils.search_WebGUI("List of IPv4 Firewall Rules")
time.sleep(10)
utils.search_WebGUI("Wireless Configuraon")
time.sleep(10)
utils.search_WebGUI("Restore Settings")
time.sleep(10)
utils.search_WebGUI("Firmware Upgrade")
time.sleep(10)
utils.search_WebGUI("Backup Settings")
time.sleep(10)
utils.search_WebGUI("Wireless Configuraon")
time.sleep(10)
utils.search_WebGUI("WAN Information")
time.sleep(10)
utils.search_WebGUI("Ping6 / Traceroute6")
time.sleep(10)
utils.search_WebGUI("List of IPv4 Firewall Rules")
time.sleep(10)
utils.search_WebGUI("Wireless Configuraon")
time.sleep(10)
utils.search_WebGUI("WAN Information")
time.sleep(10)
# print(functional_sanity.functional_sanity_62())

count = 0
while (count != 0):
    logger.warning(
        "---------------------------------------------------------------------------------------------------")
    logger.warning(f"                              Execution Iteration {count}                                        ")
    logger.warning(
        "---------------------------------------------------------------------------------------------------")
    print(functional_sanity.functional_sanity_06())
    print(functional_sanity.functional_sanity_11())
    print(functional_sanity.functional_sanity_12())
    print(functional_sanity.functional_sanity_14())
    print(functional_sanity.functional_sanity_28())
    print(functional_sanity.functional_sanity_29())
    print(functional_sanity.functional_sanity_31())
    print(functional_sanity.functional_sanity_32())
    print(functional_sanity.functional_sanity_33())
    print(functional_sanity.functional_sanity_34())
    print(functional_sanity.functional_sanity_35())
    print(functional_sanity.functional_sanity_37())
    print(functional_sanity.functional_sanity_38())
    print(functional_sanity.functional_sanity_39())
    print(functional_sanity.functional_sanity_41())
    print(functional_sanity.functional_sanity_43())
    print(functional_sanity.functional_sanity_47())
    print(functional_sanity.functional_sanity_49())
    print(functional_sanity.functional_sanity_50())
    print(functional_sanity.functional_sanity_57())
    print(functional_sanity.functional_sanity_58())
    count += 1

driver.quit()

# maintenance = Maintenance(driver)
# maintenance.restore(rf"C:\Users\ontvi\Downloads\backup-jio-2024-02-13_enc.tar.gz")
# maintenance.restore(r"C:\Users\ontvi\Downloads\backup-jio-2024-02-13_enc.tar.gz")

time.sleep(5)
# login.WebGUI_login()
# time.sleep(10)C:\Users\ontvi\Downloads\Firmware\idu\ARCNJIO_JIDU6101_D1.8.5.img
# C:\Users\ontvi\Downloads\Firmware\idu\ARCNJIO_JIDU6101_D1.8.5.sig

#


# time.sleep(10)
# login.WebGUI_login()
driver.quit()
