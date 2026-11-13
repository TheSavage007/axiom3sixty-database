-- Business questions the Axiom3Sixty database answers.
-- Each query is separated by a "-- name:" tag so scripts and tests can run them one at a time.

-- name: leads_by_city
-- Where is demand coming from?
SELECT city,
       COUNT(*)                                             AS leads,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM leads), 1) AS share_pct
FROM leads
GROUP BY city
ORDER BY leads DESC;

-- name: plan_demand_and_pipeline_value
-- Which floor plans draw the most interest, and what is the open pipeline worth?
SELECT fp.plan_name,
       fp.base_price,
       COUNT(l.lead_id)                                                        AS leads,
       SUM(CASE WHEN l.status = 'won' THEN 1 ELSE 0 END)                       AS won,
       SUM(CASE WHEN l.status IN ('site_visit', 'proposal') THEN fp.base_price ELSE 0 END) AS open_pipeline_value
FROM floor_plans fp
LEFT JOIN leads l ON l.plan_id = fp.plan_id
GROUP BY fp.plan_id
ORDER BY leads DESC;

-- name: funnel
-- How many leads reach each stage?
SELECT status,
       COUNT(*) AS leads,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM leads), 1) AS share_pct
FROM leads
GROUP BY status
ORDER BY CASE status
    WHEN 'new' THEN 1 WHEN 'contacted' THEN 2 WHEN 'site_visit' THEN 3
    WHEN 'proposal' THEN 4 WHEN 'won' THEN 5 WHEN 'lost' THEN 6 END;

-- name: speed_to_lead_by_agent
-- How fast does each agent make first contact?
SELECT u.full_name                                                         AS agent,
       COUNT(*)                                                            AS leads_contacted,
       ROUND(AVG((julianday(l.first_contacted_at) - julianday(l.submitted_at)) * 24), 1) AS avg_hours_to_contact,
       SUM(CASE WHEN (julianday(l.first_contacted_at) - julianday(l.submitted_at)) * 24 <= 24
                THEN 1 ELSE 0 END)                                         AS within_24h
FROM leads l
JOIN app_users u ON u.user_id = l.assigned_user_id
WHERE l.first_contacted_at IS NOT NULL
GROUP BY u.user_id
ORDER BY avg_hours_to_contact;

-- name: win_rate_by_source
-- Which lead source converts best? Closed leads only.
SELECT source,
       SUM(CASE WHEN status = 'won' THEN 1 ELSE 0 END)  AS won,
       SUM(CASE WHEN status = 'lost' THEN 1 ELSE 0 END) AS lost,
       ROUND(100.0 * SUM(CASE WHEN status = 'won' THEN 1 ELSE 0 END)
             / NULLIF(SUM(CASE WHEN status IN ('won', 'lost') THEN 1 ELSE 0 END), 0), 1) AS win_rate_pct
FROM leads
GROUP BY source
ORDER BY win_rate_pct DESC;

-- name: monthly_leads
-- Lead volume by month.
SELECT strftime('%Y-%m', submitted_at) AS month, COUNT(*) AS leads
FROM leads
GROUP BY month
ORDER BY month;

-- name: render_cache_coverage
-- How much of the plan by style by view render grid is cached?
SELECT fp.plan_name,
       COUNT(r.render_id)                                                   AS cached,
       (SELECT COUNT(*) FROM architectural_styles) * (SELECT COUNT(*) FROM render_views) AS possible,
       ROUND(100.0 * COUNT(r.render_id) /
             ((SELECT COUNT(*) FROM architectural_styles) * (SELECT COUNT(*) FROM render_views)), 1) AS coverage_pct
FROM floor_plans fp
LEFT JOIN adu_renders r ON r.plan_id = fp.plan_id
GROUP BY fp.plan_id
ORDER BY coverage_pct DESC;
