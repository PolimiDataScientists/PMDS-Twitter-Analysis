from sklearn.feature_extraction.text import CountVectorizer
import spacy
import pandas as pd
import re

class NgramStatistics():
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.nlp = spacy.load('en_core_web_sm')

    def max_freq_ngram(self, df, n=2, m=5):
        """
            Calculates the frequency for n-grams for a given dataframe
            and returns the top-m sorted from most freq. to least freq.
        """
        # Remove special characters and numbers
        df['text'] = df['text'].apply(lambda x : re.sub("[^a-z\s]","",x) )
        # Apply tokenification with spacy
        df['text_modified'] = df['text'].map(lambda sentence: ' '.join(
            ([chunk.text for chunk in self.nlp(sentence).noun_chunks])))
        
        word_vectorizer = CountVectorizer(ngram_range=(n,n), analyzer='word')
        sparse_matrix = word_vectorizer.fit_transform(df['text_modified'])
        frequencies = sum(sparse_matrix).toarray()[0]
        return pd.DataFrame(frequencies, index=word_vectorizer.get_feature_names(), columns=['frequency']).sort_values("frequency", ascending=False).head(m)

    def monthly_ngram(self, n=2, m=5):
        """
            Returns the monthly frequency of ngrams for the given dataset
        """
        df = self.dataset.copy()
        df["month"] = df["date"].apply(lambda x:x[5:7])

        return df.groupby(["month"]).apply(self.max_freq_ngram,n=n,m=m)