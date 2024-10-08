# **Python-Just-ETF-Scraper**
This program is a web scraper for the JustETF website, developed in Python. <br>
It downloads the HTML page of a selected ETF using its ISIN and then parses it to extract key data. <br>
The program is entirely open-source and can be used to implement APIs, however, it is not highly time-efficient, and the execution time may vary due to several factors, the time required to collect all the data ranges from 1 to 5 seconds.
The program was originally written with the intention of transforming it into a Telegram bot in the future. <br>
There are two versions of the software: one in Italian and one in English. Only these two languages are currently supported. However, the program is designed in a way that allows easy adaptation to other languages, to do so, simply modify the parsing strings accordingly.

## Recommendations 
- Ensure that Python v3.12.7 or higher is installed for optimal performance.
- When implementing, use individual data-handling functions instead of the "scraper" function to improve execution time.

## Currently supported features
- Downloading the HTML file with the correct data from JustETF
- Parsing the HTML and extracting all relevant data for a given ETF’s ISIN
- Support for both English and Italian pages, with customized output for each language

## Issues
- Unfortunately, it's not possible to determine if an ISIN exists or not. If the ISIN does not exist, the program will encounter a general error.
- It is not possible, at the moment, to search for a product without knowing the ISIN (it’s impossible to search using only the ticker).

## Execution time of all cases before the program returns
(Ryzen 7 5800H, 16GB DDR4 3200MHz, 30Mbps download speed):
- Case: Full page, language selected "it" = 1.317s
- Case: Full page, language selected "en" = 1.281s
- Case: Missing data, language selected "it" = 1.280s
- Case: Missing data, language selected "en" = 1.665s
- Case: Error type "Language not implemented" = 0.000s
- Case: Error type "ISIN bad format" = 0.001s
- Case: Error type "ISIN not existing" = 1.408s
- Case: getName(file, True) function called = 0.001s
- Case: getPercTenHoldings(file, language, True) function called = 0.001s
- Case: getGeneralInformations(file, language, True) function called = 0.001s
- Case: getTicker(tickerString, singleFunctionCall) function called = 0.001s
