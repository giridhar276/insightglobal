from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This graph acts like a tiny FAQ assistant.
# It uses a knowledge lookup node and returns the answer.
# ---------------------------------------------------------

class GraphState(TypedDict):
    question: str
    answer: str

def faq_node(state: GraphState) -> GraphState:
    faq = {
        "what is python": "Python is a programming language.",
        "what is ai": "AI is artificial intelligence.",
        "what is langgraph": "LangGraph is used to build graph-based agent workflows."
    }

    question = state["question"].lower()
    answer = faq.get(question, "Sorry, I do not know the answer.")
    return {"question": state["question"], "answer": answer}

builder = StateGraph(GraphState)
builder.add_node("faq_node", faq_node)
builder.add_edge(START, "faq_node")
builder.add_edge("faq_node", END)

graph = builder.compile()

result = graph.invoke({"question": "what is ai", "answer": ""})
print(result["answer"])
