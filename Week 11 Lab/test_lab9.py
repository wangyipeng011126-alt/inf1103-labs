"""INF1103 Lab 9 — tests for Sections 2 (Strategy) and 3 (Factory)."""

from supplier import Supplier
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from subscription_product import SubscriptionProduct
from order import Order
from discount_strategy import (
    PercentageDiscount, BulkDiscount, NoDiscount, StudentDiscount,
)
from product_factory import ProductFactory


def test_strategy_discounts() -> None:
    """Lab 9 Section 2 — Strategy pattern for order discounts."""
    print("\n--- Lab 9 Section 2: Strategy discounts ---")

    # --- strategies in isolation: all share apply(), no isinstance needed ---
    strategies = [
        NoDiscount(),
        PercentageDiscount(10),
        PercentageDiscount(5),
        BulkDiscount(200, 20),
        StudentDiscount("S1234567"),
    ]
    totals = [s.apply(100.0) for s in strategies]
    assert totals == [100.0, 90.0, 95.0, 100.0, 95.0]
    assert StudentDiscount("S1234567").apply(200.0) == 190.0

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

    # --- Section 2.3 predict-first: subtotal 250 ---
    widget = PhysicalProduct("P9", "Widget", 125.00, 10, 1.0, supplier)
    order3 = Order("ORD-3", BulkDiscount(200, 20))
    order3.add_order_line(widget, 2)                # subtotal 250.00

    # predict: 250 >= 200 → 250 - 20 = 230.0
    print(f"  order3 bulk(200,20): ${order3.calculate_total():.2f}")
    assert order3.calculate_total() == 230.0

    order3.set_discount(PercentageDiscount(10))
    # predict: 250 * 0.9 = 225.0
    print(f"  order3 after 10% off: ${order3.calculate_total():.2f}")
    assert order3.calculate_total() == 225.0

    # --- Section 2.4: fourth strategy, Order unchanged ---
    print("\n--- Lab 9 Section 2.4: StudentDiscount (extend, don't modify) ---")
    order4 = Order("ORD-4", StudentDiscount("S1234567"))
    order4.add_order_line(widget, 2)                # subtotal 250.00
    print(f"  order4 student discount: ${order4.calculate_total():.2f}")
    assert order4.calculate_total() == 250.0 * 0.95

    # invalid ID is rejected at construction, not inside Order
    try:
        StudentDiscount("   ")
        assert False, "blank student ID should raise ValueError"
    except ValueError:
        pass

    # Section 2.4 predict-first: Order 1 — 0..* DiscountStrategy (association)
    shared = PercentageDiscount(10)
    order_a = Order("ORD-A", shared)
    order_b = Order("ORD-B", shared)
    assert order_a.get_discount() is order_b.get_discount()
    assert order_a.get_discount() is shared
    print("  shared discount object across orders: True (association)")


def test_product_factory() -> None:
    """Lab 9 Section 3 — ProductFactory centralises creation."""
    print("\n--- Lab 9 Section 3: ProductFactory ---")
    supplier = Supplier("SUP-001", "Acme Supplies", "sales@acme.com")

    physical = ProductFactory.create(
        "physical", "P1", "Laptop", 1200.00, 10, supplier, weight=2.5,
    )
    digital = ProductFactory.create(
        "digital", "P2", "Python eBook", 25.00, 999, supplier,
        download_size=12.4,
    )
    subscription = ProductFactory.create(
        "subscription", "P3", "Pro Plan", 15.00, 100, supplier,
        billing_period="monthly",
    )

    # factory returns the right subclass...
    assert isinstance(physical, PhysicalProduct)
    assert isinstance(digital, DigitalProduct)
    assert isinstance(subscription, SubscriptionProduct)

    # ...but callers use them only through Product (polymorphism)
    for product in (physical, digital, subscription):
        assert product.get_product_id()
        assert product.get_fulfilment_info() != ""

    # unknown type → ValueError from factory's else branch
    try:
        ProductFactory.create("service", "P4", "X", 1.0, 1, supplier)
        assert False, "expected ValueError for unknown type"
    except ValueError as error:
        assert "Unknown product type: service" in str(error)
        print(f"  unknown type rejected: {error}")

    # missing type-specific field → clear ValueError, not TypeError
    try:
        ProductFactory.create("physical", "P5", "Y", 1.0, 1, supplier)
        assert False, "expected ValueError for missing weight"
    except ValueError as error:
        assert "weight" in str(error)
        print(f"  missing field rejected: {error}")

    # case/whitespace handling
    upper = ProductFactory.create(
        "  DIGITAL ", "P6", "Z", 1.0, 1, supplier, download_size=1.0,
    )
    assert isinstance(upper, DigitalProduct)


if __name__ == "__main__":
    test_strategy_discounts()
    test_product_factory()
    print("\nALL CHECKS PASSED")