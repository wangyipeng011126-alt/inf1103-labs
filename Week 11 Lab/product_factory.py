"""Factory pattern: centralises creation of Product objects.

Client code asks the factory for a Product and only ever sees the
Product base type — it never constructs PhysicalProduct, DigitalProduct
or SubscriptionProduct itself. Add a new product type in one place.
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
               *, weight: float | None = None,
               download_size: float | None = None,
               billing_period: str | None = None) -> Product:
        product_type = product_type.strip().lower()

        if product_type == "physical":
            if weight is None:
                raise ValueError("Physical product requires 'weight'.")
            return PhysicalProduct(product_id, name, price, stock,
                                   weight, supplier)

        elif product_type == "digital":
            if download_size is None:
                raise ValueError("Digital product requires 'download_size'.")
            return DigitalProduct(product_id, name, price, stock,
                                  download_size, supplier)

        elif product_type == "subscription":
            if billing_period is None:
                raise ValueError(
                    "Subscription product requires 'billing_period'."
                )
            return SubscriptionProduct(product_id, name, price, stock,
                                       billing_period, supplier)

        else:
            raise ValueError(f"Unknown product type: {product_type}")