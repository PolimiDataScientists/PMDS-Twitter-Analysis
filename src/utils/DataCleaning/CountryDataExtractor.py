class CountryDataExtractor:

    def __init__(self, dataset):
        self.dataset = dataset

    def extractCountry(self, countryCode):
        return self.dataset[self.dataset["iso_code"] == countryCode]