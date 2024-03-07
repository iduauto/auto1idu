import time

from utils import Utils
from logger import setup_logger

logger = setup_logger(__name__)


class Firewall:
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)

    def add_ipv4_firewall_rule(self, service='HTTP', action="Block Always"):
        logger.info("Adding IPv4 rule")
        try:
            # self.utils.search_WebGUI("List of IPv4 Firewall Rules")
            self.utils.navigate("Firewall")
            self.utils.find_element("/html/body/mainapp/div[1]/div[2]/div[4]/div[2]/div[1]/div[1]/div/div[3]").click()
            self.utils.find_element("//div[@class='jioModalWindowContent']//div[1]//div[1]//label[1]//span[1]").click()
            self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[3]/form[1]/div[2]/div[1]/div[3]/div[1]/span[1]").click()
            self.utils.find_element(f"//li[normalize-space()='{service}']").click()
            self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[3]/form[1]/div[2]/div[1]/div[5]/div[1]/span[1]").click()
            self.utils.find_element(f"//ul[@data-name='action_ul']//li[contains(text(),'{action}')]").click()
            self.utils.find_element(
                "//div[@class='jioModalWindowFooter']//button[@type='button'][normalize-space()='SAVE']").click()

            logger.info(f"IPv4 firewall rule added - Service: {service}, Action: {action}")
            time.sleep(5)
        except Exception as e:
            logger.error("Error occurred while adding IPv4 firewall rule", str(e))
            return False

    def add_ipv6_firewall_rule(self, service='HTTP', action="Block Always", rule_type="Inbound"):
        logger.info("Adding IPv6 rule")
        try:
            # self.utils.search_WebGUI( "List of IPv6 Firewall Rules" )
            self.utils.navigate("Firewall")
            self.utils.find_element(
                "/html/body/mainapp/div[1]/div[2]/div[4]/div[3]/div[1]/div[1]/div/div[3]/div").click()
            self.utils.find_element("//div[@class='jioModalWindowContent']//div[1]//div[1]//label[1]//span[1]").click()
            self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[4]/form[1]/div[2]/div[1]/div[3]/div[1]/span[1]").click()
            self.utils.find_element(f"//li[normalize-space()='{rule_type}']").click()
            self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[4]/form[1]/div[2]/div[1]/div[5]/div[1]/span[1]").click()
            self.utils.find_element(f"//li[normalize-space()='{service}']").click()
            self.utils.find_element(
                "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[4]/form[1]/div[2]/div[1]/div[7]/div[1]/span[1]").click()
            self.utils.find_element(f"//span[normalize-space()='{action}']").click()
            self.utils.find_element(
                "//div[@class='jioModalWindowFooter']//button[@type='button'][normalize-space()='SAVE']").click()

            logger.info(f"IPv6 firewall rule added - Service: {service}, Action: {action}, Rule Type: {rule_type}")
            time.sleep(5)
        except Exception as e:
            logger.error("Error occurred while adding IPv6 firewall rule", str(e))
            return False

    def add_port_forwarding_rule(self):
        self.utils.search_WebGUI("List of Port Forwarding")
        self.utils.find_element(
            "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[4]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]")
        pass

    def delete_ipv4_firewall_rule(self):
        logger.info("Deleting IPv4 rule")
        try:
            # self.utils.search_WebGUI( "List of IPv4 Firewall Rules" )
            self.utils.navigate("Firewall")
            ipv4_counter_element = self.utils.find_element(
                "/html/body/mainapp/div[1]/div[2]/div[4]/div[2]/div[3]/div[4]").text
            total_ipv4_rules = int(
                ipv4_counter_element.split("/")[1].strip())  # total number of ipv4 firewall rules present
            if total_ipv4_rules > 0:
                self.utils.find_element("//tbody/tr/td[7]/div[1]/div[4]/div[1]//*[name()='svg']").click()
                self.utils.find_element("//button[normalize-space()='DELETE']").click()
                time.sleep(5)

                logger.info(f"IPv4 firewall rule Deleted ")
        except Exception as e:
            logger.error("Error occurred while Deleting IPv4 firewall rule", str(e))
            return False

    def delete_ipv6_firewall_rule(self):
        try:
            logger.info("Deleting IPv6 rule")
            # self.utils.search_WebGUI( "List of IPv6 Firewall Rules" )
            self.utils.navigate("Firewall")
            ipv6_counter_element = self.utils.find_element(
                "/html/body/mainapp/div[1]/div[2]/div[4]/div[3]/div[3]/div[4]").text
            total_ipv6_rules = int(
                ipv6_counter_element.split("/")[1].strip())  # total number of ipv6 firewall rules present

            if total_ipv6_rules > 0:
                self.utils.find_element("//tbody/tr/td[8]/div[1]/div[4]/div[1]//*[name()='svg']").click()
                self.utils.find_element("//button[normalize-space()='DELETE']").click()
                time.sleep(5)

                logger.info(f"IPv6 firewall rule Deleted")
        except Exception as e:
            logger.error("Error occurred while Deleting IPv6 firewall rule", str(e))
            return e

    def delete_port_forwarding_rule(self):
        self.utils.search_WebGUI("List of Port Forwarding")
        self.utils.find_element(
            "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[4]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]")
        pass

    def total_ipv4_rules(self):
        logger.debug("Counting IPv6 Firewall Rules")
        try:
            # self.utils.search_WebGUI("List of IPv4 Firewall Rules")
            self.utils.navigate("Firewall")
            ipv4_counter_element = self.utils.find_element(
                "/html/body/mainapp/div[1]/div[2]/div[4]/div[2]/div[3]/div[4]").text
            total_ipv4_rules = int(
                ipv4_counter_element.split("/")[1].strip())  # total number of ipv4 firewall rules present

            logger.debug(f"Total IPv4 rules : {total_ipv4_rules}")
            return total_ipv4_rules
        except Exception as e:
            logger.error("Error occurred while Counting IPv4 firewall rule", str(e))
            return e

    def total_ipv6_rules(self):
        logger.debug("Counting IPv6 Firewall Rules")
        try:
            # self.utils.search_WebGUI("List of IPv6 Firewall Rules")
            self.utils.navigate("Firewall")
            ipv6_counter_element = self.utils.find_element(
                "/html/body/mainapp/div[1]/div[2]/div[4]/div[3]/div[3]/div[4]").text
            total_ipv6_rules = int(
                ipv6_counter_element.split("/")[1].strip())  # total number of ipv6 firewall rules present

            logger.debug(f"Total IPv6 rules : {total_ipv6_rules}")
            return total_ipv6_rules
        except Exception as e:
            logger.error("Error occurred while Counting IPv6 firewall rule", str(e))
            return e
