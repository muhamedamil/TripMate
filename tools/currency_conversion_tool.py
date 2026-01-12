import os
from typing import List
from langchain.tools import tool
from utils.currency_converter import CurrencyConverter
from dotenv import load_dotenv

class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        self.currency_service = CurrencyConverter()
        self.currency_converter_tool_list = self._setup_tools()
    
    def _setup_tools(self):
        """Setup all tools for the currency converter tool"""
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str):
            """Convert amount from one currency to another currency"""
            return self.currency_service.convert(amount, from_currency, to_currency)
        return [convert_currency]
    