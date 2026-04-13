# CSV Text Summarization Project

This project includes:

- `ecommerce_text_data.csv` — sample CSV dataset
- `text_summarization_langchain_streamlit.ipynb` — notebook for end-to-end workflow
- `app.py` — Streamlit app
- `requirements.txt` — dependencies

## Features
- CSV-based text summarization
- Sensitive data masking
- Data cleaning
- OpenAI-based summarization via LangChain
- Simple quality / accuracy checks
- Streamlit UI for upload, summarization, preview, and CSV download

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Run notebook
Open:
`text_summarization_langchain_streamlit.ipynb`

## Run Streamlit app

```bash
streamlit run app.py
```
