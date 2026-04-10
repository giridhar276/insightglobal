# pip install --upgrade langchain langchain-community langgraph

# pip install langchain-ollama

from typing import List, Dict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os
import re

load_dotenv()

# Step 1: Define State
#A State class is defined to store the conversation history as a list of messages, where each 
# message has a role (user or assistant) and content (text).
class State(Dict):
    messages: List[Dict[str, str]] 
 
#Next, a graph is created using StateGraph, which acts like a flow controller 
# for how the chatbot processes input.
# Step 2: Initialize StateGraph
graph_builder = StateGraph(State)

# Initialize the LLM
llm = llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

#A chatbot function is defined, which takes the current state (conversation), 
# sends the messages to the LLM using invoke(), and receives a response.

#This response is then added back into the state as an assistant message, 
# ensuring the conversation is preserved

#After that, the chatbot function is added as a node in the graph, and edges are defined to connect START
#  to chatbot and chatbot to END, forming a simple linear flow.

# Define chatbot function
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    state["messages"].append({"role": "assistant", "content": response.content})  # Treat response as a string
    return {"messages": state["messages"]}



# Add nodes and edges
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


# Compile the graph
graph = graph_builder.compile()

#A helper function stream_graph_updates() is created to take user input, 
# initialize the state with that input, and run the graph.

#As the graph executes, it prints the assistant’s latest response.

# Stream updates
def stream_graph_updates(user_input: str):    
    state = {"messages": [{"role": "user", "content": user_input}]}
    for event in graph.stream(state):
        for value in event.values():
            print("Assistant:", value["messages"][-1]["content"])



# Run chatbot in a loop
if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(user_input)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
