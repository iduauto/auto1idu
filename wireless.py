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

    def set_ssid_password_from_gui(self , ssid=input.test_ssid , password=input.test_ssid_password):
        logger.debug("Setting SSID and password")
        try:
            # self.utils.search_WebGUI('Wireless Configuration')
            self.utils.navigate("Wireless")
            self.utils.clear_and_send_keys(ssid, *locaters.Wireless_Ssid)
            try:
                change_password_toggle = self.utils.find_element(*locaters.Wireless_ChangePasswordToggle_1)
            except:
                change_password_toggle = self.utils.find_element(*locaters.Wireless_ChangePasswordToggle_2)
            change_password_toggle.click()
            self.utils.clear_and_send_keys(password, *locaters.Wireless_Password)
            self.utils.clear_and_send_keys(password, *locaters.Wireless_Confirmpassword)
            save_button = self.utils.find_element(*locaters.Wireless_SaveButton)
            save_button.click()
            logger.info(f"SSID Set with - Name: {ssid}, Password: {password}")
            time.sleep(5)

        except Exception as e:
            logger.error("Error occurred while Setting SSID and password ", str(e))
            logger.error(f'')

    def get_ssid_from_gui(self):
        logger.info('Initiating get SSID from gui')
        # self.utils.search_WebGUI('Wireless Configuration')
        self.utils.navigate("Wireless")
        ssid = self.utils.find_element('/html/body/mainapp/div[1]/div[2]/div[4]/div/form/div/div[1]/div[3]/div[9]/input')
        return ssid.get_attribute("value")
