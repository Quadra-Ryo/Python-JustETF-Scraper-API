from JustETFScraper import *

language = "en" # "it" for italian, "en" for english
isin = "IE00B4L5Y983"
htmlFile = getFile(isin, language) # Getting the html file to parse
name = getName(htmlFile, True) # Getting the name
ticker = getTicker(htmlFile, True) # Getting the ticker
generalData = getGeneralInformations(htmlFile, language, True) #Getting all the general data as an array
tenHold = getPercTenHoldings(htmlFile, language, True) # Getting the data relevant to the number and percentage of holdings of the ETF
totaleScarp = scrap(isin, language) # Getting all the data and a formatted output string to return
sectorsData =  getSectorsData(htmlFile, language, True) # Returns all the data of the sectors as an array
countriesData = getCountriesData(htmlFile, language, True) # Returns all the data of the countries as an array
holdingsData = getHoldingsData(htmlFile, language, True) # Returns all the data of the Holdings as an array
# Printing the datas I've got using the functions

print("\n")
print(f"DEBUG: The name of the selected ETF is: {name}")
print(f"DEBUG: The ticker of the selected ETF is: {ticker}")
print(f"DEBUG: The generalData of the selected ETF are: {generalData}")
print(f"DEBUG: The ETF have {tenHold[0]} holdings and the percentage of the first 10 holdings is {tenHold[1]}")
print(f"DEBUG: The ETF sectors are {sectorsData}")
print(f"DEBUG: The ETF sectors are {countriesData}")
print(f"DEBUG: The ETF sectors are {holdingsData}")
print("\n\nTotal scarp:")
print(totaleScarp)
print("\n")