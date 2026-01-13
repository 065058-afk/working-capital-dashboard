import streamlit as st
import pandas as pd

st.set_page_config(page_title="Working Capital Dashboard", layout="wide")

st.title("📊 Working Capital Optimization Dashboard")

# Load data
ar = pd.read_csv("AR_Big.csv")

# KPIs
avg_dso = (ar["delay_days"] * ar["invoice_amount"]).sum() / ar["invoice_amount"].sum()

st.metric("Average DSO (Days)", round(avg_dso, 2))

# Slider
reduction = st.slider("Credit Policy Tightening (Days)", 0, 15, 5)

ar["optimized_delay"] = (ar["delay_days"] - reduction).clip(lower=0)
opt_dso = (ar["optimized_delay"] * ar["invoice_amount"]).sum() / ar["invoice_amount"].sum()

st.metric("Optimized DSO (Days)", round(opt_dso, 2))

st.metric("DSO Reduction", round(avg_dso - opt_dso, 2))

# Table
st.subheader("Accounts Receivable Data")
st.dataframe(ar.head(100))
