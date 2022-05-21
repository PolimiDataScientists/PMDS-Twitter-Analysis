import pandas as pd
from CountryDataExtractor import CountryDataExtractor


dataset = pd.read_csv("./data/owid-covid-data.csv")

countryDataExtractor = CountryDataExtractor(dataset)

covidDataUS = countryDataExtractor.extractCountry("USA")

covidDataGB = countryDataExtractor.extractCountry("GBR")

covidDataAU = countryDataExtractor.extractCountry("AUS")


print(covidDataUS)

print(covidDataGB)

print(covidDataAU)