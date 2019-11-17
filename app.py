# base
import datetime
import socket
# external libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly_express as px
# my libraries
import src.twitter_data as twitter_data
import src.twitter_plots as twitter_plots


update_tweets = False
update_analysis = False

df_path_raw = "data/twitter-data-raw.csv"
df_path_clean = "data/twitter-data-clean.csv"
df_path_word_count = "data/word-count.csv"
df_path_phrase_count = "data/phrase-count.csv"

start_date = datetime.date(2019, 9, 11)  # election officially starts on sep 11
users = ["JustinTrudeau", "AndrewScheer",
         "ElizabethMay", "theJagmeetSingh", "MaximeBernier"]


###########################################
# GETTING DATA
###########################################

# check environment
if (
    socket.gethostname() != "Sams-MacBook-Pro.local" and
    socket.gethostname() != "dhcp-206-87-114-237.ubcsecure.wireless.ubc.ca" and
    socket.gethostname() != "dhcp-206-87-114-42.ubcsecure.wireless.ubc.ca"
):
    update_tweets = False
    update_analysis = False

# read or get new twitter data
print("Getting twitter data...")
if update_tweets == False and update_analysis == False:
    print("\tReading old clean twitter data from disk.")
    df = pd.read_csv(df_path_clean)
    df_word_count = pd.read_csv(df_path_word_count)
    df_phrase_count = pd.read_csv(df_path_phrase_count)
elif update_tweets == False and update_analysis == True:
    print("\tReading old raw twitter data from disk.")
    df = pd.read_csv(df_path_raw)
else:
    print("\tGetting new twitter data from Twitter API.")
    df = pd.DataFrame()
    for user in users:
        df_temp = twitter_data.tweets_get(
            user_name=user, num=200, start_date=start_date)
        df_temp['handle'] = user
        df = pd.concat([df, df_temp], sort=False)
    df.to_csv(df_path_raw, index=False)


###########################################
# ANALYSING TWITTER DATA
###########################################

if update_analysis == True:
    # clean twitter data
    print("Analysing twitter data...")
    df['date_time'] = pd.to_datetime(df['created_at'])
    df['date'] = pd.to_datetime(df['date_time'].dt.date)
    df = df[df['date'] >= start_date]
    df = df[df['lang'] == 'en']  # keep only english langauge tweets
    df['clean_tweet'] = df['full_text'].apply(twitter_data.tweets_clean_text)
    df['break_tweet'] = df['full_text'].apply(twitter_data.tweets_break)

    # add sentiment and polarity
    raw_sentiment = twitter_data.get_sentiment(df['full_text'])
    clean_sentiment = twitter_data.get_sentiment(df['clean_tweet'])
    df['polarity'] = clean_sentiment['polarity']
    df['subjectivity'] = clean_sentiment['subjectivity']

    # tweets about other leaders
    justin_search = ["justin", "trudeau", "justintrudeau"]
    scheer_search = ["scheer", "andrew", "andrewscheer"]
    may_search = ["may", "elizabeth", "ElizabethMay"]
    singh_search = ["singh", "jagmeet", "jagmeetsingh", "theJagmeetSingh"]
    bernier_search = ["bernier", "maxime", "MaximeBernier"]
    df["about_trudeau"] = df["full_text"].apply(
        twitter_data.word_search, search_words=justin_search)
    df["about_scheer"] = df["full_text"].apply(
        twitter_data.word_search, search_words=scheer_search)
    df["about_may"] = df["full_text"].apply(
        twitter_data.word_search, search_words=may_search)
    df["about_singh"] = df["full_text"].apply(
        twitter_data.word_search, search_words=singh_search)
    df["about_bernier"] = df["full_text"].apply(
        twitter_data.word_search, search_words=bernier_search)

    # word counts
    df_word_count_totals = twitter_data.get_word_counts(df['clean_tweet'])
    df_word_count_totals.columns = ['word', 'total_count']
    df_word_count_totals['rank'] = df_word_count_totals['total_count'].rank(
        ascending=False, method="first")
    df_word_count = pd.DataFrame()
    for i in users:
        temp = twitter_data.get_word_counts(
            df[df['handle'] == i]['clean_tweet'])
        temp['handle'] = i
        df_word_count = pd.concat([temp, df_word_count])
    df_word_count = pd.merge(df_word_count, df_word_count_totals, how='left',
                             on='word')
    df_word_count = df_word_count.sort_values(
        by=['total_count', 'word', 'count'], ascending=False).reset_index(drop=True)
    df_word_count.head(5000)

    # phrase counts
    df_phrase_count_total = twitter_data.get_phrase_counts(df['clean_tweet'])
    df_phrase_count_total.columns = ['phrase', 'total_count']
    df_phrase_count_total['rank'] = df_phrase_count_total['total_count'].rank(
        ascending=False, method="first")
    df_phrase_count = pd.DataFrame()
    for i in users:
        temp = twitter_data.get_phrase_counts(
            df[df['handle'] == i]['clean_tweet'])
        temp['handle'] = i
        df_phrase_count = pd.concat([temp, df_phrase_count])
    df_phrase_count = pd.merge(df_phrase_count, df_phrase_count_total, how='left',
                               on='phrase')
    df_phrase_count = df_phrase_count.sort_values(
        by=['total_count', 'phrase', 'count'], ascending=False).reset_index(drop=True)
    df_phrase_count.head(5000)

    # export clean data
    df.to_csv(df_path_clean, index=False)
    df_word_count.to_csv(df_path_word_count, index=False)
    df_phrase_count.to_csv(df_path_phrase_count, index=False)

###########################################
# APP LAYOUT
###########################################

# COLOUR AND STYLE
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "2019 Canadian Election Sentiment Analysis"
server = app.server

colors = {"dark_green": "#3a4f41",
          "dark_red": "#b9314f",
          "dark_grey": "#909590",
          "white": "#ffffff",
          "light_grey": "#d2d7df",
          "other_grey": "#d3d3d3",
          "alice_blue": "#F0F8FF"
          }

colour_dict = {'JustinTrudeau': '#D91A20',
               'AndrewScheer': '#1A4E89',
               'ElizabethMay': '#42A03A',
               "theJagmeetSingh": '#F29F24',
               'MaximeBernier': '#A9A9A9'}

leaders_dropdown = [
    {'label': 'All', 'value': 'All'},
    {'label': 'JustinTrudeau', 'value': 'JustinTrudeau'},
    {'label': 'AndrewScheer', 'value': 'AndrewScheer'},
    {'label': 'ElizabethMay', 'value': 'ElizabethMay'},
    {'label': 'theJagmeetSingh', 'value': 'theJagmeetSingh'},
    {'label': 'MaximeBernier', 'value': 'MaximeBernier'}
]


# APP LAYOUT
app.layout = html.Div(style={'backgroundColor': colors['light_grey']}, children=[
    # HEADER
    html.Div(className="row", style={'backgroundColor': colors['dark_red'], "padding": 10}, children=[
        html.H2('Canadian 2019 Election Twitter Sentiment Analysis',
                style={'color': colors['white']})
    ]),
    # MAIN BODY
    html.Div(className="row", children=[
        # SIDEBAR
        html.Div(className="three columns", style={'padding': 20}, children=[
            dcc.Markdown(open("docs/intro.md").read())]),
        # PLOTS
        html.Div(className="nine columns", style={"backgroundColor": colors['white'], "padding": 20}, children=[
            html.H4("How much are the leaders tweeting?"),
            # ROW 1 - TWEET COUNTS
            html.Div(className="row", children=[
                # ROW 1, COLUMN 1
                html.Div(className="one-half column", children=[
                    dcc.Graph(figure=twitter_plots.plot_tweets_total(df))
                ]),
                # ROW 1, COLUMN 2
                html.Div(className="one-half column", children=[
                    dcc.Graph(figure=twitter_plots.plot_tweets_time(df))
                ])
            ]),
            # ROW 2 - Sentiment Plot
            html.Div(className="row", children=[
                html.Hr(),
                html.H4("What is the sentiment of their tweets?"),
                dcc.Markdown(open("docs/sentiment-explained.md").read()),
                dcc.Graph(figure=twitter_plots.plot_tweets_sentiment(df))
            ]),
            # ROW 3 - Sentiment Distributions
            html.Div(className="row", children=[
                # ROW 3, COLUMN 1
                html.Div(className="one-half column", children=[
                    dcc.Graph(figure=twitter_plots.plot_polarity_dist(df))
                ]),
                # ROW 3, COLUMN 2
                html.Div(className="one-half column", children=[
                    dcc.Graph(figure=twitter_plots.plot_subjectivity_dist(df))
                ])
            ]),
            # ROW 4 - About eachother
            html.Div(className="row", children=[
                html.Hr(),
                html.H4("What are the leaders tweeting about?"),
                html.Br()
            ]),
            # ROW 6 - Tweet word and phrase counts title
            html.Div(className="row", children=[
                # ROW 6, COLUMN 1
                html.Div(className="one-half column", children=[
                    dcc.Markdown(open("docs/tweeting-about.md").read()),
                    html.Br()
                ]),
                # ROW 6, COLUMN 2
                html.Div(className="one-half column", children=[
                    # Tweets about eachother
                    dcc.Graph(
                        figure=twitter_plots.plot_about_eachother_heatmap(df)),
                    html.Br()
                ]),
            ]),
            # ROW 7 - Tweet counts
            html.Div(className="row", children=[
                # ROW 7, COLUMN 1
                html.Div(className="one-half column", children=[
                    # Word count bar chart
                    dcc.Dropdown(id='word-count-drop-down',
                                 options=leaders_dropdown, value="All"),
                    html.Br(),
                    dcc.Graph(id='word-count-bar'),
                    html.Br()
                ]),
                # ROW 7, COLUMN 2
                html.Div(className="one-half column", children=[
                    # Phrase count bar chart
                    dcc.Dropdown(id='phrase-count-drop-down',
                                 options=leaders_dropdown, value="All"),
                    html.Br(),
                    dcc.Graph(id='phrase-count-bar'),
                    html.Br()
                ])
            ])
        ])
    ])
])


###########################################
# APP CALL BACKS
###########################################


# Word count bar chart
@app.callback(
    Output("word-count-bar", "figure"),
    [Input("word-count-drop-down", "value")]
)
def plot_word_count_bar_stack(filter_selection):
    """
    Plots a word count horizontal bar chart
    """
    df = df_word_count
    if filter_selection != "All":
        df = df[df["handle"] == filter_selection]
        df = df.sort_values(by=['total_count'], ascending=False).reset_index(
            drop=True).head(50)
    else:
        df = df.sort_values(by=['total_count'],
                            ascending=False).reset_index(drop=True)
        df = df[df['rank'] <= 50]

    fig = px.bar(df, y='word', x='count', orientation="h", color="handle",
                 title="Tweet Word Count", height=800, color_discrete_map=colour_dict)
    fig.update_layout({"showlegend": False})
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=30), autosize=True)
    fig.update_yaxes(categoryorder="total ascending", title_text="")
    return(fig)


# Phrase count bar chart
@app.callback(
    Output("phrase-count-bar", "figure"),
    [Input("phrase-count-drop-down", "value")]
)
def plot_phrase_count_bar_stack(filter_selection):
    """
    Plots a phrase count horizontal bar chart
    """
    df = df_phrase_count
    if filter_selection != "All":
        df = df[df["handle"] == filter_selection]
        df = df.sort_values(by=['total_count'], ascending=False).reset_index(
            drop=True).head(50)
    else:
        df = df.sort_values(by=['total_count'],
                            ascending=False).reset_index(drop=True)
        df = df[df['rank'] <= 50]

    fig = px.bar(df, y='phrase', x='count', orientation="h", color="handle",
                 title="Tweet Phrase Count", height=800, color_discrete_map=colour_dict)
    fig.update_layout({"showlegend": False})
    fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=30, b=30))
    fig.update_yaxes(categoryorder="total ascending", title_text="")
    return(fig)


if __name__ == '__main__':
    app.run_server(debug=False)
