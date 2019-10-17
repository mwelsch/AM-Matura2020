import re
from json import *
import requests

import StaticVars
from OverleafDownloaderException import OverleafDownloaderException


class OverleafDownloader:
    def __init__(self):
        try:
            with open("config.json") as config:
                self.json = load(config)
            if self.json["email"] == "":
                raise OverleafDownloaderException("Email is missing in config.json")
            if self.json["password"] == "":
                raise OverleafDownloaderException("Password is missing in config.json")
            if self.json["project_id"] == "":
                raise OverleafDownloaderException("Project Id is missing in config.json")

            self.session = requests.Session()

        except IOError:
            raise OverleafDownloaderException("Please check if config.json exists.")
        except JSONDecodeError:
            raise OverleafDownloaderException("Please check format of config.json.")

    def get_email(self):
        return self.json["email"]

    def get_password(self):
        return self.json["password"]

    def get_project_id(self):
        return self.json["project_id"]

    def login(self):
        csrf_req = self.session.get(StaticVars.OVERLEAF_LOGIN)

        csrf_token = re.findall(StaticVars.OVERLEAF_CSRF_REGEX, csrf_req.text)[0]

        payload = {"_csrf": csrf_token, "email": self.get_email(), "password": self.get_password()}

        return self.session.post(StaticVars.OVERLEAF_LOGIN, payload)

    def download(self):
        project_id = self.get_project_id()
        url = StaticVars.get_download_url(project_id)
        download_request = self.session.get(url)
        open(str(project_id) + ".zip", "wb").write(download_request.content)
