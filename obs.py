import time
from time import sleep
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json

from selenium.webdriver.support.wait import WebDriverWait

if __name__ == "__main__":
    with open('test.json') as json_file:
        data = json.load(json_file)

    opp = Options()
    opp.add_argument('--blink-settings=imagesEnabled=false')
    opp.add_argument('--no-proxy-server')
    opp.add_argument('--disable-gpu')
    opp.add_argument('--hide-scrollbars')
    driver = webdriver.Chrome(options=opp)


    #driver.set_page_load_timeout(10)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36", "platform": "Windows"})
    try:
        driver.get("https://www.overleaf.com/login")
        #driver.get("https://youtube.com")
    except TimeoutException:
        driver.execute_script("window.stop();")

    driver.find_element_by_name("email").send_keys(data["email"])
    driver.find_element_by_name("password").send_keys(data["password"])
    driver.find_element_by_name("password").send_keys(Keys.ENTER)
    #driver.find_element_by_xpath("/html/body/main/div[2]/div/div/div[2]/div[2]/div/div/ul/table/tbody/tr[2]/td[4]/div/button[2]")
    #driver.find_element_by_xpath("/html/body/main/div[2]/div/div/div[2]/div[2]/div/div/ul/table/tbody/tr[2]/td[4]/div/button[2]").click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[2]/div/div/div[2]/div[2]/div/div/ul/table/tbody/tr[2]/td[4]/div/button[2]"))).click()

    print(str(driver.current_url))


    print("Hello world")
