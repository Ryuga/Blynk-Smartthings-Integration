from typing import Optional

import requests
from smartapp.interface import (
    ConfigurationRequest,
    ConfirmationRequest,
    EventRequest,
    EventType,
    InstallRequest,
    OauthCallbackRequest,
    SmartAppEventHandler,
    UninstallRequest,
    UpdateRequest
)

from blynk.models import DeviceEvent, DeviceState
from smartthings.controller import SmartthingsController
from smartthings.models import Subscription
from smartthings.utils import SmartThingsUtils
from blynk.handler import BlynkHandler


ACTIVE_SUBSCRIPTIONS = {}

blynk = BlynkHandler()


def load_active_subscriptions(auth_token, installed_app_id) -> None:
    data = SmartthingsController.get_device_subscription(
        installed_app_id=installed_app_id,
        auth_token=auth_token
    )
    subscription = Subscription.from_json(data)
    for item in subscription.items:
        ACTIVE_SUBSCRIPTIONS[item.device.deviceId] = item.id

def update_active_subscriptions(added_switches, removed_switches, auth_token, installed_app_id):
    load_active_subscriptions(auth_token, installed_app_id)

    for _id in removed_switches:
        sub_id = ACTIVE_SUBSCRIPTIONS.pop(_id, None)
        if sub_id:
            SmartthingsController.delete_device_subscription(
                installed_app_id=installed_app_id,
                auth_token=auth_token,
                subscription_id=sub_id
            )
    for _id in added_switches:
        data = SmartthingsController.create_device_subscription(
            installed_app_id=installed_app_id,
            auth_token=auth_token,
            device_id=_id
        )
        if data.get("id"):
            ACTIVE_SUBSCRIPTIONS[_id] = data.get("id")

class EventHandler(SmartAppEventHandler):

    """SmartApp event handler."""

    def handle_confirmation(self, correlation_id: Optional[str], request: ConfirmationRequest) -> None:
        """Handle a CONFIRMATION lifecycle request"""
        requests.get(request.confirmation_data.confirmation_url)

    def handle_configuration(self, correlation_id: Optional[str], request: ConfigurationRequest) -> None:
        """Handle a CONFIGURATION lifecycle request."""

    def handle_oauth_callback(self, correlation_id: Optional[str], request: OauthCallbackRequest) -> None:
        """Handle an OAUTH_CALLBACK lifecycle request."""

    def handle_uninstall(self, correlation_id: Optional[str], request: UninstallRequest) -> None:
        """Handle an UNINSTALL lifecycle request."""

    def handle_install(self, correlation_id: Optional[str], request: InstallRequest) -> None:
        data = request.install_data
        switches = data.installed_app.config.get("switch", [])

        for switch in switches:
            response = SmartthingsController.create_device_subscription(
                installed_app_id=data.installed_app.installed_app_id,
                auth_token=data.auth_token,
                device_id=switch.device_config.device_id
            )
            if response.get("id", None):
                ACTIVE_SUBSCRIPTIONS[switch.device_config.device_id] = response.get("id")



    def handle_update(self, correlation_id: Optional[str], request: UpdateRequest) -> None:
        update_data = request.update_data
        installed_app_id = update_data.installed_app.installed_app_id

        previous_data  = update_data.previous_config.get("switch", [])
        current_data = update_data.installed_app.config.get("switch", [])

        existing_switches = set(SmartThingsUtils.get_switch_ids(previous_data))
        current_switches = set(SmartThingsUtils.get_switch_ids(current_data))

        removed_switches = existing_switches - current_switches
        added_switches = current_switches - existing_switches

        update_active_subscriptions(
            added_switches=added_switches,
            removed_switches=removed_switches,
            auth_token=update_data.auth_token,
            installed_app_id=installed_app_id
        )

    def handle_event(self, correlation_id: Optional[str], request: EventRequest) -> None:
        for event in request.event_data.events:
            if event.event_type != EventType.DEVICE_EVENT:
                continue

            device_event = event.device_event or {}
            if not device_event.get("stateChange"):
                continue

            dev_id = device_event.get("deviceId")
            state = device_event.get("value")
            if not (dev_id and state):
                continue

            dev_state = DeviceState.ON if state.lower() == "on" else DeviceState.OFF
            blynk.handle_device_event(DeviceEvent(dev_id, dev_state))