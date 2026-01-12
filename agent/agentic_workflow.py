import sys
from utils.model_loader import ModelLoader
from prompt_library.prompts import SYSTEM_PROMPT

from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from logger.logger import logger
from exception.exception_handling import TripMateException


class GraphBuilder:
    """
    A class to build and compile the agentic workflow graph.
    """

    def __init__(self, model_provider: str = "groq"):
        """
        Initializes the GraphBuilder with tools and LLM.

        Args:
            model_provider (str): The provider for the LLM.
        """
        logger.info(f"Initializing GraphBuilder with model provider: {model_provider}")
        self.tools = []
        self.model_provider = ModelLoader(model_provider=model_provider)
        self.llm = self.model_provider.load_llm()

        self.calculator_tools = CalculatorTool()
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.currency_converter_tools = CurrencyConverterTool()
        self.tools.extend(
            [
                *self.calculator_tools.calculator_tool_list,
                *self.weather_tools.weather_tool_list,
                *self.place_search_tools.place_search_tool_list,
                *self.currency_converter_tools.currency_converter_tool_list,
            ]
        )
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.system_prompt = SYSTEM_PROMPT
        self.graph = None

    def agent_function(self, state: MessagesState):

        """
        The core agent logic that decides which tool to use or providing the final answer.
        Args:
            state (MessagesState): The current state of the graph containing messages.
        Returns:
            dict: The updated state with the new message from the LLM.
        """
        logger.info("Agent function invoked")
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": response}

    def build_graph(self):

        """
        Builds and compiles the StateGraph for the agent.
        Returns:
            CompiledGraph: The compiled langgraph graph.
        Raises:
            TripMateException: If an error occurs during graph building or compilation.
        """
        try:
            logger.info("Building and compiling the graph")
            graph_builder = StateGraph(MessagesState)

            graph_builder.add_node("agent", self.agent_function)
            graph_builder.add_node("tools", ToolNode(self.tools))

            graph_builder.add_edge(START, "agent")

            graph_builder.add_conditional_edges("agent", tools_condition)
            graph_builder.add_edge("tools", "agent")

            
            self.graph = graph_builder.compile()
            logger.info("Graph compiled successfully")
            return self.graph
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def __call__(self):
        """
        Allows the GraphBuilder instance to be called like a function to get the compiled graph.
        """
        return self.build_graph()
