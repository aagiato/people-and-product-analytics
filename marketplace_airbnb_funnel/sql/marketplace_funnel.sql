-- marketplace_airbnb_funnel/sql/marketplace_funnel.sql
WITH staged AS (
  SELECT * FROM airbnb_events -- replace with your staged union
),
by_user AS (
  SELECT user_id,
         MIN(CASE WHEN event='signup' THEN ts END) AS t_signup,
         MIN(CASE WHEN event='search' THEN ts END) AS t_search,
         MIN(CASE WHEN event='view'   THEN ts END) AS t_view,
         MIN(CASE WHEN event='book'   THEN ts END) AS t_book
  FROM staged
  GROUP BY 1
)
SELECT
  SUM(CASE WHEN t_signup IS NOT NULL THEN 1 ELSE 0 END) AS signups,
  SUM(CASE WHEN t_search IS NOT NULL THEN 1 ELSE 0 END) AS searches,
  SUM(CASE WHEN t_view   IS NOT NULL THEN 1 ELSE 0 END) AS views,
  SUM(CASE WHEN t_book   IS NOT NULL THEN 1 ELSE 0 END) AS bookings
FROM by_user;
