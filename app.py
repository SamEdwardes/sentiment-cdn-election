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


###########################################
# GETTING DATA
###########################################

# GET TWITTER DATA
if socket.gethostname() == "Sams-MacBook-Pro.local":
    update_tweets = True  # !!!!SWITCH HERE FOR TESTING!!!! set to True to load new twitter data
else:
    update_tweets = False
# leaders: ["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"]
users = ["JustinTrudeau", "AndrewScheer",
         "ElizabethMay", "theJagmeetSingh", "MaximeBernier"]
start_date = datetime.date(2019, 8, 5)  # election officially starts on sep 11
df_path = "data/twitter-data.csv"
print("Getting twitter data...")
if update_tweets == False:
    print("\tReading old twitter data from disk.")
    df = pd.read_csv(df_path)
else:
    print("\tGetting new twitter data from Twitter API.")
    df = pd.DataFrame()
    for user in users:
        df_temp = tweets_get(user_name=user, num=200, start_date=start_date)
        df_temp['handle'] = user
        df = pd.concat([df, df_temp], sort=False)
        df.to_csv(df_path, index=False)


###########################################
# ANALYSING TWITTER DATA
###########################################

# clean twitter data
print("Analysing twitter data...")
df['date_time'] = pd.to_datetime(df['created_at'])
df['date'] = pd.to_datetime(df['date_time'].dt.date)
df = df[df['date'] >= start_date]
df = df[df['lang'] == 'en']  # keep only english langauge tweets
df['clean_tweet'] = df['full_text'].apply(tweets_clean_text)
df['break_tweet'] = df['full_text'].apply(tweets_break)

# add sentiment and polarity
raw_sentiment = get_sentiment(df['full_text'])
clean_sentiment = get_sentiment(df['clean_tweet'])
df['polarity'] = clean_sentiment['polarity']
df['subjectivity'] = clean_sentiment['subjectivity']

# word counts
df_word_count_totals = get_word_counts(df['clean_tweet'])
df_word_count_totals.columns = ['word', 'total_count']
df_word_count = pd.DataFrame()
for i in users:
    temp = get_word_counts(df[df['handle'] == i]['clean_tweet'])
    temp['handle'] = i
    df_word_count = pd.concat([temp, df_word_count])
df_word_count = pd.merge(df_word_count, df_word_count_totals, how='left',
                         on='word')
df_word_count = df_word_count.sort_values(
    by=['total_count'], ascending=False).reset_index(drop=True).head(200)

# phrase counts
df_phrase_count_total = get_phrase_counts(df['clean_tweet'])
df_phrase_count_total.columns = ['phrase', 'total_count']
df_phrase_count = pd.DataFrame()
for i in users:
    temp = get_phrase_counts(df[df['handle'] == i]['clean_tweet'])
    temp['handle'] = i
    df_phrase_count = pd.concat([temp, df_phrase_count])
df_phrase_count = pd.merge(df_phrase_count, df_phrase_count_total, how='left',
                           on='phrase')
df_phrase_count = df_phrase_count.sort_values(
    by=['total_count'], ascending=False).reset_index(drop=True).head(100)


###########################################
# APP STUFF
###########################################

# COLOUR AND STYLE
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {"dark_green": "#3a4f41",
          "dark_red": "#b9314f",
          "dark_grey": "#909590",
          "white": "#ffffff",
          "light_grey": "#d2d7df",
          "other_grey": "#d3d3d3",
          "alice_blue": "#F0F8FF"
          }

colour_dict = {'JustinTrudeau': '#D91A20',
               'AndrewScheer': '#1A4E89',
               'ElizabethMay': '#42A03A',
               "theJagmeetSingh": '#F29F24',
               'MaximeBernier': '#A9A9A9'}

# APP LAYOUT
app.layout = html.Div(style={'backgroundColor': colors['light_grey']}, children=[
    # HEADER
    html.Div(className="row", style={'backgroundColor': colors['dark_red'], "padding": 10}, children=[
        html.H2('Canadian 2019 Election Twitter Sentiment Analysis',
                style={'color': colors['white']})
    ]),
    # MAIN BODY
    html.Div(className="row", children=[
        # SIDEBAR
        html.Div(className="one-third column", style={'padding': 20}, children=[
            dcc.Markdown(open("docs/intro.md").read())]),
        # PLOTS
        html.Div(className="two-thirds column", style={"backgroundColor": colors['white'], "padding": 20}, children=[
            html.H4("How much are our leaders tweeting?"),
            # ROW 1 - TWEET COUNTS
            html.Div(className="row", children=[
                # ROW 1, COLUMN 1
                html.Div(className="one-half column", children=[
                    dcc.Graph(figure=plot_tweets_total(df))
                ]),
                # ROW 1, COLUMN 2
                html.Div(className="one-half column", children=[
                    dcc.Graph(figure=plot_tweets_time(df))
                ])
            ]),
            # ROW 2 - Sentiment Plot
            html.Div(className="row", children=[
                html.Hr(),
                html.H4("What is the sentiment of their tweets?"),
                dcc.Markdown(open("docs/sentiment-explained.md").read()),
                dcc.Graph(figure=plot_tweets_sentiment(df))
            ]),
            # ROW 3 - Sentiment Distributions
            html.Div(className="row", children=[
                # ROW 3, COLUMN 1
                html.Div(className="one-half column", children=[
                    dcc.Graph(figure=plot_polarity_dist(df))
                ]),
                # ROW 3, COLUMN 2
                html.Div(className="one-half column", children=[
                    dcc.Graph(figure=plot_subjectivity_dist(df))
                ])
            ]),
            # ROW 4 - WORD COUNTS
            html.Div(className="row", children=[
                html.Hr(),
                html.H4("What are our leaders tweeting about?"),
                html.Br(),
                dcc.Graph(figure=plot_word_count_bar_stack(df_word_count)),
                html.Br(),
                dcc.Graph(figure=plot_phrase_count_bar_stack(df_phrase_count))
            ])
        ])
    ])
])


if __name__ == '__main__':
    app.run_server(debug=False)
