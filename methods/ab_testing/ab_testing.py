from scipy.stats import norm
import numpy as np

def calculate_sample_size(alpha : float, power : float, delta : float, variance : float) -> float:
    """ Calculates the sample size needed to perform an A/B test comparing means
    Parameters:
    ----------
    alpha : float
        The significiance threshold of the experiment. Between 0 and 1
    power : float
        The desired power of the experiment. Between 0 and 1
    delta : float
        The desired effect size that you want to detect in the experiment.
    variance : float
        The variance of the group you will be running the experiment on. The pooled variance will be calculated by doing 2*variance. Must be greater than or equal to 0

    Returns:
    n : int
        The required sample size for each group
    """
    if alpha < 0 or alpha > 1:
        raise Exception("Alpha must be between 0 and 1")

    if power < 0 or power > 1:
        raise Exception("Power must be between 0 and 1")

    if variance < 0:
        raise Exception("Variance must be greater than or equal to 0")

    Z_ALPHA = norm.ppf(1 - alpha / 2)
    Z_POWER = norm.ppf(power)
    POOLED_VARIANCE = 2 * variance 
    
    n = ((Z_ALPHA + Z_POWER)**2 * POOLED_VARIANCE) /  (delta**2)

    return int(np.ceil(n))
