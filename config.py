from decouple import config

SMARTTHINGS_API_BASE = "https://api.smartthings.com/"
BLYNK_API_BASE = "https://blynk.cloud/external/"

TARGET_URL = config("TARGET_URL")

LIGHT_B_TOKEN = config("LIGHT_B_TOKEN")
LIGHT_P_TOKEN = config("LIGHT_P_TOKEN")
