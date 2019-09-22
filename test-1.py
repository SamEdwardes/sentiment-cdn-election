# set up
import pandas as pd
from src.twitter_data import *

df = pd.read_csv("data/twitter-data.csv")
tweets = list(df['full_text'])
x1 = tweets[7]

# test functions
x2 = tweets_clean_text(x1)

# print
br = "\n##############################\n"
print(br)
print(br)
print(br)
print(x1)
print(br)
print(x2)