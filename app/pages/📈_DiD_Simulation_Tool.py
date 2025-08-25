import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from simulate.simulate import simulate
from estimate.estimate import estimate_did, placebo_test
from visualize.visualize import mean_outcomes_plot, means_plot, bias_visualization

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
st.write("""The difference-in-difference design might be a good candidate for you to measure the impact of this policy. If this method is completely new to you, check out the DiD guide tab before using this tool. 
         If you are already familiar with this method, feel free to skip over and start messing around with the simulation parameters.""")
st.markdown("""There are 5 time periods ranging from -3 to 1. If a time period is negative or zero, then it is a pre-treatment period. 
            Time period $t = 0$ marks the pre-treatment period used in the 2x2 DiD setup and $t = 1$ marks the post-treatment period.""")

# Simulation parameters and visualizations side by side
col1, col2 = st.columns([0.3, 0.7])

# Left column: Simulation parameters
with col1:
    with st.container(border=True):
        st.header("⚙️ Simulation Parameters")
        st.caption("Play around with the sliders and see how the graphs and estimates change")
        st.caption("e.g. Try making the group trends different and check the estimate!")

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
            sample_size = st.slider("Sample Size", min_value=10, max_value=2000, value=200, step=10,
                                    help="The total number of units in the study")
        
        # New parameter for realistic treatment assignment
        treat_ratio = st.slider("Treatment Group Size (%)", min_value=10, max_value=90, value=30, step=5,
                                help="Percentage of units in the treatment group (realistic DiD often has uneven groups)")

# Simulate data
df = simulate(b0_treat=treated_baseline, b0_control=control_baseline,
             b1_treat=treated_trend, b1_control=control_trend,
             treatment_effect=true_effect,
             noise=noise,
             N=sample_size,
             treat_ratio=treat_ratio/100)  # Convert percentage to decimal

# Data preview section
with st.container(border=True):
    st.header("📊 Data Preview")
    st.caption("See what your simulated data looks like in tabular form")
    
    # Show group sizes for educational purposes
    n_treated = int(sample_size * treat_ratio / 100)
    n_control = sample_size - n_treated
    st.markdown(f"📈 **Group Sizes**: {n_treated} treated units ({treat_ratio}%) | {n_control} control units ({100-treat_ratio}%)")

    df_display = df[['unit', 'treat', 'time_period', 'outcome']]    
    st.dataframe(df_display.head(5))
    df_csv = df_display.to_csv()
    st.download_button("Download Data", data=df_csv, file_name="simulated_did_data.csv", type="primary")

# Right column: Visualizations
with col2:
    with st.container(border=True):
        st.header("📈 Visualizations")
        st.caption("Visualize your simulated data")
        
        # Use DiD to model the data and get parameters
        model_results = estimate_did(df)
        
        col1_inner_viz, col2_inner_viz = st.columns(2) 
        
        with col1_inner_viz:
            # Display the mean outcomes plot (replaces raw data plot)
            fig_mean = mean_outcomes_plot(df)
            st.plotly_chart(fig_mean, use_container_width=True)
            st.caption("💡 **Note**: This shows group means over time. The raw data would vary around these points due to individual variation and noise.")
        
        with col2_inner_viz:
            # Display the means plot
            fig_means = means_plot(model_results)
            st.plotly_chart(fig_means, use_container_width=True)

# Results and Interpretation section
with st.container(border=True):
    st.header("📋 Results & Interpretation")
    st.caption("Regression results and what they mean")
    
    # Get bias visualization and statistics
    bias_fig, bias, estimated_effect, ci_lower, ci_upper = bias_visualization(model_results, true_effect)
    
    # Determine statistical significance
    p_value = model_results.pvalues['treat:time_indicator']
    is_significant = p_value < 0.05
    
    # Create two columns for results and interpretation
    col1_results, col2_results = st.columns([0.5, 0.5])
    
    with col1_results:
        st.subheader("📊 Regression Results")
        st.write(model_results.summary())
    
    with col2_results:
        st.subheader("🎯 Interpretation")
        st.markdown(f"""
        **Estimated Causal Effect**: {estimated_effect:.2f} units
        
        **95% Confidence Interval**: [{ci_lower:.2f}, {ci_upper:.2f}]
        """)
        
        # Add confidence interval coverage info
        ci_contains_true = ci_lower <= true_effect <= ci_upper
        if ci_contains_true:
            st.success("✅ **Confidence Interval**: Contains the true effect")
        else:
            st.error("❌ **Confidence Interval**: Does not contain the true effect")
        
        # Add statistical significance interpretation
        st.markdown(f"""
        **Statistical Significance** (p = {p_value:.3f}):
        """)
        
        if is_significant:
            st.success("✅ **P-value Interpretation**: The estimated effect is statistically significantly different from 0")
        else:
            st.warning("❌ **P-value Interpretation**: We don't have enough evidence to say that the estimated effect is significantly different from 0")
        
        st.markdown(f"""
        **Bias**: The estimate is {abs(bias):.2f} units {'above' if bias > 0 else 'below'} the true effect of {true_effect:.2f} units.
        """)
    
    # Bias visualization below both columns
    st.subheader("📈 Bias Visualization")
    st.caption("Tells us how far the model's estimated causal effect was from the true effect")
    st.plotly_chart(bias_fig, use_container_width=True)

# Placebo test
with st.container(border=True):
    st.header("Testing Parallel Trends Assumptions")
    st.caption("Pre-treatment falsification test")
    
    st.write("""
    This is a falsification test for the parallel trends. We run a 2x2 DiD using time periods -1 and 0 (before treatment) to test the parallel trends assumption.
    
    If parallel trends hold, the interaction term (`treat:time_indicator`) should be close to zero and statistically insignificant. If the interaction term is non-zero and statistically significant, then we have evidence that the trends between the two groups were different and not parallel.
             
    This test has limitations. The argument that the groups were similar before treatment so they should be similar after is flawed.
    There are many other methods to falsify this assumption. This one was used for simplicity.
    """)
    
    placebo_results = placebo_test(df)
    
    # Extract placebo test statistics
    placebo_effect = placebo_results.params['treat:time_indicator']
    placebo_ci_lower = placebo_results.conf_int().loc['treat:time_indicator', 0]
    placebo_ci_upper = placebo_results.conf_int().loc['treat:time_indicator', 1]
    placebo_pvalue = placebo_results.pvalues['treat:time_indicator']
    placebo_significant = placebo_pvalue < 0.05
    
    # Create two columns for results and interpretation
    col1_placebo, col2_placebo = st.columns([0.6, 0.4])
    
    with col1_placebo:
        st.subheader("📊 Placebo Test Results")
        st.write(placebo_results.summary())
    
    with col2_placebo:
        st.subheader("🎯 Interpretation")
        st.markdown(f"""
        **Placebo Effect**: {placebo_effect:.3f} units
        
        **95% Confidence Interval**: [{placebo_ci_lower:.3f}, {placebo_ci_upper:.3f}]
        
        **P-value**: {placebo_pvalue:.3f}
        """)
        
        # Assessment based on statistical significance
        if placebo_significant:
            st.error("❌ **Assessment**: Trends diverged before treatment. Parallel trends assumption likely is not believable.")
            st.warning("⚠️ **Implication**: This suggests the DiD estimate may be biased due to pre-existing differences in trends between groups.")
        else:
            st.success("✅ **Assessment**: Not enough evidence to claim there are different trends pre-treatment. Parallel trends assumption appears reasonable.")
            st.info("💡 **Implication**: This makes the assumptions of the DiD design more reasonable, but does not completely validate the assumptions.")