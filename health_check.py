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

            logger.info( "Performing health check" )

            health_issues = []

            if not self.utils.get_firmware_version()["status"]:
                health_issues.append( "Failed to retrieve firmware version." )

            if not self.utils.get_ipv6_info()["status"]:
                health_issues.append( "Failed to retrieve IPv6 information." )

            if not self.utils.check_ping( "google.com" , 4 ):
                health_issues.append( "Ping to Google IPv4 failed." )

            if not self.utils.check_ping( "google.com" , 6 ):
                health_issues.append( "Ping to Google IPv6 failed." )

            if health_issues:
                logger.error(
                    f"Device health check completed with {len( health_issues )} issue(s): {', '.join( health_issues )}" )
                return False
            else:
                logger.info( "Device health check completed successfully." )
                return True

        except Exception as e:
            logger.error( f"An error occurred while performing health check: {e}" )
            return False




