import sys
from typing import List
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage

from logger.logger import logger
from exception.exception_handling import TripMateException
from utils.model_loader import ModelLoader
from prompt_library.itinerary_prompts import ITINERARY_SYSTEM_PROMPT

# importing exisitng tools
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool
from tools.safety_concern_tool import SafetyConcernTool


class ItineraryAgent:
    """
    This agent is  Specialized for Itinerary Planning, Safety, Weather, and Budgeting real time by calling API's
    """

    def __init__(self, model_provider: str = "groq"):
        try:
            logger.info("Initializing ItineraryAgent")
            self.model_loader = ModelLoader(model_provider=model_provider)
            self.llm = self.model_loader.load_llm()

            # Initialize the tools
            self.calculator = CalculatorTool()
            self.weather = WeatherInfoTool()
            self.place_search = PlaceSearchTool()
            self.currency = CurrencyConverterTool()
            self.safety = SafetyConcernTool()

            # converting the individul tools into list of tools
            self.tools = []
            self.tools.extend(self.calculator.calculator_tool_list)
            self.tools.extend(self.weather.weather_tool_list)
            self.tools.extend(self.place_search.place_search_tool_list)
            self.tools.extend(self.currency.currency_converter_tool_list)
            self.tools.extend(self.safety.safety_tool_list)

            # Bind tools with LLM
            self.llm_with_tools = self.llm.bind_tools(self.tools)

        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def agent_function(self, state: MessagesState) -> dict:
        """
        This agent_function is responsible for getting the itinerary info for the user to get the itinerary available in the real time
        """
        try:
            from datetime import datetime
            import time

            # Throttling to prevent 429 Too Many Requests on Groq
            logger.info("Throttling: Waiting 1.0s for Groq stability...")
            time.sleep(2.0)

            current_date = datetime.now().strftime("%Y-%m-%d")
            logger.info("Itinerary Agent is processing...")
            messages = [
                SystemMessage(
                    content=ITINERARY_SYSTEM_PROMPT.format(current_date=current_date)
                )
            ] + state["messages"]

            response = self.llm_with_tools.invoke(messages)
            return {"messages": response}

        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def __call__(self):
        """
        Returns the tool list.
        """
        return self.tools
