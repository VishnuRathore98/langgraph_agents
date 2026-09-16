from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# Defining state
class TemperatureState(TypedDict):
    temp_celsius: float
    temp_fahrenheit: float
    weather_status: str


# Convert temperature (celsius -> fahrenheit)
def convert_temp(state: TemperatureState) -> TemperatureState:

    celsius = state["temp_celsius"]
    fahrenheit = (celsius * 9 / 5) + 32

    state["temp_fahrenheit"] = round(fahrenheit, 2)

    return state


# Label weather
def label_weather(state: TemperatureState) -> TemperatureState:

    fahrenheit = state["temp_fahrenheit"]

    if fahrenheit < 50:
        state["weather_status"] = "Cold"
    elif fahrenheit < 77:
        state["weather_status"] = "Mild"
    elif fahrenheit < 95:
        state["weather_status"] = "Hot"
    else:
        state["weather_status"] = "Extream Hot"

    return state


# Building graph
graph = StateGraph(TemperatureState)

# add nodes
graph.add_node("convert_temp", convert_temp)
graph.add_node("label_weather", label_weather)

# add edges
graph.add_edge(START, "convert_temp")
graph.add_edge("convert_temp", "label_weather")
graph.add_edge("label_weather", END)

# Compiling graph
workflow = graph.compile()


# Executing graph
initial_state = {"temp_celsius": 28.5}
final_state = workflow.invoke(initial_state)
print(final_state)
