

# pip install --upgrade langchain langchain-community langgraph streamlit python-dotenv
# pip install langchain-openai

from typing import List, Dict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# -------------------------------
# Step 1: Define State
# -------------------------------
class State(Dict):
    messages: List[Dict[str, str]]

# -------------------------------
# Step 2: Initialize StateGraph
# -------------------------------
graph_builder = StateGraph(State)

# -------------------------------
# Step 3: Initialize the LLM
# -------------------------------
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# -------------------------------
# Step 4: Define chatbot function
# -------------------------------
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    state["messages"].append(
        {"role": "assistant", "content": response.content}
    )
    return {"messages": state["messages"]}

# -------------------------------
# Step 5: Add nodes and edges
# -------------------------------
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# -------------------------------
# Step 6: Compile the graph
# -------------------------------
graph = graph_builder.compile()

# -------------------------------
# Step 7: Stream graph updates
# -------------------------------
def stream_graph_updates(messages: List[Dict[str, str]]) -> str:
    """
    Takes full chat history, runs graph, and returns the latest assistant reply.
    """
    state = {"messages": messages.copy()}
    final_response = ""

    for event in graph.stream(state):
        for value in event.values():
            final_response = value["messages"][-1]["content"]

    return final_response

# -------------------------------
# Step 8: Streamlit UI
# -------------------------------
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 LangGraph Chatbot")
st.write("A simple Streamlit chatbot built using LangGraph and ChatOpenAI.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar actions
with st.sidebar:
    st.header("Options")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Get assistant response from graph
        assistant_reply = stream_graph_updates(st.session_state.messages)

        # Save assistant reply
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

        # Show assistant reply
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

    except Exception as e:
        st.error(f"An error occurred: {e}")