from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This example shows conditional routing in LangGraph.
# The graph decides whether a task is high priority or low priority.
# ---------------------------------------------------------

class GraphState(TypedDict):
    task: str
    priority: str
    action: str

def detect_priority_node(state: GraphState) -> GraphState:
    task = state["task"].lower()

    if "report" in task or "client" in task:
        priority = "high"
    else:
        priority = "low"

    return {**state, "priority": priority}

def high_priority_node(state: GraphState) -> GraphState:
    return {**state, "action": "Do this task immediately."}

def low_priority_node(state: GraphState) -> GraphState:
    return {**state, "action": "You can do this later."}

def route_by_priority(state: GraphState) -> str:
    if state["priority"] == "high":
        return "high_priority_node"
    return "low_priority_node"

builder = StateGraph(GraphState)
builder.add_node("detect_priority_node", detect_priority_node)
builder.add_node("high_priority_node", high_priority_node)
builder.add_node("low_priority_node", low_priority_node)

builder.add_edge(START, "detect_priority_node")
builder.add_conditional_edges("detect_priority_node", route_by_priority)
builder.add_edge("high_priority_node", END)
builder.add_edge("low_priority_node", END)

graph = builder.compile()

result = graph.invoke({"task": "Submit client report today", "priority": "", "action": ""})
print("Priority:", result["priority"])
print("Action:", result["action"])
