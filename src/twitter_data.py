# libraries (base)
import datetime
import os

# libraries (other)
import nltk
import json
import pandas as pd
import re
from textblob import TextBlob, Word
import twitter


def tweets_get(user_name, num = 200, loops = 1):
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

    # get credentials
    path = "twitter-credentials.json"
    with open(path, "r") as file:
        creds = json.load(file)
        
    # establish API
    api = twitter.Api(consumer_key= creds['CONSUMER_KEY'],
                    consumer_secret= creds['CONSUMER_SECRET'],
                    access_token_key= creds['ACCESS_TOKEN'],
                    access_token_secret= creds['ACCESS_SECRET'],
                    tweet_mode='extended') 
    
    # get the first batch of twitter data
    # see for api.GetUserTimeline https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html
    raw = api.GetUserTimeline(screen_name = user_name, 
                             count = num, 
                             exclude_replies=True,
                             include_rts=False,
                             trim_user=True)

    # convert into dataframe
    df = pd.DataFrame.from_dict([i.AsDict() for i in raw])
    
    # loop through the dataframe x number of times based on the smallest id from the dataframe
    max_id = df['id'].min()-1
    for x in list(range(1, loops+1)):
        raw = api.GetUserTimeline(screen_name = user_name, 
                                  count = num, 
                                  exclude_replies=True,
                                  include_rts=False,
                                  trim_user=True,
                                  max_id = max_id)
        temp_df = pd.DataFrame.from_dict([i.AsDict() for i in raw])
        df = pd.concat([df, temp_df])
        max_id = df['id'].min()-1
                                
    return df

def tweets_refresh(num_loops = 1):
    '''
    Gets new twitter data if no yet downloaded for the current day

    Checks to see if twitter data has been downloaded for the day. If the data has not been downloaded, it will download
    new twitter data to data/raw and also return the data as a DataFrame. If the data has already been downloaded it will read the latest
    twitter data from disc and return the dataframe.

    Returns
    -------
    DataFrame
        Contains raw twitter data from GetUserTimeline
    '''

    brk = "\n\n*************************\n"
    print(brk + "DATA REFRESH RESULTS:")

    # get current date
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    df_path_raw = "data/raw/" + current_date + "_twitter-data-raw.csv"

    # check to see if twitter data has been downloaded for today yet
    if os.path.exists(df_path_raw) == False:
        # get twitter data
        JT = tweets_get("JustinTrudeau", 200, loops=num_loops)
        AS = tweets_get("AndrewScheer", 200, loops=num_loops)
        
        # add user name
        AS['handle'] = "@AndrewScheer"
        JT['handle'] = "@JustinTrudeau"
        
        # combine dataframes
        tweets_raw = pd.concat([JT, AS])
        
        # save dataframe to local disc
        tweets_raw.to_csv(df_path_raw)
        print("\tNew twitter data downloaded.")
        
    else:
        tweets_raw = pd.read_csv(df_path_raw)
        print('\tData read from local machine')

    return tweets_raw

def tweets_clean_df(df):
    '''
    Takes raw twitter data and cleans data. Returns new dataframe and saves to data/clean/.

    Parameters
    ----------
    df : pd.DataFrame
        dataframe of twitter data from GetUserTimeline
    '''

    # DATES

    df['date_time'] = pd.to_datetime(df['created_at'])
    df['date'] = pd.to_datetime(df['date_time'].dt.date)
    def find_monday(d):
        '''Receives a date and returns the date of the preceding Monday.'''
        while d.weekday()!=0:
            d += datetime.timedelta(-1)
        return d  
    df['date_week'] = df['date'].apply(find_monday)


    # FILTERS

    # keep starting from the min date where data exists for both
    min_as = min(df[df['handle'] == "@AndrewScheer"]['date'])
    min_js = min(df[df['handle'] == "@JustinTrudeau"]['date'])
    min_date = max(min_as, min_js)
    df = df[df['date']>= min_date]
    # keep only english langauge tweets
    df = df[df['lang'] == 'en']


    # CLEAN TWEET TEXT

    def lemmatize_with_postag(sentence):
        '''
        https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
        '''
        sent = TextBlob(sentence)
        tag_dict = {"J": 'a', 
                    "N": 'n', 
                    "V": 'v', 
                    "R": 'r'}
        words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
        lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
        return " ".join(lemmatized_list)

    def tweets_clean_text(tweet):
        '''
        Cleans the actual text of tweet

        Parameters
        ----------
        tweet : str
            Any string can be entered

        Returns
        -------
        str
            Clean tweet in all lower case with stop words removed
        '''
        # convert into a text blob object
        tweet = TextBlob(tweet)
        # create a word list: make lower case, singularize
        tweet = tweet.words.lower().singularize()
        # remove stop words
        stop_words = nltk.corpus.stopwords.words('english')
        tweet = [word for word in tweet if word not in stop_words]
        tweet = TextBlob(' '.join(tweet)).words
        # Lemmatize
        tweet = TextBlob(lemmatize_with_postag(' '.join(tweet))).words
        tweet = ' '.join(tweet)
        return(tweet)
    
    # run functions, save dataframe, and return dataframe
    tweets = df['full_text']
    df['clean_tweet'] = tweets.apply(tweets_clean_text)
    # get current date
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    df_path_clean = "data/clean/" + current_date + "_twitter-data-clean.csv"
    # df.to_csv(df_path_clean)
    return(df)

def get_sentiment(tweets):
    '''returns a dictionary with sentiment and polarity'''
    polarity = []
    subjectivity = []
    for tweet in tweets:
        tweet = TextBlob(tweet)
        pol = tweet.sentiment.polarity
        polarity.append(pol)
        subj = tweet.sentiment.subjectivity
        subjectivity.append(subj)
        
    return {'polarity': polarity, 'subjectivity': subjectivity} 