import pandas as pd

import config
from helpers import print_break
from twitter_analysis import (count_tweets_about, tweets_clean_text,
                              get_sentiment, tweets_break)
from twitter_counts import count_tweet_words


print_break("Refreshing data analysis")
df = pd.read_csv(config.df_path_raw).query('lang == "en"')

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
twitter_handles = df['screen_name'].unique().tolist()

print(" - calculating phrase count data...")
df_phrase_count = count_tweet_words(
    df=df.query('rt == False and lang == "en"'), 
    ngram_range=(2, 5),
    min_df=5
)
# write to disk
df_phrase_count.to_csv(config.df_path_phrase_count, index=False)

print(" - calculating word count data...")
df_word_count = count_tweet_words(
    df=df.query('rt == False and lang == "en"'), 
    ngram_range=(1, 1),
    min_df=10
)
# write to disk
df_word_count.to_csv(config.df_path_word_count, index=False)

