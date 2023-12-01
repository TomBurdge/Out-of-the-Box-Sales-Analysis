from datetime import datetime, timedelta

import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import polars as pl  # noqa
from functime.llm import LLMActions  # noqa

st.set_page_config(layout="wide")
st.title("Sales Trend Analysis")

revenue_file = st.file_uploader("Upload your parquet file:")

if not revenue_file:
    st.stop()

current_date = datetime.now()
one_year_ago = current_date - timedelta(days=365)

df = pl.read_parquet(revenue_file)

# perform the data tests here.

dataset_context = """
This dataset comprises of sales over a period.
"""

entity_col = df.columns[0]
date_col = df.columns[1]
value_col = df.columns[2]

min_date = df[date_col].min()

entities = (
    df.group_by(entity_col)
    .agg(pl.col(value_col).sum())
    .sort(by=value_col, descending=True)
    .select(entity_col)
    .to_series()
    .to_list()
)

selected_entity = st.selectbox("Which category would you like to analyse?", entities)
st.write("You selected:", selected_entity)

selected_second_entity = st.selectbox(
    "Which second category would you like to analyse?", entities
)
st.write("You selected:", selected_entity)

entity_df = df.filter(
    pl.col(entity_col).is_in([selected_entity, selected_second_entity])
).with_columns(
    pl.col(value_col)
    .rolling_sum(window_size="1y", by=date_col, warn_if_unsorted=False)
    .over(entity_col)
    .alias("mat_value")
)


def get_llm_description(df: pl.DataFrame, selected_entities: list[str]):
    """
    The function `get_llm_description` takes a DataFrame and a brand name as input,
    creates an instance of the LLMActions class,
    and returns the result of analyzing the dataset context and selected brand.

    :param df: The parameter `df` is a pandas DataFrame that contains the data you want
    to analyze
    :type df: pl.DataFrame
    :param brand: The brand parameter is a string that represents the brand you want
    to analyze
    :type brand: str
    :return: the result of the `analyze` method of the `LLMActions` class.
    """
    llm = LLMActions(df)
    return llm.analyze(context=dataset_context, basket=selected_entities)


tab1, tab2 = st.tabs(["Sales Trend", "MAT Trend"])
with tab1:
    col1, col2 = st.columns(2)

    fig = px.line(
        x=entity_df[date_col],
        y=entity_df[value_col],
        color=entity_df[entity_col],
        title=f"Line Chart of {selected_entity} and {selected_second_entity} Sales.",
    )
    fig.update_traces(hovertemplate="Date: %{x}<br>GBP: %{y}")
    fig.update_layout(xaxis_title="Sales", yaxis_title="Date")
    col1.plotly_chart(fig)

    fig2 = px.bar(
        x=entity_df[date_col],
        y=entity_df[value_col],
        color=entity_df[entity_col],
        title=f"Bar Chart of {selected_entity} and {selected_second_entity} sales.",
    )
    fig2.update_traces(hovertemplate="Date: %{x}<br>Sales: %{y}")
    fig2.update_layout(xaxis_title="Sales", yaxis_title="Date")
    col2.plotly_chart(fig2)

with tab2:
    year_after_start = min_date + timedelta(days=365)

    mat_df = entity_df.filter(pl.col("date") > year_after_start)

    col1, col2 = st.columns(2)

    fig = px.line(
        x=mat_df[date_col],
        y=mat_df["mat_value"],
        color=mat_df[entity_col],
        title="Line Chart of MAT Sales.",
    )
    fig.update_traces(hovertemplate="Date: %{x}<br>Sales: %{y}")
    fig.update_layout(yaxis_title="Sales", xaxis_title="Date")
    col1.plotly_chart(fig)

    fig2 = px.bar(
        x=mat_df[date_col],
        y=mat_df["mat_value"],
        color=mat_df[entity_col],
        title="Bar Chart of MAT sales.",
    )
    fig2.update_traces(hovertemplate="Date: %{x}<br>Sales: %{y}")
    fig2.update_layout(yaxis_title="Sales", xaxis_title="Date")
    col2.plotly_chart(fig2)


st.write("LLM analysis will appear here:")

analysis = get_llm_description(df, [selected_entity, selected_second_entity])
st.write(analysis)
