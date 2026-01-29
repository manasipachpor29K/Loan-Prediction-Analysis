import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Loan Approval App", layout="wide", page_icon="🏦")

# ----------------------------
# Dark Theme & Background
# ----------------------------
def set_dark_theme():
    st.markdown(
        """
        <style>
        /* App background */
        [data-testid="stAppViewContainer"] {
            background-color: #0E1117;
            color: #FFFFFF;
        }

        /* Main container */
        [data-testid="stAppViewContainer"] > .main {
            background-color: rgba(14, 17, 23, 0.85);
            padding: 2rem;
            border-radius: 10px;
        }

        /* Titles */
        h1, h2, h3 {
            color: #FFD700;
        }

        /* Table */
        .stTable td, .stTable th {
            color: #FFFFFF;
        }

        /* Form inputs */
        .stTextInput>div>div>input, .stNumberInput>div>input {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }

        /* Buttons */
        div.stButton>button {
            background-color: #FFD700;
            color: #000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_dark_theme()

# ----------------------------
# Load & preprocess data
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

# ----------------------------
# PAGE 1 – USER INPUT
# ----------------------------
if st.session_state.page == 1:
    st.title("🏦 Loan Application – Step 1")
    st.subheader("Enter Applicant Details")

    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=120)

    with st.form("loan_form"):
        name = st.text_input("Applicant Name")
        gender = st.selectbox("Gender", df['Gender'].unique())
        married = st.selectbox("Married", df['Married'].unique())
        education = st.selectbox("Education", df['Education'].unique())
        property_area = st.selectbox("Property Area", df['Property_Area'].unique())
        dependents = st.number_input("Number of Dependents", 0, 5)
        applicant_income = st.number_input("Applicant Income", min_value=0)
        loan_amount = st.number_input("Loan Amount", min_value=0)
        credit_history = st.selectbox("Credit History", [0.0, 1.0])

        next_btn = st.form_submit_button("Next ➡️")

    if next_btn:
        st.session_state.user_data = {
            'Name': name,
            'Gender': gender,
            'Married': married,
            'Education': education,
            'Property Area': property_area,
            'Dependents': dependents,
            'Applicant Income': applicant_income,
            'Loan Amount': loan_amount,
            'Credit History': credit_history
        }
        st.session_state.page = 2
        st.rerun()

# ----------------------------
# PAGE 2 – DETAILS + VISUALIZATION
# ----------------------------
if st.session_state.page == 2:
    st.title("📄 Applicant Summary & Loan Visualization – Step 2")
    st.image("https://www.vecteezy.com/photo/24269311-car-house-personal-money-loan-concept-finance-business-icon-on-wooden-cube-saving-money-for-a-car-money-and-house-wooden-cubes-with-word-loan-copy-space-for-text-loan-payment-car-and-house-wooden-cubes", width=400)

    user = st.session_state.user_data
    result = predict_loan(user['Credit History'], user['Applicant Income'], user['Loan Amount'])

    st.subheader("Entered Details")
    st.table(pd.DataFrame(user.items(), columns=["Field", "Value"]))

    if result == "Approved":
        st.success("🎉 Loan Approved")
    else:
        st.error("❌ Loan Not Approved")
        st.info(
            "💡 Tips to increase approval chances:\n"
            "- Maintain a **good credit history** (Credit History = 1).\n"
            "- Ensure **Applicant Income > Loan Amount**.\n"
            "- Reduce **Loan Amount** requested if possible.\n"
            "- Keep dependents and debt manageable."
        )

    st.subheader("Loan Status vs Applicant Income")
    fig, ax = plt.subplots(figsize=(6, 4))
    sb.scatterplot(x=df['ApplicantIncome'], y=df['LoanAmount'], hue=df['Loan_Status'], palette="coolwarm", ax=ax)
    ax.set_xlabel("Applicant Income")
    ax.set_ylabel("Loan Amount")
    ax.set_title("Loan Amount vs Applicant Income")
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.experimental_rerun()
    with col2:
        if st.button("Next ➡️ Dashboard"):
            st.session_state.page = 3
            st.rerun()

# ----------------------------
# PAGE 3 – DASHBOARD
# -
