# CAEC Looker Studio Dashboard (PDF Export)

This PDF contains the final Looker Studio dashboard for the CAEC Clickstream Analytics project.

File: `CAEC_Dashboard.pdf`  
Data Window: 3 May 2015 – 18 Sept 2015  
Tool: Google Looker Studio  
Built using: `caec_insights` BigQuery views

## Dashboard Structure

1. **User Engagement Over Time**  
   Daily active sessions (time-series trend)

2. **Event Behavior Breakdown by Type**  
   Page views, add-to-cart, and completed transactions

3. **Funnel Drop-off Summary**  
   Session counts reaching each step in the funnel

4. **Top 10 Purchased Products**  
   Display-friendly product names mapped to item_ids

5. **Cohort Activity Over Time**  
   Session behavior by signup month

## Filters Included

- Date Range
- Event Type (with friendly labels)
- Signup Month (for cohort analysis)

## Related SQL Definitions

All SQL logic powering this dashboard is stored in  
[`src/main/resources/analytics/kpis/`](../../src/main/resources/analytics/kpis/)

