# base
import datetime
import os

# external libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import nltk
import json
import pandas as pd
import plotly.graph_objs as go
import re
from textblob import TextBlob, Word
import twitter

# my libraries
from src.twitter_data import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# get twitter data
# df = tweets_refresh()
# df = tweets_clean_df(df)
# df = pd.read_csv("https://github.com/SamEdwardes/sentiment-cdn-election/raw/master/data/clean/2019-09-14_twitter-data-clean.csv")
df = tweets_get("JustinTrudeau", 200, 1)

# generate a table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div([
    html.H2('Canadian 2019 Election Twitter Sentiment Analysis'),
    html.P('WIP - to be updated'),
    html.Hr(),
    html.P("The underlying data is displayed below (first 10 rows):"),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)