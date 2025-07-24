{{ config(
    materialized='incremental',
    partition_by={'field': 'event_date', 'data_type': 'date'},
    incremental_strategy='insert_overwrite',
    cluster_by=['visitor_id']
) }}

with events as (
  select *
  from {{ ref('stg_sessionized_events') }}
)

select
  event_time,
  event_date,
  visitor_id,
  event_type,
  item_id,
  transaction_id,
  session_id,
  session_number,
  new_session,
  event_ts,
  prev_event_ts
from events
{% if is_incremental() %}
where event_date >= date_sub(current_date(), interval 2 day)  
{% endif %}
