# KPI Definitions – CAEC Insights Module

This folder contains BigQuery SQL definitions for key performance indicators (KPIs) used to analyze user behavior in the CAEC clickstream dataset. These views power the Looker Studio dashboard available in the project root.

## Source Datasets

All KPIs are derived from the curated `caec_analytics` dataset, which includes:
- `fct_events`: raw event-level interactions (e.g., view, add-to-cart, transaction)
- `fct_sessions`: session-level metadata (e.g., start/end time)
- `dim_users`: user-level identifiers

## Defined KPI Views

### `kpi_conversion_rate`
Calculates the percentage of sessions that included a purchase.

### `kpi_top_products`
Lists the top 10 products based on number of transactions (`item_id` only).

### `kpi_top_products_named`
Maps top `item_id`s to mock-friendly product names (e.g., "Wireless Mouse").

### `kpi_dropoff_funnel`
Counts how many sessions reached each funnel stage (view, cart, purchase).

### `kpi_funnel_summary`
Same funnel logic but joined with `event_type_lookup` for display name support.

### `event_type_lookup`
Lookup table mapping raw event types to friendly labels used across the dashboard.

### `kpi_event_volume_by_type`
Daily count of each event type (e.g., views, carts, transactions) for trend analysis.

### `kpi_sessions_by_signup_cohort`
Trends of session activity over time, grouped by signup month (first session).

## Where These Are Used

These views directly support visualizations in the final dashboard:
[`docs/looker/CAEC_Dashboard.pdf`](../../../../../docs/looker/CAEC_Dashboard.pdf)

The dashboard was built in Looker Studio, connected only to `caec_insights` views to ensure clean governance and separation from raw data.

## Notes

- All SQL is BigQuery Standard SQL.
- View names are prefixed with `caec_insights.` for semantic separation.
- The dashboard uses friendly names (`display_name`) instead of raw codes wherever applicable.
