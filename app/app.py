import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulate.simulate import simulate
from estimate.estimate import estimate_did
from visualize.visualize import panel_plot, means_plot
import numpy as np


# Make page wide mode
st.set_page_config(layout = "wide")

st.title("Difference-in-Difference Simulation Tool 📈")

# Sidebar controls
st.sidebar.header("Simulation Parameters")

true_effect = st.sidebar.slider("True Effect", min_value = -50, max_value = 50, value = 8)
treated_baseline = st.sidebar.slider("Treated Baseline", min_value=0, max_value=50, value=10)
treated_trend = st.sidebar.slider("Treated Trend", min_value=0, max_value=10, value=4)
control_baseline = st.sidebar.slider("Control Baseline", min_value=0, max_value=50, value=40)
control_trend = st.sidebar.slider("Control Trend", min_value=0, max_value=10, value=4)
noise = st.sidebar.slider("Noise", min_value=0, max_value=20, value=3)
sample_size = st.sidebar.slider("Sample Size", min_value=10, max_value=2000, value=500, step=10)

# Graph plots according to the parameters
df = simulate(b0_treat = treated_baseline, b0_control = control_baseline, 
                     b1_treat = treated_trend, b1_control = control_trend,
                     treatment_effect = true_effect,
                     noise = noise,
                     N = sample_size)

# Preview data in a dataframe + download data button
st.markdown("**Preview of the data**") 
st.dataframe(df.head(5))
df_csv = df.to_csv()
st.download_button("Download Data", data = df_csv, file_name = "simulated_did_data.csv")

# Visualize the data (in 2 cols)
col1, col2 = st.columns(2)

# Display the panel plot
with col1:
    fig_panel = panel_plot(df)
    st.plotly_chart(fig_panel, use_container_width=True)

# Use DiD to model the data and get parameters
model_results = estimate_did(df)

# Display the means plot
with col2:
    fig_means = means_plot(model_results)
    st.plotly_chart(fig_means, use_container_width=True)

st.write(model_results.summary())

# # TODO: 
#  - Clarify simulated data columns
#  - Label Regression results
#  - Add another page with an in depth guide