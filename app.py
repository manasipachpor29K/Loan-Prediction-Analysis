import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Loan Approval Prediction Analysis",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background-image: url("https://t4.ftcdn.net/jpg/16/97/54/69/360_F_1697546950_YG9PdzRMoRv2owtMUU7T6o0Des5fPAws.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* DARK OVERLAY */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-color: rgba(0,0,0,0.55);
    z-index: -1;
}

/* REMOVE HEADER BG */
[data-testid="stHeader"] {
    background: transparent;
}

/* MAIN TITLE */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 10px;
    margin-bottom: 30px;
}

/* WHITE CARD */
.card {
    background-color: rgba(255,255,255,0.96);
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.35);
    margin-bottom: 30px;
}

/* BADGES */
.badge-success {
    background-color: #d1fae5;
    color: #065f46;
    padding: 18px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    font-size: 22px;
}
.badge-danger {
    background-color: #fee2e2;
    color: #7f1d1d;
    padding: 18px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    font-size: 22px;
}

/* POPUP MESSAGES FIX */
.stSuccess {
    background-color: #ecfdf5 !important;
    color: #065f46 !important;
    border-radius: 10px;
}
.stError {
    background-color: #fef2f2 !important;
    color: #7f1d1d !important;
    border-radius: 10px;
}
.stInfo {
    background-color: #eff6ff !important;
    color: #1e3a8a !important;
    border-radius: 10px;
}

/* INPUT FIELDS */
.stTextInput input,
.stSelectbox select,
.stNumberInput input {
    background-color: #ffffff !important;
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏦 Loan Dashboard")
page = st.sidebar.radio(
    "Navigation",
    ["Applicant Form", "Summary", "Analytics"]
)

# ---------------- DATA ----------------
df = pd.DataFrame({
    "Gender": ["Male", "Female"],
    "Married": ["Yes", "No"]
})

# ---------------- LOGIC ----------------
def predict_loan(credit_history, income, loan):
    if credit_history == 1 and income > 5000 and loan < income * 2:
        return "Approved"
    else:
        return "Rejected"

# ================= PAGE 1 =================
if page == "Applicant Form":

    # 🔥 TOP TITLE (WHITE & BOLD)
    st.markdown(
        "<div class='main-title'>Loan Approval Prediction Analysis</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Applicant Name")
        gender = st.selectbox("Gender", df["Gender"])
        credit_history = st.selectbox("Credit History (1 = Good, 0 = Bad)", [1, 0])

    with col2:
        married = st.selectbox("Married", df["Married"])
        income = st.number_input("Applicant Income", min_value=0)
        loan = st.number_input("Loan Amount", min_value=0)

    if st.button("🔍 Predict Loan"):
        result = predict_loan(credit_history, income, loan)
        st.session_state.result = result

        if result == "Approved":
            st.success("🎉 Loan Approved Successfully!")
        else:
            st.error("❌ Loan Rejected")
            st.info("""
            **How to improve approval chances:**
            • Maintain good credit score  
            • Increase income  
            • Reduce loan amount  
            • Avoid multiple loan requests
            """)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PAGE 2 =================
elif page == "Summary":

    st.markdown(
        "<div class='main-title'>Loan Summary</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if "result" in st.session_state:
        if st.session_state.result == "Approved":
            st.markdown(
                "<d
