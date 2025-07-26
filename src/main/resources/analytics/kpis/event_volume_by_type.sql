CREATE OR REPLACE VIEW `caec_insights.kpi_event_volume_by_type` AS
SELECT
  event_date,
  e.event_type,
  l.display_name,
  COUNT(*) AS event_count
FROM `caec_analytics.fct_events` e
JOIN `caec_insights.event_type_lookup` l
  ON e.event_type = l.event_type
GROUP BY event_date, e.event_type, l.display_name
ORDER BY event_date, display_name;