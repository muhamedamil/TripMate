import os 
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool

from utils.weather_info import WeatherForecastTool

class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()
        
    def _setup_tools(self)->List:
        """Setup all tools for the weather forecast tool"""
        @tool
        def get_current_weather(city:str) ->str:
            """Get current weather for the city"""
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                temp = weather_data.get('main',{}).get('temp', 'N/A')
                desc = weather_data.get('weather',[{}])[0].get('description', 'N/A')
                return f"current weather in {city}: {temp}c, {desc}"
            return f"Couldn't fetch the details for {city}"
        
        @tool
        def get_weather_forecast(city:str)->str:
            """Get weather forecast for the city"""
            forecast_data = self.weather_service.get_weather_forecast(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp} degree celcius, {desc}")
                return f"weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Could not able to fetch the forecast for the {city}"
        return [get_current_weather,get_weather_forecast]
    
            