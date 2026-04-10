import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This example shows the smallest useful LangGraph program.
# Flow:
# START -> chatbot_node -> END
# The node reads state, calls the LLM, and writes back output.
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file")

# State is the shared data that moves through the graph
class GraphState(TypedDict):
    question: str
    answer: str

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    api_key=api_key
)

def chatbot_node(state: GraphState) -> GraphState:
    # Read user question from state
    question = state["question"]

    # Ask the model
    response = llm.invoke(question)

    # Return updated state
    return {"question": question, "answer": response.content}

builder = StateGraph(GraphState)
builder.add_node("chatbot_node", chatbot_node)
builder.add_edge(START, "chatbot_node")
builder.add_edge("chatbot_node", END)

graph = builder.compile()

result = graph.invoke({"question": "Explain Agentic AI in 3 simple lines.", "answer": ""})
print(result["answer"])
