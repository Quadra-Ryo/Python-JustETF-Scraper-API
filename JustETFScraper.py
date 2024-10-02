from urllib.request import urlretrieve
from os import listdir
from os.path import isfile, join

#Data scraping program of the JustETF site
#This application collects data by downloading the html file on the site and doing a parsing
#Author: Niccolò Quadrani
#Date:01/10/2024
print("\n---------------------------------------------------------------------------")
isin = "IE00B5BMR087"
url = (f"https://www.justetf.com/it/etf-profile.html?isin={isin}#panoramica")
path = "PATH"
urlretrieve(url, path)
path, headers = urlretrieve(url, path)
print(f"DEBUG: Success! ETF Datas downloaded inside the path \"{path}\" \n")

file = open(path, encoding="utf8")
var = file.read()
data=var.split("\n")
stateAndSectorData = ""
firstTenParticipationDataAndCompanies = ""
generalData = ""
ticker = ""
nHoldings = ""
Name = ""
flagState = 0
flagTicker = 0
flagHolding = 0 
#Finding the correct lines with the datas
for x in range(len(data)-170):
    if "<title>" in data[x+170]:
        Name = data[x+170]
        print("DEBUG: Title found")
    if "Prime 10 partecipazioni" in data[x+170]:
        firstTenParticipationDataAndCompanies = data[x+170]
        print("DEBUG: Holdings data found")
    if "Indicatore sintetico di spesa (TER)" in data[x+170]:
        generalData = data[x+170]
        print("DEBUG: General datas found")
    if "partecipazioni" in data[x+170] and flagHolding == 0:
        nHoldings = data[x+170]
        flagHolding = 1
        print("DEBUG: Holdings number found")
    if "Paesi" in data[x+170]:
        if flagState == 0:
            flagState = 1
        else:
            stateAndSectorData = data[x+170]
            print("DEBUG: States datas found")
    if "Ticker" in data[x+170] and flagTicker == 0:
        flagTicker = 1
        ticker = data[x+170]
        print("DEBUG: Ticker found")
        
split = stateAndSectorData.split("<td>")
firstState = split[21].replace("</td>", "")
secondState = split[23].replace("</td>", "")
firstSector = split[25].replace("</td>", "")
secondSector = split[27].replace("</td>", "")
perc=split[22].split("<span>")
perc=perc[1].split("</span>")
firstStatePerc = perc[0]
perc=split[24].split("<span>")
perc=perc[1].split("</span>")
secondStatePerc = perc[0]
perc=split[26].split("<span>")
perc=perc[1].split("</span>")
firstSectorPerc = perc[0]
perc=split[28].split("<span>")
perc=perc[1].split("</span>")
secondSectorPerc = perc[0]

print("\nFINAL DATAS: \n")
print(f"The state with the highest participation is: \"{firstState}\" with a percentage of: {firstStatePerc}")
print(f"The state with the second highest participation is: \"{secondState}\" with a percentage of: {secondStatePerc}")
print(f"The sector with the highest participation is: \"{firstSector}\" with a percentage of: {firstSectorPerc}")
print(f"The sector with the second highest participation is: \"{secondSector}\" with a percentage of: {secondSectorPerc}")
print("---------------------------------------------------------------------------\n")


