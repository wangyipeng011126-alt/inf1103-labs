"""Factory pattern: centralises creation of Product objects.

Client code asks the factory for a Product and only ever sees the
Product base type — it never constructs PhysicalProduct, DigitalProduct
or SubscriptionProduct itself. Add a new product type in one place.

Type-specific fields are optional: when omitted (e.g. when reading the
lab's products.csv, which has no weight/download_size/billing_period
columns) sensible defaults are used. Any explicit value is still
validated by the concrete class.
"""

from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from subscription_product import SubscriptionProduct
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str,
               price: float, stock: int, supplier: Supplier,
               *, weight: float = 0.0,
               download_size: float = 0.0,
               billing_period: str = "monthly") -> Product:
        product_type = product_type.strip().lower()

        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock,
                                   weight, supplier)

        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock,
                                  download_size, supplier)

        elif product_type == "subscription":
            return SubscriptionProduct(product_id, name, price, stock,
                                       billing_period, supplier)

        else:
            raise ValueError(f"Unknown product type: {product_type}")