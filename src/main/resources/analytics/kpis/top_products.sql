CREATE OR REPLACE VIEW `caec_insights.kpi_top_products` AS
SELECT
  item_id,
  COUNT(*) AS purchase_count
FROM `caec_analytics.fct_events`
WHERE event_type = 'transaction'
GROUP BY item_id
ORDER BY purchase_count DESC
LIMIT 10
