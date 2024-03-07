import os


from selenium import webdriver
from webdriver_auto_update.chrome_app_utils import ChromeAppUtils

from logger import setup_logger

from webdriver_auto_update.webdriver_manager import WebDriverManager

# Path to store chromedriver
driver_directory = "C:\\Users\\ontvi\\AppData\\Local\\Programs\\Python\\Python310\\Scripts"
chromedriver_path = os.path.join(driver_directory, "chromedriver.exe")

logger = setup_logger(__name__)

# Ensure the chromedriver is up-to-date
def update_driver():
    logger.info("Updating Chromedriver")
    chrome_app_utils = ChromeAppUtils()
    chrome_app_version = chrome_app_utils.get_chrome_version()
    print("Chrome application version: ", chrome_app_version)
    driver_manager = WebDriverManager(driver_directory)
    driver_manager.main()

def get_driver():
    logger.debug("Initializing Chrome WebDriver")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(15)
        return driver
    except Exception as E:
        logger.error(f"An Error Occurred While Initializing Chrome WebDriver: {str(E)}")
        return E