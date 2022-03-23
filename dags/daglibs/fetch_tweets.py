import tweepy
import csv
import pandas as pd
import json

f = open('./dags/credentials.json')
 
# returns JSON object as
# a dictionary
cred = json.load(f)

####input your credentials here
consumer_key = cred["API_key"]
consumer_secret = cred["API_key_secret"]
access_token = cred["access_token"]
access_token_secret = cred["access_token_secret"]
bearer_token = cred["bearer_token"]

client = tweepy.Client(bearer_token=bearer_token)

csvFile = open('./data/tweets.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

# Replace with your own search query
query = '#covid -is:retweet lang:en'

tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],  \
     start_time="2022-03-21T09:07:21-07:00", end_time="2022-03-22T09:07:21-07:00", \
     max_results=100,)

for tweet in tweets.data:
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])