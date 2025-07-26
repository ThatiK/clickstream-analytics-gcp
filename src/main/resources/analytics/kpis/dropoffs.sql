CREATE OR REPLACE VIEW `caec_insights.kpi_dropoff_funnel` AS
SELECT
  stage,
  COUNT(DISTINCT session_id) AS sessions
FROM (
  SELECT
    session_id,
    event_type,
    CASE
      WHEN event_type = 'view' THEN '1_view'
      WHEN event_type = 'addtocart' THEN '2_addtocart'
      WHEN event_type = 'transaction' THEN '3_purchase'
    END AS stage
  FROM `caec_analytics.fct_events`
)
WHERE stage IS NOT NULL
GROUP BY stage
ORDER BY stage
