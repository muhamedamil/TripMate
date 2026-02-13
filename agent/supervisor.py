import sys

from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage

from logger.logger import logger
from exception.exception_handling import TripMateException
from utils.model_loader import ModelLoader

from utils.schemas import NextStep
from prompt_library.supervisor_prompts import SUPERVISOR_SYSTEM_PROMPT



class SupervisorAgent:
    """
        The Orchestrator Agent.
        It analyzes the user's request and determines the next step.
        """
    def __init__(self, model_provider: str = "groq"):
        """
        Initialize the SupervisorAgent with an LLM
        """
        try :
            logger.info(f"Intializing the  SupervisorAgent with model_provider:{model_provider}")
            self.model_loader = ModelLoader(model_provider = model_provider)
            self.llm = self.model_loader.load_llm()
            self.structured_llm = self.llm.with_structured_output(NextStep)
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error
    
    def get_decision(self, state: MessagesState) ->dict:
        """
        The core logic function to be used as a node in the LangGraph.
        
        Args:
            state (MessagesState): The current graph state containing conversation history.
            
        Returns:
            dict: Updates the state with the 'next' decision.
        """
        try:
            logger.info("Getting decision from SupervisorAgent")
            messages = [SystemMessage(content = SUPERVISOR_SYSTEM_PROMPT) + state["messages"]]

            decision: NextStep = self.structured_llm.invoke(messages)
            logger.info(f"Supervisor decided to route to: {decision.next_actor}")
            return {"next": decision.next_actor}
        
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error 

    

