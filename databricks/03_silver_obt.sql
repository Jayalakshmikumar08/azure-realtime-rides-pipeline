CREATE OR REFRESH STREAMING TABLE silver_obt
COMMENT "Enriched ride stream joined to reference data for downstream modelling."
AS
SELECT
    rides.*,
    vehicle_makes.vehicle_make,
    vehicle_types.vehicle_type,
    vehicle_types.description,
    vehicle_types.base_rate,
    vehicle_types.per_mile,
    vehicle_types.per_minute,
    ride_statuses.ride_status,
    payment_methods.payment_method,
    payment_methods.is_card,
    payment_methods.requires_auth,
    pickup_cities.city AS pickup_city,
    pickup_cities.state AS pickup_state,
    pickup_cities.region AS pickup_region,
    cancellation_reasons.cancellation_reason
FROM STREAM(uber.bronze.stg_rides) WATERMARK booking_timestamp DELAY OF INTERVAL 3 MINUTES rides
LEFT JOIN uber.bronze.map_vehicle_makes vehicle_makes
    ON rides.vehicle_make_id = vehicle_makes.vehicle_make_id
LEFT JOIN uber.bronze.map_vehicle_types vehicle_types
    ON rides.vehicle_type_id = vehicle_types.vehicle_type_id
LEFT JOIN uber.bronze.map_ride_statuses ride_statuses
    ON rides.ride_status_id = ride_statuses.ride_status_id
LEFT JOIN uber.bronze.map_payment_methods payment_methods
    ON rides.payment_method_id = payment_methods.payment_method_id
LEFT JOIN uber.bronze.map_cities pickup_cities
    ON rides.pickup_city_id = pickup_cities.city_id
LEFT JOIN uber.bronze.map_cancellation_reasons cancellation_reasons
    ON rides.cancellation_reason_id = cancellation_reasons.cancellation_reason_id;

