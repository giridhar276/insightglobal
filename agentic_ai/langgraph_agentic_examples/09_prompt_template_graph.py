import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# This graph combines a prompt template with LangGraph.
# The node formats a prompt, calls the model, and stores output.
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file")

class GraphState(TypedDict):
    topic: str
    answer: str

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    api_key=api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly corporate trainer."),
    ("human", "Explain {topic} in simple words for students.")
])

def prompt_node(state: GraphState) -> GraphState:
    chain = prompt | llm
    response = chain.invoke({"topic": state["topic"]})
    return {"topic": state["topic"], "answer": response.content}

builder = StateGraph(GraphState)
builder.add_node("prompt_node", prompt_node)
builder.add_edge(START, "prompt_node")
builder.add_edge("prompt_node", END)

graph = builder.compile()

result = graph.invoke({"topic": "Agentic AI", "answer": ""})
print(result["answer"])
