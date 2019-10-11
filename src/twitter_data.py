# libraries (base)
import datetime
from os import environ
import os

# libraries (other)
import nltk
import json
import pandas as pd
import re
from textblob import TextBlob, Word
import twitter


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

    # API CREDENTIALS
    path = "twitter-credentials.json"
    if os.path.exists(path):  # if running from local machine
        with open(path, "r") as file:
            creds = json.load(file)
        CONSUMER_KEY = creds['CONSUMER_KEY']
        CONSUMER_SECRET = creds['CONSUMER_SECRET']
        ACCESS_KEY = creds['ACCESS_TOKEN']
        ACCESS_SECRET = creds['ACCESS_SECRET']
    else:  # if running from Heroku
        CONSUMER_KEY = environ['CONSUMER_KEY']
        CONSUMER_SECRET = environ['CONSUMER_SECRET']
        ACCESS_KEY = environ['ACCESS_TOKEN']
        ACCESS_SECRET = environ['ACCESS_SECRET']
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_KEY,
                      access_token_secret=ACCESS_SECRET,
                      tweet_mode='extended')

    # DATE FORMATTING
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

    ###########################################
    # LOADING TWITTER DATA
    ###########################################

    def load_tweets():
        """
        Read raw data from twitter

        see for api.GetUserTimeline https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html
        """
        raw = api.GetUserTimeline(screen_name=user_name,
                                count=num,
                                exclude_replies=True,
                                include_rts=True,
                                trim_user=True)
        return raw

    # get the first batch of twitter data
    raw = load_tweets()
    df = pd.DataFrame.from_dict([i.AsDict() for i in raw])
    df = fix_dates(df)

    # loop through the dataframe x number of times based on the smallest id from the dataframe
    max_id = df['id'].min()-1
    min_date = df['date'].min()
    while min_date > start_date:
        raw = load_tweets()
        temp_df = pd.DataFrame.from_dict([i.AsDict() for i in raw])
        temp_df = fix_dates(temp_df)
        df = pd.concat([df, temp_df], sort=False)
        max_id = df['id'].min()-1
        min_date = df['date'].min()

    return df

def lemmatize_with_postag(sentence):
    '''
    https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
    '''
    sent = TextBlob(sentence)
    tag_dict = {"J": 'a',
                "N": 'n',
                "V": 'v',
                "R": 'r'}
    words_and_tags = [(w, tag_dict.get(pos[0], 'n'))
                      for w, pos in sent.tags]
    lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
    return " ".join(lemmatized_list)


def tweets_clean_text(tweet):
    '''
    Cleans the text of a tweet

    Parameters
    ----------
    tweet : str
        Any string can be entered

    Returns
    -------
    str
        Clean tweet in all lower case with stop words removed
    '''
    # remove urls (https://stackoverflow.com/questions/24399820/expression-to-remove-url-links-from-twitter-tweet)
    tweet = re.sub(r"http\S+", "", tweet)
    # remove non alpha/numeric characters
    tweet = re.sub(r"[^a-zA-Z0-9\s]", "", tweet)
    # Make lower case
    tweet = TextBlob(tweet)
    tweet = tweet.words.lower()
    # remove stop words
    stop_words = nltk.corpus.stopwords.words('english')
    tweet = [word for word in tweet if word not in stop_words]
    tweet = TextBlob(' '.join(tweet)).words
    tweet = ' '.join(tweet)
    # remove specific characters
    tweet = re.sub(r" amp ", "", tweet)  # amp = &
    tweet = re.sub(r"'", "", tweet)
    tweet = re.sub(r"’", "", tweet)
    tweet = re.sub(r"–", " ", tweet)
    tweet = re.sub(r"    ", " ", tweet)
    tweet = re.sub(r"   ", " ", tweet)
    tweet = re.sub(r"  ", " ", tweet)
    return(tweet)


def tweets_break(x):
    '''Loop through a tweet and insert <br> every 60 characters for better spacing'''
    it = 1
    start = 0
    stop = start + 60
    num_loops = ((len(x)-1) // 60) + 1
    clean = []

    while it <= num_loops:
        i = x[start:stop]+"<br>"
        clean += i  # append to list
        # update positions
        it += 1
        start = stop
        stop = start + 60

        if stop > len(x)-1:
            stop = len(x)-1

    # concatenate list
    return "".join(clean)


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


def get_word_counts(tweets_df):
    """
    Calculates the word counts for a string

    Parameters:
    -----------
    tweets_df -- (list) a list of tweets, or column from dataframe of tweets

    Returns:
    --------
    Dictionary with word count
    """
    words = " ".join(list(tweets_df))
    counts = TextBlob(words).word_counts
    counts_df = pd.DataFrame.from_dict(dict(counts), orient="index")
    counts_df = counts_df.sort_values(by=[0], ascending=False)
    counts_df.reset_index(level=0, inplace=True)
    counts_df.columns = ['word', 'count']
    return counts_df


def get_phrase_counts(tweets_df):
    """
    Calculates the word counts for a string

    Parameters:
    -----------
    tweets_df -- (list) a list of tweets, or column from dataframe of tweets

    Returns:
    --------
    Dictionary with phrase count
    """
    # get ngrams
    words = " ".join(list(tweets_df))
    ngram_2 = TextBlob(words).ngrams(n=2)
    ngram_3 = TextBlob(words).ngrams(n=3)
    ngram_4 = TextBlob(words).ngrams(n=4)
    ngrams = ngram_2 + ngram_3 + ngram_4
    # do word count on ngrams
    phrases = []
    for i in ngrams:
        phrases.append("_".join(i))
    phrases = " ".join(list(phrases))
    counts = TextBlob(phrases).word_counts
    # turn into dataframe
    counts_df = pd.DataFrame.from_dict(dict(counts), orient="index")
    counts_df = counts_df.sort_values(by=[0], ascending=False)
    counts_df.reset_index(level=0, inplace=True)
    counts_df.columns = ['phrase', 'count']
    return counts_df
