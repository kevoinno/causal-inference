import statsmodels.formula.api as smf

# Estimate the ATT
def estimate_did(df):
    filtered_df = df[df['time_period'].isin([0, 1])].copy()
    model = smf.ols('outcome~treat*time_indicator', data = filtered_df)
    results = model.fit(cov_type = 'HC2')
    
    return results

# Run a placebo test that regresses the outcome on the treatment, time_period and their interaction
def placebo_test(df):
    # Filter to pre-treatment data
    pre_treatment_df = df[df['time_period'] <= 0].copy()

    # Fit model
    model = smf.ols('outcome~treat*time_period', data = pre_treatment_df)
    results = model.fit(cov_type = 'HC2')

    return results