"""Generate deterministic, explicitly synthetic sales data for local analysis."""
from __future__ import annotations

import csv
import random
from datetime import date, timedelta

from .config import RAW_DIR

REGIONS = ["North", "South", "East", "West"]
SEGMENTS = ["Enterprise", "Mid-Market", "SMB"]
CATEGORIES = {"P100": ("Analytics Suite", "Software", 900.0, 320.0), "P200": ("Data Platform", "Software", 1450.0, 610.0), "P300": ("Support Package", "Services", 380.0, 130.0), "P400": ("BI Connector", "Software", 240.0, 70.0)}


def generate_orders(rows: int = 2500, seed: int = 42) -> list[dict[str, object]]:
    """Create a repeatable order-level dataset with no real people or companies."""
    rng = random.Random(seed)
    start = date(2023, 1, 1)
    records = []
    for index in range(rows):
        product_id = rng.choice(list(CATEGORIES))
        product_name, category, price, cost = CATEGORIES[product_id]
        order_date = start + timedelta(days=rng.randrange(730))
        quantity = rng.randint(1, 12)
        discount = rng.choice([0.0, 0.0, 0.05, 0.1, 0.15])
        records.append({
            "order_id": f"ORD-{index + 1:06d}", "order_date": order_date.isoformat(),
            "customer_id": f"CUST-{rng.randint(1, 180):04d}", "customer_name": f"Synthetic Customer {rng.randint(1, 180):03d}",
            "segment": rng.choice(SEGMENTS), "product_id": product_id, "product_name": product_name,
            "category": category, "region": rng.choice(REGIONS), "salesperson": f"Rep {rng.randint(1, 18):02d}",
            "quantity": quantity, "unit_price": price, "unit_cost": cost, "discount_pct": discount,
        })
    return records


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output = RAW_DIR / "synthetic_sales_orders.csv"
    records = generate_orders()
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote synthetic data to {output}")


if __name__ == "__main__":
    main()
