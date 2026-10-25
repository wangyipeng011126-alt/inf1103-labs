
from product import Product


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        # Check whether the product ID already exists
        if self.search_product(product.get_product_id()):
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def display_all(self):
        print("Current Inventory")
        print("-" * 48)

        if not self.__products:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()

        print("-" * 48)

    def get_products(self):
        return self.__products
