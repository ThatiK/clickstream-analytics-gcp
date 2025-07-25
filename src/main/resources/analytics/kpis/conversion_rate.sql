CREATE OR REPLACE VIEW `caec_insights.kpi_conversion_rate` AS
SELECT
  COUNTIF(has_purchase) / COUNT(*) AS conversion_rate
FROM (
  SELECT
    session_id,
    COUNTIF(event_type = 'transaction') > 0 AS has_purchase
  FROM `caec_analytics.fct_events`
  GROUP BY session_id
);
