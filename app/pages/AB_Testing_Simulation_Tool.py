import streamlit as st
import sys
import os
from datetime import date, timedelta

# Add the parent directory to the Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from methods.ab_testing import calculate_sample_size, calculate_test_length

st.set_page_config(layout="wide")

st.title("A/B Testing")

st.subheader("Sample Size Calculator")
st.subheader("Choose test type")

METRIC_TYPES = {"MEAN": "Mean (e.g. revenue)", "RATE": "Rate (e.g. conversion rate)"}

selected_metric = st.radio(
    "Please select what type of metric you are testing",
    (METRIC_TYPES["MEAN"], METRIC_TYPES["RATE"]),
    horizontal=True,
)
st.caption(
    """Fill in the parameters to calculate the appropriate sample size you need for each group.
    Standard values for significance level and power are already inputted."""
)

# Set conditional help and placeholder for delta based on metric type
if selected_metric == METRIC_TYPES["RATE"]:
    delta_help = """The smallest absolute effect you want your test to reliably detect. Enter the change in percentage points.

- For rates (e.g., conversion rate): If your baseline is 10% and you want to detect a 2 percentage point change, enter 2."""
    delta_placeholder = "e.g., 2.0"
else:
    delta_help = """The smallest absolute effect you want your test to reliably detect. Enter the exact number, not a percentage.

- For means (e.g., revenue): If you want to detect at least a $5 difference, enter 5."""
    delta_placeholder = "e.g., 5.0"

main_col_left, main_col_right = st.columns([0.6, 0.4])

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
            placeholder=delta_placeholder,
            min_value=0.001,
            step=0.01,
            help=delta_help,
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
                placeholder="e.g., 10.0",
                min_value=0.0,
                max_value=100.0,
                step=1.0,
                help="""Baseline rate (e.g. conversion rate) for your population in percentage.

- e.g. 10% conversion rate = 10""",
            )
            baseline_rate_prop = (
                baseline_rate / 100 if baseline_rate is not None else None
            )
            variance = (
                baseline_rate_prop * (1 - baseline_rate_prop)
                if baseline_rate_prop is not None
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
            if selected_metric == METRIC_TYPES["RATE"]:
                delta_calc = delta / 100
            else:
                delta_calc = delta
            try:
                result = calculate_sample_size(
                    alpha, power, delta_calc, variance, ratio
                )
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

st.divider()  # Beginning of Experiment Length Calcultor section

st.subheader("Experiment Length Calculator")
st.caption(
    """Calculate how many days you need to run your experiment based on your daily traffic.
    Fill in the parameters below to estimate the experiment duration."""
)

exp_col_left, exp_col_right = st.columns([0.6, 0.4])

with exp_col_left:
    st.subheader("⚙️ Parameters")

    # Auto-populate sample size if available from the calculator above
    default_sample_size = None
    if "result" in st.session_state:
        default_sample_size = st.session_state["result"]["n_total"]

    daily_traffic = st.number_input(
        "Daily Traffic",
        value=None,
        placeholder="e.g., 5000",
        min_value=1,
        step=100,
        help="Total number of unique users/visitors per day that will be included in your experiment.",
    )

    total_sample_size_exp = st.number_input(
        "Total Sample Size",
        value=default_sample_size,
        placeholder="Calculate sample size above first"
        if default_sample_size is None
        else "e.g., 10000",
        min_value=1,
        step=100,
        help="Total sample size needed for your experiment (auto-populated from Sample Size Calculator above, but you can override it).",
    )

    if st.button("Calculate Experiment Length", type="primary"):
        # Validate all inputs are provided
        if daily_traffic is None or total_sample_size_exp is None:
            st.error(
                "Please fill in both Daily Traffic and Total Sample Size before calculating."
            )
        else:
            try:
                experiment_days = calculate_test_length(
                    daily_traffic, total_sample_size_exp
                )
                end_date = date.today() + timedelta(days=experiment_days)
                st.session_state["experiment_length_result"] = {
                    "days": experiment_days,
                    "end_date": end_date,
                }
            except Exception as e:
                st.error(f"Calculation error: {str(e)}")

with exp_col_right:
    st.subheader("Calculated Experiment Length")
    if "experiment_length_result" in st.session_state:
        exp_result = st.session_state["experiment_length_result"]

        with st.container(border=True):
            st.metric("Experiment Duration", f"{exp_result['days']} days")

        with st.container(border=True):
            st.metric(
                "Projected End Date",
                exp_result["end_date"].strftime("%B %d, %Y"),
                help="If you start the experiment today, it should end on this date.",
            )

        # Conditionally show warning if experiment is less than 7 days
        if exp_result["days"] < 7:
            st.warning(
                "**Recommended minimum: 7 days** - To account for different user populations or behaviors on weekdays and weekends, we recommend running your A/B test for at least 7 days.",
                icon="⚠️",
            )

st.divider()  # Beginning of Sources section

st.caption("Sources:")
st.caption(
    "[Sample Size Estimation in A/B Tests Explained!](https://www.youtube.com/watch?v=JEAsoUrX6KQ)"
)
st.caption(
    "[Statistical Rules of Thumb Chapter 2](http://vanbelle.org/chapters/webchapter2.pdf)"
)
st.caption(
    "[Calculating Sample Sizes for A/B Tests](https://blog.statsig.com/calculating-sample-sizes-for-a-b-tests-7854d56c2646)"
)
