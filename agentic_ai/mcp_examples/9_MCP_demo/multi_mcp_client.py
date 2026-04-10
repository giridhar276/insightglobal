import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

math_server = MCPServerStdio(params={
    "command": "python", "args": ["custom_mcp_server.py"]
})

wiki_server = MCPServerStdio(params={
    "command": "python", "args": ["-m", "wikipedia_mcp"]
})

agent = Agent(
    name="MultiMCPAgent",
    instructions="You have access to both math and Wikipedia tools.",
    mcp_servers=[math_server, wiki_server]
)


async def main():
    async with math_server, wiki_server:
        runner = Runner()  

        # run agent inside Runner
        res1 = await runner.run(agent, "What is factorial of 5?")
        print("Math result:", res1.final_output)

        res2 = await runner.run(agent, "Who discovered gravity?")
        print("Wiki result:", res2.final_output)

        res3 = await runner.run(agent, "What is 25*4 and also tell me about Taj Mahal?")
        print("Mixed result:", res3.final_output)

if __name__ == "__main__":
    asyncio.run(main())