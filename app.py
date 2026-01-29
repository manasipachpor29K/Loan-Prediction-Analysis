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

    df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].mean())
    df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mean())

    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    return df

df = load_data()

# ----------------------------
# Session State
# ----------------------------
if 'page' not in st.session_state:
    st.session_state.page = 1

# ----------------------------
# Prediction Logic
# ----------------------------
def predict_loan(ch, income, loan_amt):
    if ch == 1.0 and income > loan_amt:
        return "Approved"
    else:
        return "Not Approved"

# ============================
# PAGE 1 – USER INPUT
# ============================
if st.session_state.page == 1:
    st.title("🏦 Loan Application – Step 1")
    st.subheader("Enter Applicant Details")

    # Image
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135706.png",
        width=130
    )

    with st.form("loan_form"):
        name = st.text_input("Applicant Name")
        gender = st.selectbox("Gender", df['Gender]()
