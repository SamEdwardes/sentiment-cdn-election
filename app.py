import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly_express as px
from dash.dependencies import Input, Output

import src.twitter_plots as twitter_plots
from src.helpers import get_project_global_variables

users = get_project_global_variables()["twitter_handles"]
df_path_raw = get_project_global_variables()["df_path_raw"]
df_path_clean = get_project_global_variables()["df_path_clean"]
df_path_word_count = get_project_global_variables()["df_path_word_count"]
df_path_phrase_count = get_project_global_variables()["df_path_phrase_count"]

df = pd.read_csv(df_path_clean)
df['date'] = pd.to_datetime(df['date'])
df_word_count = pd.read_csv(df_path_word_count)
df_phrase_count = pd.read_csv(df_path_phrase_count)

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
        # PLOTS
        html.Div(className="twelve columns", style={"backgroundColor": colors['white'], "padding": 20}, children=[
            html.H4("How much are the leaders tweeting?"),
            # ROW 1 - TWEET COUNTS
            html.Div(className="row", children=[
                # ROW 1, COLUMN 1
                html.Div(className="one-half column", children=[
                    dcc.Graph(id='tweets-bar-count')
                ]),
                # ROW 1, COLUMN 2
                html.Div(className="one-half column", children=[
                    dcc.Graph(id='tweets-by-week-line')
                ]),
            ]),
            # ROW 1.5 FILTERS
            html.Div(className="row", children=[
                html.Br(),
                dcc.DatePickerRange(id='selected-date-range',
                                    start_date=min(df['date']),
                                    min_date_allowed=min(df['date']),
                                    end_date=max(df['date']),
                                    max_date_allowed=max(df['date']))
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
                    # Word count bar chart
                    dcc.Dropdown(id='word-count-drop-down',
                                 options=leaders_dropdown, value="All"),
                    html.Br(),
                    dcc.Graph(id='word-count-bar'),
                    html.Br(),            
                    # Phrase count bar chart
                    dcc.Dropdown(id='phrase-count-drop-down',
                                 options=leaders_dropdown, value="All"),
                    html.Br(),
                    dcc.Graph(id='phrase-count-bar'),
                    html.Br()
         
            ]),
            # ROW 8 - About
            html.Div(className="row", children=[
                html.Hr(),
                dcc.Markdown(open("docs/intro.md").read())
            ])
        ])
    ])
])


###########################################
# APP CALL BACKS
###########################################

# Tweet bar count
@app.callback(
    Output("tweets-bar-count", "figure"), [
        Input("selected-date-range", 'start_date'),
        Input("selected-date-range", 'end_date')
    ]
)
def plot_tweets_bar_count(start_date, end_date, df=df):
    """
    Plots a word count horizontal bar chart
    """
    df = df[df['date'] >= pd.to_datetime(start_date)]
    df = df[df['date'] <= pd.to_datetime(end_date)]
    return twitter_plots.plot_tweets_total(df)


# Number of tweets by week
@app.callback(
    Output("tweets-by-week-line", "figure"), [
        Input("selected-date-range", 'start_date'),
        Input("selected-date-range", 'end_date')
    ]
)
def plot_tweets_by_week_line(start_date, end_date, df=df):
    """
    Plots a word count horizontal bar chart
    """
    df = df[df['date'] >= pd.to_datetime(start_date)]
    df = df[df['date'] <= pd.to_datetime(end_date)]
    return twitter_plots.plot_tweets_time(df)


# Word count bar chart
@app.callback(
    Output("word-count-bar", "figure"), [
        Input("word-count-drop-down", "value"),
        Input("selected-date-range", 'start_date'),
        Input("selected-date-range", 'end_date')
    ]
)
def plot_word_count_bar_stack(filter_selection, start_date, end_date, 
                              df=df_word_count):
    """
    Plots a word count horizontal bar chart
    """
    # df = df[df['date'] >= pd.to_datetime(start_date)]
    # df = df[df['date'] <= pd.to_datetime(end_date)]
    if filter_selection != "All":
        df = df[df["handle"] == filter_selection]
        df = df.sort_values(by=['total_count'], ascending=False).reset_index(
            drop=True).head(50)
    else:
        df = df.sort_values(by=['total_count'],
                            ascending=False).reset_index(drop=True)
        df = df[df['rank'] <= 50]

    fig = px.bar(df, y='word', x='count', orientation="h", color="handle",
                 title="Tweet Word Count", height=800, 
                 color_discrete_map=colour_dict)
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
    if 'ON_HEROKU' in os.environ:
        debug_bool = False
    else:
        debug_bool = True
    app.run_server(debug=debug_bool)
