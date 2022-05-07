import pandas as pd
import spacy
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import glob

class SentimentAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.sentiment_df = None

    #  function that computes distributions of sentiment (positive, negative, neutral) in sentence
    def sentiment_vader(self, sentence):

        # Create a SentimentIntensityAnalyzer object.
        sid_obj = SentimentIntensityAnalyzer()

        sentiment_dict = sid_obj.polarity_scores(sentence)
        negative = sentiment_dict['neg']
        neutral = sentiment_dict['neu']
        positive = sentiment_dict['pos']
        compound = sentiment_dict['compound']

        if sentiment_dict['compound'] >= 0.05:
            overall_sentiment = "Positive"
        elif sentiment_dict['compound'] <= - 0.05:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"

        return negative, neutral, positive, compound, overall_sentiment

    # computes the sentiment distribution per day reading from the data path
    def compute_sentiment_per_day(self):

        nlp = spacy.load('en_core_web_sm')

        #df = pd.read_csv(self.data_path, names=[
        #                 "timestamp", "date", "lang", "text"])

        csv_files = glob.glob(self.data_path)
        df = []
        for file in csv_files:
            df_one = pd.read_csv(file, names=[
                        "id", "day", "lang", "geo", "text"])
            df.append(df_one)

        # computes the day column from the string data data from the tweets
        #df['day'] = df['date'].map(
        #    lambda date: datetime.strptime(date.split(" ")[0], '%Y-%m-%d'))
        #df['day'] = pd.to_datetime(df['day'])

        df['text_modified'] = df['text'].map(lambda sentence: ' '.join(
            ([chunk.text for chunk in nlp(sentence).noun_chunks])))

        # creates column with overall_sentiment for each sentence
        df["sentiment"] = df['text_modified'].map(
            lambda sentence: self.sentiment_vader(sentence)[4])

        # computes sentiment counts
        negDFs = df[df["sentiment"] == 'Negative'].groupby(
            by=df['day'].dt.date).count()
        netDFs = df[df["sentiment"] == 'Neutral'].groupby(
            by=df['day'].dt.date).count()
        posDFs = df[df["sentiment"] == 'Positive'].groupby(
            by=df['day'].dt.date).count()

        allDFs = df['day','id','sentiment'].groupby(by=df['day'].dt.date).count()

        # computes sentiment percentages
        allDFs["negPercentage"] = negDFs["sentiment"] / allDFs["sentiment"]
        allDFs["netPercentage"] = netDFs["sentiment"] / allDFs["sentiment"]
        allDFs["posPercentage"] = posDFs["sentiment"] / allDFs["sentiment"]

        self.sentiment_df = allDFs

    # exports the sentiment data
    def exportSentiment(self, out_path):
        try:
            self.sentiment_df.to_csv(out_path)
        except:
            print("Sentiments need to be computed before being exported")
