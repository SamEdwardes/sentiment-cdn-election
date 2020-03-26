import re

import nltk
import pandas as pd
from textblob import TextBlob


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
    ngrams = ngram_2 + ngram_3
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


def get_phrase_counts_df(df, selected_col, users):
    df_phrase_count_total = get_phrase_counts(df[selected_col])
    df_phrase_count_total.columns = ['phrase', 'total_count']
    df_phrase_count_total['rank'] = df_phrase_count_total['total_count'].rank(
        ascending=False, method="first")
    df_phrase_count = pd.DataFrame()

    for i in users:
        temp = get_phrase_counts(
            df[df['handle'] == i]['clean_tweet'])
        temp['handle'] = i
        df_phrase_count = pd.concat([temp, df_phrase_count])

    df_phrase_count = pd.merge(df_phrase_count, df_phrase_count_total,
                               how='left', on='phrase')
    df_phrase_count = df_phrase_count.sort_values(
        by=['total_count', 'phrase', 'count'], ascending=False
    ).reset_index(drop=True)

    return df_phrase_count.head(5000)


def get_word_counts_df(df, selected_col, users):
    df_word_count_totals = get_word_counts(df[selected_col])
    df_word_count_totals.columns = ['word', 'total_count']
    df_word_count_totals['rank'] = df_word_count_totals['total_count'].rank(
        ascending=False, method="first")
    df_word_count = pd.DataFrame()

    for i in users:
        temp = get_word_counts(
            df[df['handle'] == i]['clean_tweet'])
        temp['handle'] = i
        df_word_count = pd.concat([temp, df_word_count])

    df_word_count = pd.merge(df_word_count, df_word_count_totals, how='left',
                                on='word')
    df_word_count = df_word_count.sort_values(
        by=['total_count', 'word', 'count'], ascending=False
    ).reset_index(drop=True)
    
    return df_word_count.head(5000)


def word_search(text, search_words):
    """
    Checks to see if words exist in a body of text

    Parameters:
    -----------
    search_words -- (list) a list of words to search for in text
    text -- (string) the body of text to search

    Returns:
    --------
    True if any word is found, False otherwise
    """
    for i in search_words:
        if i.lower() in text.lower():
            return True

    return False


def count_tweets_about(df, col_to_search):
    justin_search = ["justin", "trudeau", "justintrudeau"]
    scheer_search = ["scheer", "andrew", "andrewscheer"]
    may_search = ["may", "elizabeth", "ElizabethMay"]
    singh_search = ["singh", "jagmeet", "jagmeetsingh", "theJagmeetSingh"]
    bernier_search = ["bernier", "maxime", "MaximeBernier"]

    df["about_trudeau"] = df[col_to_search].apply(
        word_search, search_words=justin_search)
    df["about_scheer"] = df[col_to_search].apply(
        word_search, search_words=scheer_search)
    df["about_may"] = df[col_to_search].apply(
        word_search, search_words=may_search)
    df["about_singh"] = df[col_to_search].apply(
        word_search, search_words=singh_search)
    df["about_bernier"] = df[col_to_search].apply(
        word_search, search_words=bernier_search)

    return df
