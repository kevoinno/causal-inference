"""
Difference-in-Differences (DiD) Methods

This module contains all functions related to DiD analysis including:
- Simulation of DiD panel data
- Estimation of treatment effects
- Visualization of results and diagnostics
"""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import plotly.express as px
import plotly.graph_objects as go


# ============================================
# SIMULATION FUNCTIONS
# ============================================

def simulate(b0_treat=10, b0_control=40, b1_treat=4, b1_control=4, treatment_effect=8, noise=3, N=500, treat_ratio=0.3):
    """
    Simulates panel data for a Difference-in-Differences setup.
    
    Parameters
    ----------
    b0_treat : float
        Baseline outcome for the treated group at time t = 0
    b0_control : float
        Baseline outcome for the control group at time t = 0
    b1_treat : float
        Time trend coefficient for the treated group
    b1_control : float
        Time trend coefficient for the control group
    treatment_effect : float
        Size of the causal effect of the treatment
    noise : float
        Standard deviation of the error term
    N : int
        Total number of units in the study
    treat_ratio : float
        Proportion of units in the treatment group (between 0 and 1)
    
    Returns
    -------
    pd.DataFrame
        Panel data with columns: unit, treat, time_period, time_indicator, 
        unit_baseline_effect, time_effect, outcome
    """
    # simulate data
    np.random.seed(1)  # for reproducibility

    # units and treatment assignment with realistic proportions
    units = np.arange(N)
    n_treated = int(N * treat_ratio)  # e.g., 30% treated
    n_control = N - n_treated         # e.g., 70% control
    
    treat = np.concatenate([np.ones(n_treated), np.zeros(n_control)])
    np.random.shuffle(treat)

    # Currently, treatment status to units is randomly assigned
    df = pd.DataFrame({
        'unit': units,
        'treat': treat
    })

    # time periods from -3 to 1
    df = df.merge(pd.DataFrame({'time_period': np.arange(-3, 2)}), how='cross')

    # add time indicator (1 if post-treatment else 0)
    df['time_indicator'] = (df['time_period'] == 1).astype(int)

    # add outcomes

    # Add unit-level baseline heterogeneity
    unit_baseline_effects = np.random.normal(0, 2, N)  # Individual baseline differences
    
    # Create unit-level effects dataframe
    unit_effects = pd.DataFrame({
        'unit': units,
        'unit_baseline_effect': unit_baseline_effects
    })
    
    # Merge unit effects with main dataframe
    df = df.merge(unit_effects, on='unit')

    # baseline outcomes with unit heterogeneity
    df['outcome'] = df['treat'].apply(lambda x: b0_treat if x == 1 else b0_control) 
    df['outcome'] = df['outcome'] + df['unit_baseline_effect']  # Add individual baseline variation

    # apply trends
    treat_mask = df['treat'] == 1 
    control_mask = df['treat'] == 0

    df.loc[treat_mask, 'outcome'] += df.loc[treat_mask, 'time_period'] * b1_treat
    df.loc[control_mask, 'outcome'] += df.loc[control_mask, 'time_period'] * b1_control

    # Add time-varying confounders (affect all units equally)
    time_effects = np.random.normal(0, 2.5, 5)  # One effect per time period (-3, -2, -1, 0, 1)
    
    # Create time effects dataframe
    time_effects_df = pd.DataFrame({
        'time_period': [-3, -2, -1, 0, 1],
        'time_effect': time_effects
    })
    
    # Merge time effects with main dataframe
    df = df.merge(time_effects_df, on='time_period')
    
    # Apply time-varying confounders to all units
    df['outcome'] = df['outcome'] + df['time_effect']

    # apply treatment effect
    df['outcome'] = df['outcome'] + treatment_effect * df['treat'] * df['time_indicator']

    # add noise
    df['outcome'] = df['outcome'] + np.random.normal(0, noise, 5*N)

    return df


# ============================================
# ESTIMATION FUNCTIONS
# ============================================

def estimate_did(df):
    """
    Estimates the Average Treatment Effect on the Treated (ATT) using a 2x2 DiD setup.
    
    Parameters
    ----------
    df : pd.DataFrame
        Panel data with columns: outcome, treat, time_period, time_indicator
    
    Returns
    -------
    statsmodels.regression.linear_model.RegressionResultsWrapper
        Regression results with the DiD estimate as the coefficient on treat:time_indicator
    """
    filtered_df = df[df['time_period'].isin([0, 1])].copy()
    model = smf.ols('outcome~treat*time_indicator', data=filtered_df)
    results = model.fit(cov_type='HC2')
    
    return results


def placebo_test(df):
    """
    Runs a placebo test (2x2 DiD setup) on time periods -1, 0 to test parallel trends.
    
    This is a falsification test where we pretend treatment occurs between t=-1 and t=0.
    If parallel trends hold, the interaction term should be close to zero and 
    statistically insignificant.
    
    Parameters
    ----------
    df : pd.DataFrame
        Panel data with columns: outcome, treat, time_period
    
    Returns
    -------
    statsmodels.regression.linear_model.RegressionResultsWrapper
        Regression results with the placebo effect as the coefficient on treat:time_indicator
    """
    filtered_df = df[df['time_period'].isin([-1, 0])].copy()
    filtered_df['time_indicator'] = filtered_df['time_period'].apply(lambda x: 1 if x == 0 else 0)

    model = smf.ols('outcome~treat*time_indicator', data=filtered_df)
    results = model.fit(cov_type='HC2')

    return results


# ============================================
# VISUALIZATION FUNCTIONS
# ============================================

def panel_plot(df):
    """
    Creates a scatter plot of raw panel data showing outcomes over time by group.
    
    Parameters
    ----------
    df : pd.DataFrame
        Panel data with columns: time_period, outcome, treat
    
    Returns
    -------
    plotly.graph_objects.Figure
        Interactive scatter plot with treatment line marker
    """
    df_plot = df.copy()
    df_plot['treat'] = df_plot['treat'].apply(lambda x: 'Treated' if x == 1 else 'Control')

    # create scatterplot
    fig = px.scatter(
        df_plot,
        x='time_period',
        y='outcome',
        color='treat',  
        title="Outcomes over Time by Group",
        opacity=0.4,
        labels={
            "time_period": "Time Period",
            "outcome": "Outcome",
            "treat": "Group"
        },
        color_discrete_map={  # Optional: set custom colors
            'Treated': 'red',
            'Control': 'blue'
        },
        template='plotly_white'
    )

    # Add the vertical line for when the treatment occurs
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="black",
        annotation_text="Treatment Start",
        annotation_position="top right"
    )

    fig.update_xaxes(tickvals=[-3, -2, -1, 0, 1])

    return fig


def mean_outcomes_plot(df):
    """
    Creates a line plot of mean outcomes over time by group.
    
    This replaces the raw data scatter plot with a cleaner visualization
    that shows the core DiD patterns more clearly.
    
    Parameters
    ----------
    df : pd.DataFrame
        Panel data with columns: treat, time_period, outcome
    
    Returns
    -------
    plotly.graph_objects.Figure
        Interactive line plot with treatment line marker
    """
    # Compute mean outcomes by group and time period
    mean_df = (
        df.groupby(["treat", "time_period"])['outcome']
          .mean()
          .reset_index()
    )
    mean_df['Group'] = mean_df['treat'].map({1: 'Treated', 0: 'Control'})
    
    # Create line plot with markers
    fig = px.line(
        mean_df,
        x="time_period",
        y="outcome",
        color="Group",
        markers=True,
        labels={"time_period": "Time Period", "outcome": "Mean Outcome"},
        template="plotly_white",
        title="Mean Outcomes Over Time by Group",
        color_discrete_map={
            'Treated': 'red',
            'Control': 'blue'
        }
    )
    
    # Add the vertical line for when the treatment occurs (without annotation text)
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="black"
    )
    
    # Add a dummy trace for treatment start in legend
    fig.add_trace(go.Scatter(
        x=[None, None],
        y=[None, None],
        mode='lines',
        line=dict(color='black', width=2, dash='dash'),
        name='Treatment Start',
        showlegend=True,
        hoverinfo='skip'
    ))
    
    # Add explicit height and fix x-axis label rotation
    fig.update_layout(
        height=400,
        margin=dict(l=50, r=50, t=100, b=50)
    )
    
    # Force horizontal x-axis labels
    fig.update_xaxes(
        tickvals=[-3, -2, -1, 0, 1],
        tickangle=0
    )
    
    return fig


def means_plot(model_results):
    """
    Creates a visualization of the DiD regression results showing actual and counterfactual means.
    
    Parameters
    ----------
    model_results : statsmodels.regression.linear_model.RegressionResultsWrapper
        Results from estimate_did() function
    
    Returns
    -------
    plotly.graph_objects.Figure
        Interactive plot showing control, treated, and counterfactual trends
    """
    coeffs = model_results.params

    b0 = coeffs['Intercept']
    b1 = coeffs['treat']
    b2 = coeffs['time_indicator']
    b3 = coeffs['treat:time_indicator']

    control_pre = b0
    control_post = b0+b2
    treat_pre = b0+b1
    treat_post = b0+b1+b2+b3
    treat_counterfactual = b0+b1+b2

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[control_pre, control_post],
        mode='lines+markers',
        line=dict(color='blue', width=2),
        name='Control',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[treat_pre, treat_post],
        mode='lines+markers',
        line=dict(color='red', width=2),
        name='Treated',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[treat_pre, treat_counterfactual],
        mode='lines+markers',
        line=dict(color='red', width=2, dash='dash'),
        name='Treated (Counterfactual)',
        showlegend=True
    ))

    # Add the vertical line for when the treatment occurs (without annotation text)
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="black"
    )
    
    # Add a dummy trace for treatment start in legend
    fig.add_trace(go.Scatter(
        x=[None, None],
        y=[None, None],
        mode='lines',
        line=dict(color='black', width=2, dash='dash'),
        name='Treatment Start',
        showlegend=True,
        hoverinfo='skip'
    ))
    
    # Fix 1: Add explicit height and better margins
    fig.update_layout(
        title="DiD Regression Visualization",
        xaxis_title="Time Period",
        yaxis_title="Outcome",
        legend_title_text='',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # Fix 2: Force horizontal x-axis labels
    fig.update_xaxes(
        tickvals=[0, 1],
        tickangle=0
    )

    return fig


def bias_visualization(model_results, true_effect):
    """
    Creates a visualization showing the estimated effect vs true effect.
    
    Includes confidence intervals and bias assessment to help users understand
    how close the estimate is to the true causal effect.
    
    Parameters
    ----------
    model_results : statsmodels.regression.linear_model.RegressionResultsWrapper
        Results from estimate_did() function
    true_effect : float
        The true treatment effect used in simulation
    
    Returns
    -------
    tuple
        (fig, bias, estimated_effect, ci_lower, ci_upper) where:
        - fig is the plotly Figure
        - bias is the difference between estimated and true effect
        - estimated_effect is the point estimate
        - ci_lower is the lower bound of 95% CI
        - ci_upper is the upper bound of 95% CI
    """
    # Extract the treatment effect estimate and confidence interval
    estimated_effect = model_results.params['treat:time_indicator']
    ci_lower = model_results.conf_int().loc['treat:time_indicator', 0]
    ci_upper = model_results.conf_int().loc['treat:time_indicator', 1]
    
    # Calculate bias
    bias = estimated_effect - true_effect
    
    # Create the visualization
    fig = go.Figure()
    
    # Add true effect line
    fig.add_hline(
        y=true_effect,
        line_dash="dash",
        line_color="green",
        annotation_text=f"True Effect: {true_effect:.2f}",
        annotation_position="top right"
    )
    
    # Add estimated effect point
    fig.add_trace(go.Scatter(
        x=[0],
        y=[estimated_effect],
        mode='markers',
        marker=dict(size=12, color='red'),
        name=f'Estimated Effect: {estimated_effect:.2f}',
        showlegend=True
    ))
    
    # Add confidence interval as a filled area
    fig.add_trace(go.Scatter(
        x=[0, 0],
        y=[ci_lower, ci_upper],
        mode='lines',
        line=dict(color='red', width=3),
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.2)',
        name=f'95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]',
        showlegend=True
    ))
    
    fig.update_layout(
        title="Estimated vs True Treatment Effect",
        xaxis_title="",
        yaxis_title="Treatment Effect",
        template='plotly_white',
        xaxis=dict(showticklabels=False, range=[-0.5, 0.5]),
        height=400
    )
    
    return fig, bias, estimated_effect, ci_lower, ci_upper

