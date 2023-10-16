from datetime import timedelta

from feast import (
    FileSource,
    KafkaSource,
    Entity,
    Field,
)
from feast.data_format import JsonFormat

from pyspark.sql import DataFrame

from feast.stream_feature_view import stream_feature_view
from feast.types import Float32

# Feast also supports pulling data from data warehouses like BigQuery, Snowflake, Redshift and data lakes (e.g. via Redshift Spectrum, Trino, Spark)

trip_details_batch_source = FileSource(
    name="trip_details_source",
    path="data/trip_historical_data.parquet",
    timestamp_field="event_timestamp",
    owner="test2@gmail.com",
)

trip_details_stream_source = KafkaSource(
    name="trip_details_stream",
    kafka_bootstrap_servers="localhost:9092",
    topic="trip_processed_topic",
    timestamp_field="event_timestamp",
    batch_source=trip_details_batch_source,
    message_format=JsonFormat(
        schema_json="trip_id integer, event_timestamp timestamp, pickup_longitude float, pickup_latitude float, dropoff_longitude float, dropoff_latitude float, Distance float, Monthly_Quarter_Q2 float, Monthly_Quarter_Q3 float, Monthly_Quarter_Q4 float, Hourly_Segments_H2 float, Hourly_Segments_H3 float, Hourly_Segments_H4 float, Hourly_Segments_H5 float, Hourly_Segments_H6 float, year_2010 float, year_2011 float, year_2012 float, year_2013 float, year_2014 float, year_2015 float, weekday_1 float, weekday_2 float, weekday_3 float, weekday_4 float, weekday_5 float, weekday_6 float, passenger_count_1 float, passenger_count_2 float, passenger_count_3 float, passenger_count_4 float, passenger_count_5 float, passenger_count_6 float, passenger_count_208 float"
    ),
    watermark_delay_threshold=timedelta(minutes=5),
    description="The Kafka stream containing the trip details",
    owner="test3@gmail.com",
)

trip = Entity(
    name="trip",
    join_keys=["trip_id"],
    description="trip id",
)

@stream_feature_view(
    entities=[trip],
    ttl=timedelta(seconds=8640000000),
    mode="spark",
    schema=[
        Field(name="pickup_longitude", dtype=Float32),
        Field(name="pickup_latitude", dtype=Float32),
        Field(name="dropoff_longitude", dtype=Float32),
        Field(name="dropoff_latitude", dtype=Float32),
        Field(name="Distance", dtype=Float32),
        Field(name="Monthly_Quarter_Q2", dtype=Float32),
        Field(name="Monthly_Quarter_Q3", dtype=Float32),
        Field(name="Monthly_Quarter_Q4", dtype=Float32),
        Field(name="Hourly_Segments_H2", dtype=Float32),
        Field(name="Hourly_Segments_H3", dtype=Float32),
        Field(name="Hourly_Segments_H4", dtype=Float32),
        Field(name="Hourly_Segments_H5", dtype=Float32),
        Field(name="Hourly_Segments_H6", dtype=Float32),
        Field(name="year_2010", dtype=Float32),
        Field(name="year_2011", dtype=Float32),
        Field(name="year_2012", dtype=Float32),
        Field(name="year_2013", dtype=Float32),
        Field(name="year_2014", dtype=Float32),
        Field(name="year_2015", dtype=Float32),
        Field(name="weekday_1", dtype=Float32),
        Field(name="weekday_2", dtype=Float32),
        Field(name="weekday_3", dtype=Float32),
        Field(name="weekday_4", dtype=Float32),
        Field(name="weekday_5", dtype=Float32),
        Field(name="weekday_6", dtype=Float32),
        Field(name="passenger_count_1", dtype=Float32),
        Field(name="passenger_count_2", dtype=Float32),
        Field(name="passenger_count_3", dtype=Float32),
        Field(name="passenger_count_4", dtype=Float32),
        Field(name="passenger_count_5", dtype=Float32),
        Field(name="passenger_count_6", dtype=Float32),
        Field(name="passenger_count_208", dtype=Float32),
    ],
    timestamp_field="event_timestamp",
    online=True,
    source=trip_details_stream_source,
    tags={},
)
def trip_details_online_stream(df: DataFrame):
    return df