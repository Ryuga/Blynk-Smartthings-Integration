import requests

import config

class SmartthingsController:

    @staticmethod
    def create_device_subscription(installed_app_id: str, auth_token: str, device_id: str):
        """
        Create a device subscription for switch attribute changes.
        """
        url = f"{config.SMARTTHINGS_API_BASE}/installedapps/{installed_app_id}/subscriptions"
        body = {
            "sourceType": "DEVICE",
            "device": {
                "deviceId": device_id,
                "componentId": "main",
                "capability": "switch",
                "attribute": "switch",
                "stateChangeOnly": True
            }
        }
        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        r = requests.post(url, headers=headers, json=body, timeout=10)
        r.raise_for_status()
        return r.json()


    @staticmethod
    def get_device_subscription(installed_app_id: str, auth_token: str):
        """
        Get all device subscription for app id.
        """
        url = f"{config.SMARTTHINGS_API_BASE}/installedapps/{installed_app_id}/subscriptions"

        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        r = requests.get(url, headers=headers, timeout=10)
        return r.json()


    @staticmethod
    def delete_device_subscription(installed_app_id: str, auth_token: str, subscription_id: str):
        """
        Delete individual device subscription for app.
        """
        url = f"{config.SMARTTHINGS_API_BASE}/installedapps/{installed_app_id}/subscriptions/{subscription_id}"

        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        r = requests.delete(url, headers=headers, timeout=10)
        return r.json()


    @staticmethod
    def delete_app_subscription(installed_app_id: str, auth_token: str):
        """
        Delete all device subscription for app.
        """
        url = f"{config.SMARTTHINGS_API_BASE}/installedapps/{installed_app_id}/subscriptions/"

        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        r = requests.delete(url, headers=headers, timeout=10)
        return r.json()