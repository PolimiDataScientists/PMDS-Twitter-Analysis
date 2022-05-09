# This module handles the grabbing of tweets in order to produce some csv Files

# Custom module for error handling
# Dot was added for using this class from other directories / should be removed for local testing
from .ErrorMod import Error 

# A bunch of useful libraries
import tweepy
import json
import csv
import datetime
import time
import re

class Grabber():
    # The Path where the credentials are stored
    credPath = './credentials.json'

    # The Path where the csv file will be saved
    #savingPath = './TweetsCSV/'
    savingPath = './data/'

    # The Path of the last saved csv
    lastSaved = ''

    def __init__(self):
        self.loadCredentials()

    def loadCredentials(self):
        try:
            credFile = open(self.credPath)
            self.cred = json.load(credFile)

        except FileNotFoundError:
            Error.print('Grabber couldn\'t find any valid credentials, check whether the file ' +
                        self.credPath + ' exists or change Grabber.credPath to a valid path')

    def connect(self):
        self.client = tweepy.Client(bearer_token=self.cred['bearer_token'])

    # Insgtantiating the CSV writer later used to save the tweets
    def SetupWriter(self, date: datetime.date, nDays: int, max: int):
        start = date.strftime('%d-%m-%Y')
        end = (date + datetime.timedelta(nDays)).strftime('%d-%m-%Y')

        try:
            self.lastSaved = Grabber.savingPath + 'Tweets_' + \
                start + '__' + end + f'[{max}].csv'

            self.csvFile = open(self.lastSaved, 'a', newline='') # newline parameter to escape empty rows
            self.csvWriter = csv.writer(self.csvFile)
        except FileNotFoundError:
            Error.print('No such directory as ' + Grabber.savingPath[:-1] +
                        ' you may have to change Grabber.savingPath')

    # Convert a date object to a suitable string for the Twitter API
    def ConvertDate(date):
        return date.strftime('%Y-%m-%dT%H:%M:%SZ')

    def CleanText(text):
        text = re.sub(r'@[A-Za-z0-9]+', '', text) #Remove tags
        text = re.sub(r'RT[\s]+', '', text) #remove ReTweets
        text = re.sub(r'https?:\/\/\S+', '', text) #remove links
        text = re.sub(r'\\\S+', '', text) #Remove emojies and sp chars
        text = re.sub(r'#', '', text) #Remove emojies and sp chars
        text = re.sub(r'b\'', '', text) #remove the "b'"
        text = re.sub(r'b\'', '', text) #remove the "b'"
        return text

    def QueryRequest(self, QueryHeader: str, startDate: datetime.date, nDays: int, place_country='us', lang='en', sleepingTime=2.0, maxResults=500, tweet_fields=['id', 'text', 'created_at', 'geo', 'lang'], place_fields=['place_type', 'geo']):
        '''Main function for Query requests, the result will be saved in a csv file\n
        Args:
            startDate (date): The starting point of the period of interest
            QueryHeader (str): The first part of the query regarding the hashtags and the retweeting
            nDays (int): the number of consecutive days of interest
            place_country (str): where should the tweets come from?
            lang (str): the language of the tweets
            sleepingTime (float): the number of seconds the program should wait before sending another request
            maxResults (int): The maximum number of Tweets recieved [min: 10]
            tweet_fields ([str]): What fields of the tweets are you interested in recieving?
            place_fields ([str]): What fields of the place are you interested in recieving?
        '''

        self.connect()
        self.SetupWriter(startDate, nDays, maxResults)

        date = startDate

        for i in range(nDays):
            print('Fetching ' + date.strftime('%d/%m/%Y') +
                  f' [{i + 1}/{nDays}]')

            endDate = date + datetime.timedelta(days=1)

            tweets = self.client.search_all_tweets(query=QueryHeader + ' place_country:' + place_country + ' lang:' + lang,
                                                   tweet_fields=tweet_fields,
                                                   start_time=Grabber.ConvertDate(
                                                       date),
                                                   end_time=Grabber.ConvertDate(
                                                       endDate),
                                                   place_fields=place_fields,
                                                   expansions='geo.place_id',
                                                   max_results=maxResults)

            if(tweets.data is None):
                Error.print('No result found')

            for tweet in tweets.data:
                self.csvWriter.writerow([tweet.id,
                                        #tweet.created_at,
                                        tweet.created_at.strftime('%Y-%m-%d'),
                                        tweet.lang,
                                        tweet.geo, #we can use it later
                                        Grabber.CleanText(tweet.text).encode('utf-8')
                ])

            date = endDate
            time.sleep(sleepingTime)

        print('[DONE]')


if __name__ == '__main__':
    g = Grabber()
    g.QueryRequest('#covid -is:retweet',
                   datetime.date(2020, 5, 1), 1, maxResults=10)
