import pytest
from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct


def test_product_is_abstract():
    with pytest.raises(TypeError):
        Product("X", "Generic", 1.00, 1)


def test_physical_product_works():
    p = PhysicalProduct("P001", "Guitar", 499.99, 5, 3.2)
    assert p.get_fulfilment_info() == "This product requires physical shipping."
    assert p.calculate_shipping_cost() == pytest.approx(11.40)


def test_digital_product_works():
    d = DigitalProduct("D001", "OS", 129.99, 100, 4500)
    assert d.get_fulfilment_info() == "This product is delivered digitally via download."
    assert not hasattr(d, "calculate_shipping_cost")