import matplotlib.pyplot as plt
import pandas as pd

sentiments = pd.read_csv("./data/sentiments.csv")
sentiments = sentiments[["day","negPercentage","netPercentage","posPercentage"]]

#print(sentiments.head(15))

sentiments.plot('day', "negPercentage")