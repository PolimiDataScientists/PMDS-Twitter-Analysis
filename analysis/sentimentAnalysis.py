import pandas as pd
import spacy
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# function that computes distributions of sentiment (positive, negative, neutral) in sentence 
def sentiment_vader(sentence):

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    sentiment_dict = sid_obj.polarity_scores(sentence)
    negative = sentiment_dict['neg']
    neutral = sentiment_dict['neu']
    positive = sentiment_dict['pos']
    compound = sentiment_dict['compound']

    if sentiment_dict['compound'] >= 0.05 :
        overall_sentiment = "Positive"

    elif sentiment_dict['compound'] <= - 0.05 :
        overall_sentiment = "Negative"

    else :
        overall_sentiment = "Neutral"
  
    return negative, neutral, positive, compound, overall_sentiment

def compute_sentiment_per_day(data_path):

    nlp = spacy.load('en_core_web_sm')

    df = pd.read_csv(data_path, names=["timestamp", "date", "lang", "text"])

    # computes the day column from the string data data from the tweets
    df['day'] = df['date'].map(lambda date: datetime.strptime(date.split(" ")[0], '%Y-%m-%d'))
    df['day'] = pd.to_datetime(df['day'])

    df['text_modified'] = df['text'].map(lambda sentence:' '.join(([chunk.text for chunk in nlp(sentence).noun_chunks])))

    # creates column with overall_sentiment for each sentence
    df["sentiment"] = df['text_modified'].map(lambda sentence: sentiment_vader(sentence)[4])

    # computes sentiment counts 
    negDFs = df[df["sentiment"] == 'Negative'].groupby(by=df['day'].dt.date).count()
    netDFs = df[df["sentiment"] == 'Neutral'].groupby(by=df['day'].dt.date).count()
    posDFs = df[df["sentiment"] == 'Positive'].groupby(by=df['day'].dt.date).count()

    allDFs = df.groupby(by=df['day'].dt.date).count()

    # computes sentiment percentages 
    allDFs["negPercentage"] = negDFs["sentiment"] / allDFs["sentiment"]
    allDFs["netPercentage"] = netDFs["sentiment"] / allDFs["sentiment"]
    allDFs["posPercentage"] = posDFs["sentiment"] / allDFs["sentiment"]

    return allDFs


sentimentDF = compute_sentiment_per_day("./data/tweets.csv")

#print(sentimentDF[["day", "negPercentage", "netPercentage", "posPercentage"]].head())

sentimentDF.to_csv("./data/sentiments.csv")