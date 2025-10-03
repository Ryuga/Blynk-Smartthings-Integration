import requests

import config
from blynk.models import Device


class BlynkController(object):

    def __init__(self):
        self.base_url = config.BLYNK_API_BASE

    def get(self, token, stream, state):
        url = f"{self.base_url}api/update?token={token}&{stream}={state.value}"
        r = requests.get(url)
        r.raise_for_status()

    def set_device_status(self, device: Device) -> None:
        self.get(device.token, device.stream, device.state)


