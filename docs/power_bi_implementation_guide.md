# Power BI Implementation Guide

## Scope and truthfulness

This guide creates a genuine report from the project's generated CSV files. A `.pbix` file is **not** included because Power BI Desktop is not available in this development environment. All resulting visuals and measures use synthetic portfolio data, not real commercial outcomes.

## 1. Generate the report inputs

```bash
PYTHONPATH=src python -m sales_intelligence.generate
PYTHONPATH=src python -m sales_intelligence.pipeline
```

Import these files from `data/processed/`: `fact_sales.csv`, `dim_date.csv`, `dim_customer.csv`, and `dim_product.csv`.

## 2. Import and type the data

In **Power BI Desktop → Get data → Text/CSV**, import every file. Set `date_key` fields to Whole number; set `dim_date[date]` to Date; use Decimal number for revenue, cost, profit, price, and discount fields. Mark `dim_date` as the date table using `dim_date[date]`.

## 3. Create the model relationships

Use **one-to-many** relationships with **single** filter direction from dimensions to `fact_sales`:

| From | To | Cardinality | Direction |
|---|---|---|---|
| `dim_date[date_key]` | `fact_sales[date_key]` | One-to-many | Single |
| `dim_customer[customer_id]` | `fact_sales[customer_id]` | One-to-many | Single |
| `dim_product[product_id]` | `fact_sales[product_id]` | One-to-many | Single |

`region` is intentionally retained in `fact_sales` in the current schema; use `fact_sales[region]` for regional visual axes and slicers. Do not invent a region dimension unless the pipeline is extended to create one.

## 4. Add measures

Copy the definitions from [`powerbi/measures.dax`](../powerbi/measures.dax). Format revenue/profit/cost/AOV as currency, margin/growth as percentages, and orders/customers/ranks as whole numbers. Growth measures return blank where no comparison period exists; this avoids artificial zero-growth values.

## 5. Build report pages

### Executive Overview

- Cards: Total Revenue, Total Profit, Total Orders, Total Customers, Average Order Value, Profit Margin %, Revenue YoY Growth %.
- Line chart: `dim_date[date]` by Total Revenue.
- Clustered bar chart: `fact_sales[region]` by Total Revenue and Total Profit.
- Slicers: `dim_date[year]`, `dim_customer[segment]`, and `fact_sales[region]`.

### Sales Analysis

- Line and clustered column chart: `dim_date[date]` with Total Revenue and Order Volume.
- Line chart: `dim_date[date]` by Revenue MoM Growth %.
- Matrix: `fact_sales[salesperson]` with Total Revenue, Total Orders, Average Order Value, and Total Profit.

### Customer Analysis

- Donut chart: `dim_customer[segment]` by Total Revenue.
- Table: `dim_customer[customer_name]`, Total Revenue, Total Orders, Customer Average Order Value, Customer Revenue Rank.
- Apply a visual-level Top N filter of 10 by Total Revenue for top customers.
- Line chart: `dim_date[date]` by Active Customers.

### Product Analysis

- Bar chart: `dim_product[product_name]` by Total Revenue; apply Top N 10 by Total Revenue.
- Matrix: `dim_product[category]`, `dim_product[product_name]`, Total Revenue, Total Profit, Product Profit Margin %, Product Revenue Rank.
- Treemap: `dim_product[category]` by Total Revenue.

### Regional Analysis

- Filled map or bar chart: `fact_sales[region]` by Total Revenue.
- Clustered bar chart: `fact_sales[region]` by Total Profit.
- Matrix: `fact_sales[region]` with Total Revenue, Total Profit, Profit Margin %, Regional MoM Growth %, and Regional Revenue Rank.

## 6. Quality checks before publishing a report

1. Confirm the three relationships are active and single-directional.
2. Confirm cards respond to year, segment, and region slicers.
3. Reconcile Total Revenue and Total Profit with totals from `fact_sales.csv`.
4. Confirm rankings sort by the intended rank/measure.
5. Do not label synthetic values as company, customer, or production results.

## Limitations

- No Power BI `.pbix` exists in this repository.
- Data is regenerated locally and must be refreshed manually in Power BI.
- Region is intentionally denormalized in the implemented fact table.
- The project does not claim a live dashboard, scheduled refresh, gateway, or cloud deployment.
