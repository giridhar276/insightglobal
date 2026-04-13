import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.set_page_config(page_title="Ecommerce Sales Prediction", layout="wide")
st.title("Ecommerce Sales Prediction using Linear Regression")

@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_regression_data.csv")

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

X = df.drop("sales_amount", axis=1)
y = df["sales_amount"]

categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numerical_cols = X.select_dtypes(exclude=["object"]).columns.tolist()

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

numerical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

preprocessor = ColumnTransformer(transformers=[
    ("cat", categorical_pipeline, categorical_cols),
    ("num", numerical_pipeline, numerical_cols)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

st.subheader("Model Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("MAE", f"{mae:.2f}")
c2.metric("MSE", f"{mse:.2f}")
c3.metric("RMSE", f"{rmse:.2f}")
c4.metric("R2 Score", f"{r2:.4f}")

st.subheader("Actual vs Predicted")
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(y_test, y_pred, alpha=0.7)
ax.set_xlabel("Actual Sales")
ax.set_ylabel("Predicted Sales")
ax.set_title("Actual vs Predicted Sales")
st.pyplot(fig)

st.subheader("Predict Sales for New Input")

col1, col2, col3 = st.columns(3)

with col1:
    product_category = st.selectbox("Product Category", sorted(df["product_category"].dropna().unique()))
    customer_segment = st.selectbox("Customer Segment", sorted(df["customer_segment"].dropna().unique()))
    payment_method = st.selectbox("Payment Method", sorted(df["payment_method"].dropna().unique()))

with col2:
    units_sold = st.number_input("Units Sold", min_value=1, max_value=20, value=5)
    discount_pct = st.slider("Discount %", min_value=0, max_value=50, value=10)
    ad_spend = st.number_input("Ad Spend", min_value=0.0, value=3000.0, step=100.0)

with col3:
    customer_rating = st.slider("Customer Rating", min_value=1.0, max_value=5.0, value=4.2, step=0.1)
    returns_count = st.number_input("Returns Count", min_value=0, max_value=10, value=0)
    is_festival_season = st.selectbox("Festival Season", [0, 1])

if st.button("Predict Sales"):
    input_df = pd.DataFrame([{
        "product_category": product_category,
        "customer_segment": customer_segment,
        "payment_method": payment_method,
        "units_sold": units_sold,
        "discount_pct": discount_pct,
        "ad_spend": ad_spend,
        "customer_rating": customer_rating,
        "returns_count": returns_count,
        "is_festival_season": is_festival_season
    }])

    prediction = model.predict(input_df)[0]
    st.success(f"Predicted Sales Amount: {prediction:.2f}")

st.subheader("How to Run")
st.code("pip install streamlit pandas scikit-learn matplotlib\nstreamlit run streamlit_app.py", language="bash")
