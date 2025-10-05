"""
This is a temporary solution for bridging my Blynk Devices with Smartthings so the devices are hard coded.
"""

import config
from blynk.controller import BlynkController
from blynk.models import Device, DeviceType, DeviceState, DeviceEvent


class BlynkHandler(object):


    def __init__(self):
        self.device_map = {}
        controller = BlynkController()

        # The device id provided is the Smartthings Virtual Switch ID.
        light_b = Device("09dda55d-f75d-4869-982a-894212e467a9", config.LIGHT_B_TOKEN, "V1", DeviceType.LIGHT, DeviceState.OFF, controller)
        light_p = Device("29d20941-7e70-4cc4-8872-c6dc94b4f24e", config.LIGHT_P_TOKEN, "V2", DeviceType.LIGHT, DeviceState.OFF, controller)
        self.device_map[light_b.id] = light_b
        self.device_map[light_p.id] = light_p


    def handle_device_event(self, event: DeviceEvent):
        device = self.device_map.get(event.device_id, None)
        if device is not None:
            if event.state == DeviceState.ON:
                device.turn_on()
            else:
                device.turn_off()