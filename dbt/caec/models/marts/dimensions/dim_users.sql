{{ config(materialized='table') }}

with base as (
  select distinct
    visitor_id
  from {{ ref('stg_sessionized_events') }}
)

select
  visitor_id,
  md5(visitor_id) as user_key,  -- optional surrogate key
  current_timestamp() as created_at
from base
