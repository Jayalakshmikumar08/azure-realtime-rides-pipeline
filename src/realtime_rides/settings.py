from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass(frozen=True)
class EventHubSettings:
    connection_string: str
    event_hub_name: str


def load_eventhub_settings() -> EventHubSettings:
    load_dotenv()
    connection_string = getenv("EVENT_HUB_CONNECTION_STRING", "")
    event_hub_name = getenv("EVENT_HUB_NAME", "")
    if not connection_string or not event_hub_name:
        raise ValueError(
            "EVENT_HUB_CONNECTION_STRING and EVENT_HUB_NAME must be set before publishing."
        )
    return EventHubSettings(connection_string=connection_string, event_hub_name=event_hub_name)

