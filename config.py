from decouple import config

SMARTTHINGS_API_BASE = "https://api.smartthings.com/"
BLYNK_API_BASE = "https://blynk.cloud/external/"

TARGET_URL = config("TARGET_URL")
NUMBER_OF_DEVICES = config("NUMBER_OF_DEVICES", 5, cast=int)
