import os.path
import time
import pyautogui
import os
import glob
import re
import time
from datetime import datetime

import locaters
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
            # self.utils.search_WebGUI( "Factory Defaults / Reboot" )
            self.utils.navigate("Maintenance")
            self.utils.find_element( *locaters.FactoryDefaultsReboot_DropDown ).click()
            self.utils.find_element( *locaters.FactoryDefaultsReboot_FactoryDefaultopt ).click()
            self.utils.find_element( *locaters.FactoryDefaultsReboot_FactoryDefaultBtn ).click()
            self.utils.find_element( *locaters.FactoryDefaultsReboot_FactoryDefaultCnfBtn ).click()
            logger.debug( "Wait for the reset process to complete : 200s" )
            time.sleep( 200 )
        except Exception as e:
            logger.error( f"An error occurred while resetting the device to factory defaults: {e}" )

    # Rebooting the device
    def reboot(self):
        logger.info( "Initiating device reboot" )
        try:
            # self.utils.search_WebGUI( "Factory Defaults / Reboot" )
            self.utils.navigate("Maintenance")
            self.utils.find_element( *locaters.FactoryDefaultsReboot_DropDown ).click()
            self.utils.find_element( *locaters.FactoryDefaultsReboot_RebootOpt ).click()
            self.utils.find_element( *locaters.FactoryDefaultsReboot_RebootBtn ).click()
            self.utils.find_element( *locaters.FactoryDefaultsReboot_RebootCnfBtn ).click()
            logger.debug("Wait for the reboot process to complete : 200s")
            time.sleep( 200 )
        except Exception as e:
            logger.error( f"An error occurred while rebooting the device: {e}" )
            raise Exception (e)


    # Backup the device and return the path if the file is present
    def backup(self):
        logger.info( "Initiating device backup" )
        backup_file_path = None
        try:
            self.utils.search_WebGUI( "Backup Settings" )
            self.utils.find_element(*locaters.BackupSettings_BackupIcon).click()
            time.sleep( 15 )  # Wait for the backup process to complete

            # Check if the backup file exists in the default download directory
            today_date = datetime.now().strftime( "%Y-%m-%d" )
            expected_file_name = f"backup-jio-{today_date}_enc.tar.gz"
            default_download_dir = rf"C:\Users\ontvi\Downloads"
            for file_name in os.listdir( default_download_dir ):
                if file_name == expected_file_name:
                    backup_file_path = os.path.join( default_download_dir , file_name )
                    break

            if backup_file_path:
                logger.debug( f"Backup file found -> '{backup_file_path}'" )
                logger.info( "Backup process initiated successfully" )
            else:
                logger.warning( "Backup file not found" )


        except Exception as e:
            logger.error( f"An error occurred during device backup: {e}" )
            return e

        return backup_file_path

    # Restore the device with given file path
    def restore(self , file_path):
        logger.info( f"Initiating device restore, File Path: {file_path}" )
        try:
            self.utils.search_WebGUI( "Restore Settings" )
            # self.utils.find_element( *locaters.RestoreSettings_RestoreOpt ).click()
            # time.sleep( 3 )
            # if os.path.exists( file_path ):
            #     pyautogui.write( file_path )
            #     pyautogui.press( 'enter' )
            #     time.sleep( 3 )
            #     logger.debug( "File path entered successfully" )
            # else:
            #     logger.error( "File not found" )
            #     pyautogui.press( 'esc' )
            #     return

            # uploading image file
            logger.debug(f"Uploading restore file : {file_path}")
            img_file_input = self.utils.find_element(*locaters.RestoreSettings_RestoreOpt)
            img_file_input.send_keys(file_path)


            self.utils.find_element( *locaters.RestoreSettings_RestoreBtn ).click()
            self.utils.find_element( *locaters.RestoreSettings_RestoreCnfBtn ).click()

            logger.debug( "Wait for the Restore process to complete : 200s" )
            time.sleep( 200 )
        except Exception as e:
            logger.error( f"An error occurred during device restore: {e}" )


    # Firmware upgrade and downgrade
    def firmware_upgrade(self, image_file, signature_file):
        logger.info("Initiating firmware changing process")
        try:
            self.utils.search_WebGUI("Firmware Upgrade")

            # uploading image file
            logger.debug(f"Uploading image file : {image_file}")
            img_file_input = self.utils.find_element(*locaters.FirmwareUpgrade_ImgFile)
            img_file_input.send_keys(image_file)

            # uploading signature file
            logger.debug(f"Uploading sign file : {signature_file}")
            sign_file_input = self.utils.find_element(*locaters.FirmwareUpgrade_SignFile)
            sign_file_input.send_keys(signature_file)
            time.sleep(5)

            self.utils.find_element(*locaters.FirmwareUpgrade_UpgradeBtn).click()
            time.sleep(5)
            self.utils.find_element(*locaters.FirmwareUpgrade_UpgradeCnfBtn).click()

            logger.debug("Wait for the upgrade process to complete : 200s")
            time.sleep(200)

        except Exception as e:
            logger.error(f"An error occurred during firmware change: {str(e)}")


