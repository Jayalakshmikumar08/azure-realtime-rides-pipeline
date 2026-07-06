from __future__ import annotations

import random
import uuid
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from faker import Faker

fake = Faker()

VEHICLE_TYPES = {
    1: {"name": "Standard", "base_rate": Decimal("2.50"), "per_mile": Decimal("1.75")},
    2: {"name": "XL", "base_rate": Decimal("3.50"), "per_mile": Decimal("2.25")},
    3: {"name": "Comfort", "base_rate": Decimal("3.00"), "per_mile": Decimal("2.00")},
    4: {"name": "Premium", "base_rate": Decimal("5.00"), "per_mile": Decimal("3.50")},
}

PAYMENT_METHOD_IDS = [1, 2, 3, 4]
CITY_IDS = list(range(1, 11))
VEHICLE_MAKE_IDS = list(range(1, 8))


def money(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def generate_ride_event() -> dict[str, Any]:
    vehicle_type_id = random.choice(list(VEHICLE_TYPES))
    vehicle_type = VEHICLE_TYPES[vehicle_type_id]
    pickup_time = datetime.now(UTC) - timedelta(days=random.randint(0, 30))
    duration_minutes = random.randint(5, 120)
    distance_miles = Decimal(str(round(random.uniform(0.5, 50.0), 2)))
    per_minute = Decimal("0.35")
    surge_multiplier = Decimal(str(round(random.uniform(1.0, 2.5), 2)))
    time_fare = Decimal(duration_minutes) * per_minute
    distance_fare = distance_miles * vehicle_type["per_mile"]
    subtotal = (vehicle_type["base_rate"] + distance_fare + time_fare) * surge_multiplier
    tip = Decimal(str(random.choice([0, 0, 1, 2, 3, 5, round(random.uniform(1, 20), 2)])))

    ride_status_id = random.choice([1, 1, 1, 2])
    cancellation_reason_id = random.choice([1, 2, 3]) if ride_status_id == 2 else 4

    return {
        "ride_id": str(uuid.uuid4()),
        "confirmation_number": fake.bothify("??#-####-??##").upper(),
        "passenger_id": str(uuid.uuid4()),
        "driver_id": str(uuid.uuid4()),
        "vehicle_id": str(uuid.uuid4()),
        "pickup_location_id": str(uuid.uuid4()),
        "dropoff_location_id": str(uuid.uuid4()),
        "vehicle_type_id": vehicle_type_id,
        "vehicle_make_id": random.choice(VEHICLE_MAKE_IDS),
        "payment_method_id": random.choice(PAYMENT_METHOD_IDS),
        "ride_status_id": ride_status_id,
        "pickup_city_id": random.choice(CITY_IDS),
        "dropoff_city_id": random.choice(CITY_IDS),
        "cancellation_reason_id": cancellation_reason_id,
        "passenger_name": fake.name(),
        "passenger_email": fake.email(),
        "passenger_phone": fake.phone_number(),
        "driver_name": fake.name(),
        "driver_rating": round(random.uniform(4.0, 5.0), 2),
        "driver_phone": fake.phone_number(),
        "driver_license": fake.bothify("??-???-#######").upper(),
        "vehicle_model": fake.word().title(),
        "vehicle_color": random.choice(["Black", "White", "Gray", "Silver", "Blue", "Red"]),
        "license_plate": fake.bothify("???-####").upper(),
        "pickup_address": fake.address().replace("\n", ", "),
        "pickup_latitude": round(random.uniform(-90, 90), 6),
        "pickup_longitude": round(random.uniform(-180, 180), 6),
        "dropoff_address": fake.address().replace("\n", ", "),
        "dropoff_latitude": round(random.uniform(-90, 90), 6),
        "dropoff_longitude": round(random.uniform(-180, 180), 6),
        "distance_miles": money(distance_miles),
        "duration_minutes": duration_minutes,
        "booking_timestamp": (pickup_time - timedelta(minutes=random.randint(1, 10))).isoformat(),
        "pickup_timestamp": pickup_time.isoformat(),
        "dropoff_timestamp": (pickup_time + timedelta(minutes=duration_minutes)).isoformat(),
        "base_fare": money(vehicle_type["base_rate"]),
        "distance_fare": money(distance_fare),
        "time_fare": money(time_fare),
        "surge_multiplier": money(surge_multiplier),
        "subtotal": money(subtotal),
        "tip_amount": money(tip),
        "total_fare": money(subtotal + tip),
        "rating": random.choice([None, 4, 5]),
    }

