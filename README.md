# 2019 Canadian Election Twitter Sentiment Analysis

## Background

The 2019 Canadian election will be held on Monday, October 21, 2019. This program analyses twitter data from the party leaders running in the 2019 Canadian elections.

The web app can be found on Heroku: [https://cdn-election-sent-app.herokuapp.com/](https://cdn-election-sent-app.herokuapp.com/)


| Party          | Leader         | Site                                                            |
|----------------|----------------|-----------------------------------------------------------------|
| Liberals       | Justin Trudeau | [2019.liberal.ca](https://2019.liberal.ca/)                     |
| Conservatives  | Andrew Scheer  | [conservative.ca](https://www.conservative.ca/)                 |
| NDP            | Jagmeet Singh  | [ndp.ca](https://www.ndp.ca/)                                   |
| Green Party    | Elizabeth May  | [greenparty.ca](https://www.greenparty.ca/en)                   |
| People's Party | Maxime Bernier | [peoplespartyofcanada.ca](https://www.peoplespartyofcanada.ca/) |


## Disclaimer

> **Please note that this is a work in progress. Results may not be 100% accurate and there could be errors in the analysis.**

## Directory

```
.
├── Procfile
├── README.md
├── app-local.py #
├── app.py # the file used by Heroku to create apps
├── data # contains example data
├── docs # used by app.py to read in text
├── election-tweets-analysis.ipynb # example of code
├── nltk.txt
├── notebooks # contain examples of code
├── requirements.txt # used by Heroku to install requirements
├── src
│   ├── twitter_data.py # functions to get and clean twitter data
│   └── twitter_plots.py # functions to create plots
```
*Tree diagram only includes most important files.*

## Environment

Use the following code with terminal to create the appropriate environment.

```
conda create --name hello-world-dash-app-env python=3.6.8
conda activate hello-world-dash-app-env

pip install pandas
pip install dash
pip install gunicorn
# see requirements.txt for additional installs
```

*I originally used conda to install the libraries but for some reason that resulted in deployment errors. When using pip to install everything worked.*

Save the requirements using pip and conda

```
pip freeze > requirements.txt # used by Heroku
```

## Resources

- Heroku Instructions from Dash - https://dash.plot.ly/deployment
- An example of plotly express on Heroku - https://github.com/plotly/dash-px/blob/master/app.py
- Good blog post with deploying machine learning model - https://blog.cambridgespark.com/deploying-a-machine-learning-model-to-the-web-725688b851c7
- Setting up Twitter API and Keys on Heroku - https://dev.to/emcain/how-to-set-up-a-twitter-bot-with-python-and-heroku-1n39


## To Do

- figure out why there are much less tweets for some users (e.g. Elizabeth May). Could be just because they retweet a lot.