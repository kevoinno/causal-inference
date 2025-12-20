import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from methods.ab_testing import calculate_sample_size

st.set_page_config(layout="wide")

st.title("A/B Testing")

st.subheader("Sample Size Calculator")
st.subheader("Choose test type")

METRIC_TYPES = {"MEAN": "Mean (e.g. revenue)", "RATE": "Rate (e.g. conversion rate)"}

selected_metric = st.selectbox(
    "Please select what type of metric you are testing",
    (METRIC_TYPES["MEAN"], METRIC_TYPES["RATE"]),
)
st.caption(
    """Fill in the parameters to calculate the appropriate sample size you need for each group.
    Standard values for significance level and power are already inputted."""
)

main_col_left, main_col_right = st.columns([1, 1])

with main_col_left:
    st.subheader("⚙️ Parameters")
    col1, col2 = st.columns(2)

    with col1:
        alpha = st.number_input(
            "Significance Threshold (α)",
            value=0.05,
            placeholder="e.g., 0.05",
            min_value=0.0,
            step=0.01,
            max_value=1.0,
            help="The chance your test finds a significant effect when there is not one (e.g. 0.05 = 5% chance of false positive).",
        )
        power = st.number_input(
            "Power (1-β)",
            value=0.8,
            placeholder="e.g., 0.8",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            help="The chance your test finds a significant effect when there is one (e.g. 0.8 = 80% chance of correctly detecting a signifcant effect)",
        )

    with col2:
        delta = st.number_input(
            "Delta (Minimum Detectable Effect)",
            value=None,
            placeholder="e.g., 0.1",
            min_value=0.001,
            step=0.01,
            help="""The smallest absolute effect you want your test to reliably detect. Enter the exact number, not a percentage.

- For rates (e.g., conversion rate): If your baseline is 10% and you want to detect a 2 percentage point change, enter 0.02.
- For means (e.g., revenue): If you want to detect at least a $5 difference, enter 5.""",
        )
        if selected_metric == METRIC_TYPES["MEAN"]:
            variance = st.number_input(
                "Variance of the target metric",
                value=None,
                placeholder="e.g., 1.0",
                min_value=0.0,
                step=0.1,
                help="How spread out your target metric (e.g. revenue) is for your population.",
            )
        else:
            baseline_rate = st.number_input(
                "Baseline rate",
                value=None,
                placeholder="e.g., 0.1 = 10%",
                min_value=0.0,
                max_value=1.0,
                step=0.1,
                help="""Baseline rate (e.g. conversion rate) for your population that you want to test

- e.g. 10% conversion rate = 0.1
                """,
            )
            variance = (
                baseline_rate * (1 - baseline_rate)
                if baseline_rate is not None
                else None
            )

    # advanced option setting to adjust test allocation ratio
    with st.expander("Advanced Options"):
        ratio = st.number_input(
            "Test Split Ratio (Treated v.s. Control)",
            value=0.5,
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
                st.session_state["result"] = result
            except Exception as e:
                st.error(f"Calculation error: {str(e)}")

with main_col_right:
    st.subheader("Calculated Sample Sizes")
    if "result" in st.session_state:
        result = st.session_state["result"]
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
                    help=f"Control + Treated = {result['n_control']} + {
                        result['n_treated']
                    } = {result['n_control'] + result['n_treated']}",
                )
