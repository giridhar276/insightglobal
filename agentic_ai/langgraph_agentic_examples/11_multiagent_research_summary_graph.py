import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# Multi-agent example:
# Agent 1 = Research Agent
# Agent 2 = Summary Agent
# The output of the first node becomes input to the second node.
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file")

class GraphState(TypedDict):
    topic: str
    research: str
    summary: str

research_agent = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)
summary_agent = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)

def research_node(state: GraphState) -> GraphState:
    topic = state["topic"]
    response = research_agent.invoke(f"Give 5 simple points about {topic} for students.")
    return {**state, "research": response.content}

def summary_node(state: GraphState) -> GraphState:
    response = summary_agent.invoke(f"Summarize this in 3 short lines:\n\n{state['research']}")
    return {**state, "summary": response.content}

builder = StateGraph(GraphState)
builder.add_node("research_node", research_node)
builder.add_node("summary_node", summary_node)

builder.add_edge(START, "research_node")
builder.add_edge("research_node", "summary_node")
builder.add_edge("summary_node", END)

graph = builder.compile()

result = graph.invoke({"topic": "LangGraph", "research": "", "summary": ""})
print("Research:\n", result["research"])
print("\nSummary:\n", result["summary"])
