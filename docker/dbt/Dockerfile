FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y git && \
    pip install --no-cache-dir \
        dbt-core==1.9.0 \
        dbt-bigquery==1.9.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app
ENTRYPOINT ["bash", "-c", "while true; do sleep 3600; done"]