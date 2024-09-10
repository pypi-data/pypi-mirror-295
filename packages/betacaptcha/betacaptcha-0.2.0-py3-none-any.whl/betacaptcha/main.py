import time
import base64
import urllib3
import requests
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

class BetaCaptcha():
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.BASE_URL = "https://betacaptcha.com"
    def image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    def get_balance(self):
        json_data = {"api_token": self.API_KEY}
        return requests.post(self.BASE_URL + "/api/balance", json=json_data, verify=False).json()
    def getJobResult(self, taskid, loop=150):
        for _ in range(loop):
            json_data = {"api_token": self.API_KEY, "taskid": taskid}
            getJobResult = requests.post(self.BASE_URL + "/api/getJobResult", json=json_data, verify=False)
            if getJobResult.json()["status"] != "running":
                return getJobResult.json()["result"]
            else:
                time.sleep(1)
    def image_to_text(self, image_as_base64=None, file=None, timeout=60):
        # Kiểm tra dữ liệu đầu vào và chuyển đổi
        if image_as_base64 is None:
            if file is None:
                raise RuntimeError("image_as_base64 and file is None ")
            else:
                image_as_base64 = self.image_to_base64(file)
        # Tạo Job lên server
        json_data = {
            "api_token": self.API_KEY,
            "data": {
                "type_job": "textcaptcha",
                "body": image_as_base64
            }
        }
        createJob = requests.post(self.BASE_URL + "/api/createJob", json=json_data, timeout=timeout, verify=False)
        return self.getJobResult(createJob.json()["taskid"])
    def funcaptcha_image(self, imginstructions=None, image_as_base64=None, file=None, timeout=60):
        # Kiểm tra dữ liệu đầu vào và chuyển đổi
        if image_as_base64 is None:
            if file is None:
                raise RuntimeError("image_as_base64 and file is None ")
            else:
                image_as_base64 = self.image_to_base64(file)
        # Tạo Job lên server
        json_data = {
            "api_token": self.API_KEY,
            "data": {
                "type_job": "fun_capcha_click",
                "imginstructions": imginstructions,
                "body": image_as_base64
            }
        }
        createJob = requests.post(self.BASE_URL + "/api/createJob", json=json_data, timeout=timeout, verify=False)
        return self.getJobResult(createJob.json()["taskid"])
    def recaptcha(self, sitekey=None, siteurl=None, timeout=60):
        # Tạo Job lên server
        json_data = {
            "api_token": self.API_KEY,
            "data": {
                "type_job": "recaptcha",
                "siteurl": siteurl,
                "sitekey": sitekey
            }
        }
        createJob = requests.post(self.BASE_URL + "/api/createJob", json=json_data, timeout=timeout, verify=False)
        return self.getJobResult(createJob.json()["taskid"])
    def tiktok_slide(self, image_as_base64=None, timeout=60):
        # Tạo Job lên server
        json_data = {
            "api_token": self.API_KEY,
            "data": {
                "type_job": "tiktok_slide",
                "body": image_as_base64
            }
        }
        createJob = requests.post(self.BASE_URL + "/api/createJob", json=json_data, timeout=timeout, verify=False)
        return self.getJobResult(createJob.json()["taskid"])
    def tiktok_click(self, image_as_base64=None, timeout=60):
        # Tạo Job lên server
        json_data = {
            "api_token": self.API_KEY,
            "data": {
                "type_job": "tiktok_click",
                "body": image_as_base64
            }
        }
        createJob = requests.post(self.BASE_URL + "/api/createJob", json=json_data, timeout=timeout, verify=False)
        return self.getJobResult(createJob.json()["taskid"])
        