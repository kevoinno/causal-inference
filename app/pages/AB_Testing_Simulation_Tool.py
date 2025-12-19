import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add the parent directory to the Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# import A/B testing functions
from methods.ab_testing import calculate_sample_size


st.title("A/B Testing")

st.subheader("Sample Size Calculator")
st.subheader("⚙️ Parameters")

st.caption(
    "Fill in the parameters to calculate the appropriate sample size you need for each group"
)

col1, col2 = st.columns(2)

with col1:
    alpha = st.number_input(
        "Significance Threshold (alpha)",
        value=None,
        placeholder="e.g., 0.05",
        min_value=0.0,
        step=0.01,
        max_value=1.0,
        help="The chance your test finds a significant effect when there is not one (e.g. 0.05 = 5% chance of false positive).",
    )
    power = st.number_input(
        "Power (chance your test correctly finds an effect)",
        value=None,
        placeholder="e.g., 0.8",
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        help="The chance your test finds a significant effect when there is one (e.g. 0.8 = 80% chance of correctly detecting a signifcant effect)",
    )


with col2:
    delta = st.number_input(
        "Delta (minimum absolute effect size to detect)",
        value=None,
        placeholder="e.g., 0.1",
        min_value=0.001,
        step=0.01,
        help="The smallest absolute effect size your test can reliably detect (e.g., 0.1 means a 10% improvement in your metric).",
    )
    variance = st.number_input(
        "Variance of the target metric (Use p(1-p) if testing a rate)",
        value=None,
        placeholder="e.g., 1.0",
        min_value=0.0,
        step=0.1,
        help="How spread out your target metric is (e.g., 1.0 means typical values vary around the average by about 1 unit).",
    )
    ratio = st.number_input(
        "Ratio (proportion treated)",
        value=None,
        placeholder="e.g., 0.5",
        min_value=0.01,
        max_value=0.99,
        step=0.01,
        help="Proportion of users in treated group (e.g., 0.9 for 90% treated, 10% control).",
    )

if st.button("Calculate sample size", type="primary"):
    # Validate all inputs are provided
    if (
        alpha is None
        or power is None
        or delta is None
        or variance is None
        or ratio is None
    ):
        st.error("Please fill in all parameters before calculating.")
    else:
        try:
            result = calculate_sample_size(alpha, power, delta, variance, ratio)
            st.subheader("📊 Required Sample Sizes")

            col_control, col_treated = st.columns(2)
            with col_control:
                with st.container(border=True):
                    st.metric("Control Group", f"{result['n_control']}")
            with col_treated:
                with st.container(border=True):
                    st.metric("Treated Group", f"{result['n_treated']}")

            _, col_total, _ = st.columns([1, 2, 1])
            with col_total:
                with st.container(border=True):
                    st.metric(
                        "Total Sample Size",
                        f"{result['n_total']}",
                        help=f"Control + Treated = {result['n_control']} + {result['n_treated']} = {result['n_control'] + result['n_treated']}",
                    )
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")
