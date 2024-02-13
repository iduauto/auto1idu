from health_check import HealthCheck
from utils import Utils
from maintenance_functionalities import Maintenance

from logger import setup_logger
logger = setup_logger( __name__ )

class FunctionalSanity:
    def __init__(self,driver):
        self.driver = driver
        self.utils=Utils(driver)
        self.health=HealthCheck(driver)
        self.maintenance = Maintenance(driver)

    #Multiple Reset
    def functional_sanity_01(self):
        logger.debug("======================================================================================")
        logger.info("Validating multiple factory reset")
        try:
            if self.health.health_check_webgui() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            for i in range(2):
                logger.debug( f"-------------{i + 1}th Factory Reset---------------------" )
                self.maintenance.reset()

                if self.health.health_check_webgui() == False:
                    logger.error('Device health check failed. Exiting the test.')
                    logger.error(f"Error occurred after {i + 1}th factory reset iteration")
                    self.utils.get_DBGLogs()
                    return False

            logger.info("Successfully factory reset from Web GUI - 5 Iterations")
            return True
        except Exception as E:
            logger.error(f"Error occurred during functional_sanity_01: {str(E)}")
            self.utils.get_DBGLogs()
            return False

    #Multiple Reboot
    def functional_sanity_02(self):
        logger.debug("======================================================================================")
        logger.info("Validating multiple reboot")
        try:
            if self.health.health_check_webgui() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            for i in range(2):
                logger.debug( f"-------------{i + 1}th Reboot---------------------" )
                self.maintenance.reboot()

                if self.health.health_check_webgui() == False:
                    logger.error('Device health check failed. Exiting the test.')
                    logger.error(f"Error occurred after {i + 1}th reboot iteration")
                    self.utils.get_DBGLogs()
                    return False

            logger.info("Successfully reboot from WebGUI - 5 Iterations")
            return True
        except Exception as E:
            logger.error(f"Error occurred during functional_sanity_01: {str(E)}")
            self.utils.get_DBGLogs()
            return False
