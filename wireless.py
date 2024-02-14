import time
import locaters
import input
from utils import Utils
from logger import setup_logger
logger = setup_logger( __name__ )


class Wireless:
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)

    def set_ssid_password_from_gui(self, ssid=input.test_ssid, password=input.test_password):
        logger.info('Initiating set SSID Password from gui')
        self.utils.search_WebGUI('Wireless Configuration')
        self.utils.clear_and_send_keys(ssid, *locaters.Wireless_Ssid)
        logger.info(f'Entered SSID as {ssid}')
        try:
            change_password_toggle = self.utils.find_element(*locaters.Wireless_ChangePasswordToggle_1)
        except:
            change_password_toggle = self.utils.find_element(*locaters.Wireless_ChangePasswordToggle_2)
        change_password_toggle.click()
        logger.info('Clicked on Change Password Toggle Button')
        self.utils.clear_and_send_keys(password, *locaters.Wireless_Password)
        logger.info(f'Entered Password as {password}')
        self.utils.clear_and_send_keys(password, *locaters.Wireless_Confirmpassword)
        logger.info(f'Entered Confirm Password as {password}')
        save_button = self.utils.find_element(*locaters.Wireless_SaveButton)
        save_button.click()
        logger.info('Clicked on save button')

    def get_ssid_from_gui(self):
        logger.info('Initiating get SSID from gui')
        self.utils.search_WebGUI('Wireless Configuration')
        ssid = self.utils.find_element('/html/body/mainapp/div[1]/div[2]/div[4]/div/form/div/div[1]/div[3]/div[9]/input')
        return ssid.get_attribute("value")
