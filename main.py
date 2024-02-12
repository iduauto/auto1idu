import setup
from functional_sanity import FunctionalSanity

from logger import setup_logger
logger = setup_logger(__name__)

driver=setup.get_driver()

functional_sanity=FunctionalSanity(driver)

print( functional_sanity.functional_sanity_01())
print( functional_sanity.functional_sanity_01())












