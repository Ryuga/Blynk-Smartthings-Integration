import codecs
import config

from fastapi import FastAPI, Request, Response
from smartapp.interface import ConfigSection, DeviceSetting, SmartAppConfigPage, SmartAppDefinition, TextSetting, \
    EnumSetting, EnumOption
from smartapp.interface import SmartAppRequestContext
from smartapp.dispatcher import SmartAppDispatcher
from fastapi.responses import JSONResponse

from smartthings.handler import EventHandler

api = FastAPI()

pin_options = [
    EnumOption(
        id=f"V{i}",
        name=f"V{i}"
    )
    for i in range(0, 11)
]

def generate_mapping_sections(slots=5):
    sections = []
    for i in range(1, slots + 1):
        sections.append(
            ConfigSection(
                name=f"Device Mapping {i}",
                settings=[
                    DeviceSetting(
                        id=f"switch_{i}",
                        name=f"Select SmartThings Switch {i}",
                        description="Tap to select a switch",
                        required=False,
                        multiple=False,
                        capabilities=["switch"],
                        permissions=["r", "x"]
                    ),
                    EnumSetting(
                        id=f"blynk_id_{i}",
                        name=f"Choose Your Blynk Data Pin",
                        description="Tap to select a data pin",
                        required=False,
                        multiple=False,
                        options=pin_options
                    ),
                    TextSetting(
                        id=f"blynk_token_{i}",
                        name=f"Blynk Token {i}",
                        description="Enter Blynk device token",
                        required=False,
                        default_value=""
                    )
                ]
            )
        )
    return sections

definition = SmartAppDefinition(
    id="blynk-smartthings-bridge",
    name="Blynk SmartThings Bridge",
    description="Bridge SmartThings Virtual Switches with Blynk resources.",
    target_url=config.TARGET_URL + "/smartapp",
    permissions=["r:devices:*", "x:devices:*"],
    config_pages=[
        SmartAppConfigPage(
            page_name="Configuration",
            sections=generate_mapping_sections(slots=config.NUMBER_OF_DEVICES)
        )
    ]
)

dispatcher = SmartAppDispatcher(definition=definition, event_handler=EventHandler())

@api.post("/smartapp")
async def smart_app(request: Request) -> Response:
    headers = request.headers
    body = codecs.decode(await request.body(), "UTF-8")
    context = SmartAppRequestContext(headers=headers, body=body)
    content = dispatcher.dispatch(context=context)
    return Response(status_code=200, content=content, media_type="application/json")


@api.api_route("/ryuga", methods=["GET", "HEAD"])
async def ping() -> JSONResponse:
    return JSONResponse(content={"message": "Hi I'm Ryuga 😀 | Thanks for discovering this hidden endpoint! | Reach me at github.com/Ryuga"}, status_code=200)

@api.api_route("/ping", methods=["GET", "HEAD"])
async def ping() -> JSONResponse:
    return JSONResponse(content={"message": "Pong!"}, status_code=200)
