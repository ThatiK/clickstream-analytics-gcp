#!/bin/bash

ENV=${1:-dev}

echo ">>> Submitting Spark job for environment: $ENV"
python3 src/main/resources/python/run_clean_clickstream.py $ENV