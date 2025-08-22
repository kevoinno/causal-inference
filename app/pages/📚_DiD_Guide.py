import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config for this specific page
st.set_page_config(
    page_title="DiD Guide",
    page_icon="📚",
    layout="wide"
)

# Back button with primary styling
if st.button("← Back to Home", type="primary"):
    st.switch_page("Home.py")

st.write("Under Construction")
# st.header("Difference-in-difference Guide")
# st.sidebar.header("DiD Guide")

# # The intuition
# st.markdown("## The intuition")
# st.markdown("""So you want to find the causal effect of some policy or marketing campaign that you've ran, 
#          but you didn't run a clean, randomized experiment. The idea behind difference-in-difference is that **if you can find
#          a group that trends similarly to the treated group before and after the policy occurred, and that group never adopted the policy,** 
#         then you can identify the impact of the policy using DiD.""")
# st.write("Let's go over a famous example of this to make the intuition clear.")

# # The example
# st.markdown("## John Snow's Cholera Example")
# st.markdown("""In mid-1800s, people were suffering from cholera in London, but no one knew what caused cholera. John Snow hypothesized
#             that cholera spreads from the water, so he used a DiD design to test this hypothesis. At the time, two water companies
#             serviced London: The Southwark and Vauxhall Company and the Lambeth Water Company.""")

# st.markdown("""**The context for this is important**. Both water companies sourced their water from the River Thames, and 
#             they both sourced from a similar location, which was downstream where the city's sewage flowed to. Both companies
#             also serviced neighboring houses. But in 1852, the Lambeth Water Company started sourcing water from upstream of the 
#             sewage site.""")

# st.markdown("""Snow wanted to answer this causal question: **\"What is the effect of the Lambeth Water Company switching to an upstream 
#             water source on the cholera death rates?\"**. Another way to frame this question is how much did the cholera death rates
#             change relative to what they would have been if the Lambeth Water Company never switched water sources?""")

# # The data
# st.markdown("""### The Data""")

# # Create the cholera data table
# cholera_data = {
#     'Water supply': [
#         'Southwark & Vauxhall Company only',
#         'Lambeth Company Only'
#     ],
#     'Cholera death rate per 100,000 (1849)': [1349, 847],
#     'Cholera death rate per 100,000 (1854)': [1466, 193],
# }

# df_cholera = pd.DataFrame(cholera_data)

# # Display the table with custom styling
# st.dataframe(
#     df_cholera,
#     use_container_width=True,
#     hide_index=True
# )

# st.markdown("""Snow had collected this data on cholera death rates per 100,000 people for households that 
#             used Southwark & Vauxhall Company as their water supply and also for households that used Lambeth Company as their
#             water supply. He got data for the death rates in 1849 and 1854. Remember, Lambeth changed to a different water source in 1852.
#             Let's see how we can figure out the effect changing water supplies on the cholera death rate.""")

# # Data for the plot
# years = [1849, 1854]
# vauxhall_rates = [1349, 1466]
# lambeth_rates = [847, 193]

# # Calculate counterfactual for Lambeth (assuming parallel trends)
# # If Lambeth followed the same trend as Vauxhall, what would their 1854 rate be?
# vauxhall_change = 1466 - 1349  # 117
# lambeth_counterfactual = 847 + vauxhall_change  # 847 + 117 = 964

# # Create the plot
# fig = go.Figure()

# # Add Vauxhall line (blue)
# fig.add_trace(go.Scatter(
#     x=years,
#     y=vauxhall_rates,
#     mode='lines+markers',
#     name='Southwark & Vauxhall',
#     line=dict(color='blue', width=3),
#     marker=dict(size=10, color='blue')
# ))

# # Add Lambeth line (red)
# fig.add_trace(go.Scatter(
#     x=years,
#     y=lambeth_rates,
#     mode='lines+markers',
#     name='Lambeth (Actual)',
#     line=dict(color='red', width=3),
#     marker=dict(size=10, color='red')
# ))

# # Add Lambeth counterfactual (dotted red)
# fig.add_trace(go.Scatter(
#     x=[1849, 1854],
#     y=[847, lambeth_counterfactual],
#     mode='lines+markers',
#     name='Lambeth (If they never switched water sources)',
#     line=dict(color='red', width=2, dash='dot'),
#     marker=dict(size=8, color='red', symbol='diamond')
# ))

# # Update layout
# fig.update_layout(
#     title='Cholera Death Rates: Lambeth vs Southwark & Vauxhall',
#     xaxis_title='Year',
#     yaxis_title='Cholera Death Rate per 100,000',
#     height=500
# )

# # Add vertical line for treatment (1852)
# fig.add_vline(x=1852, line_dash="dash", line_color="gray")

# # Display the plot
# st.plotly_chart(fig, use_container_width=True)

# st.markdown("""
# So how do we actually measure the effect of the changing of water sources for the Lambeth Company? The best way to think about this
# is assuming we had all the information possible. If we did, then we could take the difference between Lambeth's cholera death rate in 
# 1854 after moving water sources and Lambeth's cholera death rate in 1854 had they never switched water sources. Sadly, the reality
# is that Lambeth did switch water sources, so we can never know what the death rate would have been in 1854 had they never switched. 
# But, with the difference-in-difference design, we can make some assumptions to estimate it.
            
# Difference-in-difference assumes **parallel trends** between Lambeth and and Southwark & Vauxhall. This means that we are assuming 
# that if Lambeth had never switched water sources in 1852, then their cholera death rate would have trended the same as Southwark &
# Vauxhall's death rate. Remember, Southwark & Vauxhall never switched water sources. We can see this in the graph above. 
# Notice how solid blue line and dotted red line are parallel? 
            
# With this assumption, we can estimate the cholera death rate for Lambeth in 1854 to be Lambeth's death rate in 1849 + the trend of 
# Southwark & Vauxhall from 1849 to 1854. Then we have everything we need to estimate the effect! The steps are below. For some 
# clarification on notation, we'll use $E[Y_d(t)|D]$ where $d$ indicates the potential treatment status (0 for control, 1 for treated), $t$ indicates the time period (0 for pre-treatment, 1 for post-treatment), and $D$ indicates the observed treatment assignment.
# """)

# st.markdown("**Step 1:** The cholera death rate for Lambeth in 1854 after switching water sources (which we observed in the data):")

# st.latex(r'''
# E[Y_1(1)|D=1] = 193
# ''')

# st.markdown("**Step 2:** The cholera death rate for Lambeth in 1854 had they never switched water sources (which we estimated):")

# st.latex(r'''
# E[Y_0(1)|D=1] = E[Y_1(0)|D=1] + (E[Y_0(1)|D=0] - E[Y_0(0)|D=0]) = 847 + (1466 - 1349) = 964
# ''')

# st.markdown("**Step 3:** The causal effect of switching water sources on death rates for Lambeth:")

# st.latex(r'''
# \tau = E[Y_1(1)|D=1] - E[Y_0(1)|D=1] = 193 - 964 = -771
# ''')

# st.markdown("""
# So to get the effect of changing water supplies on the death rate for Lambeth, we get a causal effect of -771. This means that 
# Lambeth switching water sources decreased the death rate for households that used Lambeth's water by 771 per 100,000 people.
            
# So why is this design called difference-in-difference? Because we could have gotten that answer by taking the 2 differences:
# """)

# st.markdown("**Alternative calculation using differences:**")
# st.markdown("So why is the method called difference-in-difference? Because we could have gotten the same result by taking 2 differences:")

# st.markdown("**Difference 1:** The change in Lambeth's death rates:")

# st.latex(r'''
# \Delta E[Y_1|D=1] = E[Y_1(1)|D=1] - E[Y_1(0)|D=1] = 193 - 847 = -654
# ''')

# st.markdown("**Difference 2:** The change in Vauxhall's death rates:")

# st.latex(r'''
# \Delta E[Y_0|D=0] = E[Y_0(1)|D=0] - E[Y_0(0)|D=0] = 1466 - 1349 = 117
# ''')

# st.markdown("**DiD Estimate:**")

# st.latex(r'''
# \tau = \Delta E[Y_1|D=1] - \Delta E[Y_0|D=0] = -654 - 117 = -771
# ''')

# st.markdown("""
# See how this is the same! I introduced the calculations differently 
# because I wanted to explicitly show that we are trying to estimate a **counterfactual** (the death rate for Lambeth in 1854 had
# they never changed water sources). This concept is the basis of causal inference. We are always trying to estimate a counterfactual
# no matter what technique we use.
# """)

# st.markdown("""
# The more formal math below shows how we are able to identify the average effect on the treated group (ATT) using the parallel trends assumption:
# """)

# st.markdown("""
# Our goal is to estimate the ATT:
#             """)

# st.latex(r'''
#     ATT = E[Y_1(1)] - E[Y_1(0)]
#          ''')

# st.markdown("""
# This just is saying that the ATT is the difference between the solid red line 
# (the average outcome of the treated group if they actually recieved the treatment) and dotted red line 
# (the average outcome of the treated group had that not received the treatment). We don't observe the second term, so we make the **parallel trends
# assumption** to try to identify the ATT:
#             """)

# st.latex(r'''
#     E[Y_0(1) - Y_0(0) | D = 1] = E[Y_0(1) - Y_0(0) | D = 0]
#          ''')

# st.markdown("""
#     This assumption is saying that if the treated group wasn't actually treated, then they would follow the same trend as the untreated group over time. Using 
#     this assumption, we identify the ATT using the following proof:
#             """)

# st.latex(r'''
#     ATT = E[Y_1(1)] - E[Y_1(0)] \\
#         = E[Y_1(1) - Y_0(1) | D = 1] + E[Y_0(1) - Y_0(0) | D = 1] \\
#         = E[Y_1(1) - Y_0(1) | D = 1] + E[Y_0(1) - Y_0(0) | D = 0] \\
#         = E[Y_1(1) - Y_0(1) | D = 1] + (E[Y_0(1) | D = 0] - E[Y_0(0) | D = 0]) \\
#         = E[Y_1(1) | D = 1] - E[Y_0(1) | D = 1] + (E[Y_0(1) | D = 0] - E[Y_0(0) | D = 0]) \\
#         = E[Y_1(1) | D = 1] - E[Y_0(0) | D = 1] + (E[Y_0(1) | D = 0] - E[Y_0(0) | D = 0]) \\
#         = E[Y_1(1) | D = 1] - E[Y_0(0) | D = 1] + (E[Y_0(1) | D = 0] - E[Y_0(0) | D = 0]) \\
#         = (E[Y_1(1) | D = 1] - E[Y_0(0) | D = 1]) - (E[Y_0(1) | D = 0] - E[Y_0(0) | D = 0])
#          ''')

# st.markdown("""
# This final expression shows that the ATT can be identified as the difference between:
# 1. The change in outcomes for the treated group from pre- to post-treatment
# 2. The change in outcomes for the control group from pre- to post-treatment

# This is exactly what we calculated in our cholera example!
# """)

# st.write("Data and example sourced from: https://pmc.ncbi.nlm.nih.gov/articles/PMC8006863/")
