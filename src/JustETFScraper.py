import os
from urllib.request import urlretrieve
from os import listdir
from os.path import isfile, join

# Data scraping program for the JustETF site
# This application collects data by downloading the HTML file from the site and parsing it.
# Author: Niccolò Quadrani
# Date: 01/10/2024

def scraper(myISIN, myLanguage):
    print("\n---------------------------------------------------------------------------")

    # Hash map used to manage multiple languages and data sets within a single script.
    splitHashMap = {"en": ["Top 10 Holdings", "The Total Expense Ratio (TER)", "Countries", "Sectors", "Show more", "out of "], 
                      "it": ["Prime 10 partecipazioni", "Indicatore sintetico di spesa (TER)", "Paesi", "Settori", "Mostra di più", "su "]}
    
    # Hash map to manage multiple languages in the output
    outputHashMap = {"en": ["FINAL DATA:", "Number of holdings:", ", the percentage of the top 10 holdings within the ETF:", 
                              "The holdings to which the ETF is most exposed are:", "The countries to which the ETF is most exposed are:", 
                              "The sectors to which the ETF is most exposed are:"],
                       "it": ["DATI FINALI:", "Numero di partecipazioni:", ", la percentuale delle prime 10 partecipazioni dell'ETF è:", 
                              "Le partecipazioni alle quali l'ETF è maggiormente esposto sono:", 
                              "Gli stati ai quali l'ETF è maggiormente esposto sono:", "I settori ai quali l'ETF è maggiormente esposto sono:"]}
    
    # Initialize htmlDataiables for extracting ETF data
    USELESS_DATA = 170 #Before rr. 170 the HTML file never contains informations
    stateAndSectorData = ""
    firstTenPartecipations = ""
    generalData = ""
    ticker = ""
    name = ""
    flagData = 0
    flagPartecipation = 0 
    flagName = 0 
    flagState = 0
    flagTicker = 0
    holdings = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # len=20, max number of holdings shown on JustETF is 10
    states = ["", "", "", "", "", "", "", "", "", ""]  # len=10, max number of states shown on JustETF is 5
    sectors = ["", "", "", "", "", "", "", "", "", ""]  # len=10, max number of sectors shown on JustETF is 5
    
    ##########################################################################################
    # Basic error handling and data download
    # URL composition and HTML download
    try:
        isin = myISIN
        language = myLanguage.lower()  # Making the script not case-sensitive
        supported_languages = ["en", "it"] #List of the implemented languages 
        
        if language not in supported_languages:
            print("\nERROR: The selected language is not implemented yet")
            return -1
        
        if len(myISIN) != 12:
            print("\nERROR: Bad ISIN format, please check the ISIN code")
            return -1
        
        # Getting the correct link
        url = f"https://www.justetf.com/{language}/etf-profile.html?isin={isin}#overview"
        htmlFilePath = "resources\etf.html"
        
        # Downloading the HTML from the site
        urlretrieve(url, htmlFilePath)
        htmlFilePath, headers = urlretrieve(url, htmlFilePath)
        print(f"\nDEBUG: Success! ETF data downloaded to \"{htmlFilePath}\"")

        # Opening and reading the downloaded file
        with open(htmlFilePath, 'r', encoding="utf8") as file:
            htmlData = file.read()
        
        ##########################################################################################
        # Data handling
        data = htmlData.split("\n")
        # Finding the correct lines with the data by cycling through all the rows in the HTML file
        flagState = 0
        for x in range(len(data) - USELESS_DATA):
            
            if flagName == 1 and flagData == 1 and flagPartecipation == 1 and flagTicker == 1 and flagState == 1:
                print("DEBUG: All data found")
                break
            
            if "<title>" in data[x + USELESS_DATA]:
                name = data[x + USELESS_DATA]
                print("\nDEBUG: Title found")
                flagName = 1
                
            if splitHashMap[language][0] in data[x + USELESS_DATA]:
                firstTenPartecipations = data[x + USELESS_DATA]
                print("DEBUG: Holdings data found")
                flagPartecipation = 1
                
            if splitHashMap[language][1] in data[x + USELESS_DATA]:
                generalData = data[x + USELESS_DATA]
                print("DEBUG: General data found")
                flagData = 1
                
            if splitHashMap[language][2] in data[x + USELESS_DATA]:
                if flagState == 0:
                    flagState = 2
                else:
                    stateAndSectorData = data[x + USELESS_DATA]
                    print("DEBUG: State data found")
                    flagState = 1
                    
            if "Ticker" in data[x + USELESS_DATA] and flagTicker == 0:
                flagTicker = 1
                ticker = data[x + USELESS_DATA]
                print("DEBUG: Ticker found")

        # Getting the Ticker from the "name" string that contains both Name and Ticker of the ETF
        split = name.split("</title>")
        split = split[0].split("|")
        ticker = split[1].replace(" ", "")

        # Getting the Name of the ETF from the "name" string 
        split = name.split("</title>")
        split = split[0].split("|")
        name = split[0].replace("<title>", "")
        listName = list(name)
        listName[len(name) - 1] = ""
        name = "".join(listName)

        # Getting states, sectors and holdings data from the "stateAndSectorData" string
        if flagState == 1:
            print("\nDEBUG: Collecting holdings data\n")
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
            
            for n in range(len(splitholdings) - 1):
                if n % 2 == 0:
                    holdings[n] = splitholdings[n + 1].split("\"")
                    holdings[n] = holdings[n][3]
                    print(f"DEBUG: {holdings[n]}")
                else:
                    holdings[n] = splitholdings[n + 1].split("<span>")        
                    holdings[n] = holdings[n][1].split("<")
                    holdings[n] = holdings[n][0]
                    print(f"DEBUG: {holdings[n]}")
                    
            print("\nDEBUG: Collecting countries data\n")
            for n in range(len(splitCountries) - 1):
                if n % 2 == 0:
                    states[n] = splitCountries[n + 1].replace("</td>", "")
                    print(f"DEBUG: {states[n]}")
                else:
                    states[n] = splitCountries[n + 1].split("<span>")
                    states[n] = states[n][1].split("<")
                    states[n] = states[n][0]
                    print(f"DEBUG: {states[n]}")
                    
            print("\nDEBUG: Collecting sectors data\n")       
            for n in range(len(splitSectors) - 1):
                if n % 2 == 0:
                    sectors[n] = splitSectors[n + 1].replace("</td>", "")
                    print(f"DEBUG: {sectors[n]}")
                else:
                    sectors[n] = splitSectors[n + 1].split("<span>")
                    sectors[n] = sectors[n][1].split("<")
                    sectors[n] = sectors[n][0]
                    print(f"DEBUG: {sectors[n]}")
                
        # Getting the percentage of the first 10 participations and the total number of holdings of the ETF
        split = firstTenPartecipations.split("<div>")
        split = split[3].split("</span>")
        split = split[0].split("<")
        nHoldings = split[0].replace(splitHashMap[language][5], "")
        percTenHoldings = split[4].replace("span>", "")
        
        # Formatting the output string with all the percentages  
        sholdings = ""
        i = 0
        for s in holdings:
            if s != "":
                if i % 2 == 0:
                    sholdings += f"\"{s}\": "
                    i += 1
                else:
                    sholdings += f"{s}, "
                    i += 1
            else:
                break
            
        sStates = ""
        i = 0
        for s in states:
            if s != "":
                if i % 2 == 0:
                    sStates += f"\"{s}\": "
                    i += 1
                else:
                    sStates += f"{s}, "
                    i += 1
            else:
                break
            
        sSectors = ""
        i = 0
        for s in sectors:
            if s != "":
                if i % 2 == 0:
                    sSectors += f"\"{s}\": "
                    i += 1
                else:
                    sSectors += f"{s}, "
                    i += 1
            else:
                break

        ########################################################################################### 
        # Print of the final data
        print("\n---------------------------------------------------------------------------\n")
        # Final debug with print
        print(f"{outputHashMap[language][0]} \n")
        print(f"ETF: {name}, Ticker: \"{ticker}\", ISIN: {isin}\n")
        print(f"{outputHashMap[language][1]} {nHoldings}{outputHashMap[language][2]} {percTenHoldings}\n")   
        print(f"{outputHashMap[language][3]} {sholdings}\n")
        print(f"{outputHashMap[language][4]} {sStates}\n")
        print(f"{outputHashMap[language][5]} {sSectors}\n")
        print("---------------------------------------------------------------------------\n")
        
        # Open the file in write mode to overwrite it with an empty string to clean the html
        if os.path.exists(htmlFilePath):
            with open(htmlFilePath, 'w', encoding="utf8") as file:
                file.write("")
        return 0
    
    except Exception as e:
        print(f"\nERROR: Unexpected error occoured, please verify the ISIN and retry (Error: {e})\n")
        print("---------------------------------------------------------------------------\n")
        return -1
        
###########################################################################################
# Main function

# To successfully call the function, insert the ISIN as the first parameter and the language as the second parameter.
# The only two languages supported at the moment are Italian (IT) and English (EN).
# The function returns -1 in case of an error and returns 0 if the process succeeds.

scraper("IE00B4L5Y983", "it") #Case language selected: Italian
scraper("IE00B4L5Y983", "en") #Case language selected: English
scraper("IE00B4L5Y983", "de") #Case language selected not implemented
scraper("IEY983", "en") #Case ISIN not in the right format
scraper("IE69B4L5Y983", "en") #Case not existing ISIN

