import plotly.express as px
import plotly.graph_objects as go

# function that plots simulated panel data
def panel_plot(df):
    df_plot = df.copy()
    df_plot['treat'] = df_plot['treat'].apply(lambda x : 'Treated' if x == 1 else 'Control')

    # create scatterplot
    fig = px.scatter(
        df_plot,
        x='time_period',
        y='outcome',
        color='treat',  
        title="Outcomes over Time by Group",
        opacity = 0.4,
        labels={
            "time_period": "Time Period",
            "outcome": "Outcome",
            "treat": "Group"
        },
        color_discrete_map={ # Optional: set custom colors
            'Treated': 'red',
            'Control': 'blue'
        },
        template='plotly_white'
    )

    # Add the vertical line for when the treatment occurs
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="black",
        annotation_text="Treatment Start",
        annotation_position="top right"
    )

    fig.update_xaxes(tickvals = [-3, -2, -1, 0, 1])

    return fig

def mean_outcomes_plot(df):
    """
    Creates a line plot of mean outcomes over time by group.
    This replaces the raw data scatter plot with a cleaner visualization
    that shows the core DiD patterns more clearly.
    """
    # Compute mean outcomes by group and time period
    mean_df = (
        df.groupby(["treat", "time_period"])['outcome']
          .mean()
          .reset_index()
    )
    mean_df['Group'] = mean_df['treat'].map({1: 'Treated', 0: 'Control'})
    
    # Create line plot with markers
    fig = px.line(
        mean_df,
        x="time_period",
        y="outcome",
        color="Group",
        markers=True,
        labels={"time_period": "Time Period", "outcome": "Mean Outcome"},
        template="plotly_white",
        title="Mean Outcomes Over Time by Group",
        color_discrete_map={
            'Treated': 'red',
            'Control': 'blue'
        }
    )
    
    # Add the vertical line for when the treatment occurs
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="black",
        annotation_text="Treatment Start",
        annotation_position="top right"
    )
    
    fig.update_xaxes(tickvals=[-3, -2, -1, 0, 1])
    
    return fig

def means_plot(model_results):
    coeffs = model_results.params

    b0 = coeffs['Intercept']
    b1 = coeffs['treat']
    b2 = coeffs['time_indicator']
    b3 = coeffs['treat:time_indicator']

    control_pre = b0
    control_post = b0+b2
    treat_pre = b0+b1
    treat_post = b0+b1+b2+b3
    treat_counterfactual = b0+b1+b2

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[control_pre, control_post],
        mode='lines+markers',
        line=dict(color='blue', width=2),
        name='Control',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[treat_pre, treat_post],
        mode='lines+markers',
        line=dict(color='red', width=2),
        name='Treated',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[treat_pre, treat_counterfactual],
        mode='lines+markers',
        line=dict(color='red', width=2, dash='dash'),
        name='Treated (Counterfactual)',
        showlegend=True
    ))

    # Add the vertical line for when the treatment occurs
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="black",
        annotation_text="Treatment Start",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title="Difference-in-Difference Regression Visualized",
        xaxis_title="Time Period",
        yaxis_title="Outcome",
        legend_title_text='Color',
        template='plotly_white'
    )

    fig.update_xaxes(tickvals = [0, 1])

    return fig 

def bias_visualization(model_results, true_effect):
    """
    Creates a visualization showing the estimated effect vs true effect,
    including confidence intervals and bias assessment.
    """
    # Extract the treatment effect estimate and confidence interval
    estimated_effect = model_results.params['treat:time_indicator']
    ci_lower = model_results.conf_int().loc['treat:time_indicator', 0]
    ci_upper = model_results.conf_int().loc['treat:time_indicator', 1]
    
    # Calculate bias
    bias = estimated_effect - true_effect
    
    # Create the visualization
    fig = go.Figure()
    
    # Add true effect line
    fig.add_hline(
        y=true_effect,
        line_dash="dash",
        line_color="green",
        annotation_text=f"True Effect: {true_effect:.2f}",
        annotation_position="top right"
    )
    
    # Add estimated effect point
    fig.add_trace(go.Scatter(
        x=[0],
        y=[estimated_effect],
        mode='markers',
        marker=dict(size=12, color='red'),
        name=f'Estimated Effect: {estimated_effect:.2f}',
        showlegend=True
    ))
    
    # Add confidence interval as a filled area
    fig.add_trace(go.Scatter(
        x=[0, 0],
        y=[ci_lower, ci_upper],
        mode='lines',
        line=dict(color='red', width=3),
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.2)',
        name=f'95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]',
        showlegend=True
    ))
    
    fig.update_layout(
        title="Estimated vs True Treatment Effect",
        xaxis_title="",
        yaxis_title="Treatment Effect",
        template='plotly_white',
        xaxis=dict(showticklabels=False, range=[-0.5, 0.5]),
        height=400
    )
    
    return fig, bias, estimated_effect, ci_lower, ci_upper 

