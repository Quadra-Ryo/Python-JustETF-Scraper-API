# **Python-Just-ETF-Scraper**
This program is a web scraper for the JustETF website, developed in Python. It downloads the HTML page of a selected ETF using its ISIN and then parses it to extract key data.
The program is entirely open-source and can be used to implement APIs. However, it is not highly time-efficient to get the datas it needs ≈ 1sec
The program was originally written with the intention of transforming it into a Telegram bot in the future.
There are two versions of the software: one in Italian and one in English. Only these two languages are currently supported. However, the program is designed in a way that allows easy adaptation to other languages. 
To do so, simply modify the parsing strings accordingly.

## Currently supported features
- Downloading the HTML file with the correct data from JustETF
- Parsing the HTML and extracting all relevant data for a given ETF’s ISIN
- Support for both English and Italian pages, with customized output for each language
- 

## Issues
- Due to limited testing time, the script may encounter errors with ETFs that do not have a default page.

