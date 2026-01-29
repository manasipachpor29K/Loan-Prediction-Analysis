import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Approval App", layout="wide")


# ----------------------------
# Set Background Image
# ----------------------------
def set_bg_image():
    st.markdown(
        f"""
        <style>
        /* Target the main app background */
        [data-testid="stAppViewContainer"] {{
            background-image: url("https://images.unsplash.com/photo-1581091215364-9c6b0e2f2e64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Optional: set container opacity so text is readable */
        [data-testid="stAppViewContainer"] > .main {{
            background-color: rgba(255, 255, 255, 0.8);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_image()

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

# ----------------------------
# PAGE 1 – USER INPUT
# ----------------------------
if st.session_state.page == 1:
    st.title("🏦 Loan Application – Step 1")
    st.subheader("Enter Applicant Details")

    # Loan Image
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
# PAGE 2 – DETAILS + RESULT
# ----------------------------
if st.session_state.page == 2:
    st.title("📄 Applicant Summary – Step 2")

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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.experimental_rerun()
    with col2:
        if st.button("View Analysis ➡️"):
            st.session_state.page = 3
            st.rerun()

# ----------------------------
# PAGE 3 – DASHBOARD
# ----------------------------
if st.session_state.page == 3:
    st.title("📊 Loan Approval Analysis – Step 3")

    palette = sb.color_palette("pastel")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Loan Approval by Gender")
        fig, ax = plt.subplots(figsize=(4, 3))  # smaller size
        sb.barplot(x=df.Gender, y=df.Loan_Status, ax=ax, palette=palette)
        ax.set_ylabel("Approval Rate")
        st.pyplot(fig)

    with col2:
        st.subheader("Loan Approval by Marital Status")
        fig, ax = plt.subplots(figsize=(4, 3))
        sb.barplot(x=df.Married, y=df.Loan_Status, ax=ax, palette=palette)
        ax.set_ylabel("Approval Rate")
        st.pyplot(fig)

    st.subheader("Loan Approval by Education")
    fig, ax = plt.subplots(figsize=(4, 3))
    sb.barplot(x=df.Education, y=df.Loan_Status, ax=ax, palette=palette)
    ax.set_ylabel("Approval Rate")
    st.pyplot(fig)

    st.subheader("Loan Approval by Property Area")
    fig, ax = plt.subplots(figsize=(4, 3))
    sb.barplot(x=df.Property_Area, y=df.Loan_Status, ax=ax, palette=palette)
    ax.set_ylabel("Approval Rate")
    st.pyplot(fig)

    if st.button("⬅️ Back to Summary"):
        st.session_state.page = 2
        st.rerun()
