import pandas as pd

from helpers import get_project_global_variables, print_break
from twitter_analysis import (count_tweets_about, get_phrase_counts_df,
                              get_sentiment, get_word_counts_df, tweets_break,
                              tweets_clean_text)

start_date = get_project_global_variables()["start_date"]
users = get_project_global_variables()["twitter_handles"]
df_path_raw = get_project_global_variables()["df_path_raw"]
df_path_clean = get_project_global_variables()["df_path_clean"]
df_path_word_count = get_project_global_variables()["df_path_word_count"]
df_path_phrase_count = get_project_global_variables()["df_path_phrase_count"]
df = pd.read_csv(df_path_raw)

print_break("Refreshing model")

# clean tweet text
print(" - cleaning tweets...")
df['clean_tweet'] = df['full_text'].apply(tweets_clean_text)
df['break_tweet'] = df['full_text'].apply(tweets_break)

# add sentiment and polarity
print(" - calculating sentiment and polarity...")
raw_sentiment = get_sentiment(df['full_text'])
clean_sentiment = get_sentiment(df['clean_tweet'])
df['polarity'] = clean_sentiment['polarity']
df['subjectivity'] = clean_sentiment['subjectivity']

# creating count data
print(" - calculating count data...")
df = count_tweets_about(df, "full_text")
df_phrase_count = get_phrase_counts_df(df=df, selected_col='clean_tweet',
                                       users=users)
df_word_count = get_word_counts_df(df=df, selected_col='clean_tweet',
                                   users=users)

# export clean data
print(" - writing to disk...")
df.to_csv(df_path_clean, index=False)
df_word_count.to_csv(df_path_word_count, index=False)
df_phrase_count.to_csv(df_path_phrase_count, index=False)
