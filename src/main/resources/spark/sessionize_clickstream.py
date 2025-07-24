import sys
import logging
import time
import configparser

from pyspark import SparkFiles
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, lag, sum as _sum, concat_ws
from pyspark.sql.window import Window


def sessionize(input_path, output_path, session_gap):
    df = spark.read.parquet(input_path)

    # Sessionization logic
    window_spec = Window.partitionBy("visitorid").orderBy("event_time")

    df = df.withColumn("event_ts", unix_timestamp("event_time"))
    df = df.withColumn("prev_event_ts", lag("event_ts").over(window_spec))

    df = df.withColumn(
        "new_session",
        (col("event_ts") - col("prev_event_ts") > session_gap).cast("int")
    )

    df = df.withColumn("session_number", _sum("new_session").over(window_spec))

    df = df.withColumn("session_id", concat_ws("_", col("visitorid"), col("session_number")))

    df = df.withColumn("event_date_part", col("event_date"))

    df.write.mode("overwrite").partitionBy("event_date_part").parquet(output_path)


def get_spark():
    conf = SparkConf().setAppName("Sessionize Clickstream")
    # Output commit optimizations
    conf.set("spark.hadoop.mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
    conf.set("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")
    # Output compression
    conf.set("spark.sql.parquet.compression.codec", "snappy")
    # DataFrame Behavior/Safety
    conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic") # only overwrite partitions present in the incoming DataFrame.
    # Handle timezone
    conf.set("spark.sql.session.timeZone", "UTC")

    # AQE
    # Spark 3+ enables Adaptive Query Execution (AQE)
    # at runtime, based on data size and skew, it may:
    #   Reduce the number of shuffle partitions
    #   Combine small partitions
    #   Avoid unnecessary shuffles

    
    # To disable AQE
    #conf.set("spark.sql.adaptive.enabled", "false")
    #conf.set("spark.sql.shuffle.partitions", "12")

    spark = SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()

    return spark


if __name__ == '__main__':
    env = sys.argv[sys.argv.index("--conf") + 1] 

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
    logger.addHandler(handler)

    logger.info("ENV: {}".format(env))

    spark = get_spark()

    props_path = SparkFiles.get(f"{env}.properties")

    config = configparser.ConfigParser()
    config.read(props_path)

    input_path = config.get("PATHS", "clean_events")
    output_path = config.get("PATHS", "sessionized_events")
    session_gap = int(config.get("SETTINGS", "session_gap_minutes")) * 60

    logger.info("INPUT PATH: {}".format(input_path))
    logger.info("OUTPUT PATH: {}".format(output_path))
    logger.info("SESSION GAP IN SECONDS: {}".format(session_gap))

    sessionize(input_path, output_path, session_gap)

    spark.stop()