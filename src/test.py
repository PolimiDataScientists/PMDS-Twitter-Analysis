from pytz import country_names
from utils.DataCollection.TweetsGrabber import Grabber
from analysis.SentimentAnalysis.sentimentAnalysis import SentimentAnalysis as sa

import datetime

inFile = './data/Tweets*.csv'
outFile = './data/sent_analysis.csv'

g = Grabber()
g.loadCredentials
g.QueryRequest('#covid -is:retweet', datetime.date(2020, 3, 1), 60, maxResults=10, place_country = "us", lang = "en")

senan = sa(inFile)
senan.compute_sentiment_per_day()
senan.exportSentiment(outFile)
