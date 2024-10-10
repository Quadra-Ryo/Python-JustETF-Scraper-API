from JustETFScraper import *

# Setting the values to standard values
language = "en" # "it" for italian, "en" for english
isin = "IE00B4L5Y983"

#Getting the basic data that the script need to work
htmlFile = getFile(isin, language) # Getting the html file to parse
outputHashMap = getOutputStringHashMap()
outputGenerlaData = getGeneralDataOutputHashMap()
supportedLanguages = getSupportedLanguages()
inputStrings = getInputHashMap()

# Getting a custom input to chose the language and the ISIN dinamically
language = input(f"Select a language, the supported languages are: {supportedLanguages} \n")
isin = input(f"{inputStrings[language]}\n")

#Getting all the possible data I can get from the ETF
url = getURL(isin, language)
name = getName(htmlFile, True) # Getting the name
ticker = getTicker(htmlFile, True) # Getting the ticker
generalData = getGeneralInformations(htmlFile, language, True) #Getting all the general data as an array
tenHold = getPercTenHoldings(htmlFile, language, True) # Getting the data relevant to the number and percentage of holdings of the ETF
sectorsData =  getSectorsData(htmlFile, language, True) # Returns all the data of the sectors as an array
countriesData = getCountriesData(htmlFile, language, True) # Returns all the data of the countries as an array
holdingsData = getHoldingsData(htmlFile, language, True) # Returns all the data of the Holdings as an array
totaleScarp = scrape(isin, language) # Getting all the data and a formatted output string to return

# Composing the output string based on the selected language using the data I got with the single functions
outputString = ""
outputString += (f"ETF: {name}, Ticker: \"{ticker}\", ISIN: {isin}\n")
outputString += (f"{outputHashMap[language][1]} {tenHold[0]}{outputHashMap[language][2]} {tenHold[1]}\n\n")

if holdingsData != ["-"]:
    outputString += (f"{outputHashMap[language][3]}\n")
    for i in range(int(len(holdingsData)/2)):
        outputString += (f"{outputHashMap[language][6]}: {holdingsData[i*2]} {outputHashMap[language][7]} {holdingsData[i*2+1]}\n")
else:
        outputString += (f"{dataNotFoundHashMap[language][1]}\n") 

outputString += (f"\n{outputHashMap[language][4]} {countriesData}\n")
outputString += (f"{outputHashMap[language][5]} {countriesData}\n\n")
outputString += (f"{generalDataHashMap[language][len(generalDataHashMap[language])-1]}\n")

for i in range(len(generalData)):
    outputString += (f"{generalDataHashMap[language][i]}: {generalData[i]}\n")
outputString += (f"{outputHashMap[language][6]} {url}")

# Printing the datas I've got using the functions
print("\n")
print(f"DEBUG: The name of the selected ETF is: {name}")
print(f"DEBUG: The ticker of the selected ETF is: {ticker}")
print(f"DEBUG: The generalData of the selected ETF are: {generalData}")
print(f"DEBUG: The ETF have {tenHold[0]} holdings and the percentage of the first 10 holdings is {tenHold[1]}")
print(f"DEBUG: The ETF sectors are {sectorsData}")
print(f"DEBUG: The ETF sectors are {countriesData}")
print(f"DEBUG: The ETF sectors are {holdingsData}")
print("\n\n")
print("Total scarp:")
print(totaleScarp)
print("\n\n")
print("Print based on the selected language without using the scarp function:")
print(outputString)