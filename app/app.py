import streamlit as st
# from simulate.simulate import simulate
# from estimate.estimate import estimate_did
# from visualize.visualize import panel_plot, means_plot
import numpy as np

st.title("Difference-in-Difference Simulation Tool")

# Sidebar controls
st.sidebar.header("Simulation Parameters")

true_effect = st.sidebar.text_input("True Effect", value="8")
treated_baseline = st.sidebar.slider("Treated Baseline", min_value=0, max_value=50, value=10)
treated_trend = st.sidebar.slider("Treated Trend", min_value=0, max_value=10, value=4)
control_baseline = st.sidebar.slider("Control Baseline", min_value=0, max_value=50, value=40)
control_trend = st.sidebar.slider("Control Trend", min_value=0, max_value=10, value=4)
noise = st.sidebar.slider("Noise", min_value=0, max_value=20, value=3)
sample_size = st.sidebar.slider("Sample Size", min_value=10, max_value=2000, value=500, step=10)

# maybe use caching for generating plots

# TODO: 
# 1. fix import errors
# 2. implement sidebars
# 3. graph raw data
# 4. graph did
# 5. show regression results