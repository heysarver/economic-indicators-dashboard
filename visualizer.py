import plotly.graph_objects as go

def create_line_graph(datasets, title, y_axis_label, is_percentage=False):
    fig = go.Figure()
    
    colors = ['blue', 'red', 'green', 'purple', 'orange']  # Add more colors if needed
    
    if isinstance(datasets, dict):
        for i, (name, df) in enumerate(datasets.items()):
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['value'],
                mode='lines',
                name=name,
                line=dict(color=colors[i % len(colors)])
            ))
    else:
        fig.add_trace(go.Scatter(
            x=datasets['date'],
            y=datasets['value'],
            mode='lines',
            name=title
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=y_axis_label,
        hovermode="x unified",
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.01),
        margin=dict(l=50, r=50, t=50, b=150)  # Increase bottom margin
    )
    
    if is_percentage:
        fig.update_layout(yaxis_tickformat='.1f')
        fig.update_traces(hovertemplate='%{y:.1f}%')
    
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=10, label="10y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    return fig
