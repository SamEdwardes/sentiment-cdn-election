import pandas as pd

import config
from helpers import print_break
from twitter_analysis import (count_tweets_about, get_phrase_counts_df,
                              get_sentiment, get_word_counts_df, tweets_break,
                              tweets_clean_text)


print_break("Refreshing data analysis")
df = pd.read_csv(config.df_path_raw)

# ============================================================================
# clean tweet text
# ============================================================================
print(" - cleaning tweets...")
df['rt'] = df['full_text'].apply(lambda x: True if x[0:2] == 'RT' else False)
df['clean_tweet'] = df['full_text'].apply(tweets_clean_text)
df['break_tweet'] = df['full_text'].apply(tweets_break)

# ============================================================================
# add sentiment and polarity
# ============================================================================
print(" - calculating sentiment and polarity...")
raw_sentiment = get_sentiment(df['full_text'])
clean_sentiment = get_sentiment(df['clean_tweet'])
df['polarity'] = clean_sentiment['polarity']
df['subjectivity'] = clean_sentiment['subjectivity']
# count tweets about eachother
df = count_tweets_about(df, "full_text")
# write to disk
df.to_csv(config.df_path_clean, index=False)

# ============================================================================
# creating count data
# ============================================================================
print(" - calculating count data...")
twitter_handles = df['user_name'].unique().tolist()

df_phrase_count = get_phrase_counts_df(
    df=df.query('rt == False'), 
    selected_col='clean_tweet',
    users=twitter_handles
)
# write to disk
df_phrase_count.to_csv(config.df_path_phrase_count, index=False)

df_word_count = get_word_counts_df(
    df=df.query('rt == False'), 
    selected_col='clean_tweet',
    users=twitter_handles
)
# write to disk
df_word_count.to_csv(config.df_path_word_count, index=False)

