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

/* FULL PAGE BACKGROUND ON STREAMLIT APP */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("https://t4.ftcdn.net/jpg/16/97/54/69/360_F_1697546950_YG9PdzRMoRv2owtMUU7T6o0Des5fPAws.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    filter: blur(5px); /* blur effect */
    z-index: -2;
}

/* DARK OVERLAY TO MAKE TEXT READABLE */
.stApp::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.45);
    z-index: -1;
}

/* WHITE CARD */
.card {
    background-color: rgba(255,255,255,0.95);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.3);
    margin-bottom: 25px;
}

/* BADGES */
.badge-success {
    background-color: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    font-size: 18px;
}
.badge-danger {
    background-color: #f8d7da;
    color: #721c24;
    padding: 15px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    font-size: 18px;
}

/* CARD HEADINGS */
h1, h2, h3, h4, h5, h6 {
    color: #000000;
}

/* TEXT INPUTS & SELECTBOXES */
.stTextInput>div>div>input, 
.stSelectbox>div>div>div>select, 
.stNumberInput>div>div>input {
    background-color: rgba(255,255,255,0.95);
    color: #000;
}

</style>
""", unsafe_allow_html=True)



# ---------------- SIDEBAR ----------------
st.sidebar.title("🏦 Loan Dashboard")
page = st.sidebar.radio(
    "Navigation",
    ["Applicant Form", "Summary", "Analytics"]
)

# ---------------- DUMMY DATA ----------------
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

    st.title("Loan Approval Prediction Analysis")

    # CENTER IMAGE
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
        credit_history = st.selectbox("Credit History", [1, 0])

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
            "https://media.assettype.com/gulfnews%2Fimport%2F2023%2F02%2F07%2FStock-Bank-Loan_1862a8288fe_large.jpg",
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

