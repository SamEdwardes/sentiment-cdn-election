# base
import datetime
import socket
import os
# external libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import nltk
import json
import pandas as pd
import plotly.graph_objs as go
import plotly_express as px
import re
from textblob import TextBlob, Word
import twitter
# my libraries
from src.twitter_data import *
from src.twitter_plots import *

start_date = datetime.date(2019, 9, 11)  # election officially starts on sep 11
users = ["JustinTrudeau", "AndrewScheer",
         "ElizabethMay", "theJagmeetSingh", "MaximeBernier"]

df_temp = tweets_get(user_name="JustinTrudeau", num=200, start_date=start_date)

print(df_temp.head())