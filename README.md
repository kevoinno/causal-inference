# causal-inference

## 1. Define objectives & project structure  
- The goal of this project is to allow users to simulate and play around with different parameters of a 2x2 DiD model to see how that affects their causal estimate. This app should help them build an intuition with what can go wrong and how to run a DiD correctly.
- Sketch your folder layout (e.g. `simulate/`, `estimate/`, `visualize/`, `app/`).  

## 2. Specify key parameters  
**Goal:** Decide on the inputs users will control.  
**Actions:**  
- List each slider/field and its range:  
    - $mu_{treated}$  
    - $mu_{control}$   
    - $beta_{treated}$  
    - $beta_{control}$  
    - $tau$  
    - $\epsilon$ 
    - N
    - R


## 3. Simulate two-period panel data  
**Goal:** Generate a tidy table with columns `unit`, `time`, `treated`, `outcome`.  
**Actions:**  
- Define how treated vs. control units are assigned.  
- Map each unit’s untreated trend and add Δ₉ₐₚ for treated vs. control.  
- Add τ to treated units in period 1.  
- Add random noise to both periods.  
- Verify that group means match theoretical formulas.  

## 4. Build a placebo-test simulator  
**Goal:** Create a parallel dataset where the true effect is zero.  
**Actions:**  
- Randomly reassign treatment label or shift treatment to period 0.  
- Run the same DiD estimator and confirm estimates center on zero.  

## 5. Implement the DiD estimator  
**Goal:** Compute ATT via both difference-in-means and regression.  
**Actions:**  
- Calculate  
  1. \(\big(\bar Y_{1,\text{treat}} - \bar Y_{0,\text{treat}}\big) - \big(\bar Y_{1,\text{ctrl}} - \bar Y_{0,\text{ctrl}}\big)\)  
  2. The coefficient on `treated × time` from a two-way regression  
- Check both recover τ when Δ₉ₐₚ = 0 and σ = 0.  

## 6. Design core visualizations  
**Goal:** Create three intuitive charts:  
1. **Pre-Post lines** for treated vs. control  
2. **Histogram of DiD estimates** over R simulations with true τ marked  
3. **Bias vs. Trend-Gap plot** showing how bias grows with Δ₉ₐₚ  
**Actions:**  
- Decide axis labels, titles, legend placement.  
- Validate each plot against edge cases (no noise, no gap).  

## 7. Wire up Streamlit app layout  
**Goal:** Assemble a clean, interactive UI.  
**Actions:**  
- Place all parameter controls in a sidebar.  
- Use tabs or expanders for:  
  - Data preview  
  - DiD plot  
  - Regression output  
  - Placebo test  
- Add checkboxes for “Show raw data” and a download link for the last simulation.  

## 8. Add diagnostics & user feedback  
**Goal:** Give users immediate take-aways.  
**Actions:**  
- Display numeric summary under each plot, e.g.:  
  > Estimated ATT = …  True τ = …  ⇒ Bias = …  
- Include tooltips explaining “Parallel-trend gap” and “Placebo test.”  

## 9. Validate & test  
**Goal:** Ensure correctness under all parameter settings.  
**Actions:**  
- Test extremes: Δ₉ₐₚ = 0 (bias → 0), σ = 0 (estimate = τ).  
- Simulate small N (e.g. N = 4) to confirm handling of few observations.  
- Stress-test large R for performance.  

## 10. Document & deploy  
**Goal:** Make the applet easy to understand and share.  
**Actions:**  
- Write a README: purpose, installation, usage.  
- Add in-app markdown explanations and formula references.  
- Deploy to Streamlit Community Cloud (or similar) and share the URL.  
