import os
import sys
from typing import List
from langchain.tools import tool
from utils.currency_converter import CurrencyConverter
from dotenv import load_dotenv
from logger.logger import logger
from exception.exception_handling import TripMateException


class CurrencyConverterTool:
    """
    A class that provides currency conversion tools.
    """

    def __init__(self):
        """
        Initializes the CurrencyConverterTool and sets up the tool list.
        """
        logger.info("Initializing CurrencyConverterTool")
        load_dotenv()
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        self.currency_service = CurrencyConverter()
        self.currency_converter_tool_list = self._setup_tools()

    def _setup_tools(self):
        """
        Setup and define the tools for currency conversion.

        Returns:
            list: A list of decorated tool functions.
        """

        @tool
        def convert_currency(
            amount: float, from_currency: str, to_currency: str
        ) -> float:
            """
            Convert an amount from one currency to another.

            Args:
                amount (float): The amount to convert.
                from_currency (str): The source currency code 
                to_currency (str): The destination currency code

            Returns:
                float: The converted amount.
            """
            try:
                logger.info(
                    f"Converting {amount} from {from_currency} to {to_currency}"
                )
                return self.currency_service.convert(amount, from_currency, to_currency)
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        return [convert_currency]
