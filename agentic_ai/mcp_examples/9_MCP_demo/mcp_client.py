import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()



async def main():
    # Connect to the custom MCP math server
    async with MCPServerStdio(
        params={
            "command": "python",
            "args": ["custom_mcp_server.py"],  # runs your math server
        }
    ) as math_server:

        agent = Agent(
            name="DemoMCPAgent",
            instructions="You are a helpful math assistant. Use the available MCP tools to answer math questions.",
            mcp_servers=[math_server]
        )

        result = await Runner.run(agent, "What is 5 + 7?")
        print("Agent reply:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
