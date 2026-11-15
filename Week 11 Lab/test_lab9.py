"""INF1103 Lab 9 — tests for Section 2 (Strategy pattern for order discounts)."""

from supplier import Supplier
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from order import Order
from discount_strategy import PercentageDiscount, BulkDiscount, NoDiscount


def test_strategy_discounts() -> None:
    """Lab 9 Section 2 — Strategy pattern for order discounts."""
    print("\n--- Lab 9 Section 2: Strategy discounts ---")

    # --- strategies in isolation: all share apply(), no isinstance needed ---
    strategies = [
        NoDiscount(),
        PercentageDiscount(10),
        PercentageDiscount(5),          # 5% student discount — no Order change
        BulkDiscount(200, 20),
    ]
    totals = [s.apply(100.0) for s in strategies]
    assert totals == [100.0, 90.0, 95.0, 100.0]   # 100 < 200 → bulk does nothing

    assert BulkDiscount(200, 20).apply(199.99) == 199.99
    assert BulkDiscount(200, 20).apply(200.00) == 180.00
    assert BulkDiscount(200, 20).apply(2475.00) == 2455.00
    assert PercentageDiscount(10).apply(2475.00) == 2475.00 * 0.9

    # --- wired into an Order ---
    supplier = Supplier("SUP-001", "Acme Supplies", "sales@acme.com")
    laptop = PhysicalProduct("P1", "Laptop", 1200.00, 10, 2.5, supplier)
    ebook = DigitalProduct("P2", "Python eBook", 25.00, 999, 12.4, supplier)

    order1 = Order("ORD-1")
    order1.add_order_line(laptop, 2)
    order1.add_order_line(ebook, 3)

    # default strategy is NoDiscount
    assert isinstance(order1.get_discount(), NoDiscount)
    assert order1.calculate_subtotal() == 2475.00
    assert order1.calculate_total() == 2475.00

    order1.set_discount(PercentageDiscount(10))
    print(f"  After 10% off: ${order1.calculate_total():.2f}")
    assert order1.calculate_total() == 2475.00 * 0.9

    order1.set_discount(BulkDiscount(200, 20))
    print(f"  After bulk discount: ${order1.calculate_total():.2f}")
    assert order1.calculate_total() == 2475.00 - 20.00

    order1.set_discount(PercentageDiscount(5))
    print(f"  After 5% student discount: ${order1.calculate_total():.2f}")
    assert order1.calculate_total() == 2475.00 * 0.95

    # a discount can be passed at construction too
    order2 = Order("ORD-2", BulkDiscount(50, 5))
    order2.add_order_line(ebook, 2)                 # subtotal 50.00
    print(f"  order2 with bulk(50,5): ${order2.calculate_total():.2f}")
    assert order2.calculate_total() == 45.00


if __name__ == "__main__":
    test_strategy_discounts()
    print("\nALL CHECKS PASSED")