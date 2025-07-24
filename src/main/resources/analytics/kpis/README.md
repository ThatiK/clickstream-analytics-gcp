# KPI Definitions – CAEC Analytics

This folder contains SQL logic for key performance indicators (KPIs) derived from the curated CAEC dataset (`caec_analytics`). These KPIs are designed to support business insights and visualization use cases.

## Dataset Source
All KPIs are generated using the following tables provided by the data engineering team:
- `caec_analytics.fct_events`
- `caec_analytics.fct_sessions`
- `caec_analytics.dim_users`

## KPIs Included

### 1. Conversion Rate (`conversion_rate.sql`)
Calculates the ratio of sessions that led to at least one purchase event.

**Formula**:  
`Conversion Rate = Sessions with purchase / Total sessions`

**Use Case**: Understand overall user behavior and session quality.

---

### 2. Top Products (`top_products.sql`)
Identifies the top 10 products based on the number of purchases (by `itemid`).

**Formula**:  
`Top Products = itemid with highest count of 'purchase' events`

**Note**: Since product names are not available in the source dataset, itemids are used as identifiers. Static labels may be added for presentation purposes.

**Use Case**: Determine which products are most frequently purchased.

---

### 3. Drop-off Points (`dropoffs.sql`)
Breaks down the number of sessions reaching each funnel stage: view, add-to-cart, and purchase.

**Stages**:
- View → Add to Cart → Purchase

**Use Case**: Identify where users disengage in the purchase funnel.

---

## Notes
- All queries are intended to run in BigQuery.
- These queries can be used directly for visualization in Looker Studio.
- Static mappings or friendly labels may be added later for demo dashboards.