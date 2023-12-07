from datetime import datetime, timedelta

import polars as pl
import streamlit as st
from dotenv import load_dotenv
from plotting import plot_line_bar

load_dotenv()
# need to load OpenAI API key from secrets before imports
# this is an anti-pattern, will raise an issue on functime about this
from functime.llm import LLMActions  # noqa

st.set_page_config(layout="wide")
st.title("Sales Trend Analysis")

revenue_file = st.file_uploader("Upload your parquet file:")

if not revenue_file:
    st.stop()

current_date = datetime.now()
one_year_ago = current_date - timedelta(days=365)

# This looks weird - streamlit uploaded files are already bytes objects
# so, scan won't work
df = pl.read_parquet(revenue_file).lazy()

entity_col = df.columns[0]
date_col = df.columns[1]
value_col = df.columns[2]

min_date = df.select(date_col).min().collect()[0, 0]

entities = (
    df.group_by(entity_col)
    .agg(pl.col(value_col).sum())
    # entity with greatest share by default
    .sort(by=value_col, descending=True)
    .select(entity_col)
    .collect()
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
)

year_after_start = min_date + timedelta(days=365)
mat_df = (
    entity_df.sort(by=[entity_col, date_col])
    .with_columns(
        pl.col(value_col)
        .rolling_sum(
            window_size="1y", by=date_col, warn_if_unsorted=False, closed="left"
        )
        .over(entity_col)
        .alias("mat_value")
    )
    .filter(pl.col("date") > year_after_start)
    .select([entity_col, date_col, "mat_value"])
    .collect()
)

entity_df = entity_df.collect()

tab1, tab2 = st.tabs(["Sales Trend", "MAT Trend"])
with tab1:
    plot_line_bar(entity_df, [selected_entity, selected_second_entity])

with tab2:
    plot_line_bar(mat_df, [selected_entity, selected_second_entity], "MAT")

st.write("LLM analysis will appear here:")

dataset_context = "This dataset comprises of sales over a period."
llm = LLMActions(df.collect())
analysis = llm.analyze(
    context=dataset_context, basket=[selected_entity, selected_second_entity]
)

st.write(analysis)
