from product import Product


class OrderLine:
    """Composition part: created only by Order. Holds a *reference* to a
    Product (association) but does NOT own it — the Product exists independently."""

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        self.__product: Product = product
        self.__quantity: int = int(quantity)

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"  {self.__product.get_name()} "
              f"x{self.__quantity} @ ${self.__product.get_price():.2f} "
              f"= ${self.calculate_subtotal():.2f}")

    # --- getters ---
    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity