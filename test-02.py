from src.twitter_data import *
df = tweets_refresh(users=["JustinTrudeau","AndrewScheer"], num_loops=1)

print(df.head())
print(df.info())
print(list(df['handle'].unique()))