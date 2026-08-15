-- PostgreSQL reference schema for loading the generated Power BI-ready CSV files.
CREATE SCHEMA IF NOT EXISTS sales_intelligence;

CREATE TABLE IF NOT EXISTS sales_intelligence.dim_date (
  date_key INTEGER PRIMARY KEY,
  date DATE NOT NULL,
  year SMALLINT NOT NULL,
  month SMALLINT NOT NULL,
  month_name TEXT NOT NULL,
  quarter TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sales_intelligence.dim_customer (
  customer_id TEXT PRIMARY KEY,
  customer_name TEXT NOT NULL,
  segment TEXT NOT NULL,
  region TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sales_intelligence.dim_product (
  product_id TEXT PRIMARY KEY,
  product_name TEXT NOT NULL,
  category TEXT NOT NULL,
  unit_price NUMERIC(12,2) NOT NULL,
  unit_cost NUMERIC(12,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS sales_intelligence.fact_sales (
  order_id TEXT PRIMARY KEY,
  date_key INTEGER NOT NULL REFERENCES sales_intelligence.dim_date(date_key),
  customer_id TEXT NOT NULL REFERENCES sales_intelligence.dim_customer(customer_id),
  product_id TEXT NOT NULL REFERENCES sales_intelligence.dim_product(product_id),
  region TEXT NOT NULL,
  salesperson TEXT NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity >= 0),
  unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
  unit_cost NUMERIC(12,2) NOT NULL CHECK (unit_cost >= 0),
  discount_pct NUMERIC(5,4) NOT NULL CHECK (discount_pct BETWEEN 0 AND 1),
  gross_revenue NUMERIC(14,2) NOT NULL,
  discount_amount NUMERIC(14,2) NOT NULL,
  net_revenue NUMERIC(14,2) NOT NULL,
  total_cost NUMERIC(14,2) NOT NULL,
  gross_profit NUMERIC(14,2) NOT NULL
);
