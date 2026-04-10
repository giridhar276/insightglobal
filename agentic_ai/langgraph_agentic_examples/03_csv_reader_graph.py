import pandas as pd
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This example uses Pandas inside a LangGraph node.
# The node reads a CSV file and stores the summary in state.
# ---------------------------------------------------------

class GraphState(TypedDict):
    file_name: str
    answer: str

def read_csv_node(state: GraphState) -> GraphState:
    file_name = state["file_name"]

    # Read the CSV file
    df = pd.read_csv(file_name)

    # Prepare a simple output
    answer = f"Columns: {list(df.columns)} | Rows: {len(df)}"
    return {"file_name": file_name, "answer": answer}

builder = StateGraph(GraphState)
builder.add_node("read_csv_node", read_csv_node)
builder.add_edge(START, "read_csv_node")
builder.add_edge("read_csv_node", END)

graph = builder.compile()

# Keep students.csv in the same folder before running this file
result = graph.invoke({"file_name": "students.csv", "answer": ""})
print(result["answer"])
