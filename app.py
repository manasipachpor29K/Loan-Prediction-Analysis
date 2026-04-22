
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Loan Approval Prediction Analysis",
    page_icon="🏦",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.metric-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center
}
.badge-success {
    background-color: #d4edda;
    color: #155724;
    padding: 12px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center
}
.badge-danger {
    background-color: #f8d7da;
    color: #721c24;
    padding: 12px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("LP_Train.csv")
    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    return df

df = load_data()

# ---------------------------------------------------
# EMI CALCULATION
# ---------------------------------------------------
def calculate_emi(loan, annual_rate=10, years=20):
   

# ---------------------------------------------------
# LOAN PREDICTION LOGIC
# ---------------------------------------------------
def predict_loan(credit_history, monthly_income, loan_amount):
    emi = calculate_emi(loan_amount)
    if credit_history == 1.0 and emi <= monthly_income * 0.4:
        return "Approved", emi
    return "Rejected"

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("🏦 Loan Dashboard")
page = st.sidebar.radio(
    "Navigation",
    ["Applicant Form", "Summary", "Analytics"]
)

# ---------------------------------------------------
# PAGE 1: APPLICANT FORM
# ---------------------------------------------------
if page == "Applicant Form":

    # ✅ HEADLINE RESTORED
    st.title("Loan Approval Prediction Analysis")
    st.subheader("Enter applicant details to check loan eligibility")
    st.progress(33)

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Applicant Name")
        gender = st.selectbox("Gender", ["Male", "Female"])
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        credit_history = st.selectbox("Credit History", [1.0, 0.0])
        monthly_income = st.number_input("Monthly Income (₹)", min_value=0)

    with col2:
        married = st.selectbox("Married", ["Yes", "No"])
        dependents = st.number_input("Dependents", 0, 5)
        loan_amount = st.number_input("Loan Amount (₹)", min_value=0)

    if st.button("🔍 Predict Loan"):

        if name.strip() == "" or monthly_income == 0 or loan_amount == 0:
            st.warning("⚠️ Please !! Enter the Applicant Details ..")
        else:
            result, emi = predict_loan(
                credit_history, monthly_income, loan_amount
            )

            st.session_state.user_data = {
                "Name": name,
                "Gender": gender,
                "Education": education,
                "Married": married,
                "Dependents": dependents,
                "Income": monthly_income,
                "Loan Amount": loan_amount,
                "Credit History": credit_history,
                "Estimated EMI": round(emi, 2)
            }
            st.session_state.result = result

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write(f"💰 **Estimated EMI:** ₹{emi:,.2f}")

            if result == "Approved":
                st.success("🎉 Loan Approved")
                st.write("✅ EMI is within 40% of monthly income")
            else:
                st.error("❌ Loan Rejected")
                st.write("❌ EMI exceeds 40% of monthly income")

            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# PAGE 2: SUMMARY
# ---------------------------------------------------
if page == "Summary":

    st.title("📄 Applicant Summary")
    st.progress(66)

    if "user_data" not in st.session_state:
        st.warning("⚠️ Please fill the Applicant Form first.")
    else:
        user = st.session_state.user_data
        result = st.session_state.result

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.table(pd.DataFrame(user.items(), columns=["Field", "Value"]))

        if result == "Approved":
            st.markdown(
                "<div class='badge-success'>🎉 Loan Approved</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='badge-danger'>❌ Loan Rejected</div>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# PAGE 3: ANALYTICS
# ---------------------------------------------------
if page == "Analytics":

    st.title("📊 Loan Approval Analysis")
    st.progress(100)

    col1, col2, col3 = st.columns(3)

    col1.markdown(
        f"<div class='metric-card'>Approval Rate<br><h2>{df.Loan_Status.mean()*100:.1f}%</h2></div>",
        unsafe_allow_html=True
    )
    col2.markdown(
        f"<div class='metric-card'>Average Loan<br><h2>{df.LoanAmount.mean():.0f}</h2></div>",
        unsafe_allow_html=True
    )
    col3.markdown(
        f"<div class='metric-card'>Applicants<br><h2>{len(df)}</h2></div>",
        unsafe_allow_html=True
    )

    fig1 = px.bar(df, x="Gender", y="Loan_Status", title="Approval by Gender", color="Gender")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(df, x="Education", y="Loan_Status", title="Approval by Education", color="Education")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(df, x="Property_Area", y="Loan_Status", title="Approval by Property Area", color="Property_Area")
    st.plotly_chart(fig3, use_container_width=True)

   
