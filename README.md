# Revenue Visualisation
An enormous amount of business data involves sales.

There is plenty else, for example: logistics, HR, compliance.

But an extremely common analytics request involves summarising and analysing sales aka revenue data.

This project is an out of the box framework for prototyping revenue visualisation and analysis.

## Why out of the box?

People who are good at something are usually good enough that they have a set of stock responses for certain requests.

Like a chess opening, or a standard data model, one of the easiest ways to be better at something is to have a stock template that you build upon.

## The libraries - Functime

Functime is a python library which performs super fast forecasting on time series datasets.

Effectively all sales/revenue data is time-series data; for example, sales/month or year.

Functime contains a sub-library which calls OpenAI with a time-series dataset and asks for analysis.

With this repo, you can use functime to call OpenAI and ask for analysis.

# How to use

This repo involves code for a streamlit app which expects a sales parquet file.

To qualify as a generic sales file, the file should have three columns:
1. Entity - a column which contains categories of time series. For example, different brands of product.
2. Date - a datetime column which contains the dates for the values.
3. Value - the value (e.g. product sales in GBP).

There should be no duplicate rows, or duplicate dates for an entity (there are checks for this). You could change this, but it would result in some surprising behaviour.

It is possible to extend the app to a more complicated schema, but to be initially generic the schema is very straightforward.

This is currently a public at {site}.
If the site is down unexpectedly, please raise an issue on GitHub.

If you want to run this locally, clone the repo and run `make setup`.
You need to put your OpenAI API key in a local `.env` file.
You can then develop as you would usually with streamlit.

# Limitations
- Using LLMs, especially with an API, always carries a risk. **Always be careful of prompt injection and do not expose any of your secrets.**
- The source code here is public, but do you trust the code here to handle your data? Is the data you are uploading private or public? If it is private, or not yours, do not upload it to a public website and consider before sending it to OpenAI.
- Having the input file be a csv file is possible (easy) but I decided against because csvs can bring complications (In in particular: no headers, or non-utf8 encoding).
- This can, in principle be used for a non-additive metric over a period.
- This assumes weekly/monthly periodicity of data over at least a couple of years.
- Data sent to the LLM must not be over X rows (budget constraints).
- Data should not have repeats for a period.