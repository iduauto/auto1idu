import setup
from functional_sanity import FunctionalSanity
from wireless import Wireless
from login import Login

from logger import setup_logger
logger = setup_logger(__name__)

driver=setup.get_driver()
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











