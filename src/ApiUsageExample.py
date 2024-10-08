from JustETFScraper import *

language = "en" # "it" for italian, "en" for english
isin = "IE00B4L5Y983"
htmlFile = getFile(isin, language) # Getting the html file to parse
name = getName(htmlFile, True)
ticker = getTicker(htmlFile, True)
generalData = getGeneralInformations(htmlFile, language, True)
tenHold = getPercTenHoldings(htmlFile, language, True)
totaleScarp = scraper(isin, language)
# Printing the datas I've got using the functions

print("\n")
print(f"The name of the selected ETF is: {name}")
print(f"The ticker of the selected ETF is: {ticker}")
print(f"The generalData of the selected ETF are: {generalData}")
print(f"DEBUG: The ETF have {tenHold[0]} holdings and the percentage of the first 10 holdings is {tenHold[1]}")
#print("\n\nTotal scarp:")
#print(totaleScarp)
print("\n")