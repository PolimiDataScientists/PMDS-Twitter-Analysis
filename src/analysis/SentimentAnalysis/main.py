from sentimentAnalysis import SentimentAnalysis


if __name__ == "__main__":
    sentimentAnalysis = SentimentAnalysis("./data/tweetsAU.csv")
    sentimentAnalysis.compute_sentiment_per_day()
    sentimentAnalysis.exportSentiment("./data/sentimentsAU.csv")