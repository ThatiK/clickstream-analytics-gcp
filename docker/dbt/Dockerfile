FROM python:3.10-slim

# Install required packages and DBT dependencies
RUN apt-get update && \
    apt-get install -y git && \
    pip install --no-cache-dir \
        dbt-core==1.9.0 \
        dbt-bigquery==1.9.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/app

# Copy the DBT project files into the image
COPY src/main/resources/dbt/ /usr/app/dbt/

# Set environment variables for DBT
ENV DBT_PROFILES_DIR=/usr/app/dbt/profiles

# Default entrypoint (can be overridden in KubernetesPodOperator or Docker run command)
ENTRYPOINT ["bash", "-c", "while true; do sleep 3600; done"]