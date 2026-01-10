
from utils.model_loader import ModelLoader
from prompt_library.prompts import SYSTEM_PROMPT


from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool



from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition


class GraphBuilder:
    def __init__(self, model_provider:str="groq"):
        self.tools = []
        self.model_provider = ModelLoader(model_provider=model_provider)
        self.llm = self.model_provider.load_llm()
        
        self.calculator_tools = CalculatorTool()
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.llm_with_tools = self.llm.bind_tools(tools= self.tools)
        self.system_prompt = SYSTEM_PROMPT
        
        self.graph = None

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
