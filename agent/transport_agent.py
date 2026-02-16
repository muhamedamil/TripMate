import sys
from typing import List
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage

from logger.logger import logger
from exception.exception_handling import TripMateException
from utils.model_loader import ModelLoader
from prompt_library.transport_prompts import TRANSPORT_SYSTEM_PROMPT
from tools.amadeus_transport_tool import AmadeusTransportTool



class TransportAgent:
    """
    This agent is specialized for retreivning the details about flights and transportation.

    """

    def __init__(self):
        try:
            logger.info("Initializing the TransportAgent")
            self.model_loader = ModelLoader()
            self.llm =self.model_loader.load_llm()

            # Initializing the tools
            self.transport_tool = AmadeusTransportTool()
            self.tools = self.transport_tool.tool_list

            #Bind the tools to the LLM
            self.llm_with_tools = self.llm.bind_tools(self.tools)

        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def agent_function(self, state:MessagesState) -> dict :
        """
        This agent_function that calls the LLM with the transport search capabilities.
        """
        
        try:
            from datetime import datetime
            import time

            # Throttling to prevent 429 Too Many Requests on Groq
            logger.info("Throttling: Waiting 1.0s for Groq stability...")
            time.sleep(1.0)

            current_date = datetime.now().strftime("%Y-%m-%d")
            logger.info("Transport agent is processing the user query")
            messages = [
                SystemMessage(
                    content=TRANSPORT_SYSTEM_PROMPT.format(current_date=current_date)
                )
            ] + state["messages"]

            response = self.llm_with_tools.invoke(messages)
            return {"messages": response}

        except Exception as e:
            error= TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def __call__(self) -> List:
        """
        Returns the tool list
        """
        return self.tools