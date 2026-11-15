"""Strategy pattern for order discounts.

Each concrete strategy implements apply() and is interchangeable.
Order depends only on DiscountStrategy, so a new discount means a new
class — not an edit to Order (Open/Closed Principle).
"""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        self.__percentage: float = float(percentage)

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

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