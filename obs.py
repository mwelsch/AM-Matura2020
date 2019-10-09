import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def download_wait(og_driver):
    if not og_driver.current_url.startswith("chrome://downloads"):
        og_driver.get("chrome://downloads/")
    return og_driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)


if __name__ == "__main__":
    # Read config
    with open('test.json') as json_file:
        data = json.load(json_file)
    # Configure browser
    opp = Options()
    opp.add_argument('--blink-settings=imagesEnabled=false')
    opp.add_argument('--no-proxy-server')
    opp.add_argument('--disable-gpu')
    opp.add_argument('--hide-scrollbars')
    # Start it!
    driver = webdriver.Chrome(options=opp)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {
        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "platform": "Windows"})
    # Go to overleaf
    try:
        driver.get("https://www.overleaf.com/login")
        # driver.get("https://youtube.com")
    except TimeoutException:
        driver.execute_script("window.stop();")
    # Log in
    driver.find_element_by_name("email").send_keys(data["email"])
    driver.find_element_by_name("password").send_keys(data["password"])
    driver.find_element_by_name("password").send_keys(Keys.ENTER)
    # Download wanted document
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(
        (By.XPATH, "//tr[td/div/span/a[text() = '" + data["document"] + "']]/td/div/button[2]"))).click()
    # Wait for donwload to complete
    driver.implicitly_wait(1)
    paths = WebDriverWait(driver, 120, 1).until(download_wait)
    driver.implicitly_wait(2)
    # Quit it!
    driver.quit()
