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
        def estimate_total_hotel_cost(price_per_night: str, total_days: float) -> float:
            """
            Calculate the total hotel cost based on price per night and total days.

            Args:
                price_per_night (str): The cost of the hotel per night.
                total_days (float): The total number of days stayed.

            Returns:
                float: The total hotel cost.
            """
            try:
                logger.info(f"Estimating hotel cost: {price_per_night} x {total_days}")
                return self.calculator.multiply(price_per_night, total_days)
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        @tool
        def calculate_total_expense(*costs: float) -> float:
            """
            Calculate the total expense of the trip by summing all individual costs.

            Args:
                costs: Variable number of individual costs.

            Returns:
                float: The total sum of all costs.
            """
            try:
                logger.info(f"Calculating total expense for costs: {costs}")
                return self.calculator.calculate_total(*costs)
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """
            Calculate the daily expense budget.

            Args:
                total_cost (float): The total cost of the trip.
                days (int): The number of days for the trip.

            Returns:
                float: The daily budget.
            """
            try:
                logger.info(f"Calculating daily budget: {total_cost} / {days}")
                return self.calculator.calculate_daily_budget(total_cost, days)
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        return [estimate_total_hotel_cost, calculate_daily_expense_budget, calculate_total_expense,]
