import configparser
import subprocess
import os
import sys
import logging
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
logger.addHandler(handler)

def load_config(env="dev"):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Points to src/main/resources
    config_path = os.path.join(base_dir, "etc", f"{env}.properties")
    logger.info("Reading config from {}".format(config_path))

    config = configparser.ConfigParser()
    config.read(config_path)
    return config, base_dir

def generate_timestamped_batch_name(base_name):
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}-{ts}"

def submit_spark_job(env="dev"):
    props, base_dir = load_config(env)

    spark_script_path = os.path.join(base_dir, "spark", "clean_clickstream.py")
    input_path = props["PATHS"]["raw_events"]
    output_path = props["PATHS"]["clean_events"]
    command_type = props["COMMON"]["submit_command"]

    if command_type == "gcloud":
        base_batch_name = "caec-clean-clickstream"
        batch_name = generate_timestamped_batch_name(base_batch_name)

        spark_submit_cmd = [
            "gcloud", "dataproc", "batches", "submit", "pyspark", spark_script_path,
            "--region", props["SPARK"]["region"],
            "--batch", batch_name,
            "--deps-bucket", f"gs://{props["SPARK"]['bucket']}",
            "--version", props["SPARK"]["version"],
            "--",
            f"--input-path={input_path}",
            f"--output-path={output_path}"
        ]
    elif command_type == "spark-submit":
        spark_submit_cmd = [
            "spark-submit", 
            "--master", "local[*]",
            spark_script_path,
            f"--input-path={input_path}",
            f"--output-path={output_path}"
        ]
    else:
        raise ValueError(f"Unsupported submit_command: {command_type}")


    logger.info("Launching Spark Job")
    logger.info(" ".join(spark_submit_cmd))
    
    subprocess.run(spark_submit_cmd, check=True)

    logger.info("Completed Spark Job")

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    logger.info("ENV: {}".format("env"))

    submit_spark_job(env)
