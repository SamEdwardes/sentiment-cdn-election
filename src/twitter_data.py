import datetime
import json
import os

import pandas as pd
import twitter


def create_twitter_api():
    """Check environment and return appropriate twitter API"""

    # API CREDENTIALS
    path = "twitter-credentials.json"
    # if running from local machine
    if os.path.exists(path):  
        with open(path, "r") as file:
            creds = json.load(file)
        CONSUMER_KEY = creds['CONSUMER_KEY']
        CONSUMER_SECRET = creds['CONSUMER_SECRET']
        ACCESS_KEY = creds['ACCESS_TOKEN']
        ACCESS_SECRET = creds['ACCESS_SECRET']
    # if running from Heroku
    else:  
        CONSUMER_KEY = os.environ['CONSUMER_KEY']
        CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
        ACCESS_KEY = os.environ['ACCESS_TOKEN']
        ACCESS_SECRET = os.environ['ACCESS_SECRET']
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_KEY,
                      access_token_secret=ACCESS_SECRET,
                      tweet_mode='extended',
                      sleep_on_rate_limit=True)

    return api


def fix_dates(df):
    """fixes dates for twitter dataframe"""
    df['date_time'] = pd.to_datetime(df['created_at'])
    df['date'] = pd.to_datetime(df['date_time'].dt.date)

    def find_monday(d):
        """Receives a date and returns the date of the preceding Monday."""
        while d.weekday() != 0:
            d += datetime.timedelta(-1)
        return d
    df['date_week'] = df['date'].apply(find_monday)
    return df


def load_tweets(api, user_name, num, n_max_id=0):
    """
    Get raw data from twitter. See api.GetUserTimeline 
    https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html
    
    Paramaters
    ----------
    api : twitter.Api
        Twitter api class
    user_name : str
        A twitter handle. Do not include the "@"
    num : int
        The number of tweets to get (max 200)
    n_max_id : int
        Returns only statuses with an ID less than (that is, older than) or 
        qual to the specified ID. By default, 0.

    Returns
    -------
    twitter_data
    """
    raw = api.GetUserTimeline(
        screen_name=user_name,
        count=num,
        exclude_replies=True,
        include_rts=False,
        trim_user=True,
        max_id=n_max_id
    )
    return raw


def tweets_get(user_name, num=200, start_date=datetime.date(2019, 9, 11)):
    '''
    Gets tweets and returns a DataFrame.

    Parameters
    ----------
    user_name : str 
        The user you would like to get twitter data from (e.g. "JustinTrudeau")
    num : int
        The number of tweets you would like to return (max is 200)
    loops: int
        Because the max number of tweets is only 200, loops will indicate how many sets of "num" tweets you would like to return. 
        For example num=200 and loops=2 would get 400 tweets

    Returns
    -------
    Dataframe with twitter data
    '''

    api = create_twitter_api()
    
    # get the first batch of twitter data
    print(f"Getting tweets for: {user_name}...")
    raw = load_tweets(api=api, user_name=user_name, num=num)
    df = pd.DataFrame.from_dict([i.AsDict() for i in raw])
    df = fix_dates(df)

    # loop through the dataframe x number of times based on the smallest id
    # from the dataframe
    max_id = df['id'].min()-1
    min_date = df['date'].min()
    while min_date > start_date:
        raw = load_tweets(
            api=api, user_name=user_name, num=num, n_max_id=max_id
        )
        temp_df = pd.DataFrame.from_dict([i.AsDict() for i in raw])
        try:
            temp_df = fix_dates(temp_df)
        except KeyError:
            print(f"\terror fixing dates for {user_name}...")
            return df
        df = pd.concat([df, temp_df], sort=False)
        max_id = df['id'].min()-1
        min_date = df['date'].min()

    df = df[df['date'] >= pd.to_datetime(start_date)]
    df = df[df['lang'] == 'en']  # keep only english langauge tweets
    return df
