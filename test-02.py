from src.twitter_data import *
df = tweets_refresh(users=["JustinTrudeau","TheReaLSamlam"], num_loops=3)

print(df.head())
print(df.info())