import tweepy
import csv
import pandas as pd
import json

f = open('/usr/local/airflow/dags/credentials.json')
 
# returns JSON object as
# a dictionary
cred = json.load(f)

####input your credentials here
consumer_key = cred["API_key"]
consumer_secret = cred["API_key_secret"]
access_token = cred["access_token"]
access_token_secret = cred["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


# Open/Create a file to append data
csvFile = open('/usr/local/airflow/data/tweets.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search_tweets,q="#covid",count=10,
                           lang="en",
                           since="2022-01-01").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])