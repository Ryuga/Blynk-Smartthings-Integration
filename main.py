import codecs

from fastapi import FastAPI, Request, Response
from smartapp.interface import ConfigSection, DeviceSetting, SmartAppConfigPage, SmartAppDefinition
from smartapp.interface import SmartAppRequestContext
from smartapp.dispatcher import SmartAppDispatcher
from starlette.responses import JSONResponse

from smartthings.handler import EventHandler

import config

api = FastAPI()

definition = SmartAppDefinition(
    id="blynk",
    name="Smart App",
    description="Internal SmartApp",
    target_url=config.TARGET_URL,
    permissions=["r:devices:*"],
    config_pages=[
        SmartAppConfigPage(
            page_name="Configuration",
            sections=[
                ConfigSection(
                    name="Devices",
                    settings=[
                        DeviceSetting(
                            id="switch",
                            name="Virtual Switches",
                            description="Virual Switches",
                            required=False,
                            multiple=True,
                            capabilities=["switch"],
                            permissions=["r"],
                        ),
                    ],
                )
            ],
        )
    ],
)

dispatcher = SmartAppDispatcher(definition=definition, event_handler=EventHandler())

@api.post("/smartapp")
async def smart_app(request: Request) -> Response:
    headers = request.headers
    body = codecs.decode(await request.body(), "UTF-8")
    context = SmartAppRequestContext(headers=headers, body=body)
    content = dispatcher.dispatch(context=context)
    return Response(status_code=200, content=content, media_type="application/json")


@api.get("/ryuga")
async def ping() -> JSONResponse:
    return JSONResponse(content={"message": "Hi I'm Ryuga 😀 | Thanks for discovering this hidden endpoint! | Reach me at github.com/Ryuga"}, status_code=200)
