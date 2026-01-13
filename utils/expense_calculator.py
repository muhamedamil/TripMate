import sys
from typing import Any
from logger.logger import logger
from exception.exception_handling import TripMateException


class Calculator:
    """
    A utility class for mathematical and budgetary calculations.
    """

    @staticmethod
    def _parse_number(val: Any) -> float:
        """
        Helper to parse a value into a float, handling currency symbols and commas.
        """
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            # Remove currency symbols (like ₹, $, €), commas, and spaces
            cleaned = "".join(c for c in val if c.isdigit() or c in ".-")
            try:
                return float(cleaned)
            except ValueError:
                logger.warning(f"Could not parse '{val}' as a number. Returning 0.0")
                return 0.0
        return 0.0

    @staticmethod
    def multiply(a: Any, b: Any) -> float:
        """
        Multiply two values.

        Args:
            a: First value.
            b: Second value.

        Returns:
            float: The product of a and b.
        """
        try:
            val_a = Calculator._parse_number(a)
            val_b = Calculator._parse_number(b)
            return val_a * val_b
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    @staticmethod
    def calculate_total(*x: Any) -> float:
        """
        Calculate the sum of a given list of values.

        Args:
            x: Variable number of values.
        Returns:
            float: The sum of numbers.
        """
        try:
            parsed_values = [Calculator._parse_number(v) for v in x]
            return sum(parsed_values)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    @staticmethod
    def calculate_daily_budget(total: Any, days: Any) -> float:
        """
        Calculate the daily budget based on total cost and number of days.

        Args:
            total: Total cost.
            days: Total number of days.

        Returns:
            float: Expense for a single day.
        """
        try:
            val_total = Calculator._parse_number(total)
            val_days = Calculator._parse_number(days)
            if val_days <= 0:
                logger.warning(
                    "Number of days is zero or negative, returning 0 as budget."
                )
                return 0.0
            return val_total / val_days
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error
