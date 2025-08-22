import numpy as np
import pandas as pd

# function that simulates panel data
# N = number of people we are observing over time
def simulate(b0_treat = 10, b0_control = 40, b1_treat = 4, b1_control = 4, treatment_effect = 8, noise = 3, N = 500, treat_ratio = 0.3):
    # simulate data
    np.random.seed(1) # for reproducibility

    # units and treatment assignment with realistic proportions
    units = np.arange(N)
    n_treated = int(N * treat_ratio)  # e.g., 30% treated
    n_control = N - n_treated         # e.g., 70% control
    
    treat = np.concatenate([np.ones(n_treated), np.zeros(n_control)])
    np.random.shuffle(treat)

    # Currently, treatment status to units is randomly assigned
    df = pd.DataFrame({
        'unit' : units,
        'treat' : treat
    })

    # time periods from -3 to 1
    df = df.merge(pd.DataFrame({'time_period' : np.arange(-3, 2)}), how = 'cross')

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
    df['outcome'] = df['treat'].apply(lambda x : b0_treat if x == 1 else b0_control) 
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