import plotly
import plotly.graph_objs as go


def expense_category_chart(x, y):

    # Create basic bar chart
    fig = go.Figure([go.Bar(x=x, y=y)])
    return fig
