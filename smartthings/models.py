import uuid
from typing import List, Any, Dict
from dataclasses import dataclass, field


@dataclass
class Device:
    deviceId: str
    componentId: str
    capability: str
    attribute: str
    value: Any
    stateChangeOnly: bool
    modes: List[Any] = field(default_factory=list)

@dataclass
class Item:
    id: str
    installedAppId: str
    sourceType: str
    device: Device


class Subscription:
    items: List[Item]

    def __init__(self, items: List[Item]):
        self.items = items


    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> "Subscription":
        items = []
        for item in json_data.get("items", []):
            device_data = item["device"]
            device = Device(**device_data)
            items.append(Item(
                id=item.get("id", str(uuid.uuid4())),
                installedAppId=item["installedAppId"],
                sourceType=item.get("sourceType", "DEVICE"),
                device=device
            ))
        return Subscription(items=items)