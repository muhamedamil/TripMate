import sys
from typing import List
from utils.expense_calculator import Calculator
from langchain.tools import tool
from logger.logger import logger
from exception.exception_handling import TripMateException


class CalculatorTool:
    """
    A class that provides travel-related calculation tools.
    """

    def __init__(self):
        """
        Initializes the CalculatorTool and sets up the tool list.
        """
        logger.info("Initializing CalculatorTool")
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self):
        """
        Setup and define the tools for expense calculations.

        Returns:
            list: A list of decorated tool functions.
        """

        @tool
        def estimate_total_hotel_cost(
            price_per_night: float, total_days: float
        ) -> float:
            """
            Calculate the total hotel cost.
            IMPORTANT: Use JSON numbers only (e.g., 150.0), NOT strings (e.g., "150.0").
            """
            try:
                logger.info(f"Estimating hotel cost: {price_per_night} x {total_days}")
                return self.calculator.multiply(price_per_night, total_days)
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        @tool
        def calculate_total_expense(
            flights_cost: float, hotels_cost: float, activities_cost: float
        ) -> float:
            """
            Sum flight, hotel, and activity costs into a total.
            IMPORTANT: Use JSON numbers only.
            """
            try:
                logger.info(
                    f"Adding costs: {flights_cost}, {hotels_cost}, {activities_cost}"
                )
                return flights_cost + hotels_cost + activities_cost
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        @tool
        def calculate_daily_expense_budget(total_cost: float, days: float) -> float:
            """
            Divide total cost by number of days.
            IMPORTANT: Use JSON numbers only.
            """
            try:
                logger.info(f"Calculating daily budget: {total_cost} / {days}")
                return self.calculator.calculate_daily_budget(total_cost, days)
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        return [
            estimate_total_hotel_cost,
            calculate_daily_expense_budget,
            calculate_total_expense,
        ]
