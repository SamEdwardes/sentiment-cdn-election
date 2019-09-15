from src.twitter_data import *

brk = "\n\n*************************\n"
x = tweets_refresh()
x = tweets_clean_df(x)

print(brk + "RAW DATA:")
print(x.head())

print(brk + "RAW TWEETS:")
print(x.head()['full_text'])

print(brk + "CLEAN TWEETS:")
print(x.head()['clean_tweet'])

print(brk + "CLEAN DATA FRAME:")
print(x.info())



