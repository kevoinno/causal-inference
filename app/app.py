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
st.set_page_config(layout="wide")

# Session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# home page
def show_homepage():
    # Use Streamlit native functions instead of HTML
    st.markdown("<h1 style='text-align:center;'>Causal Buddy</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'>Tools that make learning causal inference easy</div>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # Create columns: left (narrow), right (wide)
    left, _ = st.columns([1, 3])  # Adjust ratio as needed

    with left:
        with st.container(border=True):
            st.markdown("### 🔬 Difference-in-Difference (DiD) Tool")
            st.markdown("Learn and Simulate a 2x2 DiD design")
            st.write("")
            if st.button("Launch DiD Tool", type="primary"):
                st.session_state.current_page = 'did_tool'
                st.rerun()

def show_did_tool():
    # Back button with primary styling
    if st.button("← Back to Home", type="primary"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Main title using Streamlit native function
    st.title("Difference-in-Difference Simulation Tool 📈")
    
    # Add some spacing
    st.write("")
    
    # Sidebar header using Streamlit native function
    st.sidebar.header("Simulation Parameters")
    
    # Sidebar controls
    true_effect = st.sidebar.slider("True Effect", min_value=-50, max_value=50, value=8)
    treated_baseline = st.sidebar.slider("Treated Baseline", min_value=0, max_value=50, value=10)
    treated_trend = st.sidebar.slider("Treated Trend", min_value=0, max_value=10, value=4)
    control_baseline = st.sidebar.slider("Control Baseline", min_value=0, max_value=50, value=40)
    control_trend = st.sidebar.slider("Control Trend", min_value=0, max_value=10, value=4)
    noise = st.sidebar.slider("Noise", min_value=0, max_value=20, value=3)
    sample_size = st.sidebar.slider("Sample Size", min_value=10, max_value=2000, value=500, step=10)
    
    # Graph plots according to the parameters
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
    
    # Visualizations section
    with st.container(border=True):
        st.header("📈 Visualizations")
        
        # Visualize the data (in 2 cols)
        col1, col2 = st.columns(2)
        
        # Display the panel plot
        with col1:
            st.markdown("**Panel Data Visualization**")
            fig_panel = panel_plot(df)
            st.plotly_chart(fig_panel, use_container_width=True)
        
        # Use DiD to model the data and get parameters
        model_results = estimate_did(df)
        
        # Display the means plot
        with col2:
            st.markdown("**DiD Regression Results**")
            fig_means = means_plot(model_results)
            st.plotly_chart(fig_means, use_container_width=True)
    
    # Results section
    with st.container(border=True):
        st.header("📋 Regression Results")
        st.write(model_results.summary())

# Main app logic to navigate pages
if st.session_state.current_page == 'home':
    show_homepage()
elif st.session_state.current_page == 'did_tool':
    show_did_tool()