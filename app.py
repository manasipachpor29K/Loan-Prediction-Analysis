import streamlit as st
import pandas as pd
import plotly.express as px

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
.main {
    background-color: #f5f7fb;
}
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
    text-align: center;
}
.badge-success {
    background-color: #d4edda;
    color: #155724;
    padding: 12px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
}
.badge-danger {
    background-color: #f8d7da;
    color: #721c24;
    padding: 12px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("LP_Train.csv")

    df['Dependents'] = df['Dependents'].replace(r'\+', '', regex=True)
    df['Dependents'] = df['Dependents'].fillna(0).astype(int)

    df['Gender'] = df['Gender'].fillna('Male')
    df['Married'] = df['Married'].fillna('Yes')

    df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].mean())
    df['Credit_History'] = df['Credit_History'].fillna(1.0)

    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    return df

df = load_data()

# ---------------------------------------------------
# SIMPLE PREDICTION LOGIC
# ---------------------------------------------------
def predict_loan(credit_history, income, loan_amount):
    if credit_history == 1.0 and income > loan_amount:
        return "Approved"
    else:
        return "Rejected"

# ---------------------------------------------------
# SIDEBAR NAVIGATION
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

    st.title("Loan Approval Prediction Analysis")

    # 🔹 CENTERED IMAGE
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://www.cashe.co.in/wp-content/uploads/2024/01/Loan_Term.png",
            width=400
        )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.progress(33)

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Applicant Name")
        gender = st.selectbox("Gender", df['Gender'].unique())
        education = st.selectbox("Education", df['Education'].unique())
        credit_history = st.selectbox("Credit History", [1.0, 0.0])

    with col2:
        married = st.selectbox("Married", df['Married'].unique())
        dependents = st.number_input("Dependents", 0, 5)
        applicant_income = st.number_input("Applicant Income", min_value=0)
        loan_amount = st.number_input("Loan Amount", min_value=0)

    if st.button("🔍 Predict Loan"):
        st.session_state.user_data = {
            "Name": name,
            "Gender": gender,
            "Education": education,
            "Married": married,
            "Dependents": dependents,
            "Income": applicant_income,
            "Loan Amount": loan_amount,
            "Credit History": credit_history
        }

        result = predict_loan(credit_history, applicant_income, loan_amount)
        st.session_state.result = result

        if result == "Approved":
            st.success("🎉 Loan Approved")
        else:
            st.error("❌ Loan Rejected")
            with st.expander("💡 Tips to Improve Loan Approval"):
                st.markdown("""
                ✅ Improve your credit score  
                ✅ Reduce loan amount  
                ✅ Increase income or add co-applicant  
                ✅ Clear existing EMIs  
                ✅ Maintain stable job
                """)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# PAGE 2: SUMMARY
# ---------------------------------------------------
if page == "Summary":

    st.title("📄 Applicant Summary")
    st.progress(66)

    # ➤ NEW IMAGE ON SECOND PAGE (CENTERED)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://media.assettype.com/gulfnews%2Fimport%2F2023%2F02%2F07%2FStock-Bank-Loan_1862a8288fe_large.jpg?w=640&auto=format%2Ccompress&fit=max",
            width=450
        )

    if "user_data" not in st.session_state:
        st.warning("⚠️ Please fill the Applicant Form and Predict Loan first.")
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

    st.subheader("📄 Raw Loan Dataset")
    st.dataframe(df, use_container_width=True)
