import plotly.express as px

template = "plotly_dark"


def expense_category_chart(names, values):
    fig = px.pie(values=values, names=names, template=template)
    return fig


def income_category_chart(names, values):
    fig = px.pie(values=values, names=names, template=template)
    return fig


def income_vs_expense_chart(names, values):
    fig = px.pie(values=values, names=names, template=template)
    return fig
