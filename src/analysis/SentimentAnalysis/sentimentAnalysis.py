import pandas as pd
import spacy
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalysis:
    def __init__(self, data_path, col_names=["timestamp", "date", "lang", "geo", "text"]):
        self.data_path = data_path
        self.sentiment_df = None
        self.col_names=col_names

    #  function that computes distributions of sentiment (positive, negative, neutral) in sentence
    def sentiment_vader(self, sentence, sent_threshold=[0.05, -0.05], sent_class=["Positive","Neutral","Negative"]):

        # Create a SentimentIntensityAnalyzer object.
        sid_obj = SentimentIntensityAnalyzer()

        sentiment_dict = sid_obj.polarity_scores(sentence)
        negative = sentiment_dict['neg']
        neutral = sentiment_dict['neu']
        positive = sentiment_dict['pos']
        compound = sentiment_dict['compound']

        overall_sentiment = None
        for thresh, sent in zip(sent_threshold, sent_class[:-1]):
            if sentiment_dict['compound'] >= thresh:
                overall_sentiment = sent
                break
        if overall_sentiment is None:
            overall_sentiment = sent_class[-1]

        return negative, neutral, positive, compound, overall_sentiment

    # computes the sentiment distribution per day reading from the data path
    def compute_sentiment_per_day(self, **kwargs):

        nlp = spacy.load('en_core_web_sm')

        df = pd.read_csv(self.data_path, header=None, index_col=False, names=self.col_names)

        # computes the day column from the string data data from the tweets
        df['day'] = df['date'].map(
            lambda date: datetime.strptime(date.split(" ")[0], '%Y-%m-%d'))
        df['day'] = pd.to_datetime(df['day'])

        df['text_modified'] = df['text'].map(lambda sentence: ' '.join(
            ([chunk.text for chunk in nlp(sentence).noun_chunks])))

        # creates column with overall_sentiment for each sentence
        df["sentiment"] = df['text_modified'].map(
            lambda sentence: self.sentiment_vader(sentence, **kwargs)[4])

        # computes sentiment counts
        negDFs = df[df["sentiment"] == 'Negative'].groupby(
            by=df['day'].dt.date).count()
        netDFs = df[df["sentiment"] == 'Neutral'].groupby(
            by=df['day'].dt.date).count()
        posDFs = df[df["sentiment"] == 'Positive'].groupby(
            by=df['day'].dt.date).count()

        allDFs = df.groupby(by=df['day'].dt.date).count()

        # computes sentiment percentages
        allDFs["negPercentage"] = negDFs["sentiment"] / allDFs["sentiment"]
        allDFs["netPercentage"] = netDFs["sentiment"] / allDFs["sentiment"]
        allDFs["posPercentage"] = posDFs["sentiment"] / allDFs["sentiment"]

        self.sentiment_df = allDFs[["negPercentage", "netPercentage", "posPercentage"]].fillna(0)

    # exports the sentiment data
    def exportSentiment(self, out_path):
        try:
            self.sentiment_df.to_csv(out_path)
        except:
            print("Sentiments need to be computed before being exported")

    def getSentimentStatistics(self):
        if self.sentiment_df is None:
            self.compute_sentiment_per_day()
        return self.sentiment_df[["day","negPercentage","netPercentage","posPercentage"]].idxmax()