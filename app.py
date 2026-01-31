import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Loan Approval Prediction Analysis",
    layout="wide"
)

# ---------------- CSS ----------------
css = """
<style>

/* BACKGROUND IMAGE */
[data-testid="stAppViewContainer"] {
    background-image: url("https://t4.ftcdn.net/jpg/16/97/54/69/360_F_1697546950_YG9PdzRMoRv2owtMUU7T6o0Des5fPAws.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* DARK + BLUR OVERLAY */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-color: rgba(0,0,0,0.65);
    backdrop-filter: blur(6px);
    z-index: -1;
}

/* REMOVE HEADER BACKGROUND */
[data-testid="stHeader"] {
    background: transparent;
}

/* MAIN TITLE */
.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: #ffffff;
    margin: 10px 0 30px 0;
    letter-spacing: 1px;
}

/* FORM LABELS */
label,
.stTextInput label,
.stSelectbox label,
.stNumberInput label {
    color: #ffffff !important;
    font-weight: 800;
    font-size: 18px;
}

/* WHITE CARD */
.card {
    background-color: rgba(255,255,255,0.92);
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
    margin-bottom: 30px;
}

/* BUTTON */
.stButton > button {
    font-weight: 800;
    font-size: 16px;
}

/* BADGES */
.badge-success {
    background-color: #d1fae5;
    color: #065f46;
    padding: 18px;
    border-radius: 12px;
    font-weight: 800;
    text-align: center;
    font-size: 22px;
}

.badge-danger {
    background-color: #fee2e2;
    color: #7f1d1d;
    padding: 18px;
    border-radius: 12px;
    font-weight: 800;
    text-align: center;
    font-size: 22px;
}

/* WARNING */
.custom-warning {
    background-color: #fff3cd;
    color: #664d03;
    padding: 18px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 18px;
    text-align: center;
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)

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

# ---------------- PREDICTION LOGIC ----------------
def predict_loan(credit_history, income, loan):
    if credit_history == 1 and income > 5000 and loan < income * 2:
        return "Approved"
    return "Rejected"

# ---------------- APPLICANT FORM ----------------
if page == "Applicant Form":

    st.markdown(
        "<div class='main-title'>Loan Approval Prediction Analysis</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Applicant Name")
        st.selectbox("Gender", df["Gender"])
        credit_history = st.selectbox(
            "Credit History (1 = Good, 0 = Bad)", [1, 0]
        )

    with col2:
        st.selectbox("Married", df["Married"])
        income = st.number_input("Applicant Income", min_value=0)
        loan = st.number_input("Loan Amount", min_value=0)

    if st.button("🔍 Predict Loan"):
        result = predict_loan(credit_history, income, loan)
        st.session_state["result"] = result

        if result == "Approved":
            st.success("🎉 Loan Approved Successfully!")
        else:
            st.error("❌ Loan Rejected")
            st.info(
                "How to improve approval chances:\n"
                "• Maintain good credit score\n"
                "• Increase income\n"
                "• Reduce loan amount\n"
                "• Avoid multiple loan requests"
            )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SUMMARY ----------------
elif page == "Summary":

    st.markdown(
        "<div class='main-title'>Loan Summary</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if "result" in st.session_state:
        if st.session_state["result"] == "Approved":
            st.markdown(
                "<div class='badge-success'>🎉 Congratulations! Your Loan is Approved</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='badge-danger'>❌ Sorry! Your Loan is Rejected</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='custom-warning'>⚠️ Please submit the applicant form first</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
elif page == "Analytics":

    st.markdown(
        "<div class='main-title'>Loan Analytics</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)
