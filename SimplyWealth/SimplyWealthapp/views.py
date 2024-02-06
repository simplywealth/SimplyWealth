from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
from plotly.offline import plot


@login_required
def home(request):
    return render(request, 'home.html')


def stock_graph(request):
    # Example data for stock prices
    stock_prices = [100, 110, 120, 130, 140, 150]  # Pretend these are your API results
    dates = ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01']  # Example dates

    # Create a Plotly graph
    fig = go.Figure(data=[go.Line(x=dates, y=stock_prices)])
    
    # Plotting directly to a div to embed in the template
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    # Pass the graph to the template
    return render(request, 'your_template.html', context={'plot_div': plot_div})