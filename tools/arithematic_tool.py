import os
import sys
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
from logger.logger import logger
from exception.exception_handling import TripMateException


@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: The sum of a and b.
    """
    try:
        logger.info(f"Adding {a} and {b}")
        return a + b
    except Exception as e:
        error = TripMateException(e, sys)
        logger.error(error.error_message)
        raise error


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: The product of a and b.
    """
    try:
        logger.info(f"Multiplying {a} and {b}")
        return a * b
    except Exception as e:
        error = TripMateException(e, sys)
        logger.error(error.error_message)
        raise error


@tool
def currency_converter(from_curr: str, to_curr: str, value: float) -> float:
    """
    Convert currency using Alpha Vantage API.

    Args:
        from_curr (str): The source currency code (e.g., 'USD').
        to_curr (str): The destination currency code (e.g., 'EUR').
        value (float): The amount to convert.

    Returns:
        float: The converted value.
    """
    try:
        logger.info(f"Converting {value} from {from_curr} to {to_curr}")
        os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv("ALPHAVANTAGE_API_KEY")
        alpha_vantage = AlphaVantageAPIWrapper()
        response = alpha_vantage._get_exchange_rate(from_curr, to_curr)

        if "Realtime Currency Exchange Rate" not in response:
            raise Exception(f"Error in API response: {response}")

        exchange_rate = response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        result = value * float(exchange_rate)
        logger.info(f"Conversion result: {result}")
        return result
    except Exception as e:
        error = TripMateException(e, sys)
        logger.error(error.error_message)
        raise error
