import sys
import tweepy
import csv
import json

f = open('./dags/credentials.json')

# returns JSON object as
# a dictionary
cred = json.load(f)

# Open/Create a file to append data
csvFile = open('./data/tweets.csv', 'w')
# Use csv Writer
csvWriter = csv.writer(csvFile)

client = tweepy.Client(bearer_token=cred['bearer_token'],
                       # Not needed
                       consumer_key=cred['API_key'],
                       consumer_secret=cred['API_key_secret'],
                       access_token=cred['access_token'],
                       access_token_secret=cred['access_token_secret'])

query = '#covid -is:retweet place_country:us lang:en'

start_time = '2020-04-15T00:00:00Z'
end_time = '2020-04-30T00:00:00Z'

tweets = client.search_all_tweets(query=query,
                                     tweet_fields=['id','text', 'created_at', 'geo', 'lang'],
                                     start_time=start_time,
                                     end_time=end_time,
                                     place_fields=['place_type', 'geo'],
                                     expansions='geo.place_id',
                                     max_results=500)

if tweets.data is None:
    print("No results found")
    sys.exit()

# Get list of places from includes object
places = {p["id"]: p for p in tweets.includes['places']}

for tweet in tweets.data:
    '''place = None
    if tweet.geo is not None:
        if places[tweet.geo['place_id']]:
            place = places[tweet.geo['place_id']]'''
    csvWriter.writerow([tweet.id,
                        tweet.created_at,
                        tweet.lang,
                        #place.full_name if place is not None else "",
                        tweet.text.encode('utf-8')])