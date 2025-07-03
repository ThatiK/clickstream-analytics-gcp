{{ config(
    materialized='incremental',
    partition_by={'field': 'session_start_date', 'data_type': 'date'},
    incremental_strategy='insert_overwrite'
) }}

with events as (
  select *
  from {{ ref('stg_sessionized_events') }}
),

session_metrics as (
  select
    session_id,
    visitor_id,
    min(event_time) as session_start_time,
    max(event_time) as session_end_time,
    count(*) as event_count,
    array_agg(event_type order by event_time limit 1)[safe_offset(0)] as first_event,
    array_agg(event_type order by event_time desc limit 1)[safe_offset(0)] as last_event
  from events
  group by session_id, visitor_id
)

select
  *,
  date(session_start_time) as session_start_date
from session_metrics
