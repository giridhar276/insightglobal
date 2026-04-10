from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This graph classifies an email as urgent or normal.
# It is simple, but useful for explaining decision nodes.
# ---------------------------------------------------------

class GraphState(TypedDict):
    email_text: str
    label: str

def classify_email_node(state: GraphState) -> GraphState:
    text = state["email_text"].lower()
    urgent_words = ["urgent", "asap", "immediately"]

    label = "Normal"
    for word in urgent_words:
        if word in text:
            label = "Urgent"
            break

    return {"email_text": state["email_text"], "label": label}

builder = StateGraph(GraphState)
builder.add_node("classify_email_node", classify_email_node)
builder.add_edge(START, "classify_email_node")
builder.add_edge("classify_email_node", END)

graph = builder.compile()

result = graph.invoke({
    "email_text": "Please resolve this issue ASAP. The client is waiting.",
    "label": ""
})

print("Email Category:", result["label"])
