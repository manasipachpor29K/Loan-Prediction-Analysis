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

/* MAIN BACKGROUND */
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
    background-color: rgba(0,0,0,0.45);
    z-index: -1;
}

/* REMOVE STREAMLIT DEFAULT BACKGROUND */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* WHITE CARD */
.card {
    background-color: rgba(255,255,255,0.95);
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.35);
    margin-bottom: 30px;
}

/* BADGES */
.badge-success {
    background-color: #d4edda;
    color: #155724;
    padding: 16px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    font-size: 20px;
}
.badge-danger {
    background-color: #f8d7da;
    color: #721c24;
    padding: 16px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    font-size: 20px;
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

# ---------------- SAMPLE DATA ----------------
df = pd.DataFrame({
    "Gender": ["Male", "Female"],
    "Married": ["Yes", "No"]
})

# ---------------- PREDICTION LOGIC ----------------
def predict_loan(credit_history, income, loan):
    if credit_history == 1 and income > 5000 and loan < income * 2:
        return "Approved"
    else:
        return "Rejected"

# ---------------- PAGE 1: APPLICANT FORM ----------------
if page == "Applicant Form":

    st.title("💳 Loan Approval Prediction Analysis")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(
            "https://www.cashe.co.in/wp-content/uploads/2024/01/Loan_Term.png",
            width=380
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
            st.success("🎉 Loan Approved")
        else:
            st.error("❌ Loan Rejected")
            st.info("""
            **Tips to Improve Approval:**
            - Maintain good credit history  
            - Increase monthly income  
            - Reduce loan amount  
            - Avoid multiple loan applications
            """)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PAGE 2: SUMMARY ----------------
elif page == "Summary":

    st.title("📄 Loan Summary")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(
            "https://media.assettype.com/gulfnews/import/2023/02/07/Stock-Bank-Loan_1862a8288fe_large.jpg",
            width=420
        )

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if "result" in st.session_state:
        if st.session_state.result == "Approved":
            st.markdown(
                "<div class='badge-success'>🎉 Congratulations! Loan Approved</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='badge-danger'>❌ Loan Rejected</div>",
                unsafe_allow_html=True
            )
    else:
        st.warning("Please submit the applicant form first.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PAGE 3: ANALYTICS ----------------
elif page == "Analytics":

    st.title("📊 Loan Analytics")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Sample Dataset")
    st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)
