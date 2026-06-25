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

from smartthings.controller import SmartthingsController
from smartthings.models import Subscription
from blynk.controller import BlynkController

ACTIVE_SUBSCRIPTIONS = {}

blynk = BlynkController()


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
            try:
                SmartthingsController.delete_device_subscription(
                    installed_app_id=installed_app_id,
                    auth_token=auth_token,
                    subscription_id=sub_id
                )
            except Exception as e:
                print(f"Failed to delete subscription {sub_id}: {e}")

    for _id in added_switches:
        if _id in ACTIVE_SUBSCRIPTIONS:
            continue

        try:
            data = SmartthingsController.create_device_subscription(
                installed_app_id=installed_app_id,
                auth_token=auth_token,
                device_id=_id
            )
            if data and data.get("id"):
                ACTIVE_SUBSCRIPTIONS[_id] = data.get("id")
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 409:
                print(f"Subscription for device {_id} already exists. Skipping.")
                load_active_subscriptions(auth_token, installed_app_id)
            else:
                raise err


def get_configured_mappings(config: dict) -> dict:
    """Extracts device-to-blynk mappings, handling tokens and pins separately."""
    mappings = {}
    seen = set()
    for i in range(1, 11):
        switch_config = config.get(f"switch_{i}", [])
        blynk_pin_list = config.get(f"blynk_id_{i}", [])
        blynk_token_list = config.get(f"blynk_token_{i}", [])

        if switch_config and blynk_pin_list and blynk_token_list:
            device_id = switch_config[0].device_config.device_id
            pin = blynk_pin_list[0].string_config.value
            token = blynk_token_list[0].string_config.value

            if pin and token and (device_id not in seen):
                mappings[device_id] = {"pin": pin, "token": token}
                seen.add(device_id)

    return mappings




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
        config = data.installed_app.config
        mappings = get_configured_mappings(config)

        for device_id in mappings.keys():
            response = SmartthingsController.create_device_subscription(
                installed_app_id=data.installed_app.installed_app_id,
                auth_token=data.auth_token,
                device_id=device_id
            )
            if response.get("id", None):
                ACTIVE_SUBSCRIPTIONS[device_id] = response.get("id")



    def handle_update(self, correlation_id: Optional[str], request: UpdateRequest) -> None:
        update_data = request.update_data
        installed_app_id = update_data.installed_app.installed_app_id

        current_mappings = get_configured_mappings(update_data.installed_app.config)
        previous_mappings = get_configured_mappings(update_data.previous_config)

        existing_switches = set(previous_mappings.keys())
        current_switches = set(current_mappings.keys())

        removed_switches = existing_switches - current_switches
        added_switches = current_switches - existing_switches

        update_active_subscriptions(
            added_switches=added_switches,
            removed_switches=removed_switches,
            auth_token=update_data.auth_token,
            installed_app_id=installed_app_id
        )

    def handle_event(self, correlation_id: Optional[str], request: EventRequest) -> None:
        mappings = get_configured_mappings(request.event_data.installed_app.config)

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

            mapping_data = mappings.get(dev_id)
            if mapping_data:
                token = mapping_data.get("token")
                pin = mapping_data.get("pin")
                state = 1 if state.lower() == "on" else 0
                blynk.set_status(
                    token=token,
                    pin=pin,
                    state=state
                )
