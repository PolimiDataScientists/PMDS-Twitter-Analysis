import sys
import tweepy
import csv
import json
import time
import pandas as pd
from datetime import date,timedelta


f = open('./dags/credentials.json')

# returns JSON object as
# a dictionary
cred = json.load(f)

# Open/Create a file to append data
csvFile = open('./data/tweetsAU.csv', 'a')
# Use csv Writer
csvWriter = csv.writer(csvFile)

client = tweepy.Client(bearer_token=cred['bearer_token'],
                       # Not needed
                       consumer_key=cred['API_key'],
                       consumer_secret=cred['API_key_secret'],
                       access_token=cred['access_token'],
                       access_token_secret=cred['access_token_secret'])

query = '#covid -is:retweet place_country:au lang:en'

startPandemic = date(2020,1,1)   # start date
endPandemic = date(2021,12,31) 

days = list(pd.date_range(startPandemic, endPandemic, freq='d'))

days = list(map(lambda d: d.strftime('%Y-%m-%d'), days))

print(days)

for i in range(0, len(days)-1):

    start_time = days[i]  + 'T00:00:00Z'
    end_time = days[i+1] + 'T00:00:00Z'

    print(start_time, end_time)

    time.sleep(5)

    tweets = client.search_all_tweets(query=query,
                                              tweet_fields=[
                                                  'id', 'text', 'created_at', 'geo', 'lang'],
                                              start_time=start_time,
                                              end_time=end_time,
                                              place_fields=[
                                                  'place_type', 'geo'],
                                              expansions='geo.place_id',
                                              max_results=500)

    if tweets.data is None:
        print("No results found for")
        continue

        print(end_time)

            # Get list of places from includes object
            # places = {p["id"]: p for p in tweets.includes['places']}

    for tweet in tweets.data:
        csvWriter.writerow([tweet.id,
                                    tweet.created_at,
                                    tweet.lang,
                                    # place.full_name if place is not None else "",
                                    tweet.text.encode('utf-8')])
