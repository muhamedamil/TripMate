import os
import sys
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool
from logger.logger import logger
from exception.exception_handling import TripMateException

from utils.weather_info import WeatherForecastTool


class WeatherInfoTool:
    """
    A class that provides weather information tools.
    """
    def __init__(self):
        """
        Initializes the WeatherInfoTool and sets up the tool list.
        """
        logger.info("Initializing WeatherInfoTool")
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """
        Setup and define the tools for weather information.

        Returns:
            list: A list of decorated tool functions.
        """
        @tool
        def get_current_weather(city: str) -> str:
            """
            Get the current weather for a specific city.

            Args:
                city (str): The name of the city.

            Returns:
                str: A string describing the current weather.
            """
            try:
                logger.info(f"Fetching current weather for: {city}")
                weather_data = self.weather_service.get_current_weather(city)
                if weather_data:
                    temp = weather_data.get("main", {}).get("temp", "N/A")
                    desc = weather_data.get("weather", [{}])[0].get(
                        "description", "N/A"
                    )
                    return f"Current weather in {city}: {temp}c, {desc}"
                return f"Couldn't fetch current weather details for {city}"
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error
        @tool
        def get_weather_forecast(city: str) -> str:
            """
            Get the weather forecast for a specific city.

            Args:
                city (str): The name of the city.

            Returns:
                str: A string describing the weather forecast.
            """
            try:
                logger.info(f"Fetching weather forecast for: {city}")
                forecast_data = self.weather_service.get_weather_forecast(city)
                if forecast_data and "list" in forecast_data:
                    forecast_summary = []
                    for i in range(len(forecast_data["list"])):
                        item = forecast_data["list"][i]
                        date = item["dt_txt"].split(" ")[0]
                        temp = item["main"]["temp"]
                        desc = item["weather"][0]["description"]
                        forecast_summary.append(
                            f"{date}: {temp} degree Celsius, {desc}"
                        )
                    return f"Weather forecast for {city}:\n" + "\n".join(
                        forecast_summary
                    )
                return f"Could not fetch the forecast for {city}"
            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error
        return [get_current_weather, get_weather_forecast]
