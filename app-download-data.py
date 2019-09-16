# base
import datetime
import os

# external libraries
import nltk
import json
import pandas as pd
import re
from textblob import TextBlob, Word
import twitter

# my libraries
from src.twitter_data import *
from src.twitter_plots import *

# TWITTER DATA
# leaders: ["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"]
df = tweets_refresh(users=["JustinTrudeau", "AndrewScheer", "ElizabethMay", "theJagmeetSingh", "MaximeBernier"], num_tweets=200, num_loops=4)
# clean twitter data
df = tweets_clean_df(df)
df['break_tweet'] = df['full_text'].apply(tweets_break)
# add sentiment and polarity
raw_sentiment = get_sentiment(df['full_text'])
clean_sentiment = get_sentiment(df['clean_tweet'])
df['polarity'] = clean_sentiment['polarity']
df['subjectivity'] = clean_sentiment['subjectivity']
# sort by handle so colours are consistent
df = df.sort_values(by=['handle'])

# save df to local disc
now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d")
df_path = "data/" + current_date + "_twitter-data.csv"
df.to_csv(df_path)

