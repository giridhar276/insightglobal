import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This graph uses an LLM as a planner.
# The node creates a short plan for a given goal.
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file")

class GraphState(TypedDict):
    goal: str
    plan: str

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    api_key=api_key
)

def plan_node(state: GraphState) -> GraphState:
    goal = state["goal"]
    prompt = f"Create 5 short beginner-friendly steps for this goal: {goal}"
    response = llm.invoke(prompt)
    return {"goal": goal, "plan": response.content}

builder = StateGraph(GraphState)
builder.add_node("plan_node", plan_node)
builder.add_edge(START, "plan_node")
builder.add_edge("plan_node", END)

graph = builder.compile()

result = graph.invoke({"goal": "Build a simple FAQ bot", "plan": ""})
print(result["plan"])
