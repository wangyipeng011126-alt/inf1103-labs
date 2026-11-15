"""Strategy pattern for order discounts.

Each discount is a separate class implementing DiscountStrategy.
Order depends only on the abstraction, so a new discount means a new
class, not a change to Order (Open/Closed Principle).
"""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, subtotal: float) -> float:
        """Return the amount payable after this discount is applied."""
        pass

    def get_name(self) -> str:
        return self.__class__.__name__


class NoDiscount(DiscountStrategy):
    def apply_discount(self, subtotal: float) -> float:
        return subtotal


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = float(percentage)

    def get_percentage(self) -> float:
        return self.__percentage

    def apply_discount(self, subtotal: float) -> float:
        return subtotal * (1 - self.__percentage / 100)

    def get_name(self) -> str:
        return f"{self.__percentage:g}% off"


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float = 200.0, amount: float = 20.0) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply_discount(self, subtotal: float) -> float:
        if subtotal >= self.__threshold:
            return subtotal - self.__amount
        return subtotal

    def get_name(self) -> str:
        return f"${self.__amount:.2f} off if total >= ${self.__threshold:.2f}"