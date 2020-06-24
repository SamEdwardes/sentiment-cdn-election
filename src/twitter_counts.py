from collections import defaultdict

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def count_tweet_words(df, ngram_range=(1, 1), min_df=6):
    """Create a word/ngram count dataframe by user.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain the columns: ['screen_name', 'clean_tweet']
    ngram_range : tuple (min_n, max_n), default=(1, 1)
        The lower and upper boundary of the range of n-values for different 
        word n-grams or char n-grams to be extracted. All values of n such 
        such that min_n <= n <= max_n will be used. For example an ngram_range 
        of (1, 1) means only unigrams, (1, 2) means unigrams and bigrams, and 
        (2, 2) means only bigrams. Only applies if analyzer is not callable.
    min_df : float in range [0.0, 1.0] or int, default=6
        When building the vocabulary ignore terms that have a document 
        frequency strictly lower than the given threshold. This value is also 
        called cut-off in the literature. If float, the parameter represents a 
        proportion of documents, integer absolute counts. This parameter is 
        ignored if vocabulary is not None.

    Returns
    -------
    pandas.DataFrame
        A dataframe with the top word/ngram counts by user_name
    """

    users = df['screen_name'].unique().tolist()
    count_df = defaultdict(list)
    for user in users:
        print(f'Counting for {user}...')
        vectorizer = CountVectorizer(
            ngram_range=ngram_range,
            stop_words='english',
            min_df=min_df
        )
        df_ = df.query('screen_name == @user').dropna(subset=['clean_tweet'])
        print('\tfitting CountVectorizer')
        X = vectorizer.fit_transform(df_['clean_tweet'])
        print('\tlooping and counting words')
        for i, j in vectorizer.vocabulary_.items():
            count_ = X[:, j].sum()
            count_df['screen_name'].append(user)
            count_df['phrase'].append(i)
            count_df['count'].append(X[:, j].sum())
            
    count_df = pd.DataFrame(count_df)
    
    return count_df
