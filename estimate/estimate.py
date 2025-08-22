import statsmodels.formula.api as smf

# Estimate the ATT using (2x2 DiD setup)
def estimate_did(df):
    filtered_df = df[df['time_period'].isin([0, 1])].copy()
    model = smf.ols('outcome~treat*time_indicator', data = filtered_df)
    results = model.fit(cov_type = 'HC2')
    
    return results

# Runs a placebo test (2x2 DiD setup) on time periods -1, 0
def placebo_test(df):
    filtered_df = df[df['time_period'].isin([-1, 0])].copy()
    filtered_df['time_indicator'] = filtered_df['time_period'].apply(lambda x : 1 if x == 0 else 0)

    model = smf.ols('outcome~treat*time_indicator', data = filtered_df)
    results = model.fit(cov_type = 'HC2')

    return results
