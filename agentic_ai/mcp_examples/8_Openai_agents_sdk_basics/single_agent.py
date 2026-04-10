import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a poem on programming.")

print(result.final_output)