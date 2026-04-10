from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This graph reads a text file and summarizes it.
# Good for showing how external files can be used in nodes.
# ---------------------------------------------------------

class GraphState(TypedDict):
    file_name: str
    text: str
    summary: str

def read_file_node(state: GraphState) -> GraphState:
    with open(state["file_name"], "r", encoding="utf-8") as f:
        text = f.read()

    return {**state, "text": text}

def summarize_node(state: GraphState) -> GraphState:
    text = state["text"]

    # Very simple summary logic for beginners
    summary = text[:150] + "..."
    return {**state, "summary": summary}

builder = StateGraph(GraphState)
builder.add_node("read_file_node", read_file_node)
builder.add_node("summarize_node", summarize_node)

builder.add_edge(START, "read_file_node")
builder.add_edge("read_file_node", "summarize_node")
builder.add_edge("summarize_node", END)

graph = builder.compile()

# Keep sample.txt in the same folder before running
result = graph.invoke({"file_name": "sample.txt", "text": "", "summary": ""})
print(result["summary"])
