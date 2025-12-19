from scipy.stats import norm
import numpy as np


def calculate_sample_size(
    alpha: float, power: float, delta: float, variance: float, ratio: float
) -> dict[str, int]:
    """Calculates the sample size needed to perform an A/B test comparing means
    Parameters:
    ----------
    alpha : float
        The significiance threshold of the experiment. Between 0 and 1
    power : float
        The desired power of the experiment. Between 0 and 1
    delta : float
        The desired effect size that you want to detect in the experiment. Please specify an absolute effect size.
        E.g. if the control group's conversion rate is 0.10 and the treated group's is 0.15, delta = 0.05.
        DO NOT put the relative effect size (0.5)
    variance : float
        The variance of the metric in your population. Must be greater than or equal to 0
    ratio : float
        The ratio of treated to untreated units. (e.g. 0.9 means 90% are treated, 10% are control)

    Returns:
    group_sample_sizes : dict
        A dictionary with the following keys:
            "n_control" : number of control units needed
            "n_treated" : number of treated units needed
            "n_total" : number of total units needed
    """
    if alpha < 0 or alpha > 1:
        raise Exception("Alpha must be between 0 and 1")

    if power < 0 or power > 1:
        raise Exception("Power must be between 0 and 1")

    if variance < 0:
        raise Exception("Variance must be greater than or equal to 0")

    if ratio <= 0 or ratio >= 1:
        raise Exception("Ratio must be between 0 and 1 (not including 0 or 1)")

    Z_ALPHA = norm.ppf(1 - alpha / 2)
    Z_POWER = norm.ppf(power)

    n_total = ((Z_ALPHA + Z_POWER) ** 2 * variance) / (ratio * (1 - ratio) * delta**2)
    n_treated = int(np.ceil(n_total * ratio))
    n_control = int(np.ceil(n_total - n_treated))
    n_total_new = int(
        n_treated + n_control
    )  # to make sure rounded up n_treated + n_control = n_total

    res = {"n_control": n_control, "n_treated": n_treated, "n_total": n_total_new}

    return res


def calculate_test_length(traffic: int, total_sample_size: int) -> None:
    """Calculate the number of days needed to run an A/B test experiment.

    This is a simplified estimate assuming constant daily traffic and no user overlap.
    For more accurate planning, consider traffic variability and test design.

    Parameters
    ----------
    traffic : int
        Daily traffic (number of units, e.g., visitors) the product/website receives.
    total_sample_size : int
        Total sample size required (sum for both groups, typically 2x per-group size from calculate_sample_size).

    Returns
    -------
    days : int
        Estimated number of days to reach the total sample size (rounded up).

    Notes
    -----
    - Assumes uniform daily traffic and sample accumulation.
    - Limitations: Doesn't account for seasonality, user-level effects, or variable traffic.
    - Valid for basic planning but consult experts for complex scenarios.
    """
    raise NotImplementedError("Function not yet implemented")
