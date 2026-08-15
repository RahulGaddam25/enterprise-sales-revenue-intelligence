# Architecture and Operating Notes

The project is intentionally local-first and uses synthetic data. The pipeline has no external services, credentials, or deployment claims.

1. `generate.py` creates deterministic synthetic order-level data.
2. `pipeline.py` validates the contractual columns, duplicate keys, nulls, numeric values, and discounts.
3. The same pipeline writes a date, customer, product, and sales fact CSV model.
4. PostgreSQL DDL and analytical SQL document a production-style relational loading target.
5. Power BI can import the processed CSVs and apply the provided DAX measures.

## Security considerations

- No credentials are committed; `.env` is ignored and `.env.example` is non-secret.
- Generated data is synthetic and safe to share.
- Database loading is optional; use a least-privilege, non-production database account.
- SQL scripts contain read-only analytical queries after schema creation.

## Dashboard concept

- **Executive overview:** net revenue, profit, orders, customers, and MoM trend.
- **Sales:** revenue by salesperson and order value distribution.
- **Customer:** segment performance and cohort retention proxy.
- **Product:** revenue, gross profit, and margin by product/category.
- **Region:** net revenue, profit margin, and rankings by region.
