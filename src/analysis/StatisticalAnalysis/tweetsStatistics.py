class TweetsStatistics:

    def __init__(self, dataset):
        self.dataset = dataset
        self.dataset["day"] = self.dataset["date"].apply(lambda x:x[:10])
        self.tweetsCounts = self.getTweetsCounts()


    def getTweetsCounts(self):
        self.tweetsCount = self.dataset.groupby("day").count().reset_index()
        self.tweetsCount["count"] = self.tweetsCount["timestamp"]
        self.tweetsCount = self.tweetsCount[["day", "count"]]
        self.tweetsCount["year"] = self.tweetsCount["day"].apply(lambda x:x[:4])

    def overview(self):
        tweetsCount2020 = self.tweetsCount[self.tweetsCount["year"] == "2020"]
        tweetsCount2021 = self.tweetsCount[self.tweetsCount["year"] == "2021"]

        maxTweets2020 = tweetsCount2020[tweetsCount2020["count"]
                                        == tweetsCount2020["count"].max()]
        maxTweets2021 = tweetsCount2021[tweetsCount2021["count"]
                                        == tweetsCount2021["count"].max()]

        meanTweets2020 = tweetsCount2020["count"].mean()
        meanTweets2021 = tweetsCount2021["count"].mean()

        medianTweets2020 = tweetsCount2020["count"].median()
        medianTweets2021 = tweetsCount2021["count"].median()

        print("day with max tweets 2020: ")
        print(maxTweets2020)
        print("\nday with max tweets 2021: ")
        print(maxTweets2021)

        print("\nmean tweets count 2020: {}".format(meanTweets2020))
        print("\nmean tweets count 2021: {}".format(meanTweets2021))

        print("\nmedan tweets count 2020: {}".format(medianTweets2020))
        print("\nmedian tweets count 2021: {}".format(medianTweets2021))
