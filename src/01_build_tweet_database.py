"""
This script is used to create the first database of tweets. It should only
need to be called once. The script returns a csv that will be updated as time 
goes on by another script.
"""
from datetime import date, datetime

import pandas as pd

import config
from helpers import print_break
from twitter_data import get_old_tweets, tweets_to_df

tweets = []

# call the twitter API
for user in config.twitter_handles:
    print_break(user)
    t = get_old_tweets(
        user_name=user,
        num_tweets_per_iter=200,
        max_iter=1_000, 
        include_retweets=True
    )
    tweets = t + tweets

# convert to dataframe and save to csv
df = tweets_to_df(tweets)
df.to_csv(config.df_path_raw, index=False)

print_break('COMPLETE')
print(f'Total number of tweets: {df.shape[0]}')
