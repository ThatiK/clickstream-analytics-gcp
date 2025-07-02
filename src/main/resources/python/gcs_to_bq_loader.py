import os, sys
import re
import argparse
from datetime import datetime
import logging
from google.cloud import storage
from google.cloud import bigquery


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
logger.addHandler(handler)

def load_to_bq(bucket_name, base_prefix, dataset, table, partition_field=None, write_disposition="WRITE_TRUNCATE"):
    # Initialize clients 

    bq_client = bigquery.Client()
    gcs_client = storage.Client()

    logger.info(f"Listing partitions under gs://{bucket_name}/{base_prefix}")

    blobs = gcs_client.list_blobs(bucket_name, prefix=base_prefix)
    date_folders = set()

    pattern = re.compile(r"event_date_part=(\d{4}-\d{2}-\d{2})")

    for blob in blobs:
        match = pattern.search(blob.name)
        if match:
            date_folders.add(match.group(1))

    logger.info(f"Found event_date partitions ({len(date_folders)}): {sorted(date_folders)}")
    
    # Load each date folder one by one
    for event_date in date_folders:
        base_prefix = base_prefix[:-1] if base_prefix.endswith('/') else base_prefix
        gcs_uri = f"gs://{bucket_name}/{base_prefix}/event_date_part={event_date}/*"
        table_ref = f"{bq_client.project}.{dataset}.{table}"

        #partition_suffix = datetime.strptime(event_date, "%Y-%m-%d").strftime("%Y%m%d")
        #partitioned_table = f"{bq_client.project}.{dataset}.{table}${partition_suffix}"

        # Load job config — no need for time_partitioning field now!
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # or WRITE_APPEND
            #autodetect=True
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="event_date"  
            )
        )

        print(f"Loading files for event_date_part={event_date} from {gcs_uri}")
        load_job = bq_client.load_table_from_uri(
            gcs_uri,
            table_ref,
            job_config=job_config
        )
        load_job.result()
        print(f"Loaded partition: {event_date}")

    
    # Verify
    final_table = bq_client.get_table(table_ref)
    print(f"Loaded total {final_table.num_rows} rows into {table_ref}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_name", required=True)
    parser.add_argument("--base_prefix", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--table", required=True)
    parser.add_argument("--partition_field", required=False)
    args = parser.parse_args()

    for arg, value in vars(args).items():
        logger.info(f"{arg}: {value}")

    load_to_bq(args.bucket_name, args.base_prefix, args.dataset, args.table, args.partition_field)

