import os

import polars as pl

lf_trend = (
    pl.read_excel(
        os.path.join("..", "local", "dunnhumby - Breakfast at the Frat.xlsx"),
        sheet_name="dh Transaction Data",
        read_csv_options={"has_header": True, "skip_rows": 1},
    )
    .lazy()
    .drop_nulls()
    .with_columns(pl.col("WEEK_END_DATE").str.to_datetime(format="%d-%b-%y"))
    .select(["UPC", "WEEK_END_DATE", "SPEND"])
)

lf_brand = (
    pl.read_excel(
        os.path.join("..", "local", "dunnhumby - Breakfast at the Frat.xlsx"),
        sheet_name="dh Products Lookup",
        read_csv_options={"has_header": True, "skip_rows": 1},
    )
    .drop_nulls()
    .lazy()
)

lf = (
    lf_trend.join(lf_brand, on="UPC", how="inner")
    .group_by("WEEK_END_DATE", "MANUFACTURER")
    .agg(pl.col("SPEND").sum().alias("value"))
    .select(
        pl.col("MANUFACTURER").alias("manufacturer"),
        pl.col("WEEK_END_DATE").alias("date"),
        pl.col("value"),
    )
    .with_columns(pl.col("manufacturer").str.to_titlecase())
    .sort(by=["manufacturer", "date"])
    .sink_parquet(os.path.join("..", "local", "dunnhumby.parquet"))
)
