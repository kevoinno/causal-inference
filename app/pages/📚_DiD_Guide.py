import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# Set page config
st.set_page_config(
    page_title="DiD Guide",
    page_icon="📚",
    layout="wide"
)

# Back button
if st.button("← Back to Home", type="primary"):
    st.switch_page("Home.py")

st.title("📚 Difference-in-Differences Guide")

# The intuition
st.markdown("## The intuition")
st.markdown("""So you want to find the causal effect of some policy or marketing campaign that you've ran, 
         but you didn't run a clean, randomized experiment. The idea behind difference-in-difference is that **if you can find
         a group that trends similarly to the treated group before and after the policy occurred, and that group never adopted the policy,** 
        then you can identify the impact of the policy using DiD.""")

st.markdown("## Identification Assumptions")
st.markdown("Here are the following assumptions that we must defend in order to use the DiD design. They are called **identification assumptions** because they let us identify a causal quantity of interest.")
st.markdown("1. **Parallel trends**: Without treatment, the treated and control groups would follow similar trends in outcome")
st.markdown("""2. **Stable Unit Treatment Value Assumption (SUTVA)**: There is one well-defined version of the treatment, and 
            the treatment status of one unit does not affect another unit's outcome""")
st.markdown("3. **No anticipation effects**: The treatment does not affect the outcome of the units before the treatment occurs")

st.markdown("**Important remark:** These assumptions can never truly be proven true, but they are extremely important to allow us to claim our effect is causal. There are many tests to try to falsify or show that these assumptions might not hold. Please check out the simulation tool to see how one of these placebo tests work.")
st.write("Let's go over a famous example of this to make the intuition clearer.")

# The example
st.markdown("## John Snow's Cholera Example")
st.markdown("""In the mid-1800s, people were suffering from cholera in London, but no one knew what caused cholera. John Snow hypothesized
            that cholera spreads from the water, so he used a DiD design to test this hypothesis. At the time, two water companies
            serviced London: The Southwark and Vauxhall Company and the Lambeth Water Company.""")

st.markdown("""**The context for this scenario is important**. Both water companies sourced their water from the River Thames, and 
            they both sourced from a similar location, which was downstream where the city's sewage flowed to. Both companies
            also serviced neighboring houses. But in 1852, the Lambeth Water Company started sourcing water from upstream of the 
            sewage site.""")

st.markdown("""Snow wanted to answer this causal question: **\"What is the effect of the Lambeth Water Company switching to an upstream 
            water source on the cholera death rates?\"**. Another way to frame this question is how much did the cholera death rates
            change relative to what they would have been if the Lambeth Water Company never switched water sources?""")

# The data
st.markdown("""### The Data""")

# Create the cholera data table
cholera_data = {
    'Water supply': [
        'Southwark & Vauxhall Company only',
        'Lambeth Company Only'
    ],
    'Cholera death rate per 100,000 (1849)': [1349, 847],
    'Cholera death rate per 100,000 (1854)': [1466, 193],
}

df_cholera = pd.DataFrame(cholera_data)

# Display the table with custom styling
st.dataframe(
    df_cholera,
    use_container_width=True,
    hide_index=True
)

st.markdown("""Snow had collected this data on cholera death rates per 100,000 people for households that 
            used Southwark & Vauxhall Company as their water supply and also for households that used Lambeth Company as their
            water supply. He got data for the death rates in 1849 and 1854. Remember, Lambeth changed to a different water source in 1852.
            Let's see how we can figure out the effect changing water supplies on the cholera death rate.""")

# Data for the plot
years = [1849, 1854]
vauxhall_rates = [1349, 1466]
lambeth_rates = [847, 193]

# Calculate counterfactual for Lambeth (assuming parallel trends)
# If Lambeth followed the same trend as Vauxhall, what would their 1854 rate be?
vauxhall_change = 1466 - 1349  # 117
lambeth_counterfactual = 847 + vauxhall_change  # 847 + 117 = 964

# Create the plot
fig = go.Figure()

# Add Vauxhall line (blue)
fig.add_trace(go.Scatter(
    x=years,
    y=vauxhall_rates,
    mode='lines+markers',
    name='Southwark & Vauxhall',
    line=dict(color='blue', width=3),
    marker=dict(size=10, color='blue')
))

# Add Lambeth line (red)
fig.add_trace(go.Scatter(
    x=years,
    y=lambeth_rates,
    mode='lines+markers',
    name='Lambeth (Actual)',
    line=dict(color='red', width=3),
    marker=dict(size=10, color='red')
))

# Add Lambeth counterfactual (dotted red)
fig.add_trace(go.Scatter(
    x=[1849, 1854],
    y=[847, lambeth_counterfactual],
    mode='lines+markers',
    name='Lambeth (If they never switched water sources)',
    line=dict(color='red', width=2, dash='dot'),
    marker=dict(size=8, color='red', symbol='diamond')
))

# Add causal effect line (vertical line from counterfactual to actual)
# Offset slightly to the right to avoid overlapping with data points
offset = 0.1  # Small offset to the right

# Main vertical line
fig.add_trace(go.Scatter(
    x=[1854 + offset, 1854 + offset],
    y=[lambeth_counterfactual, 193],
    mode='lines',
    name='Causal Effect',
    line=dict(color='black', width=3),
    showlegend=False
))

# Top horizontal cap
fig.add_trace(go.Scatter(
    x=[1854 + offset - 0.05, 1854 + offset + 0.05],
    y=[lambeth_counterfactual, lambeth_counterfactual],
    mode='lines',
    line=dict(color='black', width=3),
    showlegend=False
))

# Bottom horizontal cap
fig.add_trace(go.Scatter(
    x=[1854 + offset - 0.05, 1854 + offset + 0.05],
    y=[193, 193],
    mode='lines',
    line=dict(color='black', width=3),
    showlegend=False
))

# Add text annotation for causal effect
fig.add_annotation(
    x=1854 + offset + 0.2,  # Position text to the right of the bar
    y=(lambeth_counterfactual + 193) / 2,  # Position at middle of the bar
    text="Causal Effect",
    showarrow=False,
    font=dict(size=12, color='black'),
    xanchor='left',
    yanchor='middle'
)

# Update layout
fig.update_layout(
    title='Cholera Death Rates: Lambeth vs Southwark & Vauxhall',
    xaxis_title='Year',
    yaxis_title='Cholera Death Rate per 100,000',
    height=500
)

# Add vertical line for treatment (1852)
fig.add_vline(x=1852, line_dash="dash", line_color="gray")

# Display the plot
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
To estimate the causal effect of switching water sources on the cholera death rate for households that used Lambeth, the DiD design tries to estimate 
what the cholera death rate for Lambeth households would be in 1854 **had Lambeth never switched water sources**. In practice, we will never know this exact value, but
the DiD design assumes that the death rate for Lambeth households would have trended similarly to the death rate for Southwark households, allowing us to estimate what
the Lambeth cholera death rates would have been in 1854 had they never switched water sources. This is known as the **parallel trends** assumption. In the graph above,
we see the parallel trends assumption as the dotted red line (Lambeth's cholera death rate had they never switched) and the blue line (Southwark's cholera death rate) are parallel.
            
Let's examine see if making these identification assumptions (specifically parallel trends) are feasible:

**1. Parallel Trends Assumption**: Parallel trends likely holds because both water companies served similar areas of London (neighboring households). This means that any outside factors that affect cholera death rate such as the quality of healthcare would affect both groups similarly.

**2. SUTVA (Stable Unit Treatment Value Assumption)**: The validity of SUTVA can be debated. People can argue that there are spillover effects between households. If Southwark customers contracted cholera from contaminated water, they could spread the disease to their Lambeth-using neighbors through human contact, even though the water companies served different households. However, we believe this violation is likely minor because cholera is primarily waterborne rather than person-to-person transmitted, and mobility was limited in 1850s London, reducing the scope of potential spillover effects.

**3. No Anticipation Effects**: In this example, we believe the no anticipation assumption likely holds because the water source changes were not publicly announced in advance, and there was limited public awareness of the connection between water quality and cholera transmission. People in 1850s London did not understand that cholera was waterborne, so they would not have changed their behavior in anticipation of the water source change. The treatment appears to have been implemented without public knowledge, making anticipation effects unlikely.
            
Using these assumptions, we have: 
    
1. Lambeth's observed cholera death rate was in 1854

2. An estimate of Lambeth's cholera death rate in 1854 if they never switched sources

So taking the difference between **(2)** and **(1)**, we can estimate the causal effect. The graph above provides a nice visual of how the DiD design works. For clarification on notation, we'll use $E[Y_d(t)|D]$ where $d$ indicates the potential treatment status (0 for control, 1 for treated), $t$ indicates the time period (0 for pre-treatment, 1 for post-treatment), and $D$ indicates the observed treatment assignment.
""")

st.markdown("**Step 1:** The cholera death rate for Lambeth in 1854 after switching water sources (which we observed in the data):")

st.latex(r'''
E[Y_1(1)|D=1] = 193
''')

st.markdown("**Step 2:** The cholera death rate for Lambeth in 1854 had they never switched water sources (which we estimated):")

st.latex(r'''
\begin{align*}
E[Y_0(1)|D=1] &= E[Y_1(0)|D=1] + (E[Y_0(1)|D=0] - E[Y_0(0)|D=0]) \\
&= 847 + (1466 - 1349) \\
&= 964
\end{align*}
''')

st.markdown("**Step 3:** The causal effect of switching water sources on death rates for Lambeth:")

st.latex(r'''
\begin{align*}
\tau &= E[Y_1(1)|D=1] - E[Y_0(1)|D=1] \\
&= 193 - 964 \\
&= -771
\end{align*}
''')

st.markdown("""
So taking the difference between **(2)** and **(1)**, we get a causal effect of -771. This means that 
Lambeth switching water sources decreased the death rate for households that used Lambeth's water by 771 per 100,000 people.
""")

st.markdown("**Alternative calculation using two differences:**")
st.markdown("So why is the method called difference-in-difference? Because we could have gotten the same result by taking two differences:")

st.markdown("**Difference 1:** The change in Lambeth's death rates:")

st.latex(r'''
\begin{align*}
\Delta E[Y_1|D=1] &= E[Y_1(1)|D=1] - E[Y_1(0)|D=1] \\
&= 193 - 847 \\
&= -654
\end{align*}
''')

st.markdown("**Difference 2:** The change in Vauxhall's death rates:")

st.latex(r'''
\begin{align*}
\Delta E[Y_0|D=0] &= E[Y_0(1)|D=0] - E[Y_0(0)|D=0] \\
&= 1466 - 1349 \\
&= 117
\end{align*}
''')

st.markdown("**DiD Estimate:**")

st.latex(r'''
\begin{align*}
\tau &= \Delta E[Y_1|D=1] - \Delta E[Y_0|D=0] \\
&= -654 - 117 \\
&= -771
\end{align*}
''')

st.markdown("""
See how this is the same! I introduced the calculations differently 
because I wanted to explicitly show that we are trying to estimate a **counterfactual** (the death rate for Lambeth in 1854 had
they never changed water sources). This concept is the basis of causal inference. We are always trying to estimate a counterfactual
no matter what technique we use.
""")

st.markdown("### How DiD mathematically works")
st.markdown("""
The more formal math below shows how we are able to identify the average effect on the treated group (ATT) using the parallel trends assumption:
""")

st.markdown("""
Our goal is to estimate the Average Treatment Effect on the Treated Group (ATT):
            """)

st.latex(r'''
ATT = E[Y_1(1)] - E[Y_1(0)]
''')

st.markdown("""
This just is saying that the ATT is the difference between the solid red line 
(the average outcome of the treated group if they actually recieved the treatment) and dotted red line 
(the average outcome of the treated group had that not received the treatment). We don't observe the second term, so we make the **parallel trends
assumption** to try to identify the ATT:
            """)

st.latex(r'''
E[Y_0(1) - Y_0(0) | D = 1] = E[Y_0(1) - Y_0(0) | D = 0]
''')

st.markdown("""
    This assumption is saying that if the treated group wasn't actually treated, then they would follow the same trend as the untreated group over time. Using 
    this assumption, we identify the ATT using the following proof:
            """)

st.latex(r'''
\begin{align}
ATT &= E[Y_1(1) | D = 1] - E[Y_0(1) | D = 1] \tag{1} & \text{By definition} \\
    &= E[Y_1(1) | D = 1] - E[Y_0(0) | D = 1] - \{E[Y_0(1) | D = 1] - E[Y_0(0) | D = 1]\} \tag{2} & \text{Add and subtract } E[Y_0(0) | D = 1] \\ 
    &= E[Y_1(1) | D = 1] - E[Y_0(0) | D = 1] - \{E[Y_0(1) | D = 0] - E[Y_0(0) | D = 0]\} \tag{3} & \text{Parallel trends} \\
    &= E[Y(1) | D = 1] - E[Y(0) | D = 1] -  \{E[Y(1) | D = 0] - E[Y(0) | D = 0]\} \tag{4} & \text{Consistency}
\end{align}
''')

st.markdown("""
One tricky part of this proof is in going from line 3 to 4. Here, we assume $E[Y_0(0) | D = 1] = E[Y_1(0) | D = 1]$. This is saying the potential outcomes 
in the pre-treatment period for the treated group are the same had the treated group received treatment or not. This makes sense, because this is before the
treatment was applied, so the potential outcomes in the pre-treatment period should be the same for the treated group. After we make this assumption, the rest
of the proof follows by consistency.   

This final expression shows that the ATT can be identified as the difference between:
1. The change in outcomes for the treated group from pre- to post-treatment
2. The change in outcomes for the control group from pre- to post-treatment
""")



st.markdown("### Using Linear Regression to Estimate the ATT")

st.markdown("""
So far, we've worked with aggregated data where we had the mean outcomes for each group. But in practice, we usually have individual-level data 
where each row represents one person, household, or unit. When we have this type of data, we use linear regression to estimate the ATT.
""")

st.markdown("**The DiD Regression Model**")

st.markdown("""
We estimate the following regression equation:

$$Y_{it} = \\beta_0 + \\beta_1 \\text{Treat}_i + \\beta_2 \\text{Time}_t + \\beta_3 (\\text{Treat}_i \\times \\text{Time}_t) + \\epsilon_{it}$$

Where:
- $Y_{it}$ is the outcome for unit $i$ at time $t$
- $\\text{Treat}_i$ is 1 if unit $i$ is in the treated group, 0 otherwise
- $\\text{Time}_t$ is 1 if time $t$ is post-treatment, 0 if pre-treatment
- $\\epsilon_{it}$ is the error term
""")

st.markdown("**Coefficient Interpretation**")

# Create coefficient interpretation table
coef_data = {
    'Coefficient': ['β₀', 'β₁', 'β₂', 'β₃'],
    'Term': ['Intercept', 'Treat', 'Time', 'Treat × Time'],
    'Interpretation': [
        'Control group outcome in pre-treatment period',
        'Difference between treated and control groups in pre-treatment period',
        'Time trend for control group (pre to post)',
        'ATT: Causal effect of treatment'
    ]
}

df_coef = pd.DataFrame(coef_data)

st.dataframe(
    df_coef,
    use_container_width=True,
    hide_index=True
)

st.markdown("**Implementation in Python**")

st.markdown("""
Here's the exact code used in this app to estimate the DiD regression:
""")

st.code("""
import statsmodels.formula.api as smf

def estimate_did(df):
    # Filter to pre and post treatment periods
    filtered_df = df[df['time_period'].isin([0, 1])].copy()
    
    # Run the DiD regression
    model = smf.ols('outcome~treat*time_indicator', data=filtered_df)
    results = model.fit(cov_type='HC2')
    
    return results
""", language='python')

st.markdown("""
**Code Explanation:**
- We filter the data to only include pre-treatment (t=0) and post-treatment (t=1) periods
- The formula `'outcome~treat*time_indicator'` creates the interaction term automatically
- `cov_type='HC2'` uses robust standard errors to account for heteroskedasticity
- The coefficient on `treat:time_indicator` is our ATT estimate
""")

st.markdown("Now that you have a basic understanding for how this design works, play around with the simulation tool to develop your intuition!")

st.write("Data and example sourced from: https://pmc.ncbi.nlm.nih.gov/articles/PMC8006863/")