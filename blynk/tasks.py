import asyncio
from datetime import datetime, time
from zoneinfo import ZoneInfo

from blynk.controller import BlynkController
from blynk.handler import BlynkHandler
from blynk.models import DeviceState

blynk_api = BlynkController()
blynk_handler = BlynkHandler()

IST = ZoneInfo("Asia/Kolkata")


async def power_saving_background_task():
    while True:
        for device in blynk_handler.device_map.values():
            now_ist = datetime.now(IST).time()
            if time(6, 30) <= now_ist < time(18, 0):
                if blynk_api.get_device_status(device):
                    device.state = DeviceState.OFF
                    blynk_api.set_status(device.token, device.stream, device.state)

            await asyncio.sleep(30)

        print("waiting 5 minutes after next check")
        await asyncio.sleep(300)
