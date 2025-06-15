import configparser
import subprocess
import os
import sys
import logging

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

def submit_spark_job(env="dev"):
    props, base_dir = load_config(env)

    spark_script_path = os.path.join(base_dir, "spark", "sessionize_clickstream.py")

    spark_submit_cmd = [
        "spark-submit",
        "--master", props["SPARK"]["master"],
        spark_script_path,
        props["PATHS"]["clean_events"],
        props["PATHS"]["sessionized_events"],
        props["SETTINGS"]["session_gap_minutes"]
    ]

    logger.info("Launching Spark Job")
    logger.info(" ".join(spark_submit_cmd))
    
    subprocess.run(spark_submit_cmd, check=True)

    logger.info("Completed Spark Job")

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    logger.info("ENV: {}".format("env"))

    submit_spark_job(env)
