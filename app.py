import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Approval App", layout="wide")

# ----------------------------
# Load and preprocess data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("LP_Train.csv")

    df['Dependents'] = df['Dependents'].replace(r'\+', '', regex=True)
    df['Dependents'] = df['Dependents'].fillna(0).astype(int)

    df['Gender'] = df['Gender'].fillna('Male')
    df['Married'] = df['Married'].fillna('Yes')
    df['Self_Employed'] = df['Self_Employed'].fillna('No')

    df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].mean())
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mean())
    df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mean())

    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

    return df

df = load_data()

# ----------------------------
# Sidebar – User Input
# ----------------------------
st.sidebar.header("Applicant Details")

name = st.sidebar.text_input("Applicant Name")

gender = st.sidebar.selectbox("Gender", df['Gender'].unique())
married = st.sidebar.selectbox("Married", df['Married'].unique())
education = st.sidebar.selectbox("Education", df['Education'].unique())
self_employed = st.sidebar.selectbox("Self Employed", df['Self_Employed'].unique())
property_area = st.sidebar.selectbox("Property Area", df['Property_Area'].unique())

dependents = st.sidebar.number_input("Number of Dependents", min_value=0, max_value=5)
app_income = st.sidebar.number_input("Applicant Income", min_value=0)
coapp_income = st.sidebar.number_input("Co-applicant Income", min_value=0)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=0)
loan_term = st.sidebar.number_input("Loan Amount Term", min_value=0)
credit_history = st.sidebar.selectbox("Credit History", [0.0, 1.0])

# ----------------------------
# Simple Rule-Based Prediction
# ----------------------------
def predict_loan(ch, income, loan_amt):
    if ch == 1.0 and income > loan_amt:
        return "Approved"
    else:
        return "Not Approved"

if st.sidebar.button("Check Loan Status"):
    result = predict_loan(credit_history, app_income + coapp_income, loan_amount)

    st.success(f"Loan Status for **{name}**: **{result}**")

# ----------------------------
# Main Dashboard
# ----------------------------
st.title("🏦 Loan Approval Analysis Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Loan Approval Rate by Gender")
    fig, ax = plt.subplots()
    sb.barplot(x=df.Gender, y=df.Loan_Status, ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Loan Approval Rate by Marital Status")
    fig, ax = plt.subplots()
    sb.barplot(x=df.Married, y=df.Loan_Status, ax=ax)
    st.pyplot(fig)

st.subheader("Loan Approval by Education")
fig, ax = plt.subplots()
sb.barplot(x=df.Education, y=df.Loan_Status, ax=ax)
st.pyplot(fig)

st.subheader("Loan Approval by Property Area")
fig, ax = plt.subplots()
sb.barplot(x=df.Property_Area, y=df.Loan_Status, ax=ax)
st.pyplot(fig)

st.subheader("Correlation Matrix")
st.dataframe(df.corr(numeric_only=True))
