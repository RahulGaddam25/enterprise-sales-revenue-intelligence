"""Reusable KPI and customer-analysis functions used by notebooks or reporting tools."""
from __future__ import annotations

from collections import defaultdict


def kpi_summary(fact_sales: list[dict[str, object]]) -> dict[str, float | int]:
    revenue = sum(float(row["net_revenue"]) for row in fact_sales)
    profit = sum(float(row["gross_profit"]) for row in fact_sales)
    return {"net_revenue": revenue, "gross_profit": profit, "orders": len({row["order_id"] for row in fact_sales}), "customers": len({row["customer_id"] for row in fact_sales}), "profit_margin_pct": profit / revenue}


def revenue_by_dimension(fact_sales: list[dict[str, object]], dimension: str) -> list[dict[str, object]]:
    groups: dict[object, dict[str, object]] = defaultdict(lambda: {"net_revenue": 0.0, "gross_profit": 0.0, "orders": set()})
    for row in fact_sales:
        group = groups[row[dimension]]
        group["net_revenue"] += float(row["net_revenue"])
        group["gross_profit"] += float(row["gross_profit"])
        group["orders"].add(row["order_id"])
    return sorted(({dimension: key, "net_revenue": value["net_revenue"], "gross_profit": value["gross_profit"], "orders": len(value["orders"])} for key, value in groups.items()), key=lambda row: float(row["net_revenue"]), reverse=True)
