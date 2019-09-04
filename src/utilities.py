def plotly_scatter3D(data, y_label, label_text=None):
    """Plots 3D scatter plot in Plotly.
    
    Args:
        data: pd.DataFrame or np.array
            Must be in shape [n, 3]
        
        y_label: np.array
            Label for each row of data, used to color points
        
        label_text: list
            Adds text label when hovering over data point
            
     Returns:
         None
     """
    
    
    import plotly
    import plotly.graph_objs as go
    
    # Configure Plotly to be rendered inline in the notebook.
    plotly.offline.init_notebook_mode()

    # Configure the trace
    trace = [go.Scatter3d(
        x = data[:, 0],  
        y = data[:, 1],  
        z = data[:, 2],  
        mode='markers',
        marker={
            'size': 3,
            'opacity': 0.8,
            'color' : y_label
        },
        hovertext=label_text
    )]

    layout = go.Layout(
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    plot_figure = go.Figure(data=trace, layout=layout)

    # Plot it
    plotly.offline.iplot(plot_figure)