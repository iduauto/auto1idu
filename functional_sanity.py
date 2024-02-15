import input
import locaters
from health_check import HealthCheck
from login import Login
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
        self.login=Login(driver)

    #Validate mac address
    def functional_sanity_06(self):
        logger.debug( "======================================================================================" )
        logger.debug( 'Validating MAC Address after Reboot and Reset' )
        try:
            if self.health.health_check_webgui() == False:
                logger.error( 'Device health check failed. Exiting the test.' )
                return False

            #Getting wan mac address before reboot and reset
            self.utils.search_WebGUI("WAN Information")
            wan_mac_address = self.utils.find_element( *locaters.WanInfo_MacAddress ).text
            logger.debug( f'WAN MAC Address before Reboot: {wan_mac_address}' )

            # Rebooting Device
            self.maintenance.reboot()
            self.login.WebGUI_login()

            #Getting wan mac address after reboot
            self.utils.search_WebGUI( "WAN Information" )
            wan_mac_address_after_reboot = self.utils.find_element( *locaters.WanInfo_MacAddress ).text
            logger.debug( f'WAN MAC Address after Reboot: {wan_mac_address_after_reboot}' )

            success = 0
            if wan_mac_address == wan_mac_address_after_reboot:
                success += 1
                logger.info( 'WAN MAC Address is same after Reboot ' )
            else:
                logger.error( 'WAN MAC Address has changed after Reboot' )
                self.utils.get_DBGLogs()

            # Reseting Device
            self.maintenance.reset()
            self.login.WebGUI_login()

            # Getting wan mac address after reset
            self.utils.search_WebGUI( "WAN Information")
            wan_mac_address_after_reset = self.utils.find_element( *locaters.WanInfo_MacAddress  ).text
            logger.debug( f'WAN MAC Address after Reset: {wan_mac_address_after_reset}' )

            if wan_mac_address == wan_mac_address_after_reset:
                success += 1
                logger.info( 'WAN MAC Address is same after Factory Reset' )
            else:
                logger.error( 'WAN MAC Address has changed after Factory Reset' )
                self.utils.get_DBGLogs()

            if success == 2:
                logger.info( 'MAC Address is same after Reboot and Reset' )
                return True
            else:
                logger.error( 'MAC Address has changed after Reboot or Reset' )
                return False

        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_06: %s" , str( e ) )
            self.utils.get_DBGLogs()
            return False

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


    #Firmware Upgrade and Downgrade functionality
    def functional_sanity_14(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validating Firmware Upgrade and Downgrade functionality" )
        try:
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False


            #downgrade to previous version
            image_path =f"{input.base_path}\\{input.previous_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.previous_firmware_version}.sig"

            self.maintenance.firmware_upgrade( image_path , signature_path )
            self.login.WebGUI_login()

            succesCount = 0
            if self.utils.get_firmware_version() == input.previous_firmware_version: #check for update
                succesCount += 1
                logger.info( 'Firmware Downgraded Successfully to ' + input.previous_firmware_version )
            else:
                logger.error( 'Firmware is not Downgraded ' )


            # upgrade to latest version
            image_path = f"{input.base_path}\\{input.latest_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.latest_firmware_version}.sig"

            self.maintenance.firmware_upgrade( image_path , signature_path )
            self.login.WebGUI_login()

            if self.utils.get_firmware_version() == input.latest_firmware_version:#check for update
                succesCount += 1
                logger.info( 'Firmware Upgraded Successfully to ' + input.latest_firmware_version )
            else:
                logger.error( 'Firmware is not Upgraded ' )


            #conluding the test case
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed' )
                succesCount -= 1

            if succesCount == 2:
                logger.info( "Firmware Upgrade and Downgrade functionality is working as Expected" )
                return True
            else:
                logger.error( "Firmware Upgrade and Downgrade functionality is NOT working as Expected" )
                return False

        except Exception as E:
            logger.error( "Error occurred while executing functional_sanity_14: %s" , str( E ) )
            return False

