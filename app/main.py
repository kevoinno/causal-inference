from simulate.simulate import simulate
from estimate.estimate import estimate_did
from visualize.visualize import panel_plot, means_plot
import numpy as np

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)

    # Simulate data with default parameters
    df = simulate()

    # Estimate DiD model
    results = estimate_did(df)

    # Plot panel data
    panel_plot(df)

    # Plot means plot using model results
    means_plot(results) 

    print("Ran succesfully")