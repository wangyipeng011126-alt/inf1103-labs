"""Lab 9 Section 2 — Strategy pattern tests for order discounts."""

from supplier import Supplier
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from order import Order
from discount_strategy import PercentageDiscount, BulkDiscount, NoDiscount


def test_strategy_discounts() -> None:
    supplier = Supplier("SUP-001", "Acme Supplies", "sales@acme.com")
    laptop = PhysicalProduct("P1", "Laptop", 1200.00, 10, 2.5, supplier)
    ebook = DigitalProduct("P2", "Python eBook", 25.00, 999, 12.4, supplier)

    order1 = Order("ORD-1")
    order1.add_order_line(laptop, 2)
    order1.add_order_line(ebook, 3)

    assert isinstance(order1.get_discount(), NoDiscount)
    assert order1.calculate_total() == 2475.00

    order1.set_discount(PercentageDiscount(10))
    assert order1.calculate_total() == 2475.00 * 0.9

    order1.set_discount(BulkDiscount())
    assert order1.calculate_total() == 2475.00 - 20.00

    order1.set_discount(PercentageDiscount(5))
    assert order1.calculate_total() == 2475.00 * 0.95


if __name__ == "__main__":
    test_strategy_discounts()
    print("\nALL DISCOUNT CHECKS PASSED")