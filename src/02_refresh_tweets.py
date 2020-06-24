import pandas as pd
import twitter

import config
from helpers import print_break
from twitter_data import create_twitter_api, tweets_to_df

############################################################
max_iter = 1_000
############################################################

# read in the existing twitter data
tweets_df = pd.read_csv(config.df_path_raw)
tweets_df['created_at'] = pd.to_datetime(tweets_df['created_at'])

# find the newest tweet id and date for each user
users = tweets_df['screen_name'].unique().tolist()
max_date_user = tweets_df.groupby('screen_name')['created_at'].agg('max')
max_id_user = tweets_df.groupby('screen_name')['id'].agg('max')

# lop through each user and get new tweets
api = create_twitter_api()
new_tweets = []
for i in users:
    print_break(f'Refreshing tweets for {i}')
    iteration = 1
    max_id = max_id_user[i]
    while True:
        t = api.GetUserTimeline(
            screen_name=i,
            include_rts=True,
            count=200,
            since_id=max_id
        )
        print(f'\titeration {iteration}: num = {len(t)}')
        new_tweets = new_tweets + t        
        
        # check if loop should be brocken
        if len(t) == 0:
            break
        elif iteration == max_iter:
            break
        else:
            iteration += 1
            max_id = t[0].id

# parse new tweets into dataframe
new_tweets_df = tweets_to_df(new_tweets)
out = pd.concat([new_tweets_df, tweets_df])
out = out.drop_duplicates('id').reset_index(drop=True)

# summarise update
print_break('Summary of new tweets')
print(f'\tThe database contained {tweets_df.shape[0]} tweets.')
print(f'\t{new_tweets_df.shape[0]} new tweets were pulled.')
print(f'\tAfter the update, the database now contains {out.shape[0]} tweets.')

# write to disk only if more than 2 new tweets
if len(new_tweets) > 2 and type(new_tweets) is list:
    print_break('Writing to disk')
    out.to_csv(config.df_path_raw, index=False)
else:
    print_break('Not writing to disk, too few new tweets')
print('\tComplete!')