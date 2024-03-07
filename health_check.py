import input
from utils import Utils
from login import Login
from logger import setup_logger
logger = setup_logger(__name__)


class HealthCheck:
    def __init__(self,driver):
        self.driver = driver
        self.login = Login(driver)
        self.utils=Utils(driver)

    def health_check_webgui(self):
        try:
            self.login.WebGUI_login()

            logger.debug( "Performing health check" )

            health_issues = 0

            # if self.utils.get_firmware_version() != input.latest_firmware_version:
            #     health_issues += 1
            #     logger.error("Device is not having latest firmware version")
            #
            #
            # if not self.utils.get_ipv6_info()["status"]:
            #     health_issues += 1
            #     logger.error("Failed to retrieve IPv6 information.")
            #
            #
            # if not self.utils.check_ping( "google.com" , 4 ):
            #     health_issues += 1
            #     logger.error("Ping to Google IPv4 failed." )
            #
            #
            # if not self.utils.check_ping( "google.com" , 6 ):
            #     health_issues += 1
            #     logger.error( "Ping to Google IPv6 failed." )


            if health_issues != 0:
                logger.error(f"Device health check completed with {health_issues} issue(s)" )
                return False
            else:
                logger.info( "Device health check completed successfully." )
                return True

        except Exception as e:
            logger.error( f"An error occurred while performing health check: {e}" )
            return False




