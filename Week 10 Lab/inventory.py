from product import Product


class Inventory:
    def __init__(self) -> None:
        self.products: list[Product] = []      # base class, not the subclasses

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the reference only — the Product object is untouched."""
        product = self.find_product(product_id)
        if product is not None:
            self.products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.get_product_id() == product_id:
                return product          
        return None

    search_product = find_product          # keeps main.py working

    def display_all_products(self) -> None:
        print("Current Inventory")
        print("-" * 48)
        if not self.products:
            print("No products in inventory.")
        else:
            for product in self.products:       # polymorphism: no isinstance()
                product.display_information()
        print("-" * 48)

    display_all = display_all_products      # keeps main.py working

    def get_products(self) -> list[Product]:
        return list(self.products)          # copy, so callers can't mutate internals