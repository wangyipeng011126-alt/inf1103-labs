"""INF1103 Lab 8 — single test function covering Sections 2.2, 3.2, 4.3, 6.2, 7.2."""

from supplier import Supplier
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from subscription_product import SubscriptionProduct
from inventory import Inventory
from order import Order


def show_product_details(product) -> None:
    """Lab 6.2 helper: works with ANY Product — no isinstance, no subclass checks."""
    product.display_information()
    print(f"  Fulfilment: {product.get_fulfilment_info()}")


def test_lab8() -> None:

    # ============================================================
    # LAB 2.2 — Associate Supplier with Product
    # Predict-first: del supplier → products must still work
    # ============================================================
    print("\n--- Lab 2.2: Associate Supplier with Product ---")
    supplier = Supplier("SUP-001", "Acme Supplies", "sales@acme.com")
    laptop = PhysicalProduct("P1", "Laptop", 1200.00, 10, 2.5, supplier)
    ebook = DigitalProduct("P2", "Python eBook", 25.00, 999, 12.4, supplier)

    del supplier                              # prediction: products survive
    print(f"  Same Supplier shared by both products? "
          f"{laptop.get_supplier() is ebook.get_supplier()}")

    assert laptop.get_supplier() is not None
    assert laptop.get_supplier() is ebook.get_supplier()
    assert laptop.get_supplier().get_name() == "Acme Supplies"

    # ============================================================
    # LAB 3.2 — Add and remove products (aggregation)
    # Predict-first: product still usable after removal from A
    # ============================================================
    print("\n--- Lab 3.2: Add and remove products (aggregation) ---")
    inv_a = Inventory()
    inv_b = Inventory()

    assert inv_a.add_product(laptop) is True
    assert inv_a.add_product(
        PhysicalProduct("P1", "Dup", 1.0, 1, 1.0, laptop.get_supplier())
    ) is False                                # duplicate ID rejected

    removed = inv_a.remove_product("P1")
    print(f"  Removed from A, still usable: {removed.get_name()}")
    assert removed is laptop                  # same object, not a copy
    assert inv_a.products == []

    assert inv_b.add_product(removed) is True
    assert inv_b.find_product("P1") is laptop
    assert inv_b.find_product("MISSING") is None

    # ============================================================
    # LAB 4.3 — Test composition (Order <> OrderLine)
    # Predict-first: same Product in two Orders → 1 Product, 2 OrderLines
    # ============================================================
    print("\n--- Lab 4.3: Test composition (Order <> OrderLine) ---")
    order1 = Order("ORD-1")
    order2 = Order("ORD-2")
    order1.add_order_line(laptop, 2)
    order1.add_order_line(ebook, 3)
    order2.add_order_line(laptop, 1)

    print(f"  OrderLines in order1: {len(order1.order_lines)}")
    print(f"  OrderLines in order2: {len(order2.order_lines)}")
    print(f"  Same Product shared across orders? "
          f"{order1.order_lines[0].get_product() is order2.order_lines[0].get_product()}")
    print(f"  Same OrderLine shared across orders? "
          f"{order1.order_lines[0] is order2.order_lines[0]}")

    assert len(order1.order_lines) == 2
    assert len(order2.order_lines) == 1
    assert order1.order_lines[0].get_product() is order2.order_lines[0].get_product()
    assert order1.order_lines[0] is not order2.order_lines[0]
    assert order1.calculate_total() == 2 * 1200.00 + 3 * 25.00

    removed_line = order1.remove_order_line(0)
    assert removed_line.get_product() is laptop
    assert order1.calculate_total() == 3 * 25.00

    # ============================================================
    # LAB 6.2 + LAB 7.2 — LSP substitutability + polymorphism
    # Predict-first: what each get_fulfilment_info() prints
    # ============================================================
    print("\n--- Lab 6.2 + 7.2: LSP substitution + polymorphism ---")
    sub = SubscriptionProduct("P3", "Pro Plan", 15.00, 100, "monthly",
                              laptop.get_supplier())
    inv = Inventory()
    for p in (laptop, ebook, sub):
        inv.add_product(p)

    for product in inv.products:              # one loop, no isinstance
        show_product_details(product)

    assert len(inv.products) == 3
    assert laptop.get_fulfilment_info() == "This product requires physical shipping."
    assert "digitally" in ebook.get_fulfilment_info()
    assert "monthly" in sub.get_fulfilment_info()


if __name__ == "__main__":
    test_lab8()
    print("\nALL CHECKS PASSED")