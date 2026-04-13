import os
import re
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="CSV Text Summarization", layout="wide")
st.title("CSV Text Summarization with LangChain + OpenAI")
st.caption("Includes data cleaning, sensitive data masking, summarization, and quality checks.")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def clean_text(text: str) -> str:
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def mask_sensitive_data(text: str, customer_name: str = "") -> str:
    text = clean_text(text)
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_MASKED]', text)
    text = re.sub(r'(\+?\d[\d\-\s]{8,}\d)', '[PHONE_MASKED]', text)
    text = re.sub(r'\bORD\d+\b', '[ORDER_ID_MASKED]', text)
    if customer_name and pd.notna(customer_name):
        pattern = re.escape(str(customer_name))
        text = re.sub(pattern, '[CUSTOMER_MASKED]', text, flags=re.IGNORECASE)
    return text

def normalize_tokens(text: str):
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", str(text).lower())
    return [tok for tok in text.split() if tok]

def token_overlap_f1(pred: str, ref: str) -> float:
    pred_tokens = normalize_tokens(pred)
    ref_tokens = normalize_tokens(ref)
    if not pred_tokens or not ref_tokens:
        return 0.0
    pred_set, ref_set = set(pred_tokens), set(ref_tokens)
    overlap = len(pred_set & ref_set)
    precision = overlap / len(pred_set) if pred_set else 0
    recall = overlap / len(ref_set) if ref_set else 0
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)

def keyword_coverage(summary: str, row: pd.Series, product_col: str, status_col: str | None, sentiment_col: str | None) -> float:
    keywords = []
    if product_col:
        keywords.append(str(row.get(product_col, "")).lower())
    if status_col:
        keywords.append(str(row.get(status_col, "")).lower())
    if sentiment_col:
        keywords.append(str(row.get(sentiment_col, "")).lower())
    keywords = [k for k in keywords if k]
    if not keywords:
        return 0.0
    summary_lower = str(summary).lower()
    present = sum(1 for kw in keywords if kw in summary_lower)
    return present / len(keywords)

@st.cache_resource
def get_chain(model_name: str):
    llm = ChatOpenAI(model=model_name, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a careful data summarization assistant. "
         "Summarize the ecommerce or business text in 2 short sentences. "
         "Do not reveal masked data. Preserve important facts like product, status, sentiment, and issue."),
        ("human", "Text:\n{text}")
    ])
    return prompt | llm

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if not OPENAI_API_KEY:
    st.warning("OPENAI_API_KEY is missing. Add it to your environment or .env file before running summaries.")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview")
    st.dataframe(df.head(), use_container_width=True)

    columns = list(df.columns)
    text_col = st.selectbox("Choose the text column", columns, index=columns.index("text") if "text" in columns else 0)
    name_col = st.selectbox("Choose customer name column (optional)", [""] + columns, index=([""] + columns).index("customer_name") if "customer_name" in columns else 0)
    ref_col = st.selectbox("Choose reference summary column (optional)", [""] + columns, index=([""] + columns).index("reference_summary") if "reference_summary" in columns else 0)
    product_col = st.selectbox("Choose product column (optional)", [""] + columns, index=([""] + columns).index("product") if "product" in columns else 0)
    status_col = st.selectbox("Choose status column (optional)", [""] + columns, index=([""] + columns).index("status") if "status" in columns else 0)
    sentiment_col = st.selectbox("Choose sentiment column (optional)", [""] + columns, index=([""] + columns).index("sentiment") if "sentiment" in columns else 0)
    model_name = st.text_input("OpenAI model", value="gpt-4.1-mini")
    row_limit = st.slider("How many rows to process", min_value=1, max_value=min(50, len(df)), value=min(10, len(df)))

    if st.button("Generate summaries", type="primary"):
        work_df = df.head(row_limit).copy()
        work_df["clean_text"] = work_df[text_col].apply(clean_text)
        work_df["masked_text"] = work_df.apply(
            lambda row: mask_sensitive_data(row[text_col], row[name_col] if name_col else ""), axis=1
        )

        chain = get_chain(model_name)

        summaries = []
        for i, text in enumerate(work_df["masked_text"], start=1):
            try:
                response = chain.invoke({"text": text})
                summaries.append(response.content.strip())
            except Exception as e:
                summaries.append(f"ERROR: {e}")

        work_df["generated_summary"] = summaries

        if ref_col:
            work_df["token_overlap_f1"] = work_df.apply(
                lambda row: token_overlap_f1(row["generated_summary"], row[ref_col]), axis=1
            )
        else:
            work_df["token_overlap_f1"] = None

        work_df["keyword_coverage"] = work_df.apply(
            lambda row: keyword_coverage(row["generated_summary"], row, product_col, status_col or None, sentiment_col or None), axis=1
        )

        if ref_col:
            work_df["quality_score_percent"] = ((work_df["token_overlap_f1"].fillna(0) * 0.7) + (work_df["keyword_coverage"] * 0.3)) * 100
        else:
            work_df["quality_score_percent"] = work_df["keyword_coverage"] * 100

        st.subheader("Results")
        st.dataframe(work_df, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            if ref_col:
                st.metric("Avg Token Overlap F1", round(work_df["token_overlap_f1"].fillna(0).mean(), 3))
        with c2:
            st.metric("Avg Keyword Coverage", round(work_df["keyword_coverage"].fillna(0).mean(), 3))
        with c3:
            st.metric("Avg Quality Score %", round(work_df["quality_score_percent"].fillna(0).mean(), 2))

        csv_bytes = work_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download summarized CSV",
            data=csv_bytes,
            file_name="summarized_output.csv",
            mime="text/csv"
        )
else:
    st.info("Upload a CSV to begin. You can use the included sample file: ecommerce_text_data.csv")
