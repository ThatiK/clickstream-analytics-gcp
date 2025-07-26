CREATE OR REPLACE VIEW `caec_insights.kpi_sessions_by_signup_cohort` AS
WITH user_first_session AS (
  SELECT
    visitor_id,
    MIN(session_start_time) AS first_session_ts
  FROM `caec_analytics.fct_sessions`
  GROUP BY visitor_id
)
SELECT
  DATE(s.session_start_time) AS session_date,
  FORMAT_DATE('%Y-%m', DATE(u.first_session_ts)) AS signup_month,
  COUNT(DISTINCT s.session_id) AS sessions
FROM `caec_analytics.fct_sessions` s
JOIN user_first_session u USING (visitor_id)
GROUP BY session_date, signup_month
ORDER BY session_date, signup_month;
