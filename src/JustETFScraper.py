import os
from urllib.request import urlretrieve
import time

# Data scraping program for the JustETF site
# This application collects data by downloading the HTML file from the site and parsing it.
# You can call single functions in the main to get specific data or call the "scrape" function to get all the data at once
# Author: Niccolò Quadrani
# Date: 10/10/2024

##########################################################################################
# In case you don't want to show the debug print on the console
# CTRL + F -> Find "print" -> Replace "#print"
# To switch back to the debug mode 
# CTRL + F -> Find "#print" -> Replace "print"
##########################################################################################

USELESS_DATA = 184 # Before rr. 184 the HTML file never contains usefull informations
htmlFileFold = f"resources/etf.html"

# Hash map used to manage multiple languages and data sets within a single script.
splitHashMap = {"en": ["Top 10 Holdings", "Basics </h2>", "Countries", "Sectors", "Show more", "out of ", "Basics"],
                      "it": ["Prime 10 partecipazioni", "Indicatore sintetico di spesa (TER)", "Paesi", "Settori", "Mostra di più", "su ", "Nozioni di base"]}
    
# Hash map used to manage multiple languages in the output
outputHashMap = {"en": ["FINAL DATA:", "Number of holdings:", ", the percentage of the top 10 holdings within the ETF:",
                              "The holdings to which the ETF is most exposed are:", "The countries to which the ETF is most exposed are:",
                              "The sectors to which the ETF is most exposed are:", "Holding", "with the percentage of"],
                 "it": ["DATI FINALI:", "Numero di partecipazioni:", ", la percentuale delle prime 10 partecipazioni dell'ETF è:",
                        "Le partecipazioni alle quali l'ETF è maggiormente esposto sono:",
                        "Gli stati ai quali l'ETF è maggiormente esposto sono:", "I settori ai quali l'ETF è maggiormente esposto sono:",
                        "Partecipazione", "con la percentuale di"]}

# Hash map used to manage inputs
inputHashMap = {"en" : "Insert the ETF's ISIN", "it" : "Inserisci l'ISIN dell'ETF"}

# Hash map used to manage multiple languages of the general data, separated from the outputHashMap just to make the code a little bit cleaner
generalDataHashMap = {"en": ["Index","Investment focus","Fund size","Total expense ratio","Replication","Legal structure",
                             "Strategy risk","Sustainability","Fund currency","Currency risk","Volatility 1 year (in EUR)",
                             "Inception/ Listing Date","Distribution policy","Distribution frequency","Fund domicile","Fund Provider", "General data:"],
                      "it": ["Indice","Focus di investimento","Dimensione del fondo","Indicatore sintetico di spesa (TER)","Replicazione",
                             "Struttura legale","Rischio di strategia","Sostenibilità","Valuta dell'ETF","Rischio di cambio","Volatilità ad 1 anno (in EUR)",
                             "Data di lancio/ quotazione","Politica di distribuzione","Frequenza di distribuzione","Domicilio del fondo","Emittente", "Dati generali:"]}

# Hash map used to manage multiple languages when missing data occurs
dataNotFoundHashMap = {"en": ["Data not found", "It is impossible to retrieve the holdings data."],
                       "it": ["Dati non disponibili","Impossibile reperire i dati riferiti alle partecipazioni dell'ETF"]}

#Array of the API's supported languages
supportedLanguages = ["en", "it"] # List of the implemented languages

########################################################################################## Utils functions

def cleanHtml():
     # Open the file in write mode to overwrite it with an empty string to clean the html
    try:
        if os.path.exists(htmlFileFold):
            with open(htmlFileFold, 'w', encoding="utf8") as file:
                file.write("")
        return 0
    except Exception as e:
        print("The program runned into an unexpected error")
        print(f"The program runned into the error: {e}")
        return -1
        
def debug(debug):
    for s in debug:
        print(f"{s}\n")
        return 0
 
def getFile(ISIN: str, language: str) -> list[str]:
    try:
        isin = ISIN.upper() # The ISIN letters are allways uppercase
        language = language.lower()  # Making the script not case-sensitive

        if language not in supportedLanguages:
            print("\nERROR: The selected language is not implemented yet")
            return -1

        if len(isin) != 12:
            print("\nERROR: Bad ISIN format, please check the ISIN code")
            return -1

        # Getting the correct link
        url = f"https://www.justetf.com/{language}/etf-profile.html?isin={isin}#overview"
        htmlFilePath = f"resources/etf.html"

        # Downloading the HTML from the site
        urlretrieve(url, htmlFilePath)
        htmlFilePath, headers = urlretrieve(url, htmlFilePath)
        print(f"\nDEBUG: Success! ETF data downloaded to \"{htmlFilePath}\"")

        # Opening and reading the downloaded file
        with open(htmlFilePath, 'r', encoding="utf8") as file:
            output = file.read()

        output = output.split("\n")
        return output
    except Exception as e:
        print("The program runned into an unexpected error")
        print(f"The program runned into the error: {e}")
        return ["-"]

##########################################################################################
# Data Handling Functions

# How to use the functions correctly:
# Each function accepts two or three parameters.
# If required, specify the language of the file using the "language" parameter (The only two supported languages are "en" or "it").
# For the first string parameter and the flag, follow the instructions below:
# Set the "flag" attribute to "True" if you want to call a specific function (e.g. To get the Ticker, use "getTicker(string, True)") without retrieving other data.
# If the flag is set to "True," the "string" parameter should be the entire HTML file downloaded using the "urlretrieve(url, htmlFilePath)" function.
# The "flag" attribute gonna be "False" only in the case where you want all the parameters and you allready have all the right strings to parse (e.g. the "scrape" function)

##########################################################################################

# Well known data get functions

def getSupportedLanguages() -> list[str]:
    # Returning a list of the supported languages in case of API usage in an external script
    return supportedLanguages

def getOutputStringHashMap():
    # Returning the hashmap of the output strings in all the supported languages
    return outputHashMap

def getGeneralDataOutputHashMap():
    # Returning the name of the parameters of all the general data in every supported languages
    return generalDataHashMap

def getInputHashMap():
    return inputHashMap

# ETF data get functions

def getTicker(tickerString: str, singleFunctionCall: bool) -> str:
    # Getting the Ticker from the "name" string that contains both Name and Ticker of the ETF
    try:
        if singleFunctionCall: #Getting the correct data to parse in case of the call of the single function
            for x in range(len(tickerString) - USELESS_DATA -1):
                if "<title>" in tickerString[x + USELESS_DATA]:
                    tickerString = tickerString[x + USELESS_DATA]
                    print("\nDEBUG: Ticker found")
                    break

        split = tickerString.split("</title>")
        split = split[0].split("|")
        ticker = split[1].replace(" ", "")
        cleanHtml()
        return ticker
    except Exception as e:
        print("The program runned into an unexpected error")
        cleanHtml()
        print(f"The program runned into the error: {e}")
        return "-"

def getName(nameString: str, singleFunctionCall: bool) -> str:
    # Getting the Name of the ETF from the "name" string
    try:
        if singleFunctionCall: #Getting the correct data to parse in case of the call of the single function
            for x in range(len(nameString) - USELESS_DATA -1):
                if "<title>" in nameString[x + USELESS_DATA]:
                    nameString = nameString[x + USELESS_DATA]
                    print("\nDEBUG: Title found")
                    break

        split = nameString.split("</title>")
        split = split[0].split("|")
        name = split[0].replace("<title>", "")
        listName = list(name)
        listName[len(name) - 1] = ""
        name = "".join(listName)
        cleanHtml()
        return name
    except Exception as e:
        print("The program runned into an unexpected error")
        cleanHtml()
        print(f"The program runned into the error: {e}")
        return "-"

def getPercTenHoldings(tenHoldingsString: str, language: str, singleFunctionCall: bool) -> list[str]:
        # Getting the percentage of the first 10 participations and the total number of holdings of the ETF
    try:
        if singleFunctionCall: #Getting the correct data to parse in case of the call of the single function
            for x in range(len(tenHoldingsString) - USELESS_DATA -1):
                if splitHashMap[language][0] in tenHoldingsString[x + USELESS_DATA]:
                    tenHoldingsString = tenHoldingsString[x + USELESS_DATA]
                    print("DEBUG: Holdings data found")
                    break

        split = tenHoldingsString.split("<div>")
        split = split[3].split("</span>")
        split = split[0].split("<")
        nHoldings = split[0].replace(splitHashMap[language][5], "")
        percTenHoldings = split[4].replace("span>", "")
        cleanHtml()
        return [nHoldings, percTenHoldings]
    except Exception as e:
        print("The program runned into an unexpected error")
        cleanHtml()
        print(f"The program runned into the error: {e}")
        return ["-"]

def getHoldingsData(sHolding: str, language: str, singleFunctionCall: bool) -> list[str]:
    holdings = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # len=20, max number of holdings shown on JustETF is 10
    flagState = 0
    try:
        if singleFunctionCall: #Getting the correct data to parse in case of the call of the single function
            for x in range(len(sHolding) - USELESS_DATA -1):
                if splitHashMap[language][2] in sHolding[x + USELESS_DATA]:
                    if flagState == 0:
                        flagState = 1
                    else:
                        sHolding = sHolding[x + USELESS_DATA]
                        print("DEBUG: State data found")

            sHolding = sHolding.split(splitHashMap[language][2])
            sHolding = sHolding[0].split("<td>")
        
        for n in range(len(sHolding) - 1):
            if n % 2 == 0:
                holdings[n] = sHolding[n + 1].split("\"")
                holdings[n] = holdings[n][3]
                print(f"DEBUG: {holdings[n]}")
            else:
                holdings[n] = sHolding[n + 1].split("<span>")
                holdings[n] = holdings[n][1].split("<")
                holdings[n] = holdings[n][0]
                print(f"DEBUG: {holdings[n]}")
        #debug(holdings)
        cleanHtml()
        return holdings
    except Exception as e:
        print("The program runned into an unexpected error")
        cleanHtml()
        print(f"The program runned into the error: {e}")
        return ["-"]

def getCountriesData(sCountries: str, language: str, singleFunctionCall: bool) -> list[str]:
    countries = ["", "", "", "", "", "", "", "", "", ""]  # len=10, max number of countries shown on JustETF is 5
    flagState = 0

    try:
        if singleFunctionCall: #Getting the correct data to parse in case of the call of the single function
            for x in range(len(sCountries) - USELESS_DATA -1):
                if splitHashMap[language][2] in sCountries[x + USELESS_DATA]:
                    if flagState == 0:
                        flagState = 1
                    else:
                        sCountries = sCountries[x + USELESS_DATA]
                        print("DEBUG: State data found")

            split1 = sCountries.split(splitHashMap[language][2])
            sCountries = split1[1]
            sCountries = sCountries.split(splitHashMap[language][3])
            sCountries = sCountries[0].split(splitHashMap[language][4])
            sCountries = sCountries[0]
            sCountries = sCountries.split("<td>")

        print("\nDEBUG: Collecting countries data\n")
        for n in range(len(sCountries) - 1):
            if n % 2 == 0:
                countries[n] = sCountries[n + 1].replace("</td>", "")
                print(f"DEBUG: {countries[n]}")
            else:
                countries[n] = sCountries[n + 1].split("<span>")
                countries[n] = countries[n][1].split("<")
                countries[n] = countries[n][0]
                print(f"DEBUG: {countries[n]}")
        #debug(countries)
        cleanHtml()
        return countries
    except Exception as e:
        print("The program runned into an unexpected error")
        cleanHtml()
        print(f"The program runned into the error: {e}")
        return ["-"]

def getSectorsData(sSectors: str, language: str, singleFunctionCall: bool) -> list[str]:
    sectors = ["", "", "", "", "", "", "", "", "", ""]  # len=10, max number of sectors shown on JustETF is 5
    flagState = 0

    try:
        if singleFunctionCall: #Getting the correct data to parse in case of the call of the single function
            for x in range(len(sSectors) - USELESS_DATA -1):
                if splitHashMap[language][2] in sSectors[x + USELESS_DATA]:
                    if flagState == 0:
                        flagState = 1
                    else:
                        sSectors = sSectors[x + USELESS_DATA]
                        print("DEBUG: Sectors data found")
                        break

            split1 = sSectors.split(splitHashMap[language][2])
            split1 = split1[1]
            split1 = split1.split(splitHashMap[language][3])
            sSectors = split1[1].split(splitHashMap[language][4])
            sSectors = sSectors[0]
            sSectors = sSectors.split("<td>")

        print("\nDEBUG: Collecting sectors data\n")
        for n in range(len(sSectors) - 1):
            if n % 2 == 0:
                sectors[n] = sSectors[n + 1].replace("</td>", "")
                print(f"DEBUG: {sectors[n]}")
            else:
                sectors[n] = sSectors[n + 1].split("<span>")
                sectors[n] = sectors[n][1].split("<")
                sectors[n] = sectors[n][0]
                print(f"DEBUG: {sectors[n]}")
        #debug(sectors)
        cleanHtml()
        return sectors
    except Exception as e:
        print("The program runned into an unexpected error")
        cleanHtml()
        print(f"The program runned into the error: {e}")
        return ["-"]

def getGeneralInformations(sInformations: str, language: str, singleFunctionCall: bool) -> list[str]:
    finalData = ["","","","","","","","","","","","","","","",""]
    try:
        if singleFunctionCall: #Getting the correct data to parse in case of the call of the single function
            for x in range(len(sInformations) - USELESS_DATA -1):
                if splitHashMap[language][1] in sInformations[x + USELESS_DATA]:
                        sInformations = sInformations[x + USELESS_DATA]
                        print("DEBUG: General data found")
                        break
                    
        print("\nDEBUG: Collecting ETF general data\n")
        sInformations = sInformations.split(splitHashMap[language][6])
        #debug(sInformations)

        #Italian and english HTML have a different formatting
        if language == "it":
            sInformations = sInformations[2].split("</tbody>")
        elif language == "en":
            sInformations = sInformations[1].split("</tbody>")

        sInformations = sInformations[0].split("td")
        sInformationsBackup = sInformations
        count = 0

        # Getting all the general data of the ETF
        for i in range(int((len(sInformations)-1)/4)):
            sInformations = sInformationsBackup
            split = sInformations[(i*4)+3].split(">")

            if len(split) > 2: # The wanted data are at the index 2 or 1 in case the index 2 does not exists
                data = split[2].split("<")
            else:
                data = split[1].split("<")

            if count == 2: # Index 2 contains the ETF total value but the sring is " EUR 76.120 mln " so you need to delate the first " "
                listData = list(data[0])
                listData[0] = ""
                listData[len(listData) - 1] = ""
                finalData[count] = "".join(listData)
            else:
                finalData[count] = data[0]
            print(f"DEBUG: \"{finalData[count]}\"")
            count += 1
        cleanHtml()
        return finalData
    except Exception as e:
        print("The program runned into an unexpected error")
        cleanHtml()
        print(f"The program runned into the error: {e}")
        return ["-"]

########################################################################################## scraping all data using the functions

def scrape(myISIN: str, myLanguage: str) -> str:
    print("\n---------------------------------------------------------------------------")

    # Initialize htmlDataiables for extracting ETF data
    stateAndSectorData = ""
    firstTenHoldings = ""
    generalData = ""
    ticker = ""
    name = ""
    flagData = 0
    flagHoldings = 0
    flagName = 0 
    flagState = 0
    flagTicker = 0
    callFlag = False
    ##########################################################################################
    # Basic error handling and data download
    # URL composition and HTML download
    try:

        htmlData = getFile(myISIN, myLanguage)
        if htmlData != -1: #Case where both language and ISIN are good
            isin = myISIN.upper() # The ISIN letters are allways uppercase
            language = myLanguage.lower()  # Making the script not case-sensitive
        else:
            return -1

    ##########################################################################################
    # Finding the correct lines with the data by cycling through all the rows in the HTML file
        flagState = 0
        for x in range(len(htmlData) - USELESS_DATA):

            if flagName == 1 and flagData == 1 and flagHoldings == 1 and flagTicker == 1 and flagState == 1:
                print("DEBUG: All data found")
                break

            if "<title>" in htmlData[x + USELESS_DATA]:
                name = htmlData[x + USELESS_DATA]
                print("\nDEBUG: Title found")
                flagName = 1

            if splitHashMap[language][0] in htmlData[x + USELESS_DATA]:
                firstTenHoldings = htmlData[x + USELESS_DATA]
                print("DEBUG: Holdings data found")
                flagHoldings = 1

            if splitHashMap[language][1] in htmlData[x + USELESS_DATA]:
                generalData = htmlData[x + USELESS_DATA]
                print("DEBUG: General data found")
                flagData = 1

            if splitHashMap[language][2] in htmlData[x + USELESS_DATA]:
                if flagState == 0:
                    flagState = 1
                else:
                    stateAndSectorData = htmlData[x + USELESS_DATA]
                    print("DEBUG: State data found")

        ticker = getTicker(name, callFlag)
        name = getName(name, callFlag)

        # Getting countries, sectors and holdings data from the "stateAndSectorData" string
        if flagState == 1:
            print("\nDEBUG: Collecting holdings data\n")
            # Getting the right data by parsing the original string
            splitholdings = stateAndSectorData.split(splitHashMap[language][2])
            splitCountries = splitholdings[1]
            splitCountries = splitCountries.split(splitHashMap[language][3])
            splitSectors = splitCountries[1].split(splitHashMap[language][4])
            splitCountries = splitCountries[0].split(splitHashMap[language][4])
            splitCountries = splitCountries[0]
            splitSectors = splitSectors[0]
            splitholdings = splitholdings[0].split("<td>")
            splitCountries = splitCountries.split("<td>")
            splitSectors = splitSectors.split("<td>")

            arrHoldings = getHoldingsData(splitholdings, language, callFlag)
            arrCountries = getCountriesData(splitCountries, language, callFlag)
            arrSectors = getSectorsData(splitSectors, language, callFlag)

            #Formatting the countries and sectors data correctly
            sCountries = ""
            for i, s in enumerate(arrCountries):
                if s == "": break
                if i % 2 == 0:
                    sCountries += f"\"{s}\": "
                    i += 1
                else:
                    sCountries += f"{s}, "
                    i += 1

            sSectors = ""
            for i, s in enumerate(arrSectors):
                if s == "": break
                if i % 2 == 0:
                    sSectors += f"\"{s}\": "
                    i += 1
                else:
                    sSectors += f"{s}, "
                    i += 1
            listName = list(sSectors)
            listName[len(sSectors) - 2] = ""
            sSectors = "".join(listName)
            listName = list(sCountries)
            listName[len(sCountries) - 2] = ""
            sCountries = "".join(listName)

        else: # Some ETFs may not contain the data about holdings, countries and sectors on the JustETF page
            sCountries = dataNotFoundHashMap[language][0]
            sSectors = dataNotFoundHashMap[language][0]

        if flagHoldings:
            HoldingsData = getPercTenHoldings(firstTenHoldings, language, callFlag)
            nHoldings = HoldingsData[0]
            percTenHoldings = HoldingsData[1]
        else: # Some ETFs may not contain the data about number of holdings and percentage of the first 10 holdings on the JustETF page
            nHoldings = "-"
            percTenHoldings = "-"

        finalGeneralData = getGeneralInformations(generalData, language, callFlag)

        ###########################################################################################
        # Output data formatting
        outputString = ""
        outputString += (f"ETF: {name}, Ticker: \"{ticker}\", ISIN: {isin}\n")
        outputString += (f"{outputHashMap[language][1]} {nHoldings}{outputHashMap[language][2]} {percTenHoldings}\n\n")

        if flagHoldings == 1:
            outputString += (f"{outputHashMap[language][3]}\n")
            for i in range(int(len(arrHoldings)/2)):
                outputString += (f"{outputHashMap[language][6]}: {arrHoldings[i*2]} {outputHashMap[language][7]} {arrHoldings[i*2+1]}\n")
        else:
             outputString += (f"{dataNotFoundHashMap[language][1]}\n")

        outputString += (f"\n{outputHashMap[language][4]} {sCountries}\n")
        outputString += (f"{outputHashMap[language][5]} {sSectors}\n\n")
        outputString += (f"{generalDataHashMap[language][len(generalDataHashMap[language])-1]}\n")
        for i in range(len(finalGeneralData)):
            outputString += (f"{generalDataHashMap[language][i]}: {finalGeneralData[i]}\n")

        #Final print for debug purposes
        print("\n---------------------------------------------------------------------------\nDEBUG:")
        print(f"{outputHashMap[language][0]} \n")
        print(outputString)
        # End of the final print debug

        cleanHtml() #Cleaning the file
        return outputString

    except Exception as e:
        print(f"\nERROR: Unexpected error occoured, please verify the ISIN and retry")
        # Unomment this out show the error that caused the program to fail
        print(f"DEBUG: The error the program runned in is \"{e}\"\n")
        # All errors are likely caused by the non-existence of the inserted ISIN.
        print("---------------------------------------------------------------------------\n")
        cleanHtml()
        return -1

###########################################################################################
# Main function
if __name__ == "__main__":

    htmlFilePath = f"resources/etf.html"
    # To successfully call the function, insert the ISIN as the first parameter and the language as the second parameter.
    # The only two languages supported at the moment are Italian (IT) and English (EN).
    # The function returns -1 in case of an error and returns the data if the process succeeds.

    t1 = time.time()
    ack = scrape("IE00B4L5Y983", "it") #Case language selected: Italian
    t2 = time.time()
    ack = scrape("IE00B4L5Y983", "en") #Case language selected: English
    t3 = time.time()
    ack = scrape("IE00B4ND3602", "it") #Case language selected: Italian, ETF with missing data
    t4 = time.time()
    ack = scrape("IE00B4ND3602", "en") #Case language selected: English, ETF with missing data
    t5 = time.time()
    ack = scrape("IE00B4L5Y983", "de") #Case language selected not implemented
    t6 = time.time()
    ack = scrape("IEY983", "en") #Case ISIN not in the right format
    t7 = time.time()
    ack = scrape("IE69B4L5Y983", "en") #Case not existing ISIN, "IE69B4L5Y983" does not exists
    t8 = time.time()

    print(f"\nDEBUG: Full page, language selected \"it\": {t2-t1}s")
    print(f"DEBUG: Full page, language selected \"en\": {t3-t2}s")
    print(f"DEBUG: Missing data, language selected \"it\": {t4-t3}s")
    print(f"DEBUG: Missing data, language selected \"en\": {t5-t4}s")
    print(f"DEBUG: Error type \"Language not implemented\": {t6-t5}s")
    print(f"DEBUG: Error type \"ISIN not in the right format\": {t7-t6}s")
    print(f"DEBUG: Error type \"The current ISIN does not exist\": \"en\": {t8-t7}s")

    ###########################################################################################

    # Debug and example on how to use the functions to get single datas:

    language = "it"
    isin = "IE00B4L5Y983"
    t1 = time.time()
    htmlFile = getFile(isin, language) # Getting the html file to parse
    t2 = time.time()
    name = getName(htmlFile, True) # Getting the name
    t3 = time.time()
    ticker = getTicker(htmlFile, True) # Getting the ticker
    t4 = time.time()
    generalData = getGeneralInformations(htmlFile, language, True) #Getting all the general data as an array
    t5 = time.time()
    tenHold = getPercTenHoldings(htmlFile, language, True) # Getting the data relevant to the number and percentage of holdings of the ETF
    t6 = time.time()
    holdingsData = getHoldingsData(htmlFile, language, True) # Returns all the data of the Holdings as an array
    t7 = time.time()
    sectorsData =  getSectorsData(htmlFile, language, True) # Returns all the data of the sectors as an array
    t8 = time.time()
    countriesData = getCountriesData(htmlFile, language, True) # Returns all the data of the countries as an array
    t9 = time.time()
    totaleScarp = scrape(isin, language) # Getting all the data and a formatted output string to return
    t10 = time.time()

    # Printing the time usage of all the functions

    print(f"\nDEBUG: Time to get the file: {t2-t1}")
    print(f"DEBUG: Time to get name: {t3-t2}")
    print(f"DEBUG: Time to get ticker: {t4-t3}")
    print(f"DEBUG: Time to get the general data: {t5-t4}")
    print(f"\nDEBUG: Time to get the ten holdings data: {t6-t5}")
    print(f"DEBUG: Time to get holdings data: {t7-t6}")
    print(f"DEBUG: Time to get sectors data: {t8-t7}")
    print(f"DEBUG: Time to get the countries data: {t9-t8}")
    print(f"DEBUG: Time to get the total scarp: {t10-t9}")
    print("\n")
    cleanHtml()
    ack = scrape("IE00B4L5Y983", "it") #Case language selected: Italian