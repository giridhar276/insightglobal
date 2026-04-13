# E-Commerce Product Discovery Assistant using RAG

This package contains:
- ecommerce_products_dataset.csv
- Ecommerce_RAG_v5.ipynb
- app.py
- Ecommerce_QA_Validation.csv
- Ecommerce_RAG_Project_Brief.docx
- requirements.txt

## Project idea
Students build an AI-assisted product discovery system for an e-commerce catalog.
The notebook follows a RAG workflow: load structured data, convert rows to documents,
chunk text, create embeddings, store in Chroma, retrieve relevant chunks, and build QA.

## How to run
1. Install dependencies  
   `pip install -r requirements.txt`

2. Launch app  
   `streamlit run app.py`

3. Open notebook  
   Keep the CSV files in the same folder.

## Note
Embedding and LLM cells require an API key:
`OPENAI_API_KEY`