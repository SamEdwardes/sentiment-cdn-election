# base
import datetime
import socket
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


# TWITTER DATA
if socket.gethostname() == "Sams-MacBook-Pro.local":
    update_tweets = True
else:
    update_tweets = False
users = ["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"] # leaders: ["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"]
start_date = datetime.date(2019,8,5) # election officially starts on sep 11
df_path = "data/twitter-data.csv"
print("Getting twitter data...")
if update_tweets == False:
    print("\tReading old twitter data from disk.")
    df = pd.read_csv(df_path)
else:
    print("\tGetting new twitter data from Twitter API.")
    df = pd.DataFrame()
    for user in users:
        df_temp = tweets_get(user_name = user, num = 200, start_date = start_date)
        df_temp['handle'] = user
        df = pd.concat([df, df_temp], sort=False)
    # clean twitter data    
    df = df[df['date'] >= start_date]
    df = df[df['lang'] == 'en'] # keep only english langauge tweets
    df = tweets_clean_df(df)
    df['break_tweet'] = df['full_text'].apply(tweets_break)
    # add sentiment and polarity
    raw_sentiment = get_sentiment(df['full_text'])
    clean_sentiment = get_sentiment(df['clean_tweet'])
    df['polarity'] = clean_sentiment['polarity']
    df['subjectivity'] = clean_sentiment['subjectivity']
    # download
    df.to_csv(df_path, index = False)


# APP STUFF
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
  
  
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