CREATE OR REPLACE VIEW `caec_insights.event_type_lookup` AS
SELECT * FROM UNNEST([
  STRUCT('view' AS event_type,        'Page View' AS display_name),
  STRUCT('addtocart' AS event_type,   'Added to Cart' AS display_name),
  STRUCT('transaction' AS event_type, 'Completed Transaction' AS display_name)
]);
