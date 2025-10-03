from typing import List

from smartapp.interface import DeviceConfigValue


class SmartThingsUtils:

    @staticmethod
    def get_switch_ids(configs: List[DeviceConfigValue]) -> List[str]:
        return [config.device_config.device_id for config in configs]

