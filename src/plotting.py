from typing import Optional

import plotly.express as px
import streamlit as st
from polars import DataFrame


def plot_line_bar(df: DataFrame, entities: list, extra_label: Optional[str] = None):
    """
    The function `plot_line_bar` takes a DataFrame, a list of entities, and an optional
    extra label as input, and plots a line chart and a bar chart of the sales data for
    the specified entities.

    :param df: The `df` parameter is a DataFrame that contains the data for the plot.
    It should have three columns: `entity_col`, `date_col`, and `value_col`
    :type df: DataFrame
    :param entities: The `entities` parameter is a list that contains the names of the
    two entities you are comparing in the line and bar charts.
    For example,if you are comparing the sales of two products, you can pass a list
    like `["Product A", "Product B"]`
    :type entities: list
    :param extra_label: The `extra_label` parameter is an optional string that can be
    provided to add an extra label to the chart titles.
    If a value is provided for `extra_label`, it will be appended to the chart
    titles. If no value is provided, the chart titles will not have an extra label
    :type extra_label: Optional[str]
    :return: the DataFrame `df`.
    """
    col1, col2 = st.columns(2)
    entity_col, date_col, value_col = df.columns
    entity_1, entity_2 = entities

    if extra_label:
        extra_label = extra_label + " "

    fig = px.line(
        x=df[date_col],
        y=df[value_col],
        color=df[entity_col],
        title=f"Line Chart of {entity_1} and {entity_2} Sales.",
    )
    fig.update_traces(hovertemplate="Date: %{x}<br>Sales: %{y}")
    fig.update_layout(xaxis_title="Sales", yaxis_title="Date")
    col1.plotly_chart(fig)

    fig2 = px.bar(
        x=df[date_col],
        y=df[value_col],
        color=df[entity_col],
        title=f"Bar Chart of {entity_1} and {entity_2} sales.",
    )
    fig2.update_traces(hovertemplate="Date: %{x}<br>Sales: %{y}")
    fig2.update_layout(xaxis_title="Sales", yaxis_title="Date")
    col2.plotly_chart(fig2)
    return df
