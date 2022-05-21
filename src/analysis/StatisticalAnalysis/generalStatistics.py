class GeneralStatistics:

    def __init__(self, dataset):
        self.dataset = dataset

    def computeMaxDayForCol(self, col, indexCol="day",  perc=False):

        datasetNoOutliers = self.dataset[self.dataset[col]
                                         < 1] if perc else self.dataset

        return datasetNoOutliers[datasetNoOutliers[col] == datasetNoOutliers[col].max()][[indexCol, col]]

    def computeMaxMonthForCol(self, col, indexCol="day",  perc=False):

        datasetNoOutliers = self.dataset[self.dataset[col]
                                         < 1] if perc else self.dataset

        datasetNoOutliers["month"] = datasetNoOutliers[indexCol].apply(lambda x:x[:7])

        datasetByMonth = datasetNoOutliers.groupby("month").mean()

        return datasetByMonth[datasetByMonth[col] == datasetByMonth[col].max()][col]
