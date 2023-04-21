"""
Module Name:    Webscrapping routine for Germany - Frankfurter Allgemeine Zeitung
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  April 19th, 2023
Description:    This module contains the code needed for webscrapping the head titles and descriptions of all the news
                contained in the Politics section of the Frankfurter Allgemeine Zeitung: https://www.faz.net/aktuell/politik/inland/s1.html#teaserPagination.
Newest new:     April 21st, 2023
Robots.txt:     Yes, allowed according to https://www.faz.net/robots.txt
"""

# Required libraries
import time 
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Defining headers
agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]
headers = {
    "User-Agent": "".join(agent)
}

# Root URL 
root_url = "https://www.faz.net/aktuell/politik/inland/"

# General info
source   = "Frankfuter Allgemeine"
country  = "Germany"

# Defining an empty list to store the results of the provided URL
results = []

# Defining fetch/parse function to be used in the forthcoming loop
def getArticleInfo(thread):
        
    # We first identify the article relevant container
    cntr  = (thread
             .find("article")
             .find("div", class_ = "tsr-Base_TextWrapper")
             .find("div", class_ = "tsr-Base_ContentWrapper")
             .find("div"))

    # Then, we can target variables
    title = (cntr
             .find("a")
             .find("header")
             .find("h2")
             .find("span", class_ = "tsr-Base_HeadlineText")
             .text.strip())
    desc  = (cntr
             .find("div", class_ = "tsr-Base_Content")
             .text.strip())
    link  = (cntr
             .find("a")
             .get("href"))

    # Defining dictionary entry
    dct = {
        "country"     : country,
        "source"      : source,
        "title"       : title,
        "description" : desc,
        "URL"         : link
        }

    return dct

# Applying the scrapper function to the Politics section of LeMonde
for page in range(1,21):
    
    # Target page URL
    target_url = root_url + f"s{page}.html#teaserPagination"

    # Fetching/parsening
    root_response = requests.get(target_url, headers = headers)
    root_soup     = BeautifulSoup(root_response.text, "lxml")
    time.sleep(2)

    # Identifying the containers that lists all the news articles from the politics section
    target_containers = root_soup.findAll("ul", class_ = "lst-Teaser")

    # Extracting information
    for block in target_containers:
        for article in block.findAll("li", class_ = "lst-Teaser_Item"):
            article_info = getArticleInfo(article)
            results.append(article_info)

# Saving data into a dataframe  
batch = datetime.date.today()  
path4saving = os.path.join(os.path.dirname(__file__), 
                           '..',
                           "Data",
                           "News-Headlines", 
                           f"DE_frankfuter_{batch}.csv")
master_data = pd.DataFrame(results)
master_data.to_csv(path4saving, index = False, encoding = "utf-8")