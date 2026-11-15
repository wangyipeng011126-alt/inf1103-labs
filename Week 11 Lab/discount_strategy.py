"""Strategy pattern for order discounts.

Each concrete strategy implements apply() and is interchangeable.
Order depends only on DiscountStrategy, so a new discount means a new
class — not an edit to Order (Open/Closed Principle).

Each strategy validates its own parameters in __init__ (Section 4):
a broken rule raises ValueError before the object can be used.
"""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """Identity discount: returns the total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off, e.g. PercentageDiscount(10) is 10% off."""

    def __init__(self, percentage: float) -> None:
        percentage = float(percentage)
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above the threshold,
    e.g. BulkDiscount(200, 20) takes 20 off totals of 200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        threshold = float(threshold)
        amount = float(amount)
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")
        if amount > threshold:
            # otherwise a total of exactly `threshold` would go negative
            raise ValueError(
                "Discount amount cannot exceed the threshold."
            )
        self.__threshold: float = threshold
        self.__amount: float = amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total


class StudentDiscount(DiscountStrategy):
    """Fixed 5% student discount. Requires a non-empty student ID."""

    RATE: float = 0.05

    def __init__(self, student_id: str) -> None:
        student_id = student_id.strip()
        if not student_id:
            raise ValueError("Student ID is required for a student discount.")
        self.__student_id: str = student_id

    def get_student_id(self) -> str:
        return self.__student_id

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)