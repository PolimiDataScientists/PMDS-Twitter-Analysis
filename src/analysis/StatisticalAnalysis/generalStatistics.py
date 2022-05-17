class GeneralStatistics:

    def __init__(self, dataset):
        self.dataset = dataset

    def computeMaxDayForCol(self, col, perc = False):

        datasetNoOutliers = self.dataset[self.dataset[col] < 1] if perc else self.dataset 

        return datasetNoOutliers[datasetNoOutliers[col] == datasetNoOutliers[col].max()][["day",col]]


       