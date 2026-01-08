import requests

import config
from blynk.models import Device


class BlynkController(object):

    def __init__(self):
        self.base_url = config.BLYNK_API_BASE

    def set_status(self, token, stream, state):
        url = f"{self.base_url}api/update?token={token}&{stream}={state.value}"
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

    def set_device_status(self, device: Device) -> None:
        self.set_status(device.token, device.stream, device.state)

    def get_device_status(self, device: Device) -> bool:
        return self.get_status(device.token, device.stream)

