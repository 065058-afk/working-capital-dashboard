import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Working Capital Optimization Dashboard",
    layout="wide"
)

st.title("📊 Working Capital Optimization Dashboard")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
ar = pd.read_csv("AR_Big.csv")

required_cols = {"delay_days", "invoice_amount", "channel"}
if not required_cols.issubset(ar.columns):
    st.error("AR_Big.csv does not have required columns.")
    st.stop()

# --------------------------------------------------
# AVERAGE DSO
# --------------------------------------------------
avg_dso = (
    ar["delay_days"].clip(lower=0) * ar["invoice_amount"]
).sum() / ar["invoice_amount"].sum()

st.metric("Average DSO (Days)", round(avg_dso, 2))

# --------------------------------------------------
# WHAT-IF SLIDER
# --------------------------------------------------
st.subheader("What-if Analysis: Delay Reduction")

reduction = st.slider(
    "Reduce delay days by",
    min_value=0,
    max_value=20,
    value=5
)

ar["optimized_delay_days"] = (
    ar["delay_days"] - reduction
).clip(lower=0)

opt_dso = (
    ar["optimized_delay_days"] * ar["invoice_amount"]
).sum() / ar["invoice_amount"].sum()

st.metric("Optimized DSO (Days)", round(opt_dso, 2))
st.metric("DSO Reduction", round(avg_dso - opt_dso, 2))

# --------------------------------------------------
# CHANNEL ANALYSIS
# --------------------------------------------------
st.subheader("Channel-wise Invoice Value")

channel_sales = (
    ar.groupby("channel")["invoice_amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(channel_sales)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
st.subheader("Accounts Receivable Sample")
st.dataframe(ar.head(100))
