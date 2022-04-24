from sentimentAnalysis import SentimentAnalysis


if __name__ == "__main__":
    sentimentAnalysis = SentimentAnalysis("./data/tweets.csv")
    sentimentAnalysis.compute_sentiment_per_day()
    sentimentAnalysis.exportSentiment("./data/sentiments.csv")