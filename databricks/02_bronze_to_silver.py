from pyspark import pipelines as dp
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

RIDES_SCHEMA = StructType(
    [
        StructField("ride_id", StringType()),
        StructField("confirmation_number", StringType()),
        StructField("passenger_id", StringType()),
        StructField("driver_id", StringType()),
        StructField("vehicle_id", StringType()),
        StructField("pickup_location_id", StringType()),
        StructField("dropoff_location_id", StringType()),
        StructField("vehicle_type_id", LongType()),
        StructField("vehicle_make_id", LongType()),
        StructField("payment_method_id", LongType()),
        StructField("ride_status_id", LongType()),
        StructField("pickup_city_id", LongType()),
        StructField("dropoff_city_id", LongType()),
        StructField("cancellation_reason_id", LongType()),
        StructField("passenger_name", StringType()),
        StructField("passenger_email", StringType()),
        StructField("passenger_phone", StringType()),
        StructField("driver_name", StringType()),
        StructField("driver_rating", DoubleType()),
        StructField("driver_phone", StringType()),
        StructField("driver_license", StringType()),
        StructField("vehicle_model", StringType()),
        StructField("vehicle_color", StringType()),
        StructField("license_plate", StringType()),
        StructField("pickup_address", StringType()),
        StructField("pickup_latitude", DoubleType()),
        StructField("pickup_longitude", DoubleType()),
        StructField("dropoff_address", StringType()),
        StructField("dropoff_latitude", DoubleType()),
        StructField("dropoff_longitude", DoubleType()),
        StructField("distance_miles", DoubleType()),
        StructField("duration_minutes", LongType()),
        StructField("booking_timestamp", TimestampType()),
        StructField("pickup_timestamp", StringType()),
        StructField("dropoff_timestamp", StringType()),
        StructField("base_fare", DoubleType()),
        StructField("distance_fare", DoubleType()),
        StructField("time_fare", DoubleType()),
        StructField("surge_multiplier", DoubleType()),
        StructField("subtotal", DoubleType()),
        StructField("tip_amount", DoubleType()),
        StructField("total_fare", DoubleType()),
        StructField("rating", DoubleType()),
    ]
)

dp.create_streaming_table("stg_rides", comment="Typed ride events from bulk and streaming sources.")


@dp.append_flow(target="stg_rides")
def rides_bulk():
    return spark.readStream.table("bulk_rides").withColumn(
        "booking_timestamp", col("booking_timestamp").cast("timestamp")
    )


@dp.append_flow(target="stg_rides")
def rides_stream():
    return (
        spark.readStream.table("rides_raw")
        .withColumn("parsed_ride", from_json(col("ride_payload"), RIDES_SCHEMA))
        .select("parsed_ride.*")
    )

