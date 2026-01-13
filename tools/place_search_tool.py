import os
import sys
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv
from logger.logger import logger
from exception.exception_handling import TripMateException


class PlaceSearchTool:
    """
    A class that provides tools for searching places and attractions.
    """
    def __init__(self):
        """
        Initializes the PlaceSearchTool and sets up the tool list.
        """
        logger.info("Initializing PlaceSearchTool")
        load_dotenv()
        self.google_api_key = os.environ.get("GPLACES_API_KEY")
        self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """
        Setup and define the tools for place search.

        Returns:
            list: A list of decorated tool functions.
        """
        @tool
        def search_attractions(place: str) -> str:
            """
            Search for attractions in a specific place.

            Args:
                place (str): The name of the place to search for attractions

            Returns:
                str: A string describing the attractions
            """
            try:
                logger.info(f"Searching attractions for: {place}")
                attraction_result = self.google_places_search.google_search_attractions(
                    place
                )
                if attraction_result:
                    return f"Following are the attractions of {place} as suggested by google: {attraction_result}"
                return f"Google couldn't find any attractions for {place}."
            except Exception as e:
                logger.warning(
                    f"Google search failed for {place}, falling back to Tavily: {str(e)}"
                )
                try:
                    tavily_result = self.tavily_search.tavily_search_attractions(place)
                    return f"Google search failed. Following are the attractions of {place} from fallback search: {tavily_result}"
                except Exception as ex:
                    error = TripMateException(ex, sys)
                    logger.error(error.error_message)
                    raise error
        @tool
        def search_restaurants(place: str) -> str:
            """
            Search for restaurants in a specific place.

            Args:
                place (str): The name of the place to search for restaurants

            Returns:
                str: A string describing the restaurants
            """
            try:
                logger.info(f"Searching restaurants for: {place}")
                restaurants_result = (
                    self.google_places_search.google_search_restaurants(place)
                )
                if restaurants_result:
                    return f"Following are the restaurants of {place} as suggested by google: {restaurants_result}"
                return f"Google couldn't find any restaurants for {place}."
            except Exception as e:
                logger.warning(
                    f"Google search failed for {place}, falling back to Tavily: {str(e)}"
                )
                try:
                    tavily_result = self.tavily_search.tavily_search_restaurants(place)
                    return f"Google search failed. Following are the restaurants of {place} from fallback search: {tavily_result}"
                except Exception as ex:
                    error = TripMateException(ex, sys)
                    logger.error(error.error_message)
                    raise error

        @tool
        def search_activities(place: str) -> str:
            """
            Search for activities in a specific place.

            Args:
                place (str): The name of the place to search for activities.

            Returns:
                str: A string describing the activities.
            """
            try:
                logger.info(f"Searching activities for: {place}")
                activities_result = self.google_places_search.google_search_activity(
                    place
                )
                if activities_result:
                    return f"Following are the activities in and around {place} as suggested by google: {activities_result}"
                return f"Google couldn't find any activities for {place}."
            except Exception as e:
                logger.warning(
                    f"Google search failed for {place}, falling back to Tavily: {str(e)}"
                )
                try:
                    tavily_result = self.tavily_search.tavily_search_activity(place)
                    return f"Google search failed. Following are the activities of {place} from fallback search: {tavily_result}"
                except Exception as ex:
                    error = TripMateException(ex, sys)
                    logger.error(error.error_message)
                    raise error
        @tool
        def search_transportation(place: str) -> str:
            """
            Search for transportation options in a specific place.

            Args:
                place (str): The name of the place to search for transportation.
            Returns:
                str: A string describing the transportation options.
            """
            try:
                logger.info(f"Searching transportation for: {place}")
                transportation_result = (
                    self.google_places_search.google_search_transportation(place)
                )
                if transportation_result:
                    return f"Following are the modes of transportation available in {place} as suggested by google: {transportation_result}"
                return f"Google couldn't find any transportation options for {place}."
            except Exception as e:
                logger.warning(
                    f"Google search failed for {place}, falling back to Tavily: {str(e)}"
                )
                try:
                    tavily_result = self.tavily_search.tavily_search_transportation(
                        place
                    )
                    return f"Google search failed. Following are the modes of transportation available in {place} from fallback search: {tavily_result}"
                except Exception as ex:
                    error = TripMateException(ex, sys)
                    logger.error(error.error_message)
                    raise error

        return [search_attractions, search_restaurants, search_activities, search_transportation,]
