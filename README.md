# Revenue Visualization Project

Managing and analyzing sales data is a crucial aspect of business intelligence. This project provides a framework for prototyping revenue visualization and analysis, focusing on the common analytics requests related to sales or revenue data.

## Work in Progress (WIP)

This project is currently a work in progress. The `app-public.py` file requires refactoring, and additional data quality tests need to be incorporated for input validation.

## Libraries - Functime

Functime is a Python library designed for super-fast forecasting on time series datasets. 

Given that sales and revenue data are inherently time-series oriented (e.g., sales/month or year), Functime includes a sub-library that leverages OpenAI for time-series analysis.

With this repository, users can utilize Functime to call OpenAI and request analysis.

## How to Use

This repository contains code for a Streamlit app that expects a sales parquet file. To use this app, ensure your sales file adheres to the following three columns:

1. **Entity**
    - Description: A categorical column representing different entities or categories related to time series data.
    - Example: Brands of products, business units, etc.

2. **Date**
    - Description: A datetime column specifying the dates corresponding to the recorded values.
    - Example: YYYY-MM-DD HH:MM:SS

3. **Value**
    - Description: A numerical column representing the values associated with the entities and dates.
    - Example: Product sales in GBP (Great British Pounds), revenue, quantity sold, etc.

Ensure there are no duplicate rows or duplicate dates for an entity (checks for this are in place). 

While it is possible to extend the app to a more complicated schema, the initial design is deliberately straightforward for generic use.

To run the app locally, clone the repository and run `make setup`. Place your OpenAI API key in a local `.env` file. Then, proceed with development as usual with Streamlit.

It is quite easy to deploy this via streamlit (public) cloud, and there are more complicated deployment methods.

## How to Deploy
Streamlit is extremely easy to deploy to [Streamlit Community Cloud](https://streamlit.io/cloud), although I wouldn't recommend deploying a publicly available website with your own data/secrets.
Streamlit is reasonably easy to deploy as a website, either on Streamlit's cloud service or through methods [here](https://discuss.streamlit.io/t/streamlit-deployment-guide-wiki/5099).

Changes I would recommend for a *real* use case:
- Streamlit is great for prototyping, but another web-app framework would arguably be much better.
- Uploading flat files is good for showcasing. But it would be reasonably easy to refactor, more secure, and more user friendly to connect to data in a SQL database that the user could select from a drop down.

## Limitations

- Using LLMs, especially with an API, carries a risk. **Exercise caution against prompt injection and avoid exposing any secrets.**
- The source code is public, but evaluate whether you trust it to handle your data. If the data is private or not yours, avoid uploading it to a public website and reconsider before sending it to OpenAI.
- Though using a CSV file is possible, the app currently requires a parquet file for simplicity.
- The project assumes a weekly/monthly periodicity of data over at least a couple of years.
- Data sent to the LLM should not exceed a certain number of rows, say 200 at once, due to budget and token constraints.
- The data should not have repeats for a given period.
- You will probably see some smallish hallucinations with the base models. You could fine tune OpenAI or host your own model as an alternative.
