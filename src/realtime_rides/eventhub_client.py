from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from azure.eventhub import EventData, EventHubProducerClient

from realtime_rides.settings import EventHubSettings


def publish_ride_event(ride_event: Mapping[str, Any], settings: EventHubSettings) -> None:
    producer = EventHubProducerClient.from_connection_string(
        settings.connection_string,
        eventhub_name=settings.event_hub_name,
    )
    try:
        batch = producer.create_batch()
        batch.add(EventData(json.dumps(ride_event)))
        producer.send_batch(batch)
    finally:
        producer.close()

