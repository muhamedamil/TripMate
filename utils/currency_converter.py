import requests
import sys
from logger.logger import logger
from exception.exception_handling import TripMateException


class CurrencyConverter:
    """
    A class to handle currency conversion using an external API.
    """
    def __init__(self, api_key: str):
        """
        Initializes the CurrencyConverter with an API key.
        Args:
            api_key (str): The API key for the exchange rate service.
        """
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/"
        logger.info("CurrencyConverter initialized")

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert the amount from one currency to another using the exchange rate API.

        Args:
            amount (float): The amount to convert.
            from_currency (str): The source currency code.
            to_currency (str): The destination currency code.

        Returns:
            float: The converted amount.
        Raises:
            TripMateException: If the API call fails or the currency code is not found.
        """
        try:
            logger.info(f"Converting {amount} from {from_currency} to {to_currency}")
            url = f"{self.base_url}/{from_currency}"
            response = requests.get(url)

            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}")
            rates = response.json().get("conversion_rates", {})
            if to_currency not in rates:
                raise ValueError(f"{to_currency} not found in the exchange rates")

            result = amount * rates[to_currency]
            logger.info(f"Converted result: {result}")
            return result
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error
