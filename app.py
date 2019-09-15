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
import plotly_express as px
import re
from textblob import TextBlob, Word
import twitter

# my libraries
from src.twitter_data import *
from src.twitter_plots import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# get twitter data
df = tweets_refresh(num_loops=3)

# clean twitter data
df = tweets_clean_df(df)

# add sentiment and polarity
raw_sentiment = get_sentiment(df['full_text'])
clean_sentiment = get_sentiment(df['clean_tweet'])
df['raw_polarity'] = raw_sentiment['polarity']
df['raw_subjectivity'] = raw_sentiment['subjectivity']
df['clean_polarity'] = clean_sentiment['polarity']
df['clean_subjectivity'] = clean_sentiment['subjectivity']


# generate a table
# def generate_table(dataframe, max_rows=10):
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] +
#         # Body
#         [html.Tr([
#             html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#         ]) for i in range(min(len(dataframe), max_rows))]
#     )

app.layout = html.Div([
    html.H2('Canadian 2019 Election Twitter Sentiment Analysis'),
    html.P('WIP - to be updated'),
    html.Hr(),
    html.P("Tweets over time"),
    dcc.Graph(figure = plot_tweets_time(df)),
    html.Hr(),
    html.P("The underlying data is displayed below (first 10 rows):"),
    generate_table(df[['handle', 'date', 'full_text','clean_tweet','raw_polarity','clean_polarity']].head(10))
])


if __name__ == '__main__':
    app.run_server(debug=True)