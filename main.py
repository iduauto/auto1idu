import time
import setup

driver = setup.get_driver()
driver.get("http://192.168.30.1")
time.sleep(5)
print('done')
