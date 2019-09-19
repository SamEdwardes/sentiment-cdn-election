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

# Uncomment the code below to update the data
df = pd.read_csv("data/2019-09-18_twitter-data.csv")

# TWITTER DATA
# now = datetime.datetime.now()
# current_date = now.strftime("%Y-%m-%d")
# df_path = "data/" + current_date + "_twitter-data.csv"
# if os.path.exists(df_path):
#     df = pd.read_csv(df_path)
#     print("Old twitter data loaded: " + df_path)
# else:
#     # leaders: ["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"]
#     df = tweets_refresh(users=["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"], num_tweets=200, start_date=datetime.date(2019,9,11))
#     # clean twitter data
#     df = tweets_clean_df(df)
#     df = df[df['lang'] == 'en'] # keep only english langauge tweets
#     df['break_tweet'] = df['full_text'].apply(tweets_break)
#     # add sentiment and polarity
#     raw_sentiment = get_sentiment(df['full_text'])
#     clean_sentiment = get_sentiment(df['clean_tweet'])
#     df['polarity'] = clean_sentiment['polarity']
#     df['subjectivity'] = clean_sentiment['subjectivity']
#     # download
#     df.to_csv(df_path, index = False)
#     print("New twitter data downloaded: " + df_path)
  

# APP LAYOUT
app.layout = html.Div([
    html.H2('Canadian 2019 Election Twitter Sentiment Analysis'),
    dcc.Markdown(open("docs/intro.md").read()),
    html.H3("Twitter Analysis"),
    # PLOTS
    # tweet counts
    html.H4("How much are our leaders tweeting?"),
    dcc.Graph(figure = plot_tweets_total(df)),
    dcc.Graph(figure = plot_tweets_time(df)),
    # sentiment
    html.H4("What is the sentiment of their tweets?"),
    dcc.Markdown(open("docs/sentiment-explained.md").read()),
    dcc.Graph(figure = plot_polarity_dist(df)),
    dcc.Graph(figure = plot_subjectivity_dist(df)),
    dcc.Graph(figure = plot_tweets_sentiment(df)),    
    html.Hr()
])

if __name__ == '__main__':
    app.run_server(debug=True)