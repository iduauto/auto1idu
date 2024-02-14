import os.path
import time
import pyautogui
import os
import glob
import re
import time

from utils import Utils
from logger import setup_logger

logger = setup_logger( __name__ )


class Maintenance:
    def __init__(self , driver):
        self.driver = driver
        self.utils = Utils( driver )

    # Resting the device
    def reset(self):
        logger.info( "Initiating device factory defaults" )
        try:
            self.utils.search_WebGUI( "Factory Defaults / Reboot" )
            self.utils.find_element( "//span[normalize-space()='Select Option']" ).click()
            self.utils.find_element( "//li[normalize-space()='Restore to Factory Defaults']" ).click()
            self.utils.find_element( "//button[normalize-space()='DEFAULTS']" ).click()
            self.utils.find_element(
                "//div[@class='jioWrtModalWindowContainer jioFactoyDefaultRebootModal']//button[@type='button'][normalize-space()='RESTORE']" ).click()
            logger.debug( "Wait for the reset process to complete : 200s" )
            time.sleep( 200 )
            logger.info( "Device reset to factory defaults completed successfully" )
        except Exception as e:
            logger.error( f"An error occurred while resetting the device to factory defaults: {e}" )

    # Rebooting the device
    def reboot(self):
        logger.info( "Initiating device reboot" )
        try:
            self.utils.search_WebGUI( "Factory Defaults / Reboot" )
            self.utils.find_element( "//span[normalize-space()='Select Option']" ).click()
            self.utils.find_element( "//li[normalize-space()='Reboot']" ).click()
            self.utils.find_element( "//button[normalize-space()='Reboot']" ).click()
            self.utils.find_element(
                "//div[@class='jioModalWindowFooter']//button[@type='button'][normalize-space()='Reboot']" ).click()
            logger.debug("Wait for the reboot process to complete : 200s")
            time.sleep( 200 )
        except Exception as e:
            logger.error( f"An error occurred while rebooting the device: {e}" )

    # Backup the device and return the path if the file is present
    def backup(self):
        logger.info( "Initiating device backup" )
        backup_file_path = None
        try:
            self.utils.search_WebGUI( "Backup Settings" )
            self.utils.find_element(
                "//div[@class='iconActionDownload']//*[name()='svg']//*[name()='path' and @id='icon']" ).click()
            time.sleep( 15 )  # Wait for the backup process to complete

            # Check if the backup file exists in the default download directory
            default_download_dir = "C:/Users/ontvi/Downloads"  # Update with your default download directory
            for file_name in os.listdir( default_download_dir ):
                if file_name.startswith( "backup-jio-" ) and file_name.endswith( "_enc.tar.gz" ):
                    backup_file_path = os.path.join( default_download_dir , file_name )
                    break

            if backup_file_path:
                logger.debug( f"Backup file found -> '{backup_file_path}'" )
                logger.info( "Backup process initiated successfully" )
            else:
                logger.warning( "Backup file not found" )


        except Exception as e:
            logger.error( f"An error occurred during device backup: {e}" )

        return backup_file_path

    # Restore the device with given file path
    def restore(self , file_path):
        logger.info( f"Initiating device restore, File Path: {file_path}" )
        try:
            self.utils.search_WebGUI( "Restore Settings" )
            self.utils.find_element(
                "//label[@for='selectTheSavedSettings'][normalize-space()='Browse & Upload']" ).click()
            time.sleep( 3 )
            if os.path.exists( file_path ):
                pyautogui.write( file_path )
                pyautogui.press( 'enter' )
                logger.debug( "File path entered successfully" )
            else:
                logger.error( "File not found" )
                pyautogui.press( 'esc' )
                return

            self.utils.find_element("//div[@class='jioWrtSectionBottom']//button[@type='button'][normalize-space()='RESTORE']" ).click()
            self.utils.find_element("//div[@class='jioModalWindowFooter']//button[@type='button'][normalize-space()='RESTORE']" ).click()

            logger.debug( "Wait for the Restore process to complete : 200s" )
            time.sleep( 200 )
        except Exception as e:
            logger.error( f"An error occurred during device restore: {e}" )

    #Firmware upgrade and downgrade
    def firmware_upgrade(self,image_file,signature_file):
        self.utils.search_WebGUI("Firmware Upgrade")
        self.utils.find_element("/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/form[1]/div[1]/div[1]/div[2]/div[1]/label[3]/*[name()='svg'][1]/*[name()='path'][1]").click()
        time.sleep(3)
        if os.path.exists( image_file ):
            pyautogui.write( image_file )
            pyautogui.press( 'enter' )
            logger.debug( "Image File path entered successfully" )
        else:
            logger.error( "Image File NOT found" )
            pyautogui.press( 'esc' )
            return

        time.sleep(10)
        self.utils.find_element("/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/form[1]/div[1]/div[1]/div[2]/div[3]/label[3]/*[name()='svg'][1]/*[name()='path'][1]" ).click()
        time.sleep( 3 )
        if os.path.exists( signature_file ):
            pyautogui.write( signature_file )
            pyautogui.press( 'enter' )
            logger.debug( "Signature File path entered successfully" )
        else:
            logger.error( "Signature File NOT found" )
            pyautogui.press( 'esc' )
            return

        time.sleep( 10 )
        self.utils.find_element("//button[normalize-space()='UPGRADE']").click()
        time.sleep(5)
        self.utils.find_element('//*[@id="root"]/div[1]/div[2]/div[4]/div[1]/div[2]/form/div[3]/button').click()

        time.sleep(200)



