import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# Multi-agent example:
# Agent 1 = Planner
# Agent 2 = Executor/Explainer
# This is a clean example for showing collaboration between agents.
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file")

class GraphState(TypedDict):
    goal: str
    plan: str
    execution_help: str

planner_agent = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)
executor_agent = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)

def planner_node(state: GraphState) -> GraphState:
    goal = state["goal"]
    response = planner_agent.invoke(f"Create 5 short steps for this goal: {goal}")
    return {**state, "plan": response.content}

def executor_node(state: GraphState) -> GraphState:
    prompt = f"Explain this plan in simple words for students:\n\n{state['plan']}"
    response = executor_agent.invoke(prompt)
    return {**state, "execution_help": response.content}

builder = StateGraph(GraphState)
builder.add_node("planner_node", planner_node)
builder.add_node("executor_node", executor_node)

builder.add_edge(START, "planner_node")
builder.add_edge("planner_node", "executor_node")
builder.add_edge("executor_node", END)

graph = builder.compile()

result = graph.invoke({
    "goal": "Build a simple FAQ bot using LangGraph",
    "plan": "",
    "execution_help": ""
})

print("Plan:\n", result["plan"])
print("\nExecution Help:\n", result["execution_help"])
