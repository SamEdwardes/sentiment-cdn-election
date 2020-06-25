import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

colors = {
    'dark_green': '#3a4f41',
    'dark_red': '#b9314f',
    'dark_grey': '#909590',
    'white': '#ffffff',
    'light_grey': '#d2d7df',
    'other_grey': '#d3d3d3',
    'alice_blue': '#F0F8FF',
    'JustinTrudeau': '#D91A20',
    'AndrewScheer': '#1A4E89',
    'ElizabethMay': '#42A03A',
    'theJagmeetSingh': '#F29F24',
    'MaximeBernier': '#A9A9A9'
}

leaders_dropdown = [
    {'label': 'All', 'value': 'All'},
    {'label': 'JustinTrudeau', 'value': 'JustinTrudeau'},
    {'label': 'AndrewScheer', 'value': 'AndrewScheer'},
    {'label': 'ElizabethMay', 'value': 'ElizabethMay'},
    {'label': 'theJagmeetSingh', 'value': 'theJagmeetSingh'},
    {'label': 'MaximeBernier', 'value': 'MaximeBernier'}
]

def navbar():
    layout = dbc.Navbar([
            html.A(dbc.Row([
                dbc.Col(dbc.NavbarBrand("Canadian Party Leaders Twitter", className="ml-2"))
            ], align="center", no_gutters=True))
        ], color="primary", dark=True,
    )
    return layout


def welcome():
    text = (
        'Welcome to Canadian Party Leaders Twitter. This site tracks the '
        'tweets of Canadian political party leaders.'
    )
    layout = html.P(text)
    return layout

def global_filters(min_date, max_date):
    layout = html.Div([
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Party Leader:'),
                dcc.Dropdown(id='dropdown-screen-name', options=leaders_dropdown)
            ]),
            dbc.Col([
                dbc.Label('Include Retweets?'),
                dbc.RadioItems(
                    id='radio-include-rt',
                    value='All',
                    inline=False,
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'No retweets', 'value': 'No retweets'},
                        {'label': 'Retweets only', 'value': 'Retweets only'}
                    ]
                )
            ]),
            dbc.Col([
                dbc.Label('Date Range:'),
                html.Br(),
                dcc.DatePickerRange(
                    id='date-range-picker',
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    initial_visible_month=max_date,
                    clearable=True
                )
            ])
        ])
        
    ])
    return layout


def tweet_frequency():
    layout = html.Div([
        html.Br(),
        dbc.Row([
            dbc.Col([dcc.Graph(id='tweets-bar-count')]),
            dbc.Col([dcc.Graph(id='tweets-over-time-line-plot')])
        ])
    ])
    return layout


def sentiment_analysis():    
    layout = html.Div([
        html.Br(),
        dbc.Row([
            dbc.Col([dcc.Graph(id='tweet-sentiment-vs-polarity')])
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(id='plot-subjectivity-distribution')]),
            dbc.Col([dcc.Graph(id='plot-polarity-distribution')])
        ])
    ])
    return layout


def tweet_about():
    layout = html.Div([
        html.Br(),
        dbc.Row([
            dbc.Col([html.P('Placeholder text')]),
            dbc.Col([dcc.Graph(id='tweet-about-matrix')])
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(id='word-count')]),
            dbc.Col([dcc.Graph(id='phrase-count')])
        ])
    ])
    return layout
    
    