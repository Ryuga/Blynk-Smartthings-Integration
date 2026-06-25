import requests
import config

class BlynkController(object):

    def __init__(self):
        self.base_url = config.BLYNK_API_BASE

    def set_status(self, token, pin, state):
        url = f"{self.base_url}api/update?token={token}&{pin}={state}"
        r = requests.get(url)
        r.raise_for_status()

    def get_status(self, token, pin):
        url = f"{self.base_url}api/get?token={token}&{pin}"
        try:
            r = requests.get(url)
            if r.json() == 1:
                return True
            return False
        except Exception as E:
            print(E)
            return None
