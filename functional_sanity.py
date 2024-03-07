import os
import subprocess
import time
from datetime import datetime, timedelta
import datetime

import input
import locaters
from firewall import Firewall
from health_check import HealthCheck
from login import Login
from utils import Utils
from maintenance_functionalities import Maintenance
from wireless import Wireless

from logger import setup_logger

logger = setup_logger(__name__)


class FunctionalSanity:
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)
        self.health = HealthCheck(driver)
        self.maintenance = Maintenance(driver)
        self.firewall = Firewall(driver)
        self.login = Login(driver)
        self.wireless = Wireless(driver)

    # Validate mac address
    def functional_sanity_06(self):
        logger.debug("======================================================================================")
        logger.debug('Validating MAC Address after Reboot and Reset')
        try:
            if self.health.health_check_webgui() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            # Getting wan mac address before reboot and reset
            self.utils.search_WebGUI("WAN Information")
            wan_mac_address = self.utils.find_element(*locaters.WanInfo_MacAddress).text
            logger.debug(f'WAN MAC Address before Reboot: {wan_mac_address}')

            # Rebooting Device
            self.maintenance.reboot()
            self.login.WebGUI_login()

            # Getting wan mac address after reboot
            self.utils.search_WebGUI("WAN Information")
            wan_mac_address_after_reboot = self.utils.find_element(*locaters.WanInfo_MacAddress).text
            logger.debug(f'WAN MAC Address after Reboot: {wan_mac_address_after_reboot}')

            success = 0
            if wan_mac_address == wan_mac_address_after_reboot:
                success += 1
                logger.info('WAN MAC Address is same after Reboot ')
            else:
                logger.error('WAN MAC Address has changed after Reboot')
                self.utils.get_DBGLogs()

            # Reseting Device
            self.maintenance.reset()
            self.login.WebGUI_login()

            # Getting wan mac address after reset
            self.utils.search_WebGUI("WAN Information")
            wan_mac_address_after_reset = self.utils.find_element(*locaters.WanInfo_MacAddress).text
            logger.debug(f'WAN MAC Address after Reset: {wan_mac_address_after_reset}')

            if wan_mac_address == wan_mac_address_after_reset:
                success += 1
                logger.info('WAN MAC Address is same after Factory Reset')
            else:
                logger.error('WAN MAC Address has changed after Factory Reset')
                self.utils.get_DBGLogs()

            if success == 2:
                logger.info('MAC Address is same after Reboot and Reset')
                return True
            else:
                logger.error('MAC Address has changed after Reboot or Reset')
                return False
        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_06: %s", str(e))
            self.utils.get_DBGLogs()
            return False

    # Logout functionality
    def functional_sanity_11(self):
        logger.debug("======================================================================================")
        logger.info("Validating 'Logout' button functionality in WebGUI")

        try:
            if self.health.health_check_webgui() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.utils.find_element(
                "//div[@class='iconUser']//*[name()='svg']//*[name()='circle' and @id='iconBG']").click()
            self.utils.find_element("//div[normalize-space()='Logout']").click()

            if self.utils.is_element_visible('//form[@class="jioWrtLoginGrid"]'):
                logger.info("'Logout' button functionality is working as expected")
                return True
            else:
                logger.error("'Logout' button functionality is NOT working as expected")
                return False


        except Exception as E:
            logger.error(f"Error occurred during functional_sanity_11: {str(E)}")
            self.utils.get_DBGLogs()
            return False

    # Time and Date functionality
    from datetime import datetime, timedelta

    def functional_sanity_12(self):
        logger.debug("======================================================================================")
        logger.info("Validate date/time functionality in IDU")
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            self.utils.search_WebGUI("Time Configuration")
            current_time = self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/form[1]/div[1]/div[1]/div[3]/div[1]/div[2]").text

            format_str = "%A, %B %d %Y, %H:%M:%S (GMT %z)"
            check_time = datetime.strptime(current_time, format_str)
            current_time = datetime.now(check_time.tzinfo)
            threshold = timedelta(minutes=1)

            logger.info(f"Device current time : {current_time}")

            if abs(current_time - check_time) <= threshold:
                logger.info("Date/time functionality is working as expected")
                return True
            else:
                logger.error("Date/time functionality is NOT working as expected")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_12: %s", str(e))
            self.utils.get_DBGLogs()
            return False

    # Firmware Upgrade and Downgrade functionality
    def functional_sanity_14(self):
        logger.debug("======================================================================================")
        logger.info("Validating Firmware Upgrade and Downgrade functionality")
        try:
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # downgrade to previous version
            image_path = f"{input.base_path}\\{input.previous_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.previous_firmware_version}.sig"

            self.maintenance.firmware_upgrade(image_path, signature_path)
            self.login.WebGUI_login()

            succesCount = 0
            if self.utils.get_firmware_version() == input.previous_firmware_version:  # check for update
                succesCount += 1
                logger.info('Firmware Downgraded Successfully to ' + input.previous_firmware_version)
            else:
                logger.error('Firmware is not Downgraded ')

            # upgrade to latest version
            image_path = f"{input.base_path}\\{input.latest_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.latest_firmware_version}.sig"

            self.maintenance.firmware_upgrade(image_path, signature_path)
            self.login.WebGUI_login()

            if self.utils.get_firmware_version() == input.latest_firmware_version:  # check for update
                succesCount += 1
                logger.info('Firmware Upgraded Successfully to ' + input.latest_firmware_version)
            else:
                logger.error('Firmware is not Upgraded ')

            # conluding the test case
            if not self.health.health_check_webgui():
                logger.error('Device health check failed')
                succesCount -= 1

            if succesCount == 2:
                logger.info("Firmware Upgrade and Downgrade functionality is working as Expected")
                return True
            else:
                logger.error("Firmware Upgrade and Downgrade functionality is NOT working as Expected")
                return False

        except Exception as E:
            logger.error("Error occurred while executing functional_sanity_14: %s", str(E))
            return False

    # Administration user password management
    def functional_sanity_28(self):
        logger.debug("======================================================================================")
        logger.info("Validate administration user password management functionality")

        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # Changing password
            logger.debug("Changing the admin credentials to:\nUsername: 'admin'\nPassword: 'PR@sant23' ")
            self.utils.search_WebGUI("User Management")
            self.utils.find_element(
                "//tbody/tr[1]/td[5]/div[1]/div[3]/div[1]//*[name()='svg']//*[name()='path' and @id='icon']").click()
            self.utils.clear_and_send_keys("PR@sant23", "//input[@name='password']")
            self.utils.clear_and_send_keys("PR@sant23", "//input[@name='confirmPassword']")

            self.utils.find_element("//button[normalize-space()='SAVE']").click()
            time.sleep(30)

            success_count = 0
            # Check if device is logged out
            if self.utils.is_element_visible('//form[@class="jioWrtLoginGrid"]'):
                success_count += 1
                logger.info("Password changed successfully")

            # Try to login with new password
            logger.debug("Attempting login with the new admin credentials:\nUsername: 'admin'\nPassword: 'PR@sant23'")
            self.utils.clear_and_send_keys('admin', *locaters.Login_Username)
            self.utils.clear_and_send_keys("PR@sant23", *locaters.Login_Password)
            self.utils.find_element(*locaters.Login_LoginBtn).click()
            time.sleep(15)
            if self.utils.is_element_visible('//h2[normalize-space()="Dashboard"]'):
                success_count += 1
                logger.info("Successfully logged in with new credentials")

            # Revert back the password
            logger.debug("Reverting back the admin credentials to:\nUsername: 'admin'\nPassword: 'P@ssw0rd' ")
            self.utils.search_WebGUI("User Management")
            self.utils.find_element(
                "//tbody/tr[1]/td[5]/div[1]/div[3]/div[1]//*[name()='svg']//*[name()='path' and @id='icon']").click()

            self.utils.clear_and_send_keys("P@ssw0rd", "//input[@name='password']")
            self.utils.clear_and_send_keys("P@ssw0rd", "//input[@name='confirmPassword']")
            self.utils.find_element("//button[normalize-space()='SAVE']").click()
            time.sleep(30)

            if self.utils.is_element_visible('//form[@class="jioWrtLoginGrid"]'):
                success_count += 1
                logger.info("Password reverted back successfully")

            # Check if all steps were successful
            if success_count == 3:
                logger.info("Administration user password management functionality is working as expected")
                return True
            else:
                logger.error("Administration user password management functionality is NOT working as expected")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_28: %s", str(e))
            self.utils.get_DBGLogs()
            return False

    # Guest user password management
    def functional_sanity_29(self):
        logger.debug("======================================================================================")
        logger.info("Validate Guest user password management functionality")

        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # Changing password
            logger.debug("Changing the guest credentials to:\nUsername: 'guest'\nPassword: 'PR@sant23' ")
            self.utils.search_WebGUI("User Management")
            self.utils.find_element(
                "//tbody/tr[2]/td[5]/div[1]/div[3]/div[1]//*[name()='svg']//*[name()='path' and @id='icon']").click()
            self.utils.clear_and_send_keys("PR@sant23", "//input[@name='password']")
            self.utils.clear_and_send_keys("PR@sant23", "//input[@name='confirmPassword']")

            self.utils.find_element("//button[normalize-space()='SAVE']").click()
            time.sleep(30)

            self.utils.find_element(
                "//div[@class='iconUser']//*[name()='svg']//*[name()='circle' and @id='iconBG']").click()
            self.utils.find_element("//div[normalize-space()='Logout']").click()

            succes_count = 0

            # Try to login with new password
            logger.debug("Attempting login with the new guest credentials:\nUsername: 'guest'\nPassword: 'PR@sant23'")

            self.utils.clear_and_send_keys('guest', *locaters.Login_Username)
            self.utils.clear_and_send_keys("PR@sant23", *locaters.Login_Password)
            self.utils.find_element(*locaters.Login_LoginBtn).click()
            time.sleep(15)
            if self.utils.is_element_visible('//h2[normalize-space()="Dashboard"]'):
                succes_count += 1
                logger.info("Successfully logged in with new credentials")

            # checking user rights
            self.utils.search_WebGUI("Wireless Configuration")
            if self.utils.find_element("//input[@name='password']").is_enabled() == False:
                logger.info("Unable to modify wireless config")
                succes_count += 1

            if succes_count == 2:
                logger.info("Administration user password management functionality is working as expected")
                return True
            else:
                logger.error("Administration user password management functionality is NOT working as expected")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_28: %s", str(e))
            self.utils.get_DBGLogs()
            return False
        finally:
            self.utils.find_element(
                "//div[@class='iconUser']//*[name()='svg']//*[name()='circle' and @id='iconBG']").click()
            self.utils.find_element("//div[normalize-space()='Logout']").click()

    # Backup functionality
    def functional_sanity_31(self):
        logger.debug("======================================================================================")
        logger.info(
            "Validate the Maintenance functionality like Backup from Web GUI.")
        backup_file_path = ""
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # Adding IPv6 and IPv4 firewall rule
            self.firewall.add_ipv6_firewall_rule("HTTPS", "Block Always", "Inbound")
            self.firewall.add_ipv4_firewall_rule("HTTPS", "Block Always")

            backup_file_path = self.maintenance.backup()  # Backup the device
            self.maintenance.reset()  # Reset the device

            success_count = 0
            # check if firewall rules are removes are not
            self.login.WebGUI_login()
            total_ipv4_rules = self.firewall.total_ipv4_rules()
            total_ipv6_rules = self.firewall.total_ipv6_rules()
            if total_ipv4_rules == 0 and total_ipv6_rules == 0:
                logger.info("Old configuration removed successfully after reset.")
                success_count += 1
            else:
                logger.error("Old configuration NOT removed after reset.")

            self.maintenance.restore(backup_file_path)  # Restore the device with previous backup file

            # check if firewall rules are restored are not
            self.login.WebGUI_login()
            total_ipv4_rules = self.firewall.total_ipv4_rules()
            total_ipv6_rules = self.firewall.total_ipv6_rules()

            if total_ipv4_rules == 1 and total_ipv6_rules == 1:
                logger.info("Old configuration restored successfully.")
                success_count += 1
            else:
                logger.error("Old configuration NOT restored.")

            # concluding the test
            if success_count == 2:
                logger.info("Maintenance functionality like Backup is working as expected")
                return True
            else:
                logger.error("Maintenance functionality like Backup is NOT working as expected")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_31: %s", str(e))
            return False
        finally:
            if os.path.exists(backup_file_path):  # deleting backup file
                os.remove(backup_file_path)

            self.firewall.delete_ipv6_firewall_rule()  # deleting  ipv6 firewall rule
            self.firewall.delete_ipv4_firewall_rule()  # deleting  ipv4 firewall rule

    # Restore functionality
    def functional_sanity_32(self):
        logger.debug("======================================================================================")
        logger.info(
            "Validate the Maintenance functionality like Restore from Web GUI.")
        backup_file_path = ""
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # Adding IPv6 and IPv4 firewall rule
            self.firewall.add_ipv6_firewall_rule("HTTPS", "Block Always", "Inbound")
            self.firewall.add_ipv4_firewall_rule("HTTPS", "Block Always")

            backup_file_path = self.maintenance.backup()  # Backup the device
            self.maintenance.reset()  # Reset the device

            success_count = 0
            # check if firewall rules are removes are not
            self.login.WebGUI_login()
            total_ipv4_rules = self.firewall.total_ipv4_rules()
            total_ipv6_rules = self.firewall.total_ipv6_rules()
            if total_ipv4_rules == 0 and total_ipv6_rules == 0:
                logger.info("Old configuration removed successfully after reset.")
                success_count += 1
            else:
                logger.error("Old configuration NOT removed after reset.")

            self.maintenance.restore(backup_file_path)  # Restore the device with previous backup file

            # check if firewall rules are restored are not
            self.login.WebGUI_login()
            total_ipv4_rules = self.firewall.total_ipv4_rules()
            total_ipv6_rules = self.firewall.total_ipv6_rules()
            if total_ipv4_rules == 1 and total_ipv6_rules == 1:
                logger.info("Old configuration restored successfully.")
                success_count += 1
            else:
                logger.error("Old configuration NOT restored.")

            # concluding the test
            if success_count == 2:
                logger.info("Maintenance functionality like Restore is working as expected.")
                return True
            else:
                logger.error("Maintenance functionality like Restore is working as expected.")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_47: %s", str(e))
            return False
        finally:
            if os.path.exists(backup_file_path):  # deleting backup file
                os.remove(backup_file_path)

            self.firewall.delete_ipv6_firewall_rule()  # deleting  ipv6 firewall rule
            self.firewall.delete_ipv4_firewall_rule()  # deleting  ipv4 firewall rule

    # Factory Default
    def functional_sanity_33(self):
        logger.debug("======================================================================================")
        logger.info(
            "Validate the Maintenance functionality like Factory default from Web GUI.")
        backup_file_path = ""
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # Adding IPv6 and IPv4 firewall rule
            self.firewall.add_ipv6_firewall_rule("HTTPS", "Block Always", "Inbound")
            self.firewall.add_ipv4_firewall_rule("HTTPS", "Block Always")

            backup_file_path = self.maintenance.backup()  # Backup the device
            self.maintenance.reset()  # Reset the device

            # check if firewall rules are removes are not
            self.login.WebGUI_login()
            total_ipv4_rules = self.firewall.total_ipv4_rules()
            total_ipv6_rules = self.firewall.total_ipv6_rules()
            if total_ipv4_rules == 0 and total_ipv6_rules == 0:
                logger.info("Old configuration removed successfully after reset.")
                logger.info("Maintenance functionality like Factory default is working as expected.")
                return True
            else:
                logger.error("Old configuration NOT removed after reset.")
                logger.error("Maintenance functionality like Factory default is working as expected.")
                return False
        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_33: %s", str(e))
            return False
        finally:
            if os.path.exists(backup_file_path):  # deleting backup file
                os.remove(backup_file_path)

            self.firewall.delete_ipv6_firewall_rule()  # deleting  ipv6 firewall rule
            self.firewall.delete_ipv4_firewall_rule()  # deleting  ipv4 firewall rule

    # Reboot functionality
    def functional_sanity_34(self):
        logger.debug("======================================================================================")
        logger.info(
            "Validate the Maintenance functionality like Reboot from Web GUI.")
        backup_file_path = ""
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # Adding IPv6 and IPv4 firewall rule
            self.firewall.add_ipv6_firewall_rule("HTTPS", "Block Always", "Inbound")
            self.firewall.add_ipv4_firewall_rule("HTTPS", "Block Always")

            self.maintenance.reset()  # Reboot the device

            # check if firewall rules are removes are not
            self.login.WebGUI_login()
            total_ipv4_rules = self.firewall.total_ipv4_rules()
            total_ipv6_rules = self.firewall.total_ipv6_rules()
            if total_ipv4_rules == 0 and total_ipv6_rules == 0:
                logger.info("Old configuration NOT removed after reboot.")
                logger.info("Maintenance functionality like Reboot is working as expected.")
                return True
            else:
                logger.error("Old configuration removed after reset.")
                logger.error("Maintenance functionality like Reboot is NOT working as expected.")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_34: %s", str(e))
            return False
        finally:
            if os.path.exists(backup_file_path):  # deleting backup file
                os.remove(backup_file_path)

            self.firewall.delete_ipv6_firewall_rule()  # deleting  ipv6 firewall rule
            self.firewall.delete_ipv4_firewall_rule()  # deleting  ipv4 firewall rule

    # change the password upon every factory reset
    def functional_sanity_35(self):
        logger.debug("======================================================================================")
        logger.info("Validating whether the device asks to change the password upon every factory reset from WebGUI")
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # Resetting device
            self.maintenance.reset()

            # Entering login credentials
            logger.debug("Try to login with the credentials")
            logger.debug("Username : admin")
            logger.debug("Password : P@ssw0rd")
            self.utils.clear_and_send_keys(input.username, *locaters.Login_Username)
            self.utils.clear_and_send_keys(input.password, *locaters.Login_Password)
            self.utils.find_element(*locaters.Login_LoginBtn).click()

            # Checking if warning message is displayed after login
            if self.utils.is_element_visible('//div[@class="jioWrtValidationSection jioWrtErrorColor"]'):
                warning_msg = self.utils.find_element('//div[normalize-space()="Invalid Credentials!"]').text
                if "Invalid Credentials!" in warning_msg:
                    logger.info("As Expected, Device is showing Invalid Credentials!")
                    self.utils.find_element('//button[normalize-space()="OK"]').click()
                else:
                    logger.error("Unexpected warning message: %s", warning_msg)
            else:
                logger.error("No warning message displayed after login. Expected to ask to change password.")
                return False

            logger.debug("Try to login with the credentials")
            logger.debug("Username : admin")
            logger.debug("Password : Jiocentrum")
            self.utils.clear_and_send_keys(input.username, *locaters.Login_Username)
            self.utils.clear_and_send_keys(input.default_password, *locaters.Login_Password)
            self.utils.find_element(*locaters.Login_LoginBtn).click()

            if self.utils.is_element_visible('//form[@name="jioFrmFactoryReset"]'):
                logger.debug("Device is on Update Passwords page")
                logger.info("Successfully, Device is asking to change the password upon factory reset")
                return True
        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_35: %s", str(e))
            self.utils.get_DBGLogs()
            return False

    # Redirect to login page or not after firmware upgrade
    def functional_sanity_37(self):
        logger.debug("======================================================================================")
        logger.info("Validate whether the WebGUI is redirecting to Login page after Firmware upgrade from WebGUI")
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

                # downgrade to previous version
            image_path = f"{input.base_path}\\{input.previous_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.previous_firmware_version}.sig"
            self.maintenance.firmware_upgrade(image_path, signature_path)

            fail_count = 0
            # Check for the login page after downgrad
            if self.utils.is_element_visible('//form[@class="jioWrtLoginGrid"]') == False:
                fail_count += 1

            self.login.WebGUI_login()
            if self.utils.get_firmware_version() == input.previous_firmware_version:  # check for update
                logger.debug('Firmware Downgraded Successfully to ' + input.previous_firmware_version)
            else:
                fail_count += 1
                logger.error('Firmware is not Downgraded ')

            # upgrade to latest version
            logger.debug("Reverting back to latest version")
            image_path = f"{input.base_path}\\{input.latest_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.latest_firmware_version}.sig"
            self.maintenance.firmware_upgrade(image_path, signature_path)

            # Check for the login page after downgrad
            if self.utils.is_element_visible('//form[@class="jioWrtLoginGrid"]') == False:
                fail_count += 1

            self.login.WebGUI_login()
            if self.utils.get_firmware_version() == input.latest_firmware_version:  # check for update
                logger.debug('Firmware Upgraded Successfully to ' + input.latest_firmware_version)
            else:
                fail_count += 1
                logger.error('Firmware is not Upgraded ')

            # concluding the test case
            if fail_count == 0:
                logger.info("WebGUI is successfully redirecting to Login page after Firmware upgrade from WebGUI")
                return True
            else:
                logger.error("WebGUI is NOT redirecting to Login page after Firmware upgrade from WebGUI")
                return False



        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_37: %s", str(e))
            self.utils.get_DBGLogs()
            return False

    # Redirect to login page or not after reboot
    def functional_sanity_38(self):
        logger.debug("======================================================================================")
        logger.info("Validate whether the WebGUI is redirecting to Login page after Reboot from WebGUI")
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            self.maintenance.reboot()  # reset device

            # Check for the login page
            if self.utils.is_element_visible('//form[@class="jioWrtLoginGrid"]') == True:
                logger.info("WebGUI is successfully redirecting to Login page after Reboot from WebGUI")
                return True
            else:
                logger.error("WebGUI is NOT redirecting to Login page after Reboot from WebGUI")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_38: %s", str(e))
            self.utils.get_DBGLogs()
            return False

    # Redirect to login page or not after reset
    def functional_sanity_39(self):
        logger.debug("======================================================================================")
        logger.info("Validate whether the WebGUI is redirecting to Login page after Factory Reset from WebGUI")
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            self.maintenance.reset()  # reset device

            # Check for the login page
            if self.utils.is_element_visible('//form[@class="jioWrtLoginGrid"]') == True:
                logger.info("WebGUI is successfully redirecting to Login page after Factory Reset from WebGUI")
                return True
            else:
                logger.error("WebGUI is NOT redirecting to Login page after Factory Reset from WebGUI")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_39: %s", str(e))
            self.utils.get_DBGLogs()
            return False

    # Validate Default firewall functionality
    def functional_sanity_41(self):
        logger.debug("======================================================================================")
        logger.info("Validate Default firewall functionality")
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            fail_count = 0
            # Enabling Block Always functionality
            self.utils.search_WebGUI("Default Policy")
            self.utils.find_element("//span[normalize-space()='Allow Always']").click()
            self.utils.find_element("//li[normalize-space()='Block Always']").click()
            self.utils.find_element("//button[normalize-space()='SAVE']").click()

            # Checking if firewall policy is changed to Block Always
            self.utils.search_WebGUI("Security Status")
            security_status = self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[3]/form[1]/div[1]/div[1]/div[3]/div[1]/div[2]").text

            if "Block Always" in security_status:
                logger.info("Firewall Policy is changed to Block Always")
            else:
                fail_count += 1
                logger.error("Failed to change Firewall Policy to Block Always")

            # Checking websites in Block Always mode
            urls = ['https://www.youtube.com/live/ZyiRWWzwBkk?si=6_onuWoBmQPCbAIc',
                    'https://www.onlinesbi.sbi',
                    'https://www.facebook.com']
            if not self.utils.check_website_connectivity(urls):
                logger.info('Unable to access the internet, Block Always functionality is working as expected')
            else:
                fail_count += 1
                logger.error('Able to access the internet, Block Always functionality is NOT working as expected')

            time.sleep(10)

            # Enabling Allow Always functionality
            self.utils.search_WebGUI("Default Policy")
            self.utils.find_element("//span[normalize-space()='Block Always']").click()
            self.utils.find_element("//li[normalize-space()='Allow Always']").click()
            self.utils.find_element("//button[normalize-space()='SAVE']").click()

            # Checking if firewall policy is changed to Allow Always
            self.utils.search_WebGUI("Security Status")
            security_status = self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[3]/form[1]/div[1]/div[1]/div[3]/div[1]/div[2]").text

            if "Allow Always" in security_status:
                logger.info("Firewall Policy is changed to Allow Always")
            else:
                fail_count += 1
                logger.error("Failed to change Firewall Policy to Allow Always")

            # Checking websites in Allow Always mode
            urls = ['https://www.youtube.com/watch?v=VVsC2fD1BjA',
                    'https://www.onlinesbi.sbi',
                    'https://www.facebook.com']
            if self.utils.check_website_connectivity(urls):
                logger.info('Able to access the internet, Allow Always functionality is working as expected')
            else:
                fail_count += 1
                logger.error('Unable to access the internet, Allow Always functionality is NOT working as expected')

            # Concluding the test case
            if fail_count == 0:
                logger.info("Default firewall functionality is working as expected")
                return True
            else:
                logger.error("Default firewall functionality is NOT working as expected")
                self.utils.get_DBGLogs()
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_41: %s", str(e))
            return False

    # DNS proxy functionality
    def functional_sanity_43(self):
        logger.debug("======================================================================================")
        logger.info("Validate the LAN side DNS proxy functionality of the IDU")
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            self.utils.search_WebGUI("LAN IPv4 Configuration")
            self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/form[1]/div[1]/div[1]/div[2]/div[2]/div[7]/div[1]/span[1]").click()
            self.utils.find_element("//li[normalize-space()='Use DNS Proxy']").click()
            time.sleep(30)
            # Run the ipconfig /renew command
            subprocess.run(["ipconfig", "/renew"], check=True)

            # Run the ipconfig /all command to fetch the renewed configuration
            time.sleep(30)
            ipconfig_output = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True).stdout
            dns_server = ""
            for line in ipconfig_output.splitlines():
                if "DNS Servers" in line:
                    # Extract the IP address part from the line
                    dns_server = line.split(":")[-1].strip()
                    if dns_server:
                        logger.debug("DNS Server: %s", dns_server)
                    else:
                        logger.info("DNS Server not found in the ipconfig output.")
                        return False

            if dns_server == '192.168.31.1':
                logger.info("The LAN side DNS proxy functionality is working as expected")
                return True
            else:
                logger.error("The LAN side DNS proxy functionality is NOT working as expected")
                return False
        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_43: %s", str(e))
            return False

    # DNS from IPS functionality
    def functional_sanity_44(self):
        logger.debug("======================================================================================")
        logger.info("Validate the LAN side DNS from IPS functionality")
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            self.utils.search_WebGUI("LAN IPv4 Configuration")
            self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/form[1]/div[1]/div[1]/div[2]/div[2]/div[7]/div[1]/span[1]").click()
            self.utils.find_element("//li[normalize-space()='Use DNS from ISP']").click()
            time.sleep(30)
            # Run the ipconfig /renew command
            subprocess.run(["ipconfig", "/renew"], check=True)

            # Run the ipconfig /all command to fetch the renewed configuration
            time.sleep(30)
            ipconfig_output = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True).stdout
            dns_server = ""
            for line in ipconfig_output.splitlines():
                if "DNS Servers" in line:
                    # Extract the IP address part from the line
                    dns_server = line.split(":")[-1].strip()
                    if dns_server:
                        logger.debug("DNS Server: %s", dns_server)
                    else:
                        logger.info("DNS Server not found in the ipconfig output.")
                        return False

            if dns_server == '172.16.56.142':
                logger.info("The LAN side DNS from IPS functionality is working as expected")
                return True
            else:
                logger.error("The LAN side DNS from IPS functionality is NOT working as expected")
                return False
        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_44: %s", str(e))
            return False

    # Factory default functionality
    def functional_sanity_47(self):
        logger.debug("======================================================================================")
        logger.info(
            "Validating after Factory Default functionality that the old configuration is removed from the IDU.")
        backup_file_path = ""
        try:
            # Performing health check
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # Adding IPv6 and IPv4 firewall rule
            self.firewall.add_ipv6_firewall_rule("HTTPS", "Block Always", "Inbound")
            self.firewall.add_ipv4_firewall_rule("HTTPS", "Block Always")

            backup_file_path = self.maintenance.backup()  # Backup the device
            self.maintenance.reset()  # Reset the device

            success_count = 0

            # check if firewall rules are removes are not
            self.login.WebGUI_login()
            total_ipv4_rules = self.firewall.total_ipv4_rules()
            total_ipv6_rules = self.firewall.total_ipv6_rules()
            if total_ipv4_rules == 0 and total_ipv6_rules == 0:
                logger.info("Old configuration removed successfully after reset.")
                success_count += 1
            else:
                logger.error("Old configuration NOT removed after reset.")

            self.maintenance.restore(backup_file_path)  # Restore the device with previous backup file

            # check if firewall rules are restored are not
            self.login.WebGUI_login()
            total_ipv4_rules = self.firewall.total_ipv4_rules()
            total_ipv6_rules = self.firewall.total_ipv6_rules()
            if total_ipv4_rules == 1 and total_ipv6_rules == 1:
                logger.info("Old configuration restored successfully.")
                success_count += 1
            else:
                logger.error("Old configuration NOT restored.")

            # concluding the test
            if success_count == 2:
                logger.info("After Factory Default functionality that the old configuration is removed Successful.")
                return True
            else:
                logger.error("After Factory Default functionality that the old configuration is NOT removed .")
                return False

        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_47: %s", str(e))
            return False
        finally:
            if os.path.exists(backup_file_path):  # deleting backup file
                os.remove(backup_file_path)

            self.firewall.delete_ipv6_firewall_rule()  # deleting  ipv6 firewall rule
            self.firewall.delete_ipv4_firewall_rule()  # deleting  ipv4 firewall rule

    # Firmware Upgrade and Downgrade functionality
    def functional_sanity_49(self):
        logger.debug("======================================================================================")
        logger.info("Validating Firmware Upgrade and Downgrade functionality")
        try:
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_DBGLogs()
                return False

            # downgrade to previous version
            image_path = f"{input.base_path}\\{input.previous_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.previous_firmware_version}.sig"

            self.maintenance.firmware_upgrade(image_path, signature_path)
            self.login.WebGUI_login()

            succesCount = 0
            if self.utils.get_firmware_version() == input.previous_firmware_version:  # check for update
                succesCount += 1
                logger.info('Firmware Downgraded Successfully to ' + input.previous_firmware_version)
            else:
                logger.error('Firmware is not Downgraded ')

            # upgrade to latest version
            image_path = f"{input.base_path}\\{input.latest_firmware_version}.img"
            signature_path = f"{input.base_path}\\{input.latest_firmware_version}.sig"

            self.maintenance.firmware_upgrade(image_path, signature_path)
            self.login.WebGUI_login()

            if self.utils.get_firmware_version() == input.latest_firmware_version:  # check for update
                succesCount += 1
                logger.info('Firmware Upgraded Successfully to ' + input.latest_firmware_version)
            else:
                logger.error('Firmware is not Upgraded ')

            # conluding the test case
            if not self.health.health_check_webgui():
                logger.error('Device health check failed')
                succesCount -= 1

            if succesCount == 2:
                logger.info("Firmware Upgrade and Downgrade functionality is working as Expected")
                return True
            else:
                logger.error("Firmware Upgrade and Downgrade functionality is NOT working as Expected")
                return False

        except Exception as E:
            logger.error("Error occurred while executing functional_sanity_49: %s", str(E))
            return False

    # Taking dbj log
    def functional_sanity_50(self):
        logger.debug("======================================================================================")
        logger.info("Validate user should able to take DBGLOG from IDU GUI.")
        try:
            self.driver.get(f'{input.URL}/WCGI/?dbglogs')
            current_time = time.time()
            logger.info('DBG log collected at: {}'.format(datetime.datetime.now()))
            time.sleep(30)

            directory = rf"C:\Users\ontvi\Downloads"
            # Iterate over files in the directory
            for filename in os.listdir(directory):
                if filename.startswith("enc_dbglog"):
                    filepath = os.path.join(directory, filename)
                    # Get the modification time of the file
                    modification_time = os.path.getmtime(filepath)
                    # Calculate the time difference in seconds
                    time_difference = current_time - modification_time
                    # Check if the file was modified in the last 1 minute
                    if time_difference <= 60:
                        logger.debug(f"File '{filename}' was downloaded in the last 1 minute.")
                        logger.debug("Successfully taken DBGLOG")
                        return True
            logger.error("Unable to take DBGLOG")
            return False
        except Exception as e:
            logger.error("Error occurred while executing functional_sanity_50: %s", str(e))
            return False

    # Multiple Reboot
    def functional_sanity_57(self, number_of_iteration=5):
        logger.debug("======================================================================================")
        logger.info("Validating multiple reboot")

        try:
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                return False

            # Adding IPv6 and IPv4 firewall rule
            self.firewall.add_ipv6_firewall_rule("HTTPS", "Block Always", "Inbound")
            self.firewall.add_ipv4_firewall_rule("HTTPS", "Block Always")
            # self.wireless.set_ssid_password_from_gui()

            for i in range(number_of_iteration):
                logger.debug(f"-------------{i + 1}th Reboot---------------------")
                self.maintenance.reboot()

                if not self.health.health_check_webgui():
                    logger.error('Device health check failed. Exiting the test.')
                    logger.error(f"Error occurred after {i + 1}th reboot iteration")
                    self.utils.get_DBGLogs()
                    return False

                # check if firewall rules are removes are not
                total_ipv4_rules = self.firewall.total_ipv4_rules()
                total_ipv6_rules = self.firewall.total_ipv6_rules()
                # ssid_name = self.wireless.get_ssid_from_gui()

                fail_count = 0
                if total_ipv4_rules == 0:
                    fail_count += 1
                if total_ipv6_rules == 0:
                    fail_count += 1
                # if ssid_name == input.factory_ssid:
                #     fail_count += 1

                if fail_count > 0:
                    logger.error("Old configuration removed after reboot.")
                    logger.error("Maintenance functionality like Reboot is NOT working as expected.")
                    logger.error(f"Error occurred after {i + 1}th reboot iteration")
                    return False
                else:
                    logger.info("Old configuration NOT removed after reboot.")
                    logger.info("Maintenance functionality like Reboot is working as expected.")

            logger.info("Successfully reboot from WebGUI - 5 Iterations")
            return True
        except Exception as E:
            logger.error(f"Error occurred during functional_sanity_57: {str(E)}")
            self.utils.get_DBGLogs()
            return False
        finally:
            self.firewall.delete_ipv4_firewall_rule()
            self.firewall.delete_ipv6_firewall_rule()

    # Multiple Reset
    def functional_sanity_58(self, number_of_iteration=5):
        logger.debug("======================================================================================")
        logger.info("Validating multiple factory reset")
        try:
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                return False
            n = 5
            for i in range(number_of_iteration):
                logger.debug(f"-------------{i + 1}th Factory Reset---------------------")
                # Adding IPv6 and IPv4 firewall rule
                self.firewall.add_ipv6_firewall_rule("HTTPS", "Block Always", "Inbound")
                self.firewall.add_ipv4_firewall_rule("HTTPS", "Block Always")
                # self.wireless.set_ssid_password_from_gui()

                self.maintenance.reset()

                if not self.health.health_check_webgui():
                    logger.error('Device health check failed. Exiting the test.')
                    logger.error(f"Error occurred after {i + 1}th factory reset iteration")
                    self.utils.get_DBGLogs()
                    return False

                # check if firewall rules are removes are not
                total_ipv4_rules = self.firewall.total_ipv4_rules()
                total_ipv6_rules = self.firewall.total_ipv6_rules()
                # ssid_name = self.wireless.get_ssid_from_gui()

                success_count = 0
                if total_ipv4_rules == 0:
                    success_count += 1
                if total_ipv6_rules == 0:
                    success_count += 1
                # if ssid_name == input.factory_ssid:
                #     success_count += 1

                if success_count == 2:
                    logger.info("Old configuration removed after reset.")
                    logger.info("Maintenance functionality like Reset is working as expected.")

                else:
                    logger.error(f"Error occurred after {i + 1}th reboot iteration")
                    logger.info("Old configuration NOT removed after Reset.")
                    logger.error("Maintenance functionality like Reset is NOT working as expected.")
                    return False

            logger.info(f"Successfully factory reset from Web GUI - {n} Iterations")
            return True
        except Exception as E:
            logger.error(f"Error occurred during functional_sanity_58: {str(E)}")
            self.utils.get_DBGLogs()
            return False

    # ipv4 traceroute
    def traceroute_ipv4(self, domain_name):
        try:
            logger.info(f"Initiating IPv4 Traceroute for domain: {domain_name}")
            # self.utils.search_WebGUI("Ping / Traceroute")
            self.utils.navigate("Diagnostics")
            self.utils.clear_and_send_keys(domain_name, *locaters.PingTraceroute4_DomainName)
            self.utils.find_element(*locaters.PingTraceroute4_Type).click()
            self.utils.find_element("//li[normalize-space()='Traceroute']").click()
            self.utils.find_element(*locaters.PingTraceroute4_StartBtn).click()

            time.sleep(60)

            msg = self.utils.find_element(*locaters.PingTraceroute4_Msg).text
            time.sleep(5)
            self.utils.find_element(*locaters.PingTraceroute4_Msg_CancleBtn).click()

            if "bad address" in msg:
                return False
            else:
                return True
        except Exception as e:
            logger.error(f"An error occurred during IPv4 Traceroute for domain '{domain_name}': {str(e)}")
            return False

    # ipv4 traceroute
    def traceroute_ipv6(self, domain_name):
        try:
            logger.debug(f"Initiating IPv6 Traceroute for domain: {domain_name}")
            # self.utils.search_WebGUI("Ping6 / Traceroute6")
            self.utils.navigate("Diagnostics")

            self.utils.clear_and_send_keys(domain_name, *locaters.PingTraceroute6_DomainName)
            self.utils.find_element(*locaters.PingTraceroute6_Type).click()
            self.utils.find_element("//li[normalize-space()='Traceroute6']").click()
            self.utils.find_element(*locaters.PingTraceroute6_StartBtn).click()

            time.sleep(60)

            msg = self.utils.find_element(*locaters.PingTraceroute6_Msg).text
            time.sleep(5)
            self.utils.find_element(*locaters.PingTraceroute6_Msg_CancleBtn).click()

            if "bad address" in msg:
                return False
            else:
                return True
        except Exception as e:
            logger.error(f"An error occurred during IPv6 Traceroute for domain '{domain_name}': {str(e)}")
            return False

    # traceroute functionality
    def functional_sanity_62(self):
        try:
            logger.debug("Validating IPv4 Diagnostics 'Traceroute' functionality")
            if not self.health.health_check_webgui():
                logger.error('Device health check failed. Exiting the test.')
                return False

            fail_count = 0
            domains_names = ["onlinesbi.sbi", "youtube.com", "www.google.com"]
            for domain_name in domains_names:
                if self.traceroute_ipv4(domain_name):
                    logger.info(f"Successfully traceroute 4 : {domain_name}")
                else:
                    fail_count += 1
                    logger.error(f"Unable traceroute 4: {domain_name}")

            domains_names = ["onlinesbi.sbi", "youtube.com", "www.google.com"]
            for domain_name in domains_names:
                if self.traceroute_ipv6(domain_name):
                    logger.info(f"Successfully traceroute 6 : {domain_name}")
                else:
                    fail_count += 1
                    logger.error(f"Unable traceroute 6: {domain_name}")

            if fail_count == 0:
                logger.info("'Traceroute' functionality is working as expected")
                return True
            else:
                logger.error("'Traceroute' functionality is NOT working as expected")
                return False

        except Exception as e:
            logger.error(f"Error occurred during functional_sanity_62: {str(e)}")
            self.utils.get_DBGLogs()
            return False
