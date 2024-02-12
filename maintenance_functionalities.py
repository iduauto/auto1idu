import time

from utils import Utils
from logger import setup_logger
logger = setup_logger( __name__ )
class Maintenance:
    def __init__(self,driver):
        self.driver = driver
        self.utils = Utils( driver )

    def reset(self):
        try:
            logger.info( "Initiating device reset to factory defaults" )
            self.utils.search_WebGUI( "Factory Defaults / Reboot" )
            self.utils.find_element( "//span[normalize-space()='Select Option']" ).click()
            self.utils.find_element( "//li[normalize-space()='Restore to Factory Defaults']" ).click()
            self.utils.find_element( "//button[normalize-space()='DEFAULTS']" ).click()
            self.utils.find_element(
                "//div[@class='jioWrtModalWindowContainer jioFactoyDefaultRebootModal']//button[@type='button'][normalize-space()='RESTORE']" ).click()
            time.sleep( 200 )
            logger.info( "Device reset to factory defaults completed successfully" )
        except Exception as e:
            logger.error( f"An error occurred while resetting the device to factory defaults: {e}" )

    def reboot(self):
        try:
            logger.info( "Initiating device reboot" )
            self.utils.search_WebGUI( "Factory Defaults / Reboot" )
            self.utils.find_element( "//span[normalize-space()='Select Option']" ).click()
            self.utils.find_element( "//li[normalize-space()='Reboot']" ).click()
            self.utils.find_element( "//button[normalize-space()='Reboot']" ).click()
            self.utils.find_element(
                "//div[@class='jioModalWindowFooter']//button[@type='button'][normalize-space()='Reboot']" ).click()
            time.sleep( 200 )
            logger.info( "Device reboot completed successfully" )
        except Exception as e:
            logger.error( f"An error occurred while rebooting the device: {e}" )