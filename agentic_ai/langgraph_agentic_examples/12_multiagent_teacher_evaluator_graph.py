import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# Multi-agent example:
# Agent 1 creates a question
# Agent 2 evaluates a student's answer
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file")

class GraphState(TypedDict):
    question: str
    student_answer: str
    evaluation: str

teacher_agent = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)
evaluator_agent = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)

def teacher_node(state: GraphState) -> GraphState:
    response = teacher_agent.invoke("Generate one simple question on Agentic AI for beginners.")
    return {**state, "question": response.content}

def evaluator_node(state: GraphState) -> GraphState:
    prompt = (
        f"Question: {state['question']}\n"
        f"Student answer: {state['student_answer']}\n"
        "Evaluate in 2 short lines."
    )
    response = evaluator_agent.invoke(prompt)
    return {**state, "evaluation": response.content}

builder = StateGraph(GraphState)
builder.add_node("teacher_node", teacher_node)
builder.add_node("evaluator_node", evaluator_node)

builder.add_edge(START, "teacher_node")
builder.add_edge("teacher_node", "evaluator_node")
builder.add_edge("evaluator_node", END)

graph = builder.compile()

result = graph.invoke({
    "question": "",
    "student_answer": "Agentic AI uses tools and decisions to complete tasks.",
    "evaluation": ""
})

print("Question:\n", result["question"])
print("\nEvaluation:\n", result["evaluation"])
