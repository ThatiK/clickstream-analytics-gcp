SELECT
  itemid,
  COUNT(*) AS purchase_count
FROM `caec_analytics.fct_events`
WHERE event_type = 'transaction'
GROUP BY itemid
ORDER BY purchase_count DESC
LIMIT 10
