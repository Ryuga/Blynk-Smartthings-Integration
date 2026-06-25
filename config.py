from decouple import config

SMARTTHINGS_API_BASE = "https://api.smartthings.com/"
BLYNK_API_BASE = "https://blynk.cloud/external/"

RENDER_HOST = config("RENDER_EXTERNAL_HOSTNAME", None)

TARGET_URL =  f"https://{RENDER_HOST}" if RENDER_HOST else  config("TARGET_URL")
NUMBER_OF_DEVICES = config("NUMBER_OF_DEVICES", 5, cast=int)
