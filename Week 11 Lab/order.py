from product import Product
from orderline import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    """Composition whole: creates and owns its OrderLine objects.

    A discount is an injected Strategy: Order accepts it at creation
    (default NoDiscount) and calls apply() without any if/elif about
    discount types. set_discount() swaps the behaviour later."""

    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = (
            discount if discount is not None else NoDiscount()
        )

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, index: int) -> OrderLine | None:
        if 0 <= index < len(self.order_lines):
            return self.order_lines.pop(index)
        return None

    def calculate_subtotal(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.__discount.apply(total)

    def display_information(self) -> None:
        print(f"Order {self.order_id}")
        print("-" * 48)
        if not self.order_lines:
            print("  (no lines)")
        else:
            for line in self.order_lines:
                line.display_information()
        print("-" * 48)
        subtotal = self.calculate_subtotal()
        total = self.calculate_total()
        print(f"  Subtotal: ${subtotal:.2f}")
        print(f"  Discount: {type(self.__discount).__name__} "
              f"(-${subtotal - total:.2f})")
        print(f"  Total: ${total:.2f}")