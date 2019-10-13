import json
import os
import sys
import subprocess

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from zipfile import ZipFile


def download_wait(og_driver):
    if not og_driver.current_url.startswith("chrome://downloads"):
        og_driver.get("chrome://downloads/")
    return og_driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        task = sys.argv[1]
        directory = os.getcwd()

        if task == "init":
            obs_conf = ('{\n'
                        '  "email": "<your@mail>",\n'
                        '  "password": "<password>",\n'
                        '  "document": "<document_title>"\n'
                        '}')
            with open("config.json", "w+") as config:
                config.write(obs_conf)
            with open(".gitignore", "w+") as gitignore:
                gitignore.write("config.json\n")
                gitignore.write("debug.log\n")
            subprocess.call(["git", "init"])
            if len(sys.argv) >= 3:
                subprocess.call(["git", "remote", "add", "origin", str(sys.argv[2])])

        elif task == "do":
            # Read config
            with open("config.json") as config:
                data = json.load(config)
            # Configure browser
            opp = Options()
            opp.add_argument("--blink-settings=imagesEnabled=false")
            opp.add_argument("--no-proxy-server")
            opp.add_argument("--disable-gpu")
            opp.add_argument("--hide-scrollbars")
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.default_directory": r"" + directory + "\\",
                     # IMPORTANT - ENDING SLASH V IMPORTANT
                     "directory_upgrade": True}
            opp.add_experimental_option("prefs", prefs)
            opp.add_argument("download.default_directory=" + directory)
            # Start it!
            driver = webdriver.Chrome(options=opp)
            driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/73.0.3683.86 Safari/537.36",
                "platform": "Windows"})
            # Go to overleaf
            try:
                driver.get("https://www.overleaf.com/login")
            except TimeoutException:
                driver.execute_script("window.stop();")
            # Log in
            driver.find_element_by_name("email").send_keys(data["email"])
            driver.find_element_by_name("password").send_keys(data["password"])
            driver.find_element_by_name("password").send_keys(Keys.ENTER)
            # Download wanted document
            WebDriverWait(driver, 200).until(ec.element_to_be_clickable(
                (By.XPATH, "//tr[td/div/span/a[text() = '" + data["document"] + "']]/td/div/button[2]"))).click()
            # Logout
            driver.get("https://www.overleaf.com/logout")
            # Wait for donwload to complete
            driver.implicitly_wait(1)
            paths = WebDriverWait(driver, 120, 1).until(download_wait)
            driver.implicitly_wait(2)
            # Quit browser
            driver.quit()
            # Unzip download and remove zip
            backup = ZipFile(data["document"] + ".zip")
            backup.extractall()
            backup.close()
            os.remove(data["document"] + ".zip")
            # Create commit message
            if len(sys.argv) >= 3:
                msg = str(sys.argv[2])
            else:
                msg = "Updated " + data["document"]
            # Add, commit and push
            subprocess.call(["git", "add", "-A"])
            subprocess.call(["git", "commit", "-m", msg])
            subprocess.call(["git", "push", "-u", "origin", "master"])
        else:
            print("Unknown command - Viable commands are:")
            print("\tobs init [remote-repository-url]")
            print("\tobs do [commit-message]")
    else:
        print("No command given - Viable commands are:")
        print("\tobs init [remote-repository-url]")
        print("\tobs do [commit-message]")
