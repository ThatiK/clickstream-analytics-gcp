# Enter dbt container
docker exec -it caec_dbt /bin/sh

# Run models
dbt run --profile caec_bigquery --project-dir dbt/caec --select stg_sessionized_events
dbt run --profile caec_bigquery --project-dir dbt/caec --select dim_users fct_events
dbt run --profile caec_bigquery --project-dir dbt/caec --select fct_sessions

# Run tests
dbt test --profile caec_bigquery --project-dir dbt/caec --select stg_sessionized_events
dbt test --profile caec_bigquery --project-dir dbt/caec --select dim_users fct_events
dbt test --profile caec_bigquery --project-dir dbt/caec --select fct_sessions

# Generate documentation
dbt docs generate --profile caec_bigquery --project-dir dbt/caec

# Serve docs on alternative port (if 8080 in use)
dbt docs serve --profile caec_bigquery --project-dir dbt/caec --port 8085

OR

cd dbt/caec/target 
python3 -m http.server 8085