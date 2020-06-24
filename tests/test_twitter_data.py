import pandas as pd
import twitter

from src.twitter_data import get_old_tweets, tweets_to_df


def test_get_tweets():
    x = get_old_tweets('TheRealSamlAm', 20, 2)
    assert type(x) is list
    assert type(x[0]) is twitter.Status


def test_tweets_to_df():
    x = get_old_tweets('TheRealSamlAm', 20, 2)
    df = tweets_to_df(x)
    assert type(df) is pd.DataFrame
