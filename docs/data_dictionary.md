# Data Dictionary

All fields are generated from synthetic data. No real companies, customers, or transactions are represented.

| Table | Field | Definition |
|---|---|---|
| `fact_sales` | `order_id` | Unique synthetic order identifier. |
| `fact_sales` | `net_revenue` | Gross revenue less discount amount. |
| `fact_sales` | `gross_profit` | Net revenue less total product cost. |
| `fact_sales` | `discount_pct` | Decimal discount rate from 0 to 1. |
| `dim_customer` | `segment` | Synthetic Enterprise, Mid-Market, or SMB segment. |
| `dim_product` | `category` | Product grouping used for product analysis. |
| `dim_date` | `date_key` | Integer date surrogate key in `YYYYMMDD` format. |

## KPI definitions

| KPI | Formula | Intended use |
|---|---|---|
| Net Revenue | `SUM(fact_sales[net_revenue])` | Revenue after discounts. |
| Gross Profit | `SUM(fact_sales[gross_profit])` | Profit before operating expenses. |
| Profit Margin % | `Gross Profit / Net Revenue` | Product, region, and segment comparison. |
| Average Order Value | `Net Revenue / Orders` | Commercial efficiency signal. |
