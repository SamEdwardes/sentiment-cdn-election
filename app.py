import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly_express as px
from dash.dependencies import Input, Output

import src.twitter_plots as twitter_plots
from src import config
from src import ui

##############################################################################
# GLOBAL DATA
##############################################################################

# Twitter full data
print('Reading data...')
print('\ttwitter data')
df = pd.read_csv(config.df_path_clean).query('lang == "en"')#.head(1000)
df['created_at'] = pd.to_datetime(df['created_at'])
df['created_at'] = df['created_at'].dt.tz_localize(None)
min_date = df['created_at'].min()
max_date = df['created_at'].max()

# Word count data
print('\tword count data')
df_word_count = pd.read_csv(config.df_path_word_count)
df_word_count = df_word_count.sort_values(by='count', ascending=False).head(50)

# Phrase count data
print('\tphrase count data')
df_phrase_count = pd.read_csv(config.df_path_phrase_count)
df_phrase_count = df_phrase_count.sort_values(by='count', ascending=False).head(50)
print('all data read!')


##############################################################################
# BOILERPLATE
##############################################################################

# COLOUR AND STYLE
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
app.title = "Canadian Party Leaders Twitter"
port = int(os.environ.get("PORT", 5000))
server = app.server

##############################################################################
# APP LAYOUT
##############################################################################

app.layout = html.Div([
    ui.navbar(),
    dbc.Col(html.Div([
        html.Br(),
        ui.welcome(),
        html.Br(),
        ui.global_filters(min_date, max_date),
        html.Br(),
        dbc.Tabs([
            dbc.Tab(ui.tweet_frequency(), label='Tweet Frequency'),
            dbc.Tab(ui.sentiment_analysis(), label='Sentiment Analysis'),
            dbc.Tab(ui.tweet_about(), label='Tweeting About')
        ])
    ]))
])

##############################################################################
# APP CALL BACKS
##############################################################################

@app.callback(
    [Output('tweets-bar-count', 'figure'),
     Output('tweets-over-time-line-plot', 'figure'),
     Output('plot-subjectivity-distribution', 'figure'),
     Output('plot-polarity-distribution', 'figure'),
     Output('tweet-sentiment-vs-polarity', 'figure'),
     Output('tweet-about-matrix', 'figure'),
     Output('word-count', 'figure'),
     Output('phrase-count', 'figure')],
    [Input('dropdown-screen-name', 'value'),
     Input('radio-include-rt', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def apply_filters_to_plots(screen_name, 
                           include_rt,
                           start_date,
                           end_date):
    """Filter data based on global filters and pass to plotting functions"""
    df_ = df.copy()
    
    # filter data
    if screen_name != 'All' and screen_name is not None:
        df_ = df_.query('screen_name == @screen_name')
    if include_rt == 'No retweets':
        df_ = df_.query('rt == False')
    if include_rt == 'Retweets only':
        df_ = df_.query('rt == True')
    if start_date is not None:
        df_ = df_.query('created_at >= @start_date')
    if end_date is not None:
        df_ = df_.query('created_at <= @end_date')
        
    return (twitter_plots.plot_tweets_total(df_), 
            twitter_plots.plot_tweets_time(df_),
            twitter_plots.plot_subjectivity_dist(df_),
            twitter_plots.plot_polarity_dist(df_),
            twitter_plots.plot_tweets_sentiment(df_),
            twitter_plots.plot_about_eachother_heatmap(df_),
            twitter_plots.plot_word_count_bar_stack(df_word_count),
            twitter_plots.plot_phrase_count_bar_stack(df_phrase_count))
    

##############################################################################
# IF NAME == MAIN
##############################################################################

if __name__ == '__main__':
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=port
    )
