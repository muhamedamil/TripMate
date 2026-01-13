import os
import sys
import json
from langchain_tavily import TavilySearch
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper
from logger.logger import logger
from exception.exception_handling import TripMateException


class GooglePlaceSearchTool:
    """
    A class to search for places and information using the Google Places API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the GooglePlaceSearchTool with an API key.
        Args:
            api_key (str): The Google Places API key.
        """
        try:
            logger.info("Initializing GooglePlaceSearchTool")
            self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=api_key)
            self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def google_search_attractions(self, place: str) -> str:
        """
        Searches for attractions in a specified place.
        Args:
            place (str): The name of the place.
        Returns:
            str: Results from the Google Places search tool.
        """
        try:
            logger.info(f"Google searching attractions for: {place}")
            return self.places_tool.run(f"top attractive places in and around {place}")
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def google_search_restaurants(self, place: str) -> str:
        """
        Searches for restaurants in a specified place.
        Args:
            place (str): The name of the place.
        Returns:
            str: Results from the Google Places search tool.
        """
        try:
            logger.info(f"Google searching restaurants for: {place}")
            return self.places_tool.run(
                f"what are the top 10 restaurants and eateries in and around {place}?"
            )
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def google_search_activity(self, place: str) -> str:
        """
        Searches for popular activities in a specified place.
        Args:
            place (str): The name of the place.

        Returns:
            str: Results from the Google Places search tool.
        """

        try:
            logger.info(f"Google searching activities for: {place}")
            return self.places_tool.run(f"Activities in and around {place}")
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def google_search_transportation(self, place: str) -> str:
        """
        Searches for transportation information in a specified place.
        Args:
            place (str): The name of the place.

        Returns:
            str: Results from the Google Places search tool.
        """
        try:
            logger.info(f"Google searching transportation for: {place}")
            return self.places_tool.run(
                f"What are the different modes of transportations available in {place}"
            )
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def google_custom_search(self, query: str) -> str:
        """
        Executes a custom search query using Google Places.
        """
        try:
            logger.info(f"Google custom search for: {query}")
            return self.places_tool.run(query)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error


class TavilyPlaceSearchTool:
    """
    A class to search for places and information using the Tavily Search API.
    """

    def __init__(self, api_key: str = None):
        """
        Initializes the TavilyPlaceSearchTool.
        Args:
            api_key (str): The Tavily API key.
        """
        try:
            logger.info("Initializing TavilyPlaceSearchTool")
            self.api_key = (
                api_key
                or os.environ.get("TAVILY_API_KEY")
                or os.environ.get("TAVILAY_API_KEY")
            )
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def tavily_search_attractions(self, place: str) -> str:
        """
        Searches for attractions in a specified place using Tavily.
        Args:
            place (str): The name of the place.
        Returns:
            str: Answers from the Tavily search tool.
        """
        try:
            logger.info(f"Tavily searching attractions for: {place}")
            tavily_tool = TavilySearch(
                tavily_api_key=self.api_key, topic="general", include_answer="advanced"
            )
            result = tavily_tool.invoke(
                {"query": f"top attractive places in and around {place}"}
            )
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def tavily_search_restaurants(self, place: str) -> str:
        """
        Searches for restaurants in a specified place using Tavily.
        Args:
            place (str): The name of the place.

        Returns:
            str: Answers from the Tavily search tool.
        """
        try:
            logger.info(f"Tavily searching restaurants for: {place}")
            tavily_tool = TavilySearch(
                tavily_api_key=self.api_key, topic="general", include_answer="advanced"
            )
            result = tavily_tool.invoke(
                {
                    "query": f"what are the top 10 restaurants and eateries in and around {place}."
                }
            )
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def tavily_search_activity(self, place: str) -> str:
        """
        Searches for activities in a specified place using Tavily.
        Args:
            place (str): The name of the place.

        Returns:
            str: Answers from the Tavily search tool.
        """
        try:
            logger.info(f"Tavily searching activities for: {place}")
            tavily_tool = TavilySearch(
                tavily_api_key=self.api_key, topic="general", include_answer="advanced"
            )
            result = tavily_tool.invoke({"query": f"activities in and around {place}"})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def tavily_search_transportation(self, place: str) -> str:
        """
        Searches for transportation in a specified place using Tavily.
        Args:
            place (str): The name of the place.
        Returns:
            str: Answers from the Tavily search tool.
        """
        try:
            logger.info(f"Tavily searching transportation for: {place}")
            tavily_tool = TavilySearch(
                tavily_api_key=self.api_key, topic="general", include_answer="advanced"
            )
            result = tavily_tool.invoke(
                {
                    "query": f"What are the different modes of transportations available in {place}"
                }
            )
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def tavily_custom_search(self, query: str) -> str:
        """
        Executes a custom search query using Tavily.
        """
        try:
            logger.info(f"Tavily custom search for: {query}")
            tavily_tool = TavilySearch(
                tavily_api_key=self.api_key, topic="general", include_answer="advanced"
            )
            result = tavily_tool.invoke({"query": query})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error
