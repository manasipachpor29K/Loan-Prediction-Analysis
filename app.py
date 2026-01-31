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

/* REMOVE DEFAULT HEADER */
[data-testid="stHeader"] {
    background: transparent;
}

/* REMOVE EXTRA WHITE BAR UNDER TITLE */
[data-testid="stVerticalBlock"] > div:has(h1) + div {
    display: none;
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
.stButton>button {
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
    te
