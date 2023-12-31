import os
import pandas as pd
from pyspark.sql import SparkSession
from feast.infra.contrib.stream_processor import ProcessorConfig
from feast.infra.contrib.spark_kafka_processor import SparkProcessorConfig
from feast.infra.contrib.stream_processor import get_stream_processor_object
from feast import FeatureStore
from feast.repo_config import RepoConfig
from time import sleep

store = FeatureStore(repo_path="feature_repo/")

# See https://spark.apache.org/docs/3.1.2/structured-streaming-kafka-integration.html#deploying for notes on why we need this environment variable.
os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages=org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 pyspark-shell"
spark = SparkSession.builder.master("local").appName("feast-spark").getOrCreate()
spark.conf.set("spark.sql.shuffle.partitions", 5)

def preprocess_fn(rows: pd.DataFrame):
    print(f"df columns: {rows.columns}")
    print(f"df size: {rows.size}")
    print(f"df preview:\n{rows.head()}")
    return rows

ingestion_config = SparkProcessorConfig(mode="spark", source="kafka", spark_session=spark, processing_time="10 seconds", query_timeout=15)
sfv = store.get_stream_feature_view("trip_details_online_stream")

processor = get_stream_processor_object(
    config=ingestion_config,
    fs=store,
    sfv=sfv,
    preprocess_fn=preprocess_fn,
)

query = processor.ingest_stream_feature_view()

try:
    while not query.isActive:
        sleep(1)
    query.awaitTermination()
except KeyboardInterrupt:
    # Stop the query gracefully when a keyboard interrupt (Ctrl+C) is received
    query.stop()
finally:
    spark.stop()