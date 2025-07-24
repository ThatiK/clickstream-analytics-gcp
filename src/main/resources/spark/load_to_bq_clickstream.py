import sys
import configparser
import logging

from pyspark import SparkFiles
from pyspark import SparkConf
from pyspark.sql import SparkSession

def load_to_bq(gcs_prefix, bq_table, bucket_temp, partition_field):
    logger.info("Reading sessionized events from: {}".format(gcs_prefix))
    df = spark.read.parquet(gcs_prefix)

    df = df.drop("event_date_part")

    logger.info(df.show())

    logger.info(f"Writing to BQ Table: {bq_table} using partition field: {partition_field}")
    df.write.format("bigquery") \
        .option("table", bq_table) \
        .option("temporaryGcsBucket", bucket_temp) \
        .option("partitionField", partition_field) \
        .option("partitionType", "DAY") \
        .mode("overwrite") \
        .save()

def get_spark():
    conf = SparkConf().setAppName("Load To BQ Clickstream")

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

    gcs_prefix = config.get("PATHS", "sessionized_events")
    project_id = config.get("COMMON", "project_id")
    bucket_temp = config.get("COMMON", "bucket")
    dataset = config.get("BQ", "dataset_staging")
    table = config.get("BQ", "table_sessionized")
    partition_field = config.get("BQ", "table_sessionized_partition_field")

    bq_table = f"{project_id}.{dataset}.{table}"

    load_to_bq(gcs_prefix, bq_table, bucket_temp, partition_field)

    spark.stop()