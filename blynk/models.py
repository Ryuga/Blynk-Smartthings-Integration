from enum import Enum
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from blynk.controller import BlynkController


class Controllable:
    def turn_on(self):
        raise NotImplementedError

    def turn_off(self):
        raise NotImplementedError


class DeviceType(Enum):
    SWITCH = "switch"
    LIGHT = "light"


class DeviceState(Enum):
    ON = 1
    OFF = 0

@dataclass
class DeviceEvent:
    device_id: str
    state: DeviceState

@dataclass
class Device(Controllable):
    id: str
    token: str
    stream: str
    type: DeviceType
    state: DeviceState
    controller: "BlynkController"

    def turn_on(self):
        self.set_state(DeviceState.ON)

    def turn_off(self):
        self.set_state(DeviceState.OFF)

    def set_state(self, state: DeviceState):
        self.state = state
        self.controller.set_device_status(self)