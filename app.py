import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Loan Approval App", layout="wide", page_icon="🏦")

# ----------------------------
# CSS for dark theme, fonts, and white form labels
# ----------------------------
st.markdown("""
<style>
/* Full-page dark gradient background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #E0E0E0;
}

/* Header dark */
[data-testid="stHeader"] {
    background-color: #1E1E1E;
}

/* Buttons */
.stButton>button {
    background-color: #BB86FC;
    color: black;
    font-weight: bold;
}

/* Card/container style */
.st-bk {
    background-color: rgba(30,30,30,0.85) !important;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

/* Centered hero image container */
.hero-image {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

/* Center form */
.form-center {
    display: flex;
    justify-content: center;
}

/* Top bold title with custom font */
.top-title {
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    font-size: 36px;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 20px;
}

/* White labels for form fields */
.css-1aumxhk, .stTextInput>label, label, .st-bk label {
    color: white !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load CSV data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("LP_Train.csv")
    df['Dependents'] = df['Dependents'].replace(r'\+', '', regex=True).fillna(0).astype(int)
    df['Gender'] = df['Gender'].fillna('Male')
    df['Married'] = df['Married'].fillna('Yes')
    df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].mean())
    df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mean())
    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    return df

df = load_data()

# ----------------------------
# Session state
# ----------------------------
if 'page' not in st.session_state:
    st.session_state.page = 1

# ----------------------------
# Prediction function
# ----------------------------
def predict_loan(ch, income, loan_amt):
    return "Approved" if ch == 1.0 and income > loan_amt else "Not Approved"

# ----------------------------
# PAGE 1 – User Input
# ----------------------------
if st.session_state.page == 1:
    st.markdown("<div class='st-bk'>", unsafe_allow_html=True)
    
    # Top bold title
    st.markdown('<div class="top-title">Loan Approval Prediction Analysis</div>', unsafe_allow_html=True)

    # Hero image centered
    st.markdown('<div class="hero-image">', unsafe_allow_html=True)
    st.image(
        "https://daxg39y63pxwu.cloudfront.net/images/blog/loan-prediction-using-machine-learning-project-source-code/Loan_Prediction_using__Machine_Learning_Project.webp",
        width=350
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Enter Applicant Details")

    # Form in two columns
    with st.form("loan_form"):
        col1, col2 = st.columns([1,1])
        with col1:
            name = st.text_input("Name")
            gender = st.selectbox("Gender", df['Gender'].unique())
            married = st.selectbox("Married", df['Married'].unique())
            education = st.selectbox("Education", df['Education'].unique())
        with col2:
            property_area = st.selectbox("Property Area", df['Property_Area'].unique())
            dependents = st.slider("Number of Dependents", 0, 5)
            applicant_income = st.number_input("Applicant Income", min_value=0, step=500)
            loan_amount = st.number_input("Loan Amount", min_value=0, step=1000)
            credit_history = st.radio("Credit History", [0.0, 1.0], format_func=lambda x: "Good" if x==1.0 else "Bad")
        
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

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# PAGE 2 – Summary & Result
# ----------------------------
if st.session_state.page == 2:
    st.markdown("<div class='st-bk'>", unsafe_allow_html=True)
    st.title("📄 Applicant Summary - Step 2")

    user = st.session_state.user_data
    result = predict_loan(user['Credit History'], user['Applicant Income'], user['Loan Amount'])

    st.subheader("Entered Details")
    st.table(pd.DataFrame(user.items(), columns=["Field", "Value"]))

    if result == "Approved":
        st.success("🎉 Loan Approved")
    else:
        st.error("❌ Loan Not Approved")
        st.info(
            "💡 Tips:\n"
            "- Maintain a good credit history\n"
            "- Applicant Income > Loan Amount\n"
            "- Reduce requested Loan Amount\n"
            "- Manage dependents/debts"
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.rerun()
    with col2:
        if st.button("View Analysis ➡️"):
            st.session_state.page = 3
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# PAGE 3 – Dashboard / Analysis
# ----------------------------
if st.session_state.page == 3:
    st.markdown("<div class='st-bk'>", unsafe_allow_html=True)
    st.title("📊 Loan Approval Analysis")

    view_option = st.radio("Choose view:", ["Data Table", "Graphs"])

    if view_option == "Data Table":
        st.data
