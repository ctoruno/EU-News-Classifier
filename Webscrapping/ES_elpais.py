"""
Module Name:    Webscrapping routine for Spain - El Pais
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  April 20th, 2023
Description:    This module contains the code needed for webscrapping the head titles and descriptions of all the news
                contained in the Politics section of El Pais Newspaper: https://elpais.com/noticias/politica/.
Newest new:     April 20th, 2023
Robots.txt:     Yes, allowed according to https://elpais.com/robots.txt
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
root_url = "https://elpais.com/noticias/politica/"

# General info
source   = "El Pais"
country  = "Spain"

# Defining an empty list to store the results of the provided URL
results = []

# Defining fetch/parse function to be used in the forthcoming loop
def getArticleInfo(thread):

    # Then, we can target variables
    title = (thread
             .find("header", class_ = "c_h")
             .find("h2")
             .find("a").text.strip())
    desc  = (thread
             .find("p", class_ = "c_d").text.strip())
    link  = (thread
             .find("header", class_ = "c_h")
             .find("h2")
             .find("a").get("href"))

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
for page in range(0,20):
    
    # Target page URL
    target_url = root_url + f"{page}"

    # Fetching/parsening
    root_response = requests.get(target_url, 
                                 headers = headers)
    root_soup     = BeautifulSoup(root_response.text, "lxml")
    time.sleep(2)

    # Identifying the container that lists all the news articles from the politics section
    target_container = root_soup.find("div", class_ = "b-b b-au_b")

    # Extracting information
    for article in target_container.findAll("article", class_ = "c c-d c--m"):
        article_info = getArticleInfo(article)
        results.append(article_info)

# Saving data into a dataframe  
batch = datetime.date.today()  
path4saving = os.path.join(os.path.dirname(__file__), 
                           '..',
                           "Data",
                           "News-Headlines", 
                           f"ES_elpais_{batch}.csv")
master_data = pd.DataFrame(results)
master_data.to_csv(path4saving, index = False, encoding = "utf-8")