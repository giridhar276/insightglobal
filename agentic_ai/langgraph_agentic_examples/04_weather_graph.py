from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This graph shows a two-step workflow:
# 1. Get weather
# 2. Suggest action
# ---------------------------------------------------------

class GraphState(TypedDict):
    city: str
    weather: str
    advice: str

def get_weather_node(state: GraphState) -> GraphState:
    city = state["city"].lower()

    # Fake weather data for teaching/demo purposes
    data = {
        "hyderabad": "hot",
        "delhi": "rainy",
        "mumbai": "humid"
    }

    weather = data.get(city, "pleasant")
    return {**state, "weather": weather}

def suggest_action_node(state: GraphState) -> GraphState:
    weather = state["weather"]

    if weather == "hot":
        advice = "Carry water and wear light clothes."
    elif weather == "rainy":
        advice = "Carry an umbrella."
    elif weather == "humid":
        advice = "Stay hydrated."
    else:
        advice = "Weather looks fine."

    return {**state, "advice": advice}

builder = StateGraph(GraphState)
builder.add_node("get_weather_node", get_weather_node)
builder.add_node("suggest_action_node", suggest_action_node)

builder.add_edge(START, "get_weather_node")
builder.add_edge("get_weather_node", "suggest_action_node")
builder.add_edge("suggest_action_node", END)

graph = builder.compile()

result = graph.invoke({"city": "Hyderabad", "weather": "", "advice": ""})
print("Weather:", result["weather"])
print("Advice:", result["advice"])
