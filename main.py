import time
import setup
from login import Login

driver=setup.get_driver()
driver.get( "https://192.168.31.1/" )

login_obj=Login(driver)
time.sleep(30)