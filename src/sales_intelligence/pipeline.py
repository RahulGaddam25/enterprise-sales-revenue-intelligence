"""Validate and transform order-level data into a reporting-friendly star schema."""
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date, datetime, timedelta

from .config import PROCESSED_DIR, RAW_DIR, REQUIRED_COLUMNS


class DataQualityError(ValueError):
    """Raised when the input violates the minimum analytical contract."""


def validate_orders(rows: list[dict[str, object]]) -> None:
    if not rows:
        raise DataQualityError("input contains no orders")
    missing = REQUIRED_COLUMNS.difference(rows[0])
    if missing:
        raise DataQualityError(f"Missing required columns: {sorted(missing)}")
    if len({row["order_id"] for row in rows}) != len(rows):
        raise DataQualityError("order_id must be unique")
    for row in rows:
        if any(row.get(key) in (None, "") for key in REQUIRED_COLUMNS):
            raise DataQualityError("input contains null values")
        if any(float(row[key]) < 0 for key in ("quantity", "unit_price", "unit_cost")):
            raise DataQualityError("quantities, prices, and costs must be non-negative")
        if not 0 <= float(row["discount_pct"]) <= 1:
            raise DataQualityError("discount_pct must be between 0 and 1")


def build_star_schema(orders: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    validate_orders(orders)
    staged, customers, products = [], {}, {}
    for source in orders:
        row = dict(source)
        ordered_on = datetime.fromisoformat(str(row["order_date"])).date()
        quantity, price, cost, discount = (float(row[key]) for key in ("quantity", "unit_price", "unit_cost", "discount_pct"))
        gross_revenue = quantity * price
        row.update({"date_key": int(ordered_on.strftime("%Y%m%d")), "gross_revenue": gross_revenue, "discount_amount": gross_revenue * discount, "total_cost": quantity * cost})
        row["net_revenue"] = row["gross_revenue"] - row["discount_amount"]
        row["gross_profit"] = row["net_revenue"] - row["total_cost"]
        staged.append(row)
        customers[str(row["customer_id"])] = {key: row[key] for key in ("customer_id", "customer_name", "segment", "region")}
        products[str(row["product_id"])] = {key: row[key] for key in ("product_id", "product_name", "category", "unit_price", "unit_cost")}
    dates = [datetime.fromisoformat(str(row["order_date"])).date() for row in staged]
    dim_date, current = [], min(dates)
    while current <= max(dates):
        dim_date.append({"date_key": int(current.strftime("%Y%m%d")), "date": current.isoformat(), "year": current.year, "month": current.month, "month_name": current.strftime("%B"), "quarter": f"Q{((current.month - 1) // 3) + 1}"})
        current += timedelta(days=1)
    fact_columns = ("order_id", "date_key", "customer_id", "product_id", "region", "salesperson", "quantity", "unit_price", "unit_cost", "discount_pct", "gross_revenue", "discount_amount", "net_revenue", "total_cost", "gross_profit")
    fact_sales = [{key: row[key] for key in fact_columns} for row in staged]
    dim_customer = sorted(customers.values(), key=lambda row: str(row["customer_id"]))
    dim_product = sorted(products.values(), key=lambda row: str(row["product_id"]))
    return {"dim_date": dim_date, "dim_customer": dim_customer, "dim_product": dim_product, "fact_sales": fact_sales}


def write_schema(schema: dict[str, list[dict[str, object]]]) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for name, rows in schema.items():
        with (PROCESSED_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    with (RAW_DIR / "synthetic_sales_orders.csv").open(newline="", encoding="utf-8") as handle:
        orders = list(csv.DictReader(handle))
    schema = build_star_schema(orders)
    write_schema(schema)
    print("Validated and wrote star-schema CSV files")


if __name__ == "__main__":
    main()
