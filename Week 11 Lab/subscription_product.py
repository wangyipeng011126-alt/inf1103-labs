from product import Product
from supplier import Supplier


class SubscriptionProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, billing_period: str, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__billing_period: str = billing_period

    def get_billing_period(self) -> str:
        return self.__billing_period

    def display_information(self) -> None:
        super().display_information()
        print(f"  Billing Period: {self.__billing_period}")

    def get_fulfilment_info(self) -> str:
        return f"This product is delivered as a {self.__billing_period} subscription."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "subscription"
        data["billing_period"] = self.__billing_period
        return data