import statsmodels.formula.api as smf

def estimate_did(df):
    model = smf.ols(formula = 'outcome ~ treat * time_indicator', data = df)
    results = model.fit(cov_type = 'HC2')
    return results 