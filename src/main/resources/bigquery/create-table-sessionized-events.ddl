CREATE OR REPLACE TABLE `caec_staging.sessionized_events`
(
  visitorid STRING,
  event STRING,
  itemid STRING,
  transactionid STRING,
  event_time TIMESTAMP,
  event_ts INT64,
  prev_event_ts INT64,
  new_session INT64,
  session_number INT64,
  session_id STRING,
  event_date DATE
)
PARTITION BY event_date;