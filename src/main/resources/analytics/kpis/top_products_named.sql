CREATE OR REPLACE VIEW `caec_insights.kpi_top_products_named` AS
SELECT
  item_id,
  CASE item_id
    WHEN '461686' THEN 'Wireless Mouse'
    WHEN '119736' THEN 'Noise-Cancelling Headphones'
    WHEN '213834' THEN 'Smartphone Case'
    WHEN '312728' THEN 'Portable Charger'
    WHEN '7943'   THEN 'Bluetooth Speaker'
    WHEN '445351' THEN 'Laptop Stand'
    WHEN '48030'  THEN 'Mechanical Keyboard'
    WHEN '420960' THEN 'Webcam'
    WHEN '248455' THEN 'USB Hub'
    WHEN '17478'  THEN 'LED Desk Lamp'
    ELSE 'Unknown Product'
  END AS product_name,
  purchase_count
FROM `caec_insights.kpi_top_products`;
