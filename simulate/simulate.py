import numpy as np
import pandas as pd

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