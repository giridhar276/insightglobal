'''
Sales Negotiation Agents

Seller agent proposes value
Buyer agent pushes for lower price
Both agents talk for multiple rounds

Key concept:
Negotiation through multi-agent conversation
'''

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file")

seller = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)
buyer = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)

product = "Corporate AI training package"
starting_price = 50000
conversation = f"Product: {product}\nStarting price: {starting_price}\n"

for round_no in range(1, 4):
    seller_msg = seller.invoke(
        f"You are a seller. Negotiate professionally in 2 short lines. Context:\n{conversation}"
    ).content
    conversation += f"Seller Round {round_no}: {seller_msg}\n"

    buyer_msg = buyer.invoke(
        f"You are a buyer. Negotiate for a lower price in 2 short lines. Context:\n{conversation}"
    ).content
    conversation += f"Buyer Round {round_no}: {buyer_msg}\n"

print(conversation)
