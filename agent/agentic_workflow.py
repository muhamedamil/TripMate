import sys
from typing import Literal

from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from logger.logger import logger
from exception.exception_handling import TripMateException


# Import our Agents
from agent.supervisor import SupervisorAgent
from agent.transport_agent import TransportAgent
from agent.accommodation_agent import AccommodationAgent
from agent.itinerary_agent import ItineraryAgent


class GraphBuilder:
    """
    This class is responsible for building the entire multi agent system
    """

    def __init__(self):
        # Initializing the Agents
        self.supervisor_agent = SupervisorAgent()
        self.transport_agent = TransportAgent()
        self.accommodation_agent = AccommodationAgent()
        self.itinerary_agent = ItineraryAgent()

        self.graph = None

    def build_graph(self):
        try:
            logger.info("Building the Multi Agent System")
            workflow = StateGraph(MessagesState)

            # Defining the Agent Nodes
            workflow.add_node("supervisor", self.supervisor_agent.get_decision)
            workflow.add_node("transport_agent", self.transport_agent.agent_function)
            workflow.add_node("hotel_agent", self.accommodation_agent.agent_function)
            workflow.add_node("itinerary_agent", self.itinerary_agent.agent_function)

            # Defining the Tool Nodes
            transport_tools_node = ToolNode(self.transport_agent.tools)
            hotel_tools_node = ToolNode(self.accommodation_agent.tools)
            itinerary_tools_node = ToolNode(self.itinerary_agent.tools)

            workflow.add_node("transport_tools", transport_tools_node)
            workflow.add_node("hotel_tools", hotel_tools_node)
            workflow.add_node("itinerary_tools", itinerary_tools_node)

            # Defining the Entry point

            workflow.add_edge(START, "supervisor")

            # Supervisor agent routing logic is defined like below:

            def route_supervisor(state):
                next_node = state.get("next")
                if next_node == "FINISH":
                    return END
                if next_node == "TransportAgent":
                    return "transport_agent"
                if next_node == "HotelAgent":
                    return "hotel_agent"
                if next_node == "ItineraryAgent":
                    return "itinerary_agent"
                return END

            workflow.add_conditional_edges("supervisor", route_supervisor)

            # Defining the tool routing logic between the tools and the agents

            # transport Agent Loop to acheive the finality of the agent
            workflow.add_conditional_edges(
                "transport_agent",
                tools_condition,
                {"tools": "transport_tools", END: "supervisor"},
            )
            workflow.add_edge("transport_tools", "transport_agent")

            # hotel Agent Loop to acheive the finality of the agent
            workflow.add_conditional_edges(
                "hotel_agent",
                tools_condition,
                {"tools": "hotel_tools", END: "supervisor"},
            )
            workflow.add_edge("hotel_tools", "hotel_agent")

            # itinerary Agent Loop to acheive the finality of the agent
            workflow.add_conditional_edges(
                "itinerary_agent",
                tools_condition,
                {"tools": "itinerary_tools", END: "supervisor"},
            )

            workflow.add_edge("itinerary_tools", "itinerary_agent")

            self.graph = workflow.compile()
            logger.info("MultiAgent Graph Compiled Successfully")
            return self.graph
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def __call__(self):
        return self.build_graph()
