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
                if st.button("Simulation Tool", type="primary"):
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
    
    # Back button with primary styling
    if st.button("← Back to Home", type="primary"):
        st.session_state.current_page = 'home'
        st.rerun()

    st.header("Difference-in-difference Guide")

    # The intuition
    st.markdown("## The intuition")
    st.markdown("""So you want to find the causal effect of some policy or marketing campaign that you've ran, 
             but you didn't run a clean, randomized experiment. The idea behind difference-in-difference is that **if you can find
             a group that trends similarly to the treated group before and after the policy occurred, and that group never adopted the policy,** 
            then you can identify the impact of the policy using DiD.""")
    st.write("Let's go over a famous example of this to make the intuition clear.")

    # The example
    st.markdown("## John Snow's Cholera Example")
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
    
    # The data
    st.markdown("""### The Data""")
    
    # Create the cholera data table
    cholera_data = {
        'Water supply': [
            'Southwark & Vauxhall Company only',
            'Lambeth Company Only'
        ],
        'Cholera death rate per 100,000 (1849)': [1349, 847],
        'Cholera death rate per 100,000 (1854)': [1466, 193],
    }
    
    df_cholera = pd.DataFrame(cholera_data)
    
    # Display the table with custom styling
    st.dataframe(
        df_cholera,
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("""Snow had collected this data on cholera death rates per 100,000 people for households that 
                used Southwark & Vauxhall Company as their water supply and also for households that used Lambeth Company as their
                water supply. He got data for the death rates in 1849 and 1854. Remember, Lambeth changed to a different water source in 1852.
                Let's see how we can figure out the effect changing water supplies on the cholera death rate.""")
    
    # Create Plotly visualization
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    # Data for the plot
    years = [1849, 1854]
    vauxhall_rates = [1349, 1466]
    lambeth_rates = [847, 193]
    
    # Calculate counterfactual for Lambeth (assuming parallel trends)
    # If Lambeth followed the same trend as Vauxhall, what would their 1854 rate be?
    vauxhall_change = 1466 - 1349  # 117
    lambeth_counterfactual = 847 + vauxhall_change  # 847 + 117 = 964
    
    # Create the plot
    fig = go.Figure()
    
    # Add Vauxhall line (blue)
    fig.add_trace(go.Scatter(
        x=years,
        y=vauxhall_rates,
        mode='lines+markers',
        name='Southwark & Vauxhall',
        line=dict(color='blue', width=3),
        marker=dict(size=10, color='blue')
    ))
    
    # Add Lambeth line (red)
    fig.add_trace(go.Scatter(
        x=years,
        y=lambeth_rates,
        mode='lines+markers',
        name='Lambeth (Actual)',
        line=dict(color='red', width=3),
        marker=dict(size=10, color='red')
    ))
    
    # Add Lambeth counterfactual (dotted red)
    fig.add_trace(go.Scatter(
        x=[1849, 1854],
        y=[847, lambeth_counterfactual],
        mode='lines+markers',
        name='Lambeth (If they never switched water sources)',
        line=dict(color='red', width=2, dash='dot'),
        marker=dict(size=8, color='red', symbol='diamond')
    ))
    
    # Update layout
    fig.update_layout(
        title='Cholera Death Rates: Lambeth vs Southwark & Vauxhall',
        xaxis_title='Year',
        yaxis_title='Cholera Death Rate per 100,000',
        height=500
    )
    
    # Add vertical line for treatment (1852)
    fig.add_vline(x=1852, line_dash="dash", line_color="gray")
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    So how do we actually measure the effect of the changing of water sources for the Lambeth Company? The best way to think about this
    is assuming we had all the information possible. If we did, then we could take the difference between Lambeth's cholera death rate in 
    1854 after moving water sources and Lambeth's cholera death rate in 1854 had they never switched water sources. Sadly, the reality
    is that Lambeth did switch water sources, so we can never know what the death rate would have been in 1854 had they never switched. 
    But, with the difference-in-difference design, we can make some assumptions to estimate it.
                
    Difference-in-difference assumes **parallel trends** between Lambeth and and Southwark & Vauxhall. This means that we are assuming 
    that if Lambeth had never switched water sources in 1852, then their cholera death rate would have trended the same as Southwark &
    Vauxhall's death rate. Remember, Southwark & Vauxhall never switched water sources. We can see this in the graph above. 
    Notice how solid blue line and dotted red line are parallel? 
                
    With this assumption, we can estimate the cholera death rate for Lambeth in 1854 to be Lambeth's death rate in 1849 + the trend of 
    Southwark & Vauxhall from 1849 to 1854. Then we have everything we need to estimate the effect! The steps are below. For some 
    clarification on notation, $Y$ is the outcome of interest (cholera death rate per 100,000). Counterfactual means that the outcome
    never actually occurred.
    """)
    
    st.markdown("**Step 1:** The cholera death rate for Lambeth in 1854 after switching water sources (which we observed in the data):")
    
    st.latex(r'''
    Y_{Lambeth, 1854}^{observed} = 193
    ''')
    
    st.markdown("**Step 2:** The cholera death rate for Lambeth in 1854 had they never switched water sources (which we estimated):")
    
    st.latex(r'''
    Y_{Lambeth, 1854}^{counterfactual} = Y_{Lambeth, 1849} + (Y_{Vauxhall, 1854} - Y_{Vauxhall, 1849}) = 847 + (1466 - 1349) = 964
    ''')
    
    st.markdown("**Step 3:** The causal effect of switching water sources on death rates for Lambeth:")
    
    st.latex(r'''
    \tau = Y_{Lambeth, 1854}^{observed} - Y_{Lambeth, 1854}^{counterfactual} = 193 - 964 = -771
    ''')
    
    st.markdown("""
    So to get the effect of changing water supplies on the death rate for Lambeth, we get a causal effect of -771. This means that 
    Lambeth switching water sources decreased the death rate for households that used Lambeth's water by 771 per 100,000 people.
                
    So why is this design called difference-in-difference? Because we could have gotten that answer by taking the 2 differences:
    """)
    
    st.markdown("**Alternative calculation using differences:**")
    st.markdown("So why is the method called difference-in-difference? Because we could have gotten the same result by taking 2 differences:")
    
    st.markdown("**Difference 1:** The change in Lambeth's death rates:")
    
    st.latex(r'''
    \Delta Y_{Lambeth} = Y_{Lambeth, 1854} - Y_{Lambeth, 1849} = 193 - 847 = -654
    ''')
    
    st.markdown("**Difference 2:** The change in Vauxhall's death rates:")
    
    st.latex(r'''
    \Delta Y_{Vauxhall} = Y_{Vauxhall, 1854} - Y_{Vauxhall, 1849} = 1466 - 1349 = 117
    ''')
    
    st.markdown("**DiD Estimate:**")
    
    st.latex(r'''
    \tau = \Delta Y_{Lambeth} - \Delta Y_{Vauxhall} = -654 - 117 = -771
    ''')
    
    st.markdown("""
    See how this is the same! I introduced the calculations differently 
    because I wanted to explicitly show that we are trying to estimate a **counterfactual** (the death rate for Lambeth in 1854 had
    they never changed water sources). This concept is the basis of causal inference. We are always trying to estimate a counterfactual
    no matter what technique we use.
    """)
    

    st.write("Data and example sourced from: https://pmc.ncbi.nlm.nih.gov/articles/PMC8006863/")


# Main app logic to navigate pages
if st.session_state.current_page == 'home':
    show_homepage()
elif st.session_state.current_page == 'did_tool':
    show_did_tool()
elif st.session_state.current_page == 'did_guide':
    show_did_guide()