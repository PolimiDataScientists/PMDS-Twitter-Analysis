import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')
  
df = pd.read_csv("./data/tweets.csv", names=["timestamp", "text"])


df['text_modified'] = df['text'].map(lambda sentence: ' '.join([chunk.text for chunk in nlp(sentence).noun_chunks]))

print(df.head(10))

def expand(df, col, sep=','):
    r = df[col].str.split(sep)
    d = {c: df[c].values.repeat(r.str.len(), axis=0) for c in df.columns}
    d[col] = [i for sub in r for i in sub]
    return pd.DataFrame(d)

df = expand(df, 'text_modified', sep=' ')

words =  df.groupby("text_modified") \
    .count() \
    .sort_values(by="timestamp", ascending=False) \


words.to_csv("./data/words.csv")

