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


# app stuff
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


# TWITTER DATA
# leaders: ["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"]
df = tweets_refresh(users=["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"], num_tweets=200, num_loops=2)
# clean twitter data
df = tweets_clean_df(df)
df['break_tweet'] = df['full_text'].apply(tweets_break)
# add sentiment and polarity
raw_sentiment = get_sentiment(df['full_text'])
clean_sentiment = get_sentiment(df['clean_tweet'])
df['polarity'] = clean_sentiment['polarity']
df['subjectivity'] = clean_sentiment['subjectivity']


# APP LAYOUT
app.layout = html.Div([
    html.H2('Canadian 2019 Election Twitter Sentiment Analysis'),
    dcc.Markdown(open("docs/intro.md").read()),
    html.Hr(),
    dcc.Graph(figure = plot_tweets_time(df)),
    dcc.Graph(figure = plot_tweets_sentiment(df)),
    dcc.Graph(figure = plot_polarity_dist(df)),
    html.Hr(),
    html.H3("Top 5 Most Negative Tweets for Andrew Scheer:"),
    generate_table(df[df['handle']=="AndrewScheer"].sort_values(by=['polarity']).head(5)[['handle', 'date', 'full_text','polarity','subjectivity']]),
    html.H3("Top 5 Most Negative Tweets for Justin Trudeau:"),
    generate_table(df[df['handle']=="JustinTrudeau"].sort_values(by=['polarity']).head(5)[['handle', 'date', 'full_text','polarity','subjectivity']])
])

if __name__ == '__main__':
    app.run_server(debug=True)