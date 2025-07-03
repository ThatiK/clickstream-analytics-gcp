{{ config(materialized='view') }}

with source as (
  select * from {{ source('caec_staging', 'sessionized_events') }}
),

renamed as (
  select
    visitorid as visitor_id,
    event as event_type,
    itemid as item_id,
    transactionid as transaction_id,
    event_time,
    event_ts,
    prev_event_ts,
    new_session,
    session_number,
    session_id,
    event_date
  from source
)

select * from renamed
