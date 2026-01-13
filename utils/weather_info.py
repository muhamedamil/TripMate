import requests
import sys
from logger.logger import logger
from exception.exception_handling import TripMateException


class WeatherForecastTool:
    """
    A class to fetch weather information from OpenWeatherMap API.
    """
    def __init__(self, api_key: str):
        """
        Initializes the WeatherForecastTool with an API key.
        Args:
            api_key (str): The OpenWeatherMap API key.
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        logger.info("WeatherForecastTool initialized")

    def get_current_weather(self, place: str) -> dict:
        """
        Fetch current weather for a specific place.
        Args:
            place (str): The name of the place.
        Returns:
            dict: The JSON response from the API.
        Raises:
            TripMateException: If the API call fails or an error occurs.
        """
        try:
            logger.info(f"Fetching current weather for: {place}")
            url = f"{self.base_url}/weather"
            params = {"q": place, "appid": self.api_key, "units": "metric"}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Failed to fetch weather for {place}: {response.status_code} - {response.text}"
                )
                return {}
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def get_weather_forecast(self, place: str) -> dict:
        """
        Fetch 5 day weather forecast for a specific place.
        Args:
            place (str): The name of the place.
        Returns:
            dict: The JSON response from the API.

        Raises:
            TripMateException: If the API call fails or an error occurs.
        """
        try:
            logger.info(f"Fetching weather forecast for: {place}")
            url = f"{self.base_url}/forecast"
            params = {"q": place, "appid": self.api_key, "cnt": 10, "units": "metric"}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Failed to fetch forecast for {place}: {response.status_code} - {response.text}"
                )
                return {}
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error
