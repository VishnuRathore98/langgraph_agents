from typing import Literal

import requests
from langchain_core.tools import tool
from langgraph.types import Command, interrupt
from rich import print
from tavily import TavilyClient

from config import settings

# Tool1: Calculator tool
# Tool2: Web Search tool
# Tool3: Weather tool
# Tool4: Stock price tool


@tool
def calculator_tool(
    num1: float,
    num2: float,
    operation: Literal["addition", "substraction", "multiplication", "division"],
) -> float | None:
    """
    Use this function to perform basic mathematical operations like, 'addition', 'substraction', 'multiplication', 'division'. These can be used in any order to combine them to perform any sort of complex calculations.
    eg. calculator_tool(3.4,4,"addition")
    """
    # print("in calculator tool")
    match operation:
        case "addition":
            return round((num1 + num2), ndigits=2)
        case "substraction":
            return round((num1 - num2), ndigits=2)
        case "multiplication":
            return round((num1 * num2), ndigits=2)
        case "division":
            return round((num1 / num2), ndigits=2)
        case _:
            return None


@tool
def web_search_tool(query: str):
    """
    Use this function for getting information from internet, this will return the search reasults for any query that is passed to it.
    eg.
    web_search_tool(query="Who won max golds in 2026 winter olympics?")
    """
    tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    result = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=2,
    )
    return result


@tool
def weather_tool(location: str):
    """
    Use this function to get the weather related information, get the current weather for any place, and historical data as well.
    eg.

    """
    # Get geocoding, lat and lon from location name
    geocoding_result = requests.get(
        url=f"{settings.OPEN_WEATHER_BASE_URL}/geo/1.0/direct",
        params={
            "q": location,
            "limit": 1,
            "appid": settings.OPEN_WEATHER_API_KEY,
        },
    )
    geocode_lat = geocoding_result.json()[0]["lat"]
    geocode_lon = geocoding_result.json()[0]["lon"]
    # print("Geocoding lat: ", geocode_lat, "Geocode lon: ", geocode_lon)
    weather_result = requests.get(
        url=f"{settings.OPEN_WEATHER_BASE_URL}/data/2.5/weather",
        params={
            "lat": geocode_lat,
            "lon": geocode_lon,
            "units": "metric",
            "appid": settings.OPEN_WEATHER_API_KEY,
        },
    )
    # print("Weather result: ", weather_result.json())
    return weather_result.json()


@tool
def stock_price_tool(
    stock_name: str,
    frequecy: Literal[
        "TIME_SERIES_DAILY",
        "TIME_SERIES_WEEKLY",
        "TIME_SERIES_WEEKLY_ADJUSTED",
        "TIME_SERIES_MONTHLY",
        "TIME_SERIES_MONTHLY_ADJUSTED",
        "GLOBAL_QUOTE",
    ],
):
    """
    This function can be used to get the latest stock prices, and historical data as well.
    This is using the alpha vantage stock api.
    eg. stock_price_tool(stock_name="IBM", frequency="GLOBAL_QUOTE")
    """
    response = requests.get(
        url=f"{settings.ALPHA_VANTAGE_STOCK_BASE_URL}/query",
        params={
            "function": frequecy,
            "symbol": stock_name,
            "apikey": settings.ALPHA_VANTAGE_STOCK_API_KEY,
        },
    )
    return response.json()


@tool
def buy_stocks(symbol: str, stock_count: int):
    user_decision = interrupt(
        value=f"Do you wish to continue with the transaction of {stock_count} stocks, for {symbol}? (yes/no)"
    )

    if user_decision.strip().lower() == "yes":
        # execute the desired action
        return "approved"
    elif user_decision.strip().lower() == "no":
        # do not execute the action
        return "declined"


# result = calculator_tool(3.3, 4.7, "division")
# result = weather_tool()
# print(result)
# print(stock_price_tool(stock_name="IBM", frequecy="GLOBAL_QUOTE"))
