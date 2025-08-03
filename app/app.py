import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulate.simulate import simulate
from estimate.estimate import estimate_did
from estimate.estimate import placebo_test
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
    st.markdown("<div style='text-align:center;'color = #666666;'>Tools that make learning causal inference easy</div>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # Create columns: left (narrow), right (wide)
    left, _ = st.columns([1, 3])  # Adjust ratio as needed

    with left:
        with st.container(border=True):
            st.markdown("### 🔬 Difference-in-Difference (DiD) Tool")
            st.markdown("Learn and Simulate a 2x2 DiD design")
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Learn DiD", type="primary"):
                    st.session_state.current_page = 'did_guide'
                    st.rerun()
            with col2:
                if st.button("Launch Tool", type="primary"):
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

    # Introduction
    st.write("""Have you ever wanted to measure the impact of a policy or marketing campaign, but for some reason you couldn't run a 
             traditional A/B test or randomized experiment? Or maybe you already launched the policy and need to understand the effects 
             using observational data.""")
    st.write("""The difference-in-difference design might be a good candidate for you to measure the impact of this policy. Let's learn more
             about this design. If you are already familiar with this method, feel free to skip over and start messing around with the simulation 
             parameters.""")
    
    # Sidebar header using Streamlit native function
    st.sidebar.header("Placeholder")
    
    # Simulation parameters and visualizations side by side
    col1, col2 = st.columns([0.4, 0.6])
    
    # Left column: Simulation parameters
    with col1:
        with st.container(border=True):
            st.header("⚙️ Simulation Parameters")
            st.caption("Play around with the sliders and see how the graphs change")

            true_effect = st.slider("True Effect", min_value=-50, max_value=50, value=8, 
                                    help = "Size of the causal effect of the treatment")
            
            col1_inner_sim, col2_inner_sim = st.columns(2)
            with col1_inner_sim:
                treated_baseline = st.slider("Treated Baseline", min_value=0, max_value=50, value=10, 
                                             help = "Baseline outcome of the treated group at time t = 0")
                treated_trend = st.slider("Treated Trend", min_value=0, max_value=10, value=4,
                                            help = "The trend that the outcome of the treated group follows over time")
                noise = st.slider("Noise", min_value=0, max_value=20, value=3,
                                  help = "How much the variation in outcome can be")
            with col2_inner_sim:
                control_baseline = st.slider("Control Baseline", min_value=0, max_value=50, value=40, 
                                             help = "Baseline outcome of the control group at time t = 0")
                control_trend = st.slider("Control Trend", min_value=0, max_value=10, value=4,
                                          help = "The trend that the outcome of the control group follows over time")
                sample_size = st.slider("Sample Size", min_value=10, max_value=2000, value=500, step=10,
                                        help = "The number of observations in each group")

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

    # Right column: Visualizations (stacked vertically)
    with col2:
        with st.container(border=True):
            st.header("📈 Visualizations")
            
            # Use DiD to model the data and get parameters
            model_results = estimate_did(df)
            
            col1_inner_viz, col2_inner_viz = st.columns(2) 
            
            with col1_inner_viz:
                # Display the panel plot (top)
                fig_panel = panel_plot(df)
                st.plotly_chart(fig_panel, use_container_width=True)
            
            with col2_inner_viz:
                # Display the means plot (bottom)
                fig_means = means_plot(model_results)
                st.plotly_chart(fig_means, use_container_width=True)
    
    # Results section
    with st.container(border=True):
        st.header("📋 Regression Results")
        st.write(model_results.summary())

    # Placebo test
    with st.container(border = True):
        st.header("Testing Parallel Trends Assumptions")
        placebo_results = placebo_test(df)
        st.write(placebo_results.summary())

def show_did_guide():
    st.header("Difference-in-difference Guide")

    st.write("")

    st.subheader("The intuition")
    st.markdown("""So you want to find the causal effect of some policy or marketing campaign that you've ran, 
             but you didn't run a clean, randomized experiment. The idea behind difference-in-difference is that **if you can find
             a group that trends similarly to the treated group before and after the policy occurred,** then you can identify the
             impact of the policy using DiD.""")
    st.write("Let's go over a famous example of this to make the intuition clear")

    st.write("")
    st.subheader("John Snow's Cholera Example")
    st.markdown("""In mid-1800s, people were suffering from cholera in London, but no one knew what caused cholera. John Snow hypothesized
                that cholera spreads from the water, so he used a DiD design to test this hypothesis. At the time, two water companies
                serviced London: The Southwark and Vauxhall Company and the Lambeth Water Company.""")
    
    st.markdown("""**The context for this is important**. Both water companies sourced their water from the River Thames, and 
                they both sourced from a similar location, which was downstream where the city's sewage flowed to. Both companies
                also serviced neighboring houses. But in 1852, the Lambeth Water Company started sourcing water from upstream of the 
                sewage site.""")
    
    st.markdown("""Snow wanted to answer this causal question: **\"What is the effect of the Lambeth Water Company switching to an upstream 
                water source on the cholera death rates?\"**. Another way to frame this question is how much did the cholera death rates
                change relative to what they would have been if the Lambeth Water Company never switched water sources?""")
    
    
    st.write("Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC8006863/")


# Main app logic to navigate pages
if st.session_state.current_page == 'home':
    show_homepage()
elif st.session_state.current_page == 'did_tool':
    show_did_tool()
elif st.session_state.current_page == 'did_guide':
    show_did_guide()