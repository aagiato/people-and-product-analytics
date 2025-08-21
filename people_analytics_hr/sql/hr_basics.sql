-- people_analytics_hr/sql/hr_basics.sql
-- Example (DuckDB/SQLite). First create a table named hr from the CSV.

-- Headcount by Department
SELECT Department, COUNT(*) AS headcount
FROM hr
GROUP BY 1
ORDER BY headcount DESC;

-- Attrition by Department
SELECT Department,
       AVG(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS attrition_rate
FROM hr
GROUP BY 1
ORDER BY attrition_rate DESC;
