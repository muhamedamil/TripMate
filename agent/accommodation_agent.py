import sys
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage

from logger.logger import logger
from exception.exception import TripMateException
from utils.model_loader import ModelLoader
from prompts.accommodation_prompts import ACCOMMODATION_SYSTEM_PROMPT
from tools.amadeus_hotel_search_tool import AmadeusHotelTool



class AccommodationAgent:
    """
    The Specialized Agent for hotel bookings
    """

    def __init__(self, model_provider : str = 'groq'):
        try :
            logger.info(f"Initializing {self.__class__.__name__}")
            self.model_loader = ModelLoader(model_provider)
            self.llm = self.model_loader.load_model()

            self.hotel_tools = AmadeusHotelTool()
            self.tools = self.hotel_tools.tool_list

            self.llm_with_tools = self.llm.bind_tools(self.tools)

        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error
    
    def agent_function(self, state: MessagesState) -> dict :
        """
        The node function that calls the LLM with hotel search capabilities.
        """
        try : 
            logger.info("Accommodation agent is processing the user query")
            messages = [SystemMessage(content = ACCOMMODATION_SYSTEM_PROMPT) + state["messages"]]

            response = self.llm_with_tools.invoke(messages)
            return {"messages": response}

        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error
    
    def __call__(self) :
        """
        returns the tool list
        """
        return self.tools
