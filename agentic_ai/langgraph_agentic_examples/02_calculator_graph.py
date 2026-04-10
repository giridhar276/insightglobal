from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This example shows a very simple agentic workflow.
# The graph:
# 1. Reads the user request
# 2. Decides which tool to use
# 3. Runs the tool
# 4. Returns the answer
# ---------------------------------------------------------

class GraphState(TypedDict):
    query: str
    operation: str
    a: int
    b: int
    result: int
    answer: str

def detect_operation_node(state: GraphState) -> GraphState:
    query = state["query"].lower()

    # Very simple rule-based decision making
    if "add" in query or "plus" in query:
        operation = "add"
    elif "multiply" in query:
        operation = "multiply"
    else:
        operation = "unknown"

    return {**state, "operation": operation}

def run_tool_node(state: GraphState) -> GraphState:
    a = state["a"]
    b = state["b"]
    operation = state["operation"]

    if operation == "add":
        result = a + b
        answer = f"The sum of {a} and {b} is {result}."
    elif operation == "multiply":
        result = a * b
        answer = f"The product of {a} and {b} is {result}."
    else:
        result = 0
        answer = "I could not identify the operation."

    return {**state, "result": result, "answer": answer}

builder = StateGraph(GraphState)
builder.add_node("detect_operation_node", detect_operation_node)
builder.add_node("run_tool_node", run_tool_node)

builder.add_edge(START, "detect_operation_node")
builder.add_edge("detect_operation_node", "run_tool_node")
builder.add_edge("run_tool_node", END)

graph = builder.compile()

result = graph.invoke({
    "query": "add two numbers",
    "operation": "",
    "a": 12,
    "b": 8,
    "result": 0,
    "answer": ""
})

print(result["answer"])
