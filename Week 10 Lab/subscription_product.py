from product import Product


class SubscriptionProduct(Product):
    def __init__(self, product_id, name, price, stock, billing_period):
        super().__init__(product_id, name, price, stock)
        self.__billing_period = billing_period   

    def get_billing_period(self):
        return self.__billing_period

    def display_information(self):
        super().display_information()
        print(f"  Billing Period: {self.__billing_period}")

    def get_fulfilment_info(self):
        return f"This product is delivered as a {self.__billing_period} subscription."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "subscription"
        data["billing_period"] = self.__billing_period
        return data