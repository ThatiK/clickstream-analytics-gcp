import sys
import logging
import configparser

from pyspark import SparkFiles
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, lower, substring_index


def clean(input_path, output_path):

    df = spark.read.option("header", "true").csv(input_path)

    clean_df = (
        df.dropna(subset=["visitorid", "timestamp", "event"])
        .withColumn("event_time", to_timestamp(col("timestamp") / 1000))
        .withColumn("event", lower(col("event")))
        .withColumn("event_date", col("event_time").cast("date"))
        .drop("timestamp")
    )

    clean_df.write.mode("overwrite").partitionBy("event_date").parquet(output_path)



def get_spark():
    conf = SparkConf().setAppName("Clean Clickstream")
    # Output commit optimizations
    conf.set("spark.hadoop.mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
    conf.set("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")
    # Output compression
    conf.set("spark.sql.parquet.compression.codec", "snappy")
    # DataFrame Behavior/Safety
    conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic") # only overwrite partitions present in the incoming DataFrame.
    # Handle timezone
    conf.set("spark.sql.session.timeZone", "UTC")

    spark = SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()

    return spark


if __name__ == '__main__':
    env = sys.argv[sys.argv.index("--conf") + 1] 
    props_path = SparkFiles.get(f"{env}.properties")

    config = configparser.ConfigParser()
    config.read(props_path)

    input_path = config.get("PATHS", "raw_events")
    output_path = config.get("PATHS", "clean_events")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
    logger.addHandler(handler)

    logger.info("INPUT PATH: {}".format(input_path))
    logger.info("OUTPUT PATH: {}".format(output_path))

    spark = get_spark()

    clean(input_path, output_path)

    spark.stop()