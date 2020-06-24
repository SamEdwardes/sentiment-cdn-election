import json
import os
from collections import defaultdict
from datetime import date, datetime

import pandas as pd
import twitter


def create_twitter_api():
    """Check environment and return appropriate twitter API"""

    # API CREDENTIALS
    path = "twitter-credentials.json"
    # if running from local machine
    if os.path.exists(path):             
        creds = json.load(open(path, "r"))
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


def get_old_tweets(user_name, 
                   num_tweets_per_iter=200,
                   max_iter=10,
                   include_retweets=True):
    '''Gets tweets and returns a list of Status instances.

    Parameters
    ----------
    user_name : str 
        The user you would like to get twitter data from (e.g. "JustinTrudeau")
    num : int
        The number of tweets you would like to return (max is 200)
    loops: int
        Because the max number of tweets is only 200, loops will indicate how 
        many sets of "num" tweets you would like to return. For example 
        num=200 and loops=2 would get 400 tweets

    Returns
    -------
    Dataframe with twitter data
    '''

    print(f"Getting tweets for: {user_name}...")
    api = create_twitter_api()
    tweets = []

    # keep adding more tweets until the max limit is reached
    iteration = 1
    while True:
        if iteration == 1:
            # get the first batch of twitter data
            t = api.GetUserTimeline(
                screen_name=user_name, 
                include_rts=include_retweets,
                count=num_tweets_per_iter
            )
        else:
            # call the api with max_id
            t = api.GetUserTimeline(
                screen_name=user_name, 
                include_rts=include_retweets,
                count=num_tweets_per_iter,
                max_id=oldest_tweet_id - 1
            )
        # add api response to list and get stats
        tweets = tweets + t
        oldest_tweet_id = tweets[-1].id
        oldest_tweet_date = tweets[-1].created_at
        oldest_tweet_date = datetime.strptime(oldest_tweet_date, '%a %b %d %H:%M:%S %z %Y')
        print(f'\tIteration {iteration}: ' 
              f'tweets = {len(t)}, oldeset = {oldest_tweet_date}')
        iteration += 1

        # check to see if the loop should be brocken
        if iteration > max_iter:
            print('\t', 'x' * 32, sep='')
            print(f'\tMax iterations reached! Oldest tweet is {oldest_tweet_date}')
            break

        if len(t) == 0:
            print('\t', 'x' * 32, sep='')
            print(f'\tNo new tweets found in last iteration')
            break
    
    print('\t', 'x' * 32, sep='')
    print(f'\tTotal tweets: {len(tweets)}')
    print(f'\tOldeset tweet: {oldest_tweet_date}')       

    return tweets


def tweets_to_df(tweets):
    """Convert list of tweets into a DataFrame

    Paramaters
    ----------
    tweets : list of Statuses
        Should be a list of statuses that is returned by `get_tweets`.

    Returns
    -------
    pandas.DataFrame
        A dataframe of the tweets
    """

    out = defaultdict(list)

    for x in tweets:
        out['screen_name'].append(x.user.screen_name)
        out['user_name'].append(x.user.name)
        out['user_id'].append(x.user.id)
        out['id'].append(x.id)
        out['created_at'].append(
            datetime.strptime(x.created_at, '%a %b %d %H:%M:%S %z %Y')
        )
        out['lang'].append(x.lang)
        out['retweet_count'].append(x.retweet_count)
        out['favorite_count'].append(x.favorite_count)
        out['location'].append(x.location)
        out['place'].append(x.place)
        out['hashtags'].append(x.hashtags)
        out['full_text'].append(x.full_text)


    return pd.DataFrame(out)

# ============================================================================
# Testing
# ============================================================================

# se_tweets = get_tweets('TheRealSamlAm', 20, 2)
# se_df = tweets_to_df(se_tweets)
