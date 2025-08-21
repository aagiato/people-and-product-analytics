-- product_ab_cookiecats/sql/ab_funnel.sql
-- Sketch of a variant funnel using window functions.
WITH events AS (
  SELECT * FROM cookie_cats_events
),
by_user AS (
  SELECT user_id,
         MIN(CASE WHEN event='install' THEN ts END) AS t_install,
         MIN(CASE WHEN event='level2'  THEN ts END) AS t_level2,
         MIN(CASE WHEN event='levelX'  THEN ts END) AS t_levelx,
         variant
  FROM events
  GROUP BY 1, variant
)
SELECT variant,
       SUM(CASE WHEN t_install IS NOT NULL THEN 1 ELSE 0 END) AS installs,
       SUM(CASE WHEN t_level2  IS NOT NULL THEN 1 ELSE 0 END) AS level2,
       SUM(CASE WHEN t_levelx  IS NOT NULL THEN 1 ELSE 0 END) AS levelx
FROM by_user
GROUP BY 1;
