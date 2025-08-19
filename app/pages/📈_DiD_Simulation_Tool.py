import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from simulate.simulate import simulate
from estimate.estimate import estimate_did, placebo_test
from visualize.visualize import panel_plot, means_plot

# Set page config for this specific page
st.set_page_config(
    page_title="DiD Simulation Tool",
    page_icon="📈",
    layout="wide"
)

# Back button with primary styling
if st.button("← Back to Home", type="primary"):
    st.switch_page("Home.py")

st.title("Difference-in-Difference Simulation Tool 📈")
st.sidebar.header("DiD Simulation Tool")

# Introduction
st.write("""Have you ever wanted to measure the impact of a policy or marketing campaign, but for some reason you couldn't run a 
         traditional A/B test or randomized experiment? Or maybe you already launched the policy and need to understand the effects 
         using observational data.""")
st.write("""The difference-in-difference design might be a good candidate for you to measure the impact of this policy. Let's learn more
         about this design. If you are already familiar with this method, feel free to skip over and start messing around with the simulation 
         parameters.""")

# Simulation parameters and visualizations side by side
col1, col2 = st.columns([0.4, 0.6])

# Left column: Simulation parameters
with col1:
    with st.container(border=True):
        st.header("⚙️ Simulation Parameters")
        st.caption("Play around with the sliders and see how the graphs change")

        true_effect = st.slider("True Effect", min_value=-50, max_value=50, value=8, 
                                help="Size of the causal effect of the treatment")
        
        col1_inner_sim, col2_inner_sim = st.columns(2)
        with col1_inner_sim:
            treated_baseline = st.slider("Treated Baseline", min_value=0, max_value=50, value=10, 
                                         help="Baseline outcome of the treated group at time t = 0")
            treated_trend = st.slider("Treated Trend", min_value=0, max_value=10, value=4,
                                        help="The trend that the outcome of the treated group follows over time")
            noise = st.slider("Noise", min_value=0, max_value=20, value=3,
                              help="How much the variation in outcome can be")
        with col2_inner_sim:
            control_baseline = st.slider("Control Baseline", min_value=0, max_value=50, value=40, 
                                         help="Baseline outcome of the control group at time t = 0")
            control_trend = st.slider("Control Trend", min_value=0, max_value=10, value=4,
                                      help="The trend that the outcome of the control group follows over time")
            sample_size = st.slider("Sample Size", min_value=10, max_value=2000, value=500, step=10,
                                    help="The number of observations in each group")

# Simulate data
df = simulate(b0_treat=treated_baseline, b0_control=control_baseline,
             b1_treat=treated_trend, b1_control=control_trend,
             treatment_effect=true_effect,
             noise=noise,
             N=sample_size)

# Data preview section
with st.container(border=True):
    st.header("📊 Data Preview")
    st.dataframe(df.head(5))
    df_csv = df.to_csv()
    st.download_button("Download Data", data=df_csv, file_name="simulated_did_data.csv", type="primary")

# Right column: Visualizations
with col2:
    with st.container(border=True):
        st.header("📈 Visualizations")
        
        # Use DiD to model the data and get parameters
        model_results = estimate_did(df)
        
        col1_inner_viz, col2_inner_viz = st.columns(2) 
        
        with col1_inner_viz:
            # Display the panel plot
            fig_panel = panel_plot(df)
            st.plotly_chart(fig_panel, use_container_width=True)
        
        with col2_inner_viz:
            # Display the means plot
            fig_means = means_plot(model_results)
            st.plotly_chart(fig_means, use_container_width=True)

# Results section
with st.container(border=True):
    st.header("📋 Regression Results")
    st.write(model_results.summary())

# Placebo test
with st.container(border=True):
    st.header("Testing Parallel Trends Assumptions")
    placebo_results = placebo_test(df)
    st.write(placebo_results.summary())