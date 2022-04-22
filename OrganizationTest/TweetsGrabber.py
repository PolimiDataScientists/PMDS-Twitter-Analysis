# This module handles the grabbing of tweets in order to produce some csv Files
from colorama import Cursor
from ErrorMod import Error
import tweepy
import json
import csv
import datetime
import time


class Grabber():
    credPath = './credentials.json'
    savingPath = './TweetsCSV/'

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

    def SetupWriter(self, date, nDays, max):
        start = date.strftime('%d-%m-%Y')
        end = (date + datetime.timedelta(nDays)).strftime('%d-%m-%Y')

        try:
            self.csvFile = open(Grabber.savingPath + 'Tweets_' +
                                start + '__' + end + f'[{max}].csv', 'a')
            self.csvWriter = csv.writer(self.csvFile)
        except FileNotFoundError:
            Error.print('No such directory as ' + Grabber.savingPath[:-1] +
                        ' you may have to change Grabber.savingPath')

    def ConvertDate(date):
        return date.strftime('%Y-%m-%dT%H:%M:%SZ')

    def QueryRequest(self, QueryHeader, startDate, nDays, place_country='us', lang='en', sleepingTime=2, maxResults=500, tweet_fields=['id', 'text', 'created_at', 'geo', 'lang'], place_fields=['place_type', 'geo']):
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
                                         tweet.created_at,
                                         tweet.lang,
                                         tweet.text.encode('utf-8')])

            date = endDate
            time.sleep(sleepingTime)

        print('[DONE]')


if __name__ == '__main__':
    g = Grabber()
    g.QueryRequest('#covid -is:retweet',
                   datetime.date(2020, 5, 1), 1, maxResults=10)
