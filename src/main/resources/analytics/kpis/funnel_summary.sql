CREATE OR REPLACE VIEW `caec_insights.kpi_funnel_summary` AS
WITH steps AS (
  SELECT
    session_id,
    MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS seen_view,
    MAX(CASE WHEN event_type = 'addtocart' THEN 1 ELSE 0 END) AS seen_cart,
    MAX(CASE WHEN event_type = 'transaction' THEN 1 ELSE 0 END) AS seen_txn
  FROM `caec_analytics.fct_events`
  GROUP BY session_id
),
funnel AS (
  SELECT 'view' AS event_type, COUNTIF(seen_view = 1) AS sessions FROM steps
  UNION ALL
  SELECT 'addtocart', COUNTIF(seen_cart = 1) FROM steps
  UNION ALL
  SELECT 'transaction', COUNTIF(seen_txn = 1) FROM steps
)
SELECT
  f.event_type,
  l.display_name,
  f.sessions
FROM funnel f
JOIN `caec_insights.event_type_lookup` l
  ON f.event_type = l.event_type;
