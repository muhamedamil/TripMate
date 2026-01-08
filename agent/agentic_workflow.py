
from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT


from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool



from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition


class GraphBuilder:
    def __init__(self):
        self.tools = [
            WeatherInfoTool(),
            PlaceSearchTool(),
            CalculatorTool(),
            CurrencyConverterTool(),
        ]
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": response}

    def build_graph(self):

        graph_builder = StateGraph(MessagesState)

        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(self.tools))

        graph_builder.add_edge(START, "agent")

        # This handles both "Go to Tools" and "Go to End"
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agents",END)
        
        self.graph = graph_builder.compile()
        return self.graph
    def __call__(self):
        return self.build_graph()
