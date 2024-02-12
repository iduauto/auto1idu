

import input
import locaters
from utils import Utils
import time
from logger import setup_logger

logger = setup_logger( __name__ )


class Login:
    def __init__(self , driver):
        self.driver = driver
        self.utils = Utils( driver )

    def WebGUI_login(self):
        logger.info( "Try to Login Through WebGUI" )
        try:
            self.driver.get( "https://192.168.32.1/" )

            if self.utils.is_element_visible( "//div[@class='jioWrtErrorColor']" ):
                logger.info( "Device is in Factory Reset State" )
                self.utils.clear_and_send_keys( input.username , *locaters.Login_Username )
                self.utils.clear_and_send_keys( input.default_password , *locaters.Login_Password )
                self.utils.find_element( *locaters.Login_LoginBtn ).click()

                time.sleep( 10 )
                self.utils.clear_and_send_keys( input.password , *locaters.DefaultLogin_AdminPass )
                self.utils.clear_and_send_keys( input.password , *locaters.DefaultLogin_CnfAdminPass )
                self.utils.clear_and_send_keys( input.password , *locaters.DefaultLogin_GuestPass )
                self.utils.clear_and_send_keys( input.password , *locaters.DefaultLogin_CnfGuestPass )

                self.utils.find_element( *locaters.DefaultLogin_UpdateBtn ).click()

            time.sleep( 5 )
            self.utils.clear_and_send_keys( input.username , *locaters.Login_Username )
            self.utils.clear_and_send_keys( input.password , *locaters.Login_Password )
            self.utils.find_element( *locaters.Login_LoginBtn ).click()


            if self.utils.is_element_visible( "//div[@class='jioModalWindowFooter']//button[@type='button'][normalize-space()='OK']"):
                self.utils.find_element( "//div[@class='jioModalWindowFooter']//button[@type='button'][normalize-space()='OK']" ).click()


        except Exception as E:
            logger.error( f"Error Occurred While Login Through WebGUI: {str( E )}" )
