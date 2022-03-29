import pandas as pd
import spacy
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

nlp = spacy.load('en_core_web_sm')

df = pd.read_csv("./data/tweets.csv", names=["timestamp", "date", "lang", "region", "text"])

# cleans input text
df['text_modified'] = df['text'].map(lambda sentence:' '.join(([chunk.text for chunk in nlp(sentence).noun_chunks])))


# creates column with overall_sentiment for each sentence
df["sentiments"] = df['text_modified'].map(lambda sentence: sentiment_vader(sentence)[4])

print(df["sentiments"].head(20))

# counts the number of sentences for each type of sentiment
print(df["sentiments"].value_counts())