import plotly.express as px
import plotly.graph_objects as go

def panel_plot(df):
    df_plot = df.copy()

    df_plot['treat'] = df_plot['treat'].apply(lambda x : 'Treated' if x == 1 else 'Control')

    fig = px.scatter(
        df_plot,
        x='time_period',
        y='outcome',
        color='treat',  
        title="Simulated Difference-in-Differences Data",
        opacity = 0.4,
        labels={
            "time_period": "Time Period",
            "outcome": "Outcome",
            "treat": "Group"
        },
        color_discrete_map={
            'Treated': 'red',
            'Control': 'blue'
        },
        template='plotly_white'
    )
    fig.add_vline(
        x=4,
        line_dash="dash",
        line_color="black",
        annotation_text="Treatment Start",
        annotation_position="top right"
    )
    fig.show()

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
    fig.update_layout(
        title="Difference-in-Difference Visualized",
        xaxis_title="Time Period (Pre-treatment vs Post-treatment)",
        yaxis_title="Outcome",
        legend_title_text='Color',
        template='plotly_white'
    )
    fig.show() 