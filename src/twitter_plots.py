import dash_html_components as html
import plotly_express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


# colours for eachleader
colour_dict = {'JustinTrudeau': '#D91A20',
               'AndrewScheer': '#1A4E89',
               'ElizabethMay': '#42A03A',
               "theJagmeetSingh": '#F29F24',
               'MaximeBernier': '#A9A9A9'}

colors = {"dark_green": "#3a4f41",
          "dark_red": "#b9314f",
          "dark_grey": "#909590",
          "white": "#ffffff",
          "light_grey": "#d2d7df"
          }

# Note to self. To change plot background color
# fig.update_layout({"showlegend": False, "paper_bgcolor": colors['dark_grey']})


def generate_table(df, max_rows=10):
    '''
    Renders a table in dash app.
    '''
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(min(len(df), max_rows))]
    )


def plot_tweets_total(df):
    df_count = df.groupby(['handle'], as_index=False).count().iloc[:, 0:2]
    df_count.columns = ['handle', 'number of tweets']
    # create plot
    fig = px.bar(df_count, x='handle',
                 y='number of tweets', color="handle", color_discrete_map=colour_dict,
                 title="Number of Tweets", height=400)
    fig.update_layout({"showlegend": False})
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=30), autosize=True)
    return(fig)


def plot_tweets_time(df):
    '''
    Plots tweets by week for each unique handle
    '''
    df_weekly_count = df.groupby(
        ['date_week', 'handle'], as_index=False).count().iloc[:, 0:3]
    df_weekly_count.columns = ['week', 'handle', 'number of tweets']
    # create plot
    fig = px.line(df_weekly_count, x='week',
                  y='number of tweets', color="handle", color_discrete_map=colour_dict,
                  title="Number of Tweets by Week", height=400)
    fig.update_layout({"showlegend": False})
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=30))
    return fig


def plot_tweets_sentiment(df):
    '''
    Plots sentiment vs. subjectivity for every tweet.
    '''
    fig_scatter = px.scatter(df, x='subjectivity', y='polarity', height=600,
                             hover_name='break_tweet', color='handle', color_discrete_map=colour_dict, opacity=0.5,
                             title="Tweet Polarity Vs. Subjectivity", trendline='ols')
    return fig_scatter


def plot_polarity_dist(df):
    '''
    Plots a histogram distribution of sentiment for each unique handle.
    '''
    # define variables
    polarity = []
    tweets = []
    group_labels = []
    leaders = list(df['handle'].unique())
    for user in leaders:
        polarity.append(df[df['handle'] == user]['polarity'])
        tweets.append(df[df['handle'] == user]['break_tweet'])
        group_labels.append(user)
    # turn data into lists
    data_dist = polarity
    rug_text = tweets
    colors = [colour_dict[i] for i in leaders]
    # plot
    fig = ff.create_distplot(data_dist, group_labels,
                             show_hist=False, colors=colors, rug_text=rug_text)
    fig.update_layout(title_text='Polarity Distribution')
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=30))
    fig.update_layout({"showlegend": False})
    return fig


def plot_subjectivity_dist(df):
    '''
    Plots a histogram distribution of sentiment for each unique handle.
    '''
    # define variables
    subjectivity = []
    tweets = []
    group_labels = []
    leaders = list(df['handle'].unique())
    for user in leaders:
        subjectivity.append(df[df['handle'] == user]['subjectivity'])
        tweets.append(df[df['handle'] == user]['break_tweet'])
        group_labels.append(user)
    # turn data into lists
    data_dist = subjectivity
    rug_text = tweets
    colors = [colour_dict[i] for i in leaders]
    # plot
    fig = ff.create_distplot(data_dist, group_labels,
                             show_hist=False, colors=colors, rug_text=rug_text)
    fig.update_layout(title_text='Subjectivity Distribution')
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=30))
    fig.update_layout({"showlegend": False})
    return fig


def plot_about_eachother_heatmap(df):
    '''
    Plots a heatmap about how much they are tweeting about eachother
    '''
    df = df[["handle", "about_scheer", "about_may",
             "about_trudeau", "about_bernier",  "about_singh"]]
    df = df.groupby(['handle']).sum()
    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        x=df.columns,
        y=df.index
    ))
    fig.update_layout(title_text='Tweets About Eachother')
    return fig
