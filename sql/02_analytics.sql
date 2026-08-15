-- PostgreSQL analytical queries. All results depend on synthetic project data.

-- Monthly revenue, prior month, and month-over-month growth.
WITH monthly AS (
  SELECT d.year, d.month, date_trunc('month', d.date)::date AS month_start,
         SUM(f.net_revenue) AS net_revenue, SUM(f.gross_profit) AS gross_profit
  FROM sales_intelligence.fact_sales f JOIN sales_intelligence.dim_date d USING (date_key)
  GROUP BY d.year, d.month, date_trunc('month', d.date)
)
SELECT *, LAG(net_revenue) OVER (ORDER BY month_start) AS prior_month_revenue,
       ROUND(100 * (net_revenue / NULLIF(LAG(net_revenue) OVER (ORDER BY month_start), 0) - 1), 2) AS mom_growth_pct
FROM monthly ORDER BY month_start;

-- Customer segmentation and revenue ranking within each segment.
WITH customer_revenue AS (
  SELECT c.segment, c.customer_id, c.customer_name, SUM(f.net_revenue) AS net_revenue
  FROM sales_intelligence.fact_sales f JOIN sales_intelligence.dim_customer c USING (customer_id)
  GROUP BY c.segment, c.customer_id, c.customer_name
)
SELECT *, DENSE_RANK() OVER (PARTITION BY segment ORDER BY net_revenue DESC) AS revenue_rank
FROM customer_revenue ORDER BY segment, revenue_rank;

-- Product profitability and running cumulative revenue.
WITH product_profitability AS (
  SELECT p.category, p.product_name, SUM(f.net_revenue) AS net_revenue, SUM(f.gross_profit) AS gross_profit
  FROM sales_intelligence.fact_sales f JOIN sales_intelligence.dim_product p USING (product_id)
  GROUP BY p.category, p.product_name
)
SELECT *, ROUND(100 * gross_profit / NULLIF(net_revenue, 0), 2) AS margin_pct,
       SUM(net_revenue) OVER (ORDER BY net_revenue DESC) AS cumulative_revenue
FROM product_profitability ORDER BY net_revenue DESC;

-- Cohort retention proxy: active customers by their first purchase month.
WITH first_purchase AS (
  SELECT customer_id, MIN(date_key) AS first_date_key FROM sales_intelligence.fact_sales GROUP BY customer_id
), activity AS (
  SELECT d.year || '-' || LPAD(d.month::text, 2, '0') AS activity_month,
         fd.year || '-' || LPAD(fd.month::text, 2, '0') AS cohort_month,
         f.customer_id
  FROM sales_intelligence.fact_sales f
  JOIN sales_intelligence.dim_date d USING (date_key)
  JOIN first_purchase fp USING (customer_id)
  JOIN sales_intelligence.dim_date fd ON fd.date_key = fp.first_date_key
)
SELECT cohort_month, activity_month, COUNT(DISTINCT customer_id) AS active_customers
FROM activity GROUP BY cohort_month, activity_month ORDER BY cohort_month, activity_month;
