from product import Product
from orderline import OrderLine


class Order:
    """Composition whole: creates and owns its OrderLine objects.
    OrderLines cannot be passed in from outside, cannot be transferred
    to another Order, and die with this Order."""

    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Order creates its own OrderLine — the caller never supplies one.
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, index: int) -> OrderLine | None:
        if 0 <= index < len(self.order_lines):
            return self.order_lines.pop(index)
        return None

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_information(self) -> None:
        print(f"Order {self.order_id}")
        print("-" * 48)
        if not self.order_lines:
            print("  (no lines)")
        else:
            for line in self.order_lines:
                line.display_information()
        print("-" * 48)
        print(f"  Total: ${self.calculate_total():.2f}")