import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report, roc_auc_score

st.set_page_config(page_title="Ecommerce Return Classification", layout="wide")
st.title("Ecommerce Return Prediction using Logistic Regression")

@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_classification_data.csv")

@st.cache_resource
def train_model(df):
    X = df.drop(columns=['returned', 'order_id'])
    y = df['returned']

    categorical_features = X.select_dtypes(include='object').columns.tolist()
    numerical_features = X.select_dtypes(exclude='object').columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000))
    ])

    model.fit(X_train, y_train)
    return model, X_test, y_test, categorical_features, numerical_features

df = load_data()
model, X_test, y_test, categorical_features, numerical_features = train_model(df)

st.subheader("Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rows", len(df))
with col2:
    st.metric("Columns", df.shape[1])
with col3:
    st.metric("Return Rate", f"{df['returned'].mean()*100:.2f}%")

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

st.subheader("Model Performance")
c1, c2 = st.columns(2)
with c1:
    st.write("**Accuracy:**", round(accuracy_score(y_test, y_pred), 4))
with c2:
    st.write("**ROC-AUC:**", round(roc_auc_score(y_test, y_prob), 4))

st.text("Classification Report")
st.code(classification_report(y_test, y_pred))

fig, ax = plt.subplots()
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax)
st.pyplot(fig)

st.subheader("Predict Return for a New Order")

col1, col2, col3, col4 = st.columns(4)
with col1:
    product_category = st.selectbox("Product Category", sorted(df["product_category"].unique()))
    unit_price = st.number_input("Unit Price", min_value=50.0, max_value=10000.0, value=1500.0, step=50.0)
with col2:
    customer_segment = st.selectbox("Customer Segment", sorted(df["customer_segment"].unique()))
    quantity = st.number_input("Quantity", min_value=1, max_value=10, value=2, step=1)
with col3:
    payment_method = st.selectbox("Payment Method", sorted(df["payment_method"].unique()))
    discount_percent = st.slider("Discount Percent", min_value=0, max_value=50, value=10)
with col4:
    region = st.selectbox("Region", sorted(df["region"].unique()))
    customer_rating = st.slider("Customer Rating", min_value=2.5, max_value=5.0, value=4.0, step=0.1)

input_df = pd.DataFrame([{
    "product_category": product_category,
    "customer_segment": customer_segment,
    "payment_method": payment_method,
    "region": region,
    "unit_price": unit_price,
    "quantity": quantity,
    "discount_percent": discount_percent,
    "customer_rating": customer_rating
}])

if st.button("Predict"):
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.write("### Prediction Result")
    st.write("Predicted Class:", "Returned" if prediction == 1 else "Not Returned")
    st.write("Probability of Return:", round(float(probability), 4))
    st.dataframe(input_df, use_container_width=True)

st.subheader("Sample Test Predictions")
sample_results = X_test.head(15).copy()
sample_results["actual_returned"] = y_test.head(15).values
sample_results["predicted_returned"] = model.predict(X_test.head(15))
sample_results["return_probability"] = model.predict_proba(X_test.head(15))[:, 1].round(4)
st.dataframe(sample_results, use_container_width=True)
