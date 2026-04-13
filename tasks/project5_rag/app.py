import pandas as pd
import streamlit as st

st.set_page_config(page_title="E-Commerce Product Discovery Assistant", layout="wide")
st.title("E-Commerce Product Discovery Assistant using RAG")
st.caption("Student mini project: product search, retrieval, and AI-ready recommendations")

@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_products_dataset.csv")

def build_product_text(dataframe):
    text_cols = [
        "product_id", "product_name", "category", "brand", "price",
        "rating", "stock", "discount_percent", "seller", "description"
    ]
    for col in text_cols:
        dataframe[col] = dataframe[col].fillna("").astype(str)

    dataframe["product_text"] = (
        "Product ID: " + dataframe["product_id"] + ". " +
        "Product Name: " + dataframe["product_name"] + ". " +
        "Category: " + dataframe["category"] + ". " +
        "Brand: " + dataframe["brand"] + ". " +
        "Price: " + dataframe["price"] + ". " +
        "Rating: " + dataframe["rating"] + ". " +
        "Stock: " + dataframe["stock"] + ". " +
        "Discount Percent: " + dataframe["discount_percent"] + ". " +
        "Seller: " + dataframe["seller"] + ". " +
        "Description: " + dataframe["description"]
    )
    return dataframe

def simple_retrieve(dataframe, query, top_k=5):
    query_terms = [term.strip().lower() for term in query.replace("/", " ").replace(",", " ").split() if term.strip()]
    matches = []

    for _, row in dataframe.iterrows():
        text = str(row.get("product_text", "")).lower()
        score = sum(1 for term in query_terms if term in text)
        if score > 0:
            try:
                rating = float(row.get("rating", 0))
            except:
                rating = 0
            matches.append((score, row, rating))

    matches.sort(key=lambda x: (x[0], x[2]), reverse=True)
    return [m[1] for m in matches[:top_k]]

df = build_product_text(load_data())

with st.sidebar:
    st.header("Project Snapshot")
    st.metric("Products", len(df))
    st.write("Use this app to simulate product discovery and AI-ready search for an e-commerce catalog.")
    st.write("Students can later connect embeddings, vector DB, and LLM response generation.")

tab1, tab2, tab3 = st.tabs(["Dataset Preview", "Product Search", "Validation Q&A"])

with tab1:
    st.subheader("Catalog Dataset")
    st.dataframe(df.drop(columns=["product_text"]), use_container_width=True)

with tab2:
    st.subheader("Ask a Shopping Query")
    query = st.text_input("Example: show budget-friendly electronics with good ratings", "premium electronics high rating travel friendly")
    top_k = st.slider("Top results", 1, 10, 5)
    if st.button("Search Products"):
        results = simple_retrieve(df, query, top_k=top_k)
        if results:
            st.success("Relevant products retrieved")
            for row in results:
                with st.expander(f"{row['product_name']} | {row['category']} | Rating {row['rating']}"):
                    st.write(f"**Brand:** {row['brand']}")
                    st.write(f"**Price:** ₹{row['price']}")
                    st.write(f"**Discount:** {row['discount_percent']}%")
                    st.write(f"**Stock:** {row['stock']}")
                    st.write(f"**Seller:** {row['seller']}")
                    st.write(f"**Description:** {row['description']}")
        else:
            st.warning("No matching products found.")

with tab3:
    st.subheader("Validation Questions")
    qa = pd.read_csv("Ecommerce_QA_Validation.csv")
    st.dataframe(qa, use_container_width=True)