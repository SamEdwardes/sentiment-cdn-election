# set up
import pandas as pd
from src.twitter_data import *

df = pd.read_csv("data/twitter-data.csv")
df = df[df['handle'] == "AndrewScheer"]


# test functions
x = get_word_counts(df['clean_tweet'])

# print
br = "\n##############################"
print(br)
print(br)
print(br)
print(x.head(n=20))