import plotly_express as px
import dash_html_components as html

def plot_tweets_time(df):
    df_weekly_count = df.groupby(['date_week', 'handle'], as_index=False).count().iloc[:, 0:3]
    df_weekly_count.columns = ['date_week', 'handle', 'count']
    # create plot
    fig_tweet_count_weekly = px.line(df_weekly_count, x = 'date_week', 
                                    y = 'count', color="handle", 
                                    title="Tweet Count Weekly")
    return fig_tweet_count_weekly

# generate a table
def generate_table(df, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(min(len(df), max_rows))]
    )