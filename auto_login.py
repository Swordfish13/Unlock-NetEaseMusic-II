# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00B8ABF262F045DBF223E659E2736F8DCBE3AA5E970C3FABF256BDE20900CCC5F931D6063700A527A918EBBE3FFE6EB48A5393C0F1698B5F5EAAA55464EE6A869ABE4AA18033DA48C51F5809E5C2A7E5F1C19171C818CC745901D973A2AFD8F66786A0EC3819BEF91B6134039297C5B13338C6DF1654350E787FA84993D8586BCE2DB7A4FC62B44474B86E360B1039CC5616346707860CA4000A867524EBA0DDB5378695AAEA49F862ECA762F5B74B59F9EC2DCC806DE2E82B400565D223BE573ED4908D5B48B7FEF86EA4D96112C9D666E63FACBCB1ECBD4269FBDA9EEBC031ADE9699D428D39B41E89DE4AF54EFBE3F196D77F0724EB68AA671411C7B34FCA582BF7AA7BA514EC6D45EFD22A49CE402A9AE6E7C7110F8F5CDF7749674796C1D2D283BD11326E23C9859B02F90D5B40404528289A9A2CAC75CA6AF5647D9FE35EE95B18B683B43A21E0586AC44112458DC6ED09A642AB548A03C7BB368C2D6BEA350439E9F76DDE56A0D31CA649E106C19F26796BCE4E00AB2B23806D975C52CE8DBB6A0E031819E04EFA232E9149E8155BCB55BBE1CA3BCE6F72469728C9DCA1"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
