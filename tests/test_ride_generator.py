from realtime_rides.ride_generator import generate_ride_event


def test_generate_ride_event_contains_pipeline_keys():
    event = generate_ride_event()

    assert event["ride_id"]
    assert event["confirmation_number"]
    assert event["passenger_id"]
    assert event["driver_id"]
    assert event["vehicle_id"]
    assert event["pickup_city_id"] in range(1, 11)
    assert event["dropoff_city_id"] in range(1, 11)
    assert event["total_fare"] >= event["subtotal"]


def test_cancelled_rides_have_cancellation_reason():
    for _ in range(50):
        event = generate_ride_event()
        if event["ride_status_id"] == 2:
            assert event["cancellation_reason_id"] in [1, 2, 3]
        else:
            assert event["cancellation_reason_id"] == 4

