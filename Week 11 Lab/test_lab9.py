"""INF1103 Lab 9 — Automated tests covering Sections 2, 3, 4, 5, and 7."""

import os
import csv
import tempfile
from unittest.mock import patch

from supplier import Supplier
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from subscription_product import SubscriptionProduct
from inventory import Inventory
from order import Order
from discount_strategy import (
    PercentageDiscount, BulkDiscount, NoDiscount, StudentDiscount,
)
from product_factory import ProductFactory
from main import load_products, get_positive_float, get_non_negative_int


def test_strategy_discounts() -> None:
    """Lab 9 Section 2 & 7.1-7.3 — Strategy pattern and Order delegation."""
    print("\n--- Lab 9 Section 2 & 7: Strategy discounts ---")
    supplier = Supplier("SUP-001", "Acme Supplies", "sales@acme.com")
    laptop = PhysicalProduct("P1", "Laptop", 1200.00, 10, 2.5, supplier)
    ebook = DigitalProduct("P2", "Python eBook", 25.00, 999, 12.4, supplier)

    order1 = Order("ORD-1")
    order1.add_order_line(laptop, 2)
    order1.add_order_line(ebook, 3)

    # 7.1 Order calculates totals through a DiscountStrategy
    # 7.3 The strategy on an existing order can be changed with set_discount()
    assert isinstance(order1.get_discount(), NoDiscount)
    assert order1.calculate_total() == 2475.00

    order1.set_discount(PercentageDiscount(10))
    assert order1.calculate_total() == 2475.00 * 0.9

    # 7.2 A new discount strategy (StudentDiscount) added without changing Order
    order1.set_discount(StudentDiscount("S1234567"))
    assert order1.calculate_total() == 2475.00 * 0.95
    
    order1.set_discount(BulkDiscount(200, 20))
    assert order1.calculate_total() == 2475.00 - 20.00
    print("  Order delegates to strategies correctly.")


def test_product_factory() -> None:
    """Lab 9 Section 3 & 7.4-7.5 — Factory pattern."""
    print("\n--- Lab 9 Section 3 & 7: ProductFactory ---")
    supplier = Supplier("SUP-001", "Acme Supplies", "sales@acme.com")

    # 7.4 Products are created through ProductFactory rather than directly
    physical = ProductFactory.create("physical", "P1", "Laptop", 1200.00, 10, supplier, weight=2.5)
    assert isinstance(physical, PhysicalProduct)

    # 7.5 An unknown product type raises a ValueError with a clear message
    try:
        ProductFactory.create("service", "P4", "X", 1.0, 1, supplier)
        assert False, "Should have raised ValueError"
    except ValueError as error:
        assert "Unknown product type: service" in str(error)
    print("  Factory creates products and rejects unknown types.")


def test_validation() -> None:
    """Lab 9 Section 4 & 7.6 — Validation rules owned by classes."""
    print("\n--- Lab 9 Section 4 & 7: Validation ---")
    supplier = Supplier("SUP-001", "Acme Supplies", "sales@acme.com")

    # 7.6 Invalid prices, stock quantities and order quantities are rejected
    try:
        PhysicalProduct("P1", "X", -5.0, 1, 1.0, supplier) # Bad price
        assert False
    except ValueError as e:
        assert "Price" in str(e)

    try:
        DigitalProduct("P2", "X", 1.0, -1, 1.0, supplier) # Bad stock
        assert False
    except ValueError as e:
        assert "Stock" in str(e)

    try:
        OrderLine(PhysicalProduct("P3", "X", 1.0, 1, 1.0, supplier), 0) # Bad quantity
        assert False
    except ValueError as e:
        assert "Quantity" in str(e)
    print("  Validation rules reject bad data.")


def test_exception_handling() -> None:
    """Lab 9 Section 5 & 7.7-7.10 — Graceful error handling."""
    print("\n--- Lab 9 Section 5 & 7: Exception handling ---")
    supplier = Supplier("SUP-001", "Acme Supplies", "sales@acme.com")

    # 7.7 Invalid user input is handled without crashing, and the user is asked again
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
        assert get_positive_float("Price: ") == 12.5

    # 7.8 A missing products file is handled gracefully
    inv = Inventory()
    load_products("does-not-exist.csv", inv, supplier)
    assert len(inv.get_products()) == 0

    # 7.9 Bad rows in the products file are reported and skipped, and valid rows still load
    rows = [
        ["product_type", "product_id", "name", "price", "stock_quantity"],
        ["physical", "P001", "Desk Lamp", "25.00", "10"],
        ["service", "S001", "Installation", "30.00", "5"],   # Bad type
        ["physical", "P002", "Office Chair", "abc", "3"],    # Bad price
        ["physical", "P003", "Monitor Stand", "39.50", "7"],
    ]
    fd, path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "w", newline="") as f:
            csv.writer(f).writerows(rows)
        
        inv = Inventory()
        load_products(path, inv, supplier)
        assert len(inv.get_products()) == 2  # P001 and P003 loaded successfully
    finally:
        os.unlink(path)
    print("  Exceptions handled gracefully; bad rows skipped.")


if __name__ == "__main__":
    # Fix missing import for OrderLine in test_validation
    from orderline import OrderLine
    
    test_strategy_discounts()
    test_product_factory()
    test_validation()
    test_exception_handling()
    print("\nALL SECTION 7 CHECKS PASSED")