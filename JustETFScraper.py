from urllib.request import urlretrieve
from os import listdir
from os.path import isfile, join

#Data scalping program of the JustETF site
#This application collects data by downloading the html file on the site and doing a parsing
#Author: Niccolò Quadrani
#Date:01/10/2024

#Data Handling variables
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
company = ["","","","","","","","","","","","","","","","","","","",""]
states = ["","","","","","","","","",""]
sectors = ["","","","","","","","","",""]

#Url composition and HTML download
isin = "IE00B4L5Y983"
url = (f"https://www.justetf.com/it/etf-profile.html?isin={isin}#panoramica")
path = "C:/Users/niccoloq/OneDrive - Ars Srl/Desktop/FinanceDrips/etf.html"
urlretrieve(url, path)
path, headers = urlretrieve(url, path)
print(f"\nSuccess! ETF Datas downloaded inside the path \"{path}\"")
##########################################################################################

#Basic split with each row of the PDF
file = open(path, encoding="utf8")
var = file.read()
data=var.split("\n")
##########################################################################################

#Finding the correct lines with the datas
for x in range(len(data)-170):
    if flagName == 1 and flagData == 1 and flagPartecipation == 1 and flagTicker == 1 and flagState == 1:
        print("All the datas was found")
        break
    if "<title>" in data[x+170]:
        name = data[x+170]
        print("\nTitle found")
        flagName = 1
        continue
    if "Prime 10 partecipazioni" in data[x+170]:
        firstTenPartecipations = data[x+170]
        print("Holdings data found")
        flagPartecipation = 1
    if "Indicatore sintetico di spesa (TER)" in data[x+170]:
        generalData = data[x+170]
        print("General datas found")
        flagData = 1
        continue
    if "Paesi" in data[x+170]:
        if flagState == 0:
            flagState = 2
            continue
        else:
            stateAndSectorData = data[x+170]
            print("States datas found")
            flagState = 1
            continue
    if "Ticker" in data[x+170] and flagTicker == 0:
        flagTicker = 1
        ticker = data[x+170]
        print("Ticker found")
        continue
##########################################################################################

#Getting the Ticker from the "name" string that contains both Name and Ticker of the ETF
split = name.split("</title>")
split = split[0].split("|")
ticker = split[1].replace(" ", "")
##########################################################################################

#Getting the Name of the ETF from the "name" string 
split = name.split("</title>")
split = split[0].split("|")
name = split[0].replace("<title>", "")
listName = list(name)
listName[len(name)-1] = ""
name = "".join(listName)
##########################################################################################

#Getting states, sectors and company datas from the "stateAndSectorData" string
if flagState == 1:
    print("\nCollecting company datas\n")
    splitAziende = stateAndSectorData.split("Paesi")
    splitPaesi = splitAziende[1]
    splitPaesi = splitPaesi.split("Settori")
    splitSettori = splitPaesi[1].split("Mostra di più")
    splitPaesi = splitPaesi[0].split("Mostra di più")
    splitPaesi = splitPaesi[0]
    splitSettori = splitSettori[0]
    splitAziende = splitAziende[0].split("<td>")
    splitPaesi = splitPaesi.split("<td>")
    splitSettori = splitSettori.split("<td>")
        
    for n in range(len(splitAziende)-1):
        if n%2 == 0:
            company[n] = splitAziende[n+1].split("\"")
            company[n] = company[n][3]
            print(company[n])
        else:
            company[n] = splitAziende[n+1].split("<span>")
            company[n] = company[n][1].split("<")
            company[n] = company[n][0]
            print(company[n])
            
    for n in range(len(splitPaesi)-1):
        if n%2 == 0:
            states[n] = splitPaesi[n+1].replace("</td>", "")
            print(states[n])
        else:
            states[n] = splitAziende[n+1].split("<span>")
            states[n] = states[n][1].split("<")
            states[n] = states[n][0]
            print(states[n])
            
    for n in range(len(splitSettori)-1):
        if n%2 == 0:
            sectors[n] = splitSettori[n+1].replace("</td>", "")
            print(sectors[n])
        else:
            sectors[n] = splitSettori[n+1].split("<span>")
            sectors[n] = sectors[n][1].split("<")
            sectors[n] = sectors[n][0]
            print(sectors[n])
##########################################################################################
          
#Getting the percentage of the first 10 partecipations and the total number of the holdings of the ETF
split = firstTenPartecipations.split("<div>")
split = split[3].split("</span>")
split = split[0].split("<")
nHoldings = split[0].replace("su ", "")
percTenHoldings = split[4].replace("span>", "")
    
sCompany = ""
i = 0
for s in company:
    if s != "":
        if i%2 == 0:
            sCompany += f"\"{s}\": "
            i+=1
        else:
            sCompany += f"{s}, "
            i+=1
    else:
        break
      
sStates = ""
i = 0
for s in states:
    if s != "":
        if i%2 == 0:
            sStates += f"\"{s}\": "
            i+=1
        else:
            sStates += f"{s}, "
            i+=1
    else:
        break
    
sSectors = ""
i = 0
for s in sectors:
    if s != "":
        if i%2 == 0:
            sSectors += f"\"{s}\": "
            i+=1
        else:
            sSectors += f"{s}, "
            i+=1
    else:
        break
###########################################################################################

#Final debug with print
print("\nFINAL DEBUG: \n")
print(f"ETF: {name}, Ticker: \"{ticker}\", ISIN: {isin}\n")
print(f"Holdings number: {nHoldings}, first 10 holdings percentage: {percTenHoldings}\n")   
print(f"Companies in the ETF: {sCompany}\n")
print(f"States of the ETF: {sStates}\n")
print(f"Sectors of the ETF: {sSectors}\n")
###########################################################################################

generalData = generalData.split("Nozioni di base")
generalData = generalData[2]