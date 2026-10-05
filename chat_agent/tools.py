from altair.datasets import url
from typing import Literal

import requests
from langchain_core.tools import tool

from config import settings

# Tool1: Calculator tool
# Tool2: Web Search tool
# Tool3: Weather tool
# Tool4: Stock price tool


# @tool
def calculator_tool(
    num1: float,
    num2: float,
    operation: Literal["addition", "substraction", "multiplication", "division"],
) -> float | None:
    """
    Use this function to perform basic mathematical operations like, 'addition', 'substraction', 'multiplication', 'division'. These can be used in any order to combine them to perform any sort of complex calculations.
    eg. calculator_tool(3.4,4,"addition") => returns 7.4
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


# @tool
def web_search_tool():
    """
    Use this function for getting information from internet, this will return the search reasults for any query that is passed to it.
    eg.
    """


# @tool
def weather_tool():
    """
    Use this function to get the weather related information, get the current weather for any place, and historical data as well.
    eg.

    """
    requests.get(
        url=settings.OPEN_WEATHER_BASE_URL,
    )


# @tool
def stock_price_tool():
    """
    This function can be used to get the latest stock prices, and historical data as well.
    eg.
    """
    requests.get(url=settings.ALPHA_VANTAGE_STOCK_BASE_URL)


# result = calculator_tool(3.3, 4.7, "division")
# result = weather_tool()
# print(result)
