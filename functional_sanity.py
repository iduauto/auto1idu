import time
from datetime import datetime, timedelta


import input
import locaters
from health_check import HealthCheck
from login import Login
from utils import Utils
from maintenance_functionalities import Maintenance
from wireless import Wireless

from logger import setup_logger

logger = setup_logger( __name__ )


class FunctionalSanity:
    def __init__(self , driver):
        self.driver = driver
        self.utils = Utils( driver )
        self.health = HealthCheck( driver )
        self.maintenance = Maintenance( driver )
        self.login = Login( driver )
        self.wireless = Wireless( driver )

    # Multiple Reset
    def functional_sanity_01(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validating multiple factory reset" )
        try:
            if self.health.health_check_webgui() == False:
                logger.error( 'Device health check failed. Exiting the test.' )
                return False

            for i in range( 2 ):
                logger.debug( f"-------------{i + 1}th Factory Reset---------------------" )
                self.maintenance.reset()

                if self.health.health_check_webgui() == False:
                    logger.error( 'Device health check failed. Exiting the test.' )
                    logger.error( f"Error occurred after {i + 1}th factory reset iteration" )
                    self.utils.get_DBGLogs()
                    return False

            logger.info( "Successfully factory reset from Web GUI - 5 Iterations" )
            return True
        except Exception as E:
            logger.error( f"Error occurred during functional_sanity_01: {str( E )}" )
            self.utils.get_DBGLogs()
            return False

    # Multiple Reboot
    def functional_sanity_02(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validating multiple reboot" )
        try:
            if self.health.health_check_webgui() == False:
                logger.error( 'Device health check failed. Exiting the test.' )
                return False

            for i in range( 2 ):
                logger.debug( f"-------------{i + 1}th Reboot---------------------" )
                self.maintenance.reboot()

                if self.health.health_check_webgui() == False:
                    logger.error( 'Device health check failed. Exiting the test.' )
                    logger.error( f"Error occurred after {i + 1}th reboot iteration" )
                    self.utils.get_DBGLogs()
                    return False

            logger.info( "Successfully reboot from WebGUI - 5 Iterations" )
            return True
        except Exception as E:
            logger.error( f"Error occurred during functional_sanity_01: {str( E )}" )
            self.utils.get_DBGLogs()
            return False

    # Validate mac address
    def functional_sanity_06(self):
        logger.debug( "======================================================================================" )
        logger.debug( 'Validating MAC Address after Reboot and Reset' )
        try:
            if self.health.health_check_webgui() == False:
                logger.error( 'Device health check failed. Exiting the test.' )
                return False

            # Getting wan mac address before reboot and reset
            self.utils.search_WebGUI( "WAN Information" )
            wan_mac_address = self.utils.find_element( *locaters.WanInfo_MacAddress ).text
            logger.debug( f'WAN MAC Address before Reboot: {wan_mac_address}' )

            # Rebooting Device
            self.maintenance.reboot()
            self.login.WebGUI_login()

            # Getting wan mac address after reboot
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
            self.utils.search_WebGUI( "WAN Information" )
            wan_mac_address_after_reset = self.utils.find_element( *locaters.WanInfo_MacAddress ).text
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

    # Logout functionality
    def functional_sanity_11(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validating 'Logout' button functionality in WebGUI" )

        try:
            if self.health.health_check_webgui() == False:
                logger.error( 'Device health check failed. Exiting the test.' )
                return False

            self.utils.find_element(
                "//div[@class='iconUser']//*[name()='svg']//*[name()='circle' and @id='iconBG']" ).click()
            self.utils.find_element( "//div[normalize-space()='Logout']" ).click()

            if self.utils.is_element_visible( '//form[@class="jioWrtLoginGrid"]' ) == True:
                logger.info( "'Logout' button functionality is working as expected" )
                return True
            else:
                logger.error( "'Logout' button functionality is NOT working as expected" )
                return False


        except Exception as E:
            logger.error( f"Error occurred during functional_sanity_11: {str( E )}" )
            self.utils.get_DBGLogs()
            return False

    #Time and Date functionality
    def functional_sanity_12(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validate date/time functionality in IDU" )
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False

            self.utils.search_WebGUI("Time Configuration")
            current_time = self.utils.find_element("/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/form[1]/div[1]/div[1]/div[3]/div[1]/div[2]").text

            format_str = "%A, %B %d %Y, %H:%M:%S (GMT %z)"
            check_time = datetime.strptime( current_time , format_str )
            current_time = datetime.now( check_time.tzinfo )
            threshold = timedelta( minutes=1 )

            logger.info(f"Device current time : {current_time}")

            if abs(current_time - check_time) <= threshold:
                logger.info( "date/time functionality is working as expected" )
                return True
            else:
                logger.error( "date/time functionality is NOT working as expected" )
                return False

        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_12: %s" , str( e ) )
            self.utils.get_DBGLogs()
            return False

    # Multiple Reset
    def functional_sanity_58(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validating multiple factory reset" )
        try:
            if self.health.health_check_webgui() == False:
                logger.error( 'Device health check failed. Exiting the test.' )
                return False
            n = 5
            for i in range( n ):
                logger.debug( f"-------------{i + 1}th Factory Reset---------------------" )
                self.maintenance.reset()

                if self.health.health_check_webgui() == False:
                    logger.error( 'Device health check failed. Exiting the test.' )
                    logger.error( f"Error occurred after {i + 1}th factory reset iteration" )
                    self.utils.get_DBGLogs()
                    return False

            logger.info( f"Successfully factory reset from Web GUI - {n} Iterations" )
            return True
        except Exception as E:
            logger.error( f"Error occurred during functional_sanity_58: {str( E )}" )
            self.utils.get_DBGLogs()
            return False

    # Firmware Upgrade and Downgrade functionality
    def functional_sanity_14(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validating Firmware Upgrade and Downgrade functionality" )
        try:
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False

            # downgrade to previous version
            image_path = f"{input.base_path}\\{input.previous_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.previous_firmware_version}.sig"

            self.maintenance.firmware_upgrade( image_path , signature_path )
            self.login.WebGUI_login()

            succesCount = 0
            if self.utils.get_firmware_version() == input.previous_firmware_version:  # check for update
                succesCount += 1
                logger.info( 'Firmware Downgraded Successfully to ' + input.previous_firmware_version )
            else:
                logger.error( 'Firmware is not Downgraded ' )

            # upgrade to latest version
            image_path = f"{input.base_path}\\{input.latest_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.latest_firmware_version}.sig"

            self.maintenance.firmware_upgrade( image_path , signature_path )
            self.login.WebGUI_login()

            if self.utils.get_firmware_version() == input.latest_firmware_version:  # check for update
                succesCount += 1
                logger.info( 'Firmware Upgraded Successfully to ' + input.latest_firmware_version )
            else:
                logger.error( 'Firmware is not Upgraded ' )

            # conluding the test case
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

    # Administration user password management
    def functional_sanity_28(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validate administration user password management functionality" )

        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False


            # Changing password
            logger.debug( "Changing the admin credentials to:\nUsername: 'admin'\nPassword: 'PR@sant23' " )
            self.utils.search_WebGUI( "User Management" )
            self.utils.find_element(
                "//tbody/tr[1]/td[5]/div[1]/div[3]/div[1]//*[name()='svg']//*[name()='path' and @id='icon']" ).click()
            self.utils.clear_and_send_keys( "PR@sant23" , "//input[@name='password']" )
            self.utils.clear_and_send_keys( "PR@sant23" , "//input[@name='confirmPassword']" )

            self.utils.find_element( "//button[normalize-space()='SAVE']" ).click()
            time.sleep( 30 )

            succes_count=0
            # Check if device is logged out
            if self.utils.is_element_visible( '//form[@class="jioWrtLoginGrid"]' ):
                succes_count+=1
                logger.info( "Password changed successfully" )


            # Try to login with new password
            logger.debug("Attempting login with the new admin credentials:\nUsername: 'admin'\nPassword: 'PR@sant23'")
            self.utils.clear_and_send_keys( 'admin' , *locaters.Login_Username )
            self.utils.clear_and_send_keys( "PR@sant23" , *locaters.Login_Password )
            self.utils.find_element( *locaters.Login_LoginBtn ).click()
            time.sleep( 15 )
            if self.utils.is_element_visible( '//h2[normalize-space()="Dashboard"]' ):
                succes_count+=1
                logger.info( "Successfully logged in with new credentials" )

            # Revert back the password
            logger.debug( "Reverting back the admin credentials to:\nUsername: 'admin'\nPassword: 'P@ssw0rd' " )
            self.utils.search_WebGUI( "User Management" )
            self.utils.find_element(
                "//tbody/tr[1]/td[5]/div[1]/div[3]/div[1]//*[name()='svg']//*[name()='path' and @id='icon']" ).click()

            self.utils.clear_and_send_keys( "P@ssw0rd" , "//input[@name='password']" )
            self.utils.clear_and_send_keys( "P@ssw0rd" , "//input[@name='confirmPassword']" )
            self.utils.find_element( "//button[normalize-space()='SAVE']" ).click()
            time.sleep( 30 )

            if self.utils.is_element_visible( '//form[@class="jioWrtLoginGrid"]' ):
                succes_count += 1
                logger.info("Password reverted back successfully")

            # Check if all steps were successful
            if succes_count == 3:
                logger.info( "Administration user password management functionality is working as expected" )
                return True
            else:
                logger.error( "Administration user password management functionality is NOT working as expected" )
                return False

        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_28: %s" , str( e ) )
            self.utils.get_DBGLogs()
            return False

    #Guest user password management
    def functional_sanity_29(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validate Guest user password management functionality" )

        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False


            # Changing password
            logger.debug( "Changing the guest credentials to:\nUsername: 'guest'\nPassword: 'PR@sant23' " )
            self.utils.search_WebGUI( "User Management" )
            self.utils.find_element(
                "//tbody/tr[2]/td[5]/div[1]/div[3]/div[1]//*[name()='svg']//*[name()='path' and @id='icon']" ).click()
            self.utils.clear_and_send_keys( "PR@sant23" , "//input[@name='password']" )
            self.utils.clear_and_send_keys( "PR@sant23" , "//input[@name='confirmPassword']" )

            self.utils.find_element( "//button[normalize-space()='SAVE']" ).click()
            time.sleep( 30 )

            self.utils.find_element(
                "//div[@class='iconUser']//*[name()='svg']//*[name()='circle' and @id='iconBG']" ).click()
            self.utils.find_element( "//div[normalize-space()='Logout']" ).click()


            succes_count=0

            # Try to login with new password
            logger.debug("Attempting login with the new guest credentials:\nUsername: 'guest'\nPassword: 'PR@sant23'")

            self.utils.clear_and_send_keys( 'guest' , *locaters.Login_Username )
            self.utils.clear_and_send_keys( "PR@sant23" , *locaters.Login_Password )
            self.utils.find_element( *locaters.Login_LoginBtn ).click()
            time.sleep( 15 )
            if self.utils.is_element_visible( '//h2[normalize-space()="Dashboard"]' ):
                succes_count+=1
                logger.info( "Successfully logged in with new credentials" )


            #checking user rights
            self.utils.search_WebGUI("Wireless Configuration")
            if self.utils.find_element("//input[@name='password']").is_enabled()== False:
                logger.info("Unable to modify wireless config")
                succes_count += 1

            if succes_count == 2:
                logger.info( "Administration user password management functionality is working as expected" )
                return True
            else:
                logger.error( "Administration user password management functionality is NOT working as expected" )
                return False

        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_28: %s" , str( e ) )
            self.utils.get_DBGLogs()
            return False
        finally:
            self.utils.find_element(
                "//div[@class='iconUser']//*[name()='svg']//*[name()='circle' and @id='iconBG']" ).click()
            self.utils.find_element( "//div[normalize-space()='Logout']" ).click()

    #change the password upon every factory reset
    def functional_sanity_35(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validating whether the device asks to change the password upon every factory reset from WebGUI" )
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False

            # Resetting device
            self.maintenance.reset()

            # Entering login credentials
            logger.debug("Try to login with the credentials")
            logger.debug("Username : admin")
            logger.debug("Password : P@ssw0rd")
            self.utils.clear_and_send_keys( input.username , *locaters.Login_Username )
            self.utils.clear_and_send_keys( input.password , *locaters.Login_Password )
            self.utils.find_element( *locaters.Login_LoginBtn ).click()

            # Checking if warning message is displayed after login
            if self.utils.is_element_visible( '//div[@class="jioWrtValidationSection jioWrtErrorColor"]' ):
                warning_msg = self.utils.find_element( '//div[normalize-space()="Invalid Credentials!"]' ).text
                if "Invalid Credentials!" in warning_msg:
                    logger.info( "As Expected, Device is showing Invalid Credentials!" )
                    self.utils.find_element('//button[normalize-space()="OK"]').click()
                else:
                    logger.error( "Unexpected warning message: %s" , warning_msg )
            else:
                logger.error( "No warning message displayed after login. Expected to ask to change password." )
                return False

            logger.debug( "Try to login with the credentials" )
            logger.debug( "Username : admin" )
            logger.debug( "Password : Jiocentrum" )
            self.utils.clear_and_send_keys( input.username , *locaters.Login_Username )
            self.utils.clear_and_send_keys( input.default_password , *locaters.Login_Password )
            self.utils.find_element( *locaters.Login_LoginBtn ).click()

            if self.utils.is_element_visible('//form[@name="jioFrmFactoryReset"]'):
                logger.debug( "Device is on Update Passwords page" )
                logger.info( "Successfully, Device is asking to change the password upon factory reset" )
                return True
        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_35: %s" , str( e ) )
            self.utils.get_DBGLogs()
            return False

    # Redirect to login page or not after firmware upgrade
    def functional_sanity_37(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validate whether the WebGUI is redirecting to Login page after Firmware upgrade from WebGUI" )
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False

                # downgrade to previous version
            image_path = f"{input.base_path}\\{input.previous_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.previous_firmware_version}.sig"
            self.maintenance.firmware_upgrade( image_path , signature_path )

            fail_count = 0
            # Check for the login page after downgrad
            if self.utils.is_element_visible( '//form[@class="jioWrtLoginGrid"]' ) == False:
                fail_count += 1

            self.login.WebGUI_login()
            if self.utils.get_firmware_version() == input.previous_firmware_version:  # check for update
                logger.debug( 'Firmware Downgraded Successfully to ' + input.previous_firmware_version )
            else:
                fail_count += 1
                logger.error( 'Firmware is not Downgraded ' )

            # upgrade to latest version
            logger.debug( "Reverting back to latest version" )
            image_path = f"{input.base_path}\\{input.latest_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.latest_firmware_version}.sig"
            self.maintenance.firmware_upgrade( image_path , signature_path )

            # Check for the login page after downgrad
            if self.utils.is_element_visible( '//form[@class="jioWrtLoginGrid"]' ) == False:
                fail_count += 1

            self.login.WebGUI_login()
            if self.utils.get_firmware_version() == input.latest_firmware_version:  # check for update
                logger.debug( 'Firmware Upgraded Successfully to ' + input.latest_firmware_version )
            else:
                fail_count += 1
                logger.error( 'Firmware is not Upgraded ' )

            # concluding the test case
            if fail_count == 0:
                logger.info( "WebGUI is successfully redirecting to Login page after Firmware upgrade from WebGUI" )
                return True
            else:
                logger.error( "WebGUI is NOT redirecting to Login page after Firmware upgrade from WebGUI" )
                return False



        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_37: %s" , str( e ) )
            self.utils.get_DBGLogs()
            return False

    # Redirect to login page or not after reboot
    def functional_sanity_38(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validate whether the WebGUI is redirecting to Login page after Reboot from WebGUI" )
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False

            self.maintenance.reboot()  # reset device

            # Check for the login page
            if self.utils.is_element_visible( '//form[@class="jioWrtLoginGrid"]' ) == True:
                logger.info( "WebGUI is successfully redirecting to Login page after Reboot from WebGUI" )
                return True
            else:
                logger.error( "WebGUI is NOT redirecting to Login page after Reboot from WebGUI" )
                return False

        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_38: %s" , str( e ) )
            self.utils.get_DBGLogs()
            return False

    # Redirect to login page or not after reset
    def functional_sanity_39(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validate whether the WebGUI is redirecting to Login page after Factory Reset from WebGUI" )
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False

            self.maintenance.reset()  # reset device

            # Check for the login page
            if self.utils.is_element_visible( '//form[@class="jioWrtLoginGrid"]' ) == True:
                logger.info( "WebGUI is successfully redirecting to Login page after Factory Reset from WebGUI" )
                return True
            else:
                logger.error( "WebGUI is NOT redirecting to Login page after Factory Reset from WebGUI" )
                return False

        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_39: %s" , str( e ) )
            self.utils.get_DBGLogs()
            return False

    # Validate Default firewall functionality
    def functional_sanity_41(self):
        logger.debug( "======================================================================================" )
        logger.info( "Validate Default firewall functionality" )
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error( 'Device health check failed. Exiting the test.' )
                self.utils.get_DBGLogs()
                return False

            fail_count = 0
            # Enabling Block Always functionality
            self.utils.search_WebGUI( "Default Policy" )
            self.utils.find_element( "//span[normalize-space()='Allow Always']" ).click()
            self.utils.find_element( "//li[normalize-space()='Block Always']" ).click()
            self.utils.find_element( "//button[normalize-space()='SAVE']" ).click()

            # Checking if firewall policy is changed to Block Always
            self.utils.search_WebGUI( "Security Status" )
            security_status = self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[3]/form[1]/div[1]/div[1]/div[3]/div[1]/div[2]" ).text

            if "Block Always" in security_status:
                logger.info( "Firewall Policy is changed to Block Always" )
            else:
                fail_count += 1
                logger.error( "Failed to change Firewall Policy to Block Always" )

            # Checking websites in Block Always mode
            urls = ['https://www.youtube.com/live/ZyiRWWzwBkk?si=6_onuWoBmQPCbAIc' ,
                    'https://www.onlinesbi.sbi' ,
                    'https://www.facebook.com']
            if not self.utils.check_website_connectivity( urls ):
                logger.info( 'Unable to access the internet, Block Always functionality is working as expected' )
            else:
                fail_count += 1
                logger.error( 'Able to access the internet, Block Always functionality is NOT working as expected' )

            time.sleep( 10 )

            # Enabling Allow Always functionality
            self.utils.search_WebGUI( "Default Policy" )
            self.utils.find_element( "//span[normalize-space()='Block Always']" ).click()
            self.utils.find_element( "//li[normalize-space()='Allow Always']" ).click()
            self.utils.find_element( "//button[normalize-space()='SAVE']" ).click()

            # Checking if firewall policy is changed to Allow Always
            self.utils.search_WebGUI( "Security Status" )
            security_status = self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[3]/form[1]/div[1]/div[1]/div[3]/div[1]/div[2]" ).text

            if "Allow Always" in security_status:
                logger.info( "Firewall Policy is changed to Allow Always" )
            else:
                fail_count += 1
                logger.error( "Failed to change Firewall Policy to Allow Always" )

            # Checking websites in Allow Always mode
            urls = ['https://www.youtube.com/watch?v=VVsC2fD1BjA' ,
                    'https://www.onlinesbi.sbi' ,
                    'https://www.facebook.com']
            if self.utils.check_website_connectivity( urls ):
                logger.info( 'Able to access the internet, Allow Always functionality is working as expected' )
            else:
                fail_count += 1
                logger.error( 'Unable to access the internet, Allow Always functionality is NOT working as expected' )

            # Concluding the test case
            if fail_count == 0:
                logger.info( "Default firewall functionality is working as expected" )
                return True
            else:
                logger.error( "Default firewall functionality is NOT working as expected" )
                self.utils.get_DBGLogs()
                return False

        except Exception as e:
            logger.error( "Error occurred while executing functional_sanity_41: %s" , str( e ) )
            return False
