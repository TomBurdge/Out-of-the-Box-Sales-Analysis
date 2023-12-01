# Revenue Visualization Project

Managing and analyzing sales data is a crucial aspect of business intelligence. This project provides a framework for prototyping revenue visualization and analysis, focusing on the common analytics requests related to sales or revenue data.

## Work in Progress (WIP)

This project is currently a work in progress. The `app-public` file requires refactoring, and additional data quality tests need to be incorporated for input validation.

### Why Out of the Box?

Professionals often excel by having stock responses for common requests, similar to chess openings or standard data models. This project aims to provide an out-of-the-box solution to streamline revenue analysis, enabling users to build upon a pre-established template.

## Libraries - Functime

Functime is a Python library designed for super-fast forecasting on time series datasets. Given that sales and revenue data are inherently time-series oriented (e.g., sales/month or year), Functime includes a sub-library that leverages OpenAI for time-series analysis.

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

Ensure there are no duplicate rows or duplicate dates for an entity (checks for this are in place). While it's possible to extend the app to a more complicated schema, the initial design is deliberately straightforward for generic use.

The app is currently public at [site](site). If the site is unexpectedly down, please raise an issue on GitHub.

To run the app locally, clone the repository and run `make setup`. Place your OpenAI API key in a local `.env` file. Then, proceed with development as usual with Streamlit.

## Limitations

- Using LLMs, especially with an API, carries a risk. **Exercise caution against prompt injection and avoid exposing any secrets.**
- The source code is public, but evaluate whether you trust it to handle your data. If the data is private or not yours, avoid uploading it to a public website and reconsider before sending it to OpenAI.
- Though using a CSV file is possible, the app currently requires a parquet file for simplicity.
- The project assumes a weekly/monthly periodicity of data over at least a couple of years.
- Data sent to the LLM must not exceed a certain number of rows due to budget constraints.
- The data should not have repeats for a given period.
