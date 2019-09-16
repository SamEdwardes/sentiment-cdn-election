import plotly_express as px
import plotly.figure_factory as ff
import dash_html_components as html

def generate_table(df, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(min(len(df), max_rows))]
    )

def plot_tweets_time(df):
    df_weekly_count = df.groupby(['date_week', 'handle'], as_index=False).count().iloc[:, 0:3]
    df_weekly_count.columns = ['date_week', 'handle', 'count']
    # create plot
    fig_tweet_count_weekly = px.line(df_weekly_count, x = 'date_week', 
                                    y = 'count', color="handle", 
                                    title="Number of Tweets by Week")
    return fig_tweet_count_weekly


def plot_tweets_sentiment(df):
    fig_scatter = px.scatter(df.sort_values(by=['handle']), x = 'subjectivity', y = 'polarity', 
                            hover_name='break_tweet', color = 'handle', opacity=0.5, 
                            title = "Sentiment Analysis on Tweets", trendline='ols',size='retweet_count')
    return fig_scatter

def plot_polarity_dist(df):
    # sort df
    df = df.sort_values(by=['handle'])
    # define variables
    polarity = []
    tweets = []
    group_labels = []
    for user in list(df['handle'].unique()):
        polarity.append(df[df['handle'] == user]['polarity'])
        tweets.append(df[df['handle'] == user]['break_tweet'])
        group_labels.append(user)
    # turn data into lists
    data_dist = polarity
    rug_text = tweets
    colors = ['#A2AAFD', '#F79B94']
    # plot
    fig_hist2 = ff.create_distplot(data_dist, group_labels, show_hist = False, colors = colors, rug_text = rug_text)
    fig_hist2.update_layout(title_text='Polarity Distribution')
    return fig_hist2