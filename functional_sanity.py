import input
from health_check import HealthCheck
from utils import Utils
from maintenance_functionalities import Maintenance
from wireless import Wireless

from logger import setup_logger
logger = setup_logger( __name__ )

class FunctionalSanity:
    def __init__(self,driver):
        self.driver = driver
        self.utils=Utils(driver)
        self.health=HealthCheck(driver)
        self.maintenance = Maintenance(driver)
        self.wireless = Wireless(driver)

    #Multiple Reset
    def functional_sanity_58(self):
        logger.debug("======================================================================================")
        logger.info("Validating multiple factory reset")
        try:
            if self.health.health_check_webgui() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False
            n = 5
            for i in range(n):
                logger.debug( f"-------------{i + 1}th Factory Reset---------------------" )
                self.maintenance.reset()

                if self.health.health_check_webgui() == False:
                    logger.error('Device health check failed. Exiting the test.')
                    logger.error(f"Error occurred after {i + 1}th factory reset iteration")
                    self.utils.get_DBGLogs()
                    return False

            logger.info(f"Successfully factory reset from Web GUI - {n} Iterations")
            return True
        except Exception as E:
            logger.error(f"Error occurred during functional_sanity_58: {str(E)}")
            self.utils.get_DBGLogs()
            return False

    #Multiple Reboot
    def functional_sanity_01(self):
        logger.debug("======================================================================================")
        logger.info("Validating multiple reboot")
        n = 2
        try:
            if self.health.health_check_webgui() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.wireless.set_ssid_password_from_gui()

            for i in range(n):
                logger.debug( f"-------------{i + 1}th Reboot---------------------" )
                self.maintenance.reboot()

                if self.health.health_check_webgui() == False:
                    logger.error('Device health check failed. Exiting the test.')
                    logger.error(f"Error occurred after {i + 1}th reboot iteration")
                    self.utils.get_DBGLogs()
                    return False
                ssid_from_gui = self.wireless.get_ssid_from_gui()
                if ssid_from_gui == input.test_ssid:
                    logger.info(f'SSID post reboot is the same: {ssid_from_gui}')
                else:
                    logger.error(f'SSID post reboot is not the same. '
                                 f'Expected:{input.test_ssid}, Actual:{ssid_from_gui}')
                    return False

            logger.info(f"Successfully reboot from WebGUI - {n} Iterations")
            return True
        except Exception as E:
            logger.error(f"Error occurred during functional_sanity_01: {str(E)}")
            self.utils.get_DBGLogs()
            return False
