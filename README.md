# Revenue Visualization

Managing and analyzing sales data is a crucial aspect of business intelligence. This project provides a framework for prototyping revenue visualization and analysis, focusing on the common analytics requests related to sales or revenue data.

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

Ensure there are no duplicate rows or duplicate dates for an entity. 

While it is possible to extend the app to a more complicated schema, the initial design is deliberately straightforward for generic use.

To run the app locally, clone the repository and run `make setup`. Place your OpenAI API key in a local `.env` file. Then, proceed with development as usual with Streamlit.

## Don't have example data at hand?
Dunnhumby's [Breakfast at the Frat](https://www.dunnhumby.com/source-files/) dataset will work well for this app, with a bit of modification.
This data can be downloaded freely from their site, but their [terms of use](https://www.dunnhumby.com/terms-and-conditions/) prohibit sharing it beyond their site.
Once you have downloaded the data, you can run the prep_dunhummby.py file to make a suitable parquet. 
The download excel should be in your "local" folder, which is made in the MakeFile and won't be tracked by git.

## How to Deploy
Streamlit is extremely easy to deploy to [Streamlit Community Cloud](https://streamlit.io/cloud), although I wouldn't recommend deploying a publicly available website with your own data/secrets.
Streamlit is reasonably easy to deploy as a website, either on Streamlit's cloud service or through methods [here](https://discuss.streamlit.io/t/streamlit-deployment-guide-wiki/5099).

Changes I would recommend for a *real* use case:
- Streamlit is great for prototyping, but other web-app frameworks have much more flexibility.
- Uploading flat files is good for showcasing. But it would be reasonably easy to refactor, more secure, and more user friendly to connect to data in a SQL database that the user could select from a drop down.

## Limitations

- Using LLMs, especially with an API, carries a risk. **Exercise caution against prompt injection and avoid exposing any secrets.**
- The source code is public, but evaluate whether you trust it to handle your data. Use at your own risk. If the data is private or not yours, avoid uploading it to a public website and reconsider before sending it to OpenAI.
- Though using a CSV file is possible, the app currently requires a parquet file for simplicity. With CSVs, the following become an issue: encoding, quotechars, seps.
- The project assumes a weekly/monthly periodicity of data over at least a couple of years. If you had lower/higher periodicity, you would want to resample.
- A full time series for an entity should be relatively small. This is for memory limits, and LLM API budget and token constraints.
- The data should not have repeats for a given period.
- You will probably see some smallish hallucinations with the base models. You could fine tune OpenAI or host your own model as an alternative (this is not currently possible with `functime`).
