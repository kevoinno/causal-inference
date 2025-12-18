# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: venv
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import statsmodels.formula.api as smf


# %%
# function that simulates panel data
# N = number of people we are observing over time
def simulate(b0_treat = 10, b0_control = 40, b1_treat = 4, b1_control = 4, treatment_effect = 8, noise = 3, N = 500, R = 100):
    # simulate data

    # units and treatment assignment
    units = np.arange(N)
    treat = np.repeat([0, 1], np.floor(N/2)) 
    np.random.shuffle(treat)

    df = pd.DataFrame({
        'unit' : units,
        'treat' : treat
    })

    # time periods from -3 to 1
    df = df.merge(pd.DataFrame({'time_period' : np.arange(-3, 2)}), how = 'cross')

    # add time indicator (1 if post-treatment else 0)
    df['time_indicator'] = (df['time_period'] == 1).astype(int)

    # add outcomes

    # baseline outcomes
    df['outcome'] = df['treat'].apply(lambda x : b0_treat if x == 1 else b0_control) 

    # apply trends
    treat_mask = df['treat'] == 1 
    control_mask = df['treat'] == 0

    df.loc[treat_mask, 'outcome'] += df.loc[treat_mask, 'time_period'] * b1_treat
    df.loc[control_mask, 'outcome'] += df.loc[control_mask, 'time_period'] * b1_control

    # apply treatment effect
    df['outcome'] = df['outcome'] + treatment_effect * df['treat'] * df['time_indicator']

    # add noise
    df['outcome'] = df['outcome'] + np.random.normal(0, noise, 5*N)

    return df        


# %%
# function that plots simulated panel data
def panel_plot(df):
    df_plot = df.copy()
    df_plot['treat'] = df_plot['treat'].apply(lambda x : 'Treated' if x == 1 else 'Control')

    # create scatterplot
    fig = px.scatter(
        df_plot,
        x='time_period',
        y='outcome',
        color='treat',  
        title="Simulated Difference-in-Differences Data",
        opacity = 0.4,
        labels={
            "time_period": "Time Period",
            "outcome": "Outcome",
            "treat": "Group"
        },
        color_discrete_map={ # Optional: set custom colors
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

    fig.update_xaxes(tickvals = [-3, -2, -1, 0, 1])

    fig.show()


# %%
# set default parameters
np.random.seed(42)

# %%
df = simulate(b0_treat = 20, b0_control = 10, b1_treat = 4, b1_control = 4, treatment_effect = -50, noise = 0)

# %%
panel_plot(df)


# %% [markdown]
# $$ Y_i = \beta_0 + \beta_1*treat + \beta_2*time + \beta_3*treat*time$$

# %%
def estimate(df):
    filtered_df = df[df['time_period'].isin([0, 1])].copy()
    model = smf.ols('outcome~treat*time_indicator', data = filtered_df)
    results = model.fit(cov_type = 'HC2')
    
    return results


# %%
# function that plots the classic DiD means visualization
def means_plot(model_results):
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

    # plot pre-treatment values
    fig = px.scatter(
        x = [0, 1, 0, 1, 1],
        y = [control_pre, control_post, treat_pre, treat_post, treat_counterfactual],
        color = ['blue', 'blue', 'red', 'red', 'red'],
        title="Difference-in-Difference Visualized",
        labels={
            "x": "Time Period (Pre-treatment vs Post-treatment)",
            "y": "Outcome"
        },
        template = 'plotly_white'
    )

    # Control line (pre to post)
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[control_pre, control_post],
        mode='lines',
        line=dict(color='blue', width=2),
        name='Control',
        showlegend=False  # hide from legend since you already have the points
    ))

    # Treated line (pre to post)
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[treat_pre, treat_post],
        mode='lines',
        line=dict(color='red', width=2),
        name='Treated',
        showlegend=False
    ))

    # Counterfactual line (dashed)
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[treat_pre, treat_counterfactual],
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Treated (Counterfactual)',
        showlegend=False
    ))

    fig.show()


# %%
def placebo_test(df):
    # Filter to pre-treatment data
    pre_treatment_df = df[df['time_period'] <= 0].copy()

    # Fit model
    model = smf.ols('outcome~treat*time_period', data = pre_treatment_df)
    results = model.fit(cov_type = 'HC2')

    return results


# %%
test_df = simulate()
print(test_df.shape)

panel_plot(test_df)

# %%
res = estimate(test_df)

# %%
means_plot(res)

# %%
placebo_results = placebo_test(test_df)
print(placebo_results.summary())

