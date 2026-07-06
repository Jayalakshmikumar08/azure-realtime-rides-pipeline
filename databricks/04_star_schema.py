from pyspark import pipelines as dp


def silver_stream():
    return spark.readStream.table("uber.bronze.silver_obt")


@dp.view
def dim_passenger_view():
    return silver_stream().select(
        "passenger_id", "passenger_name", "passenger_email", "passenger_phone"
    ).dropDuplicates(["passenger_id"])


dp.create_streaming_table("dim_passenger")
dp.create_auto_cdc_flow(
    target="dim_passenger",
    source="dim_passenger_view",
    keys=["passenger_id"],
    sequence_by="passenger_id",
    stored_as_scd_type=1,
)


@dp.view
def dim_vehicle_view():
    return silver_stream().select(
        "vehicle_id",
        "vehicle_make_id",
        "vehicle_type_id",
        "vehicle_model",
        "vehicle_color",
        "license_plate",
        "vehicle_make",
        "vehicle_type",
    ).dropDuplicates(["vehicle_id"])


dp.create_streaming_table("dim_vehicle")
dp.create_auto_cdc_flow(
    target="dim_vehicle",
    source="dim_vehicle_view",
    keys=["vehicle_id"],
    sequence_by="vehicle_id",
    stored_as_scd_type=1,
)


@dp.view
def fact_rides_view():
    return silver_stream().select(
        "ride_id",
        "pickup_city_id",
        "payment_method_id",
        "driver_id",
        "passenger_id",
        "vehicle_id",
        "distance_miles",
        "duration_minutes",
        "base_fare",
        "distance_fare",
        "time_fare",
        "surge_multiplier",
        "total_fare",
        "tip_amount",
        "rating",
    )


dp.create_streaming_table("fact_rides")
dp.create_auto_cdc_flow(
    target="fact_rides",
    source="fact_rides_view",
    keys=["ride_id"],
    sequence_by="ride_id",
    stored_as_scd_type=1,
)

