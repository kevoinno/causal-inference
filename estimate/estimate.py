import statsmodels.formula.api as smf

def estimate_did(df):
    filtered_df = df[df['time_period'].isin([0, 1])].copy()
    model = smf.ols('outcome~treat*time_indicator', data = filtered_df)
    results = model.fit(cov_type = 'HC2')
    
    return results