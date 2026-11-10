from product import Product
from orderline import OrderLine


class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Order creates its own OrderLine — the caller never supplies one."""
        self.order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, index: int) -> None:
        if 0 <= index < len(self.order_lines):
            self.order_lines.pop(index)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_information(self) -> None:
        print(f"Order {self.order_id}")
        print("-" * 48)
        if not self.order_lines:
            print("  (no lines)")
        for line in self.order_lines:
            line.display_information()
        print("-" * 48)
        print(f"  Total: ${self.calculate_total():.2f}")