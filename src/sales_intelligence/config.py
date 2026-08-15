from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
REQUIRED_COLUMNS = {
    "order_id", "order_date", "customer_id", "customer_name", "segment",
    "product_id", "product_name", "category", "region", "salesperson",
    "quantity", "unit_price", "unit_cost", "discount_pct",
}
