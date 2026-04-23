import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class ChartGenerator:
    @staticmethod
    def plot_line(df, x, y, title):
        fig = px.line(df, x=x, y=y, title=title, template="plotly_dark")
        return fig

    @staticmethod
    def plot_bar(df, x, y, title):
        fig = px.bar(df, x=x, y=y, title=title, template="plotly_dark")
        return fig

    @staticmethod
    def plot_pie(df, names, values, title):
        fig = px.pie(df, names=names, values=values, title=title, template="plotly_dark")
        return fig

    @staticmethod
    def plot_heatmap(df, title):
        corr = df.select_dtypes(include=['number']).corr()
        fig = px.imshow(corr, text_auto=True, title=title, template="plotly_dark")
        return fig

    @staticmethod
    def plot_histogram(df, x, title):
        fig = px.histogram(df, x=x, title=title, template="plotly_dark")
        return fig

    @staticmethod
    def plot_kpi_metric(label, value, delta=None):
        fig = go.Figure(go.Indicator(
            mode = "number+delta" if delta else "number",
            value = value,
            title = {"text": label},
            delta = {'reference': delta} if delta else None,
            domain = {'x': [0, 1], 'y': [0, 1]}
        ))
        fig.update_layout(template="plotly_dark", height=250)
        return fig
