# set up
import pandas as pd
from src.twitter_data import *


df = pd.read_csv("data/twitter-data.csv")
df['clean_tweet'] = df['full_text'].apply(tweets_clean_text)
df = df[df['handle'] == "AndrewScheer"]
df = df[df['lang'] == 'en']  # keep only english langauge tweets


# test functions
x = get_phrase_counts(df['clean_tweet'])

# print
br = "\n##############################"
print(br)
print(br)
print(br)
print(x.head(n=20))