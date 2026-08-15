import unittest

from sales_intelligence.generate import generate_orders
from sales_intelligence.pipeline import DataQualityError, build_star_schema, validate_orders


class PipelineTest(unittest.TestCase):
    def test_generated_orders_build_a_star_schema(self):
        schema = build_star_schema(generate_orders(rows=20))
        self.assertEqual(set(schema), {"dim_date", "dim_customer", "dim_product", "fact_sales"})
        self.assertEqual(len(schema["fact_sales"]), 20)
        self.assertTrue(all(row["gross_profit"] == row["net_revenue"] - row["total_cost"] for row in schema["fact_sales"]))


    def test_rejects_duplicate_order_ids(self):
        orders = generate_orders(rows=3)
        orders[1]["order_id"] = orders[0]["order_id"]
        with self.assertRaisesRegex(DataQualityError, "unique"):
            validate_orders(orders)


    def test_rejects_invalid_discount(self):
        orders = generate_orders(rows=3)
        orders[0]["discount_pct"] = 1.2
        with self.assertRaisesRegex(DataQualityError, "between"):
            validate_orders(orders)
