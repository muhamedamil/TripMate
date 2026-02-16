import os
import sys
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv
from logger.logger import logger
from exception.exception_handling import TripMateException
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool


class SafetyConcernTool:
    """
    A tool to fetch safety-related information including crises, health issues,
    and authority locations (Embassies, Police Stations).
    """

    def __init__(self):
        logger.info("Initializing SafetyConcernTool")
        load_dotenv()
        self.google_api_key = (
            os.environ.get("GPLACES_API_KEY")
            or os.environ.get("GPLACE_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )
        self.google_search = GooglePlaceSearchTool(api_key=self.google_api_key)
        self.tavily_api_key = os.environ.get("TAVILY_API_KEY") or os.environ.get(
            "TAVILAY_API_KEY"
        )
        self.tavily_search = TavilyPlaceSearchTool(self.tavily_api_key)
        self.safety_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def fetch_current_crises(country_or_city: str) -> str:
            """
            Fetch travel safety/crisis advisories for a location.
            """
            try:
                logger.info(f"Fetching crisis news for {country_or_city}")

                query = f"current safety travel advisory, crises, war, or health issues in {country_or_city} 2026"
                result = self.tavily_search.tavily_custom_search(query)
                return f"Safety/Crisis Report for {country_or_city}: {result}"

            except Exception as e:
                logger.warning(
                    f"Tavily search failed for crisis in {country_or_city}, trying Google fallback: {str(e)}"
                )
                try:
                    fallback_query = (
                        f"travel safety and current crisis in {country_or_city}"
                    )
                    result = self.google_search.google_custom_search(fallback_query)
                    return f"Safety/Crisis Report for {country_or_city} (Google search fallback): {result}"
                except Exception as ex:
                    error = TripMateException(ex, sys)
                    logger.error(error.error_message)
                    return f"Could not fetch real-time safety data for {country_or_city} from any source."

        @tool
        def locate_authorities(place: str) -> str:
            """
            Locate nearest embassies, police stations, and hospitals.
            """
            try:
                logger.info(f"Locating authorities in: {place}")

                query = f"nearest embassy, police station, and hospital in {place}"
                result = self.google_search.google_custom_search(query)

                if result and "not find" not in result.lower():
                    return f"Local Authorities in {place} (Google): {result}"
                raise ValueError("Google Places found no specific matches.")

            except Exception as e:
                logger.warning(
                    f"Google Places failed for authorities in {place}, trying Tavily fallback: {str(e)}"
                )
                try:
                    # Fallback: Tavily search
                    query = (
                        f"location of police station, hospital, and embassy in {place}"
                    )
                    result = self.tavily_search.tavily_custom_search(query)
                    return f"Local Authorities in {place} (Tavily search fallback): {result}"
                except Exception as ex:
                    error = TripMateException(ex, sys)
                    logger.error(error.error_message)
                    return f"Could not locate authorities in {place} from any source."

        return [fetch_current_crises, locate_authorities]
