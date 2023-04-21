"""
Module Name:    Webscrapping routine for France - Le Monde
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  April 19th, 2023
Description:    This module contains the code needed for webscrapping the head titles and descriptions of all the news
                contained in the Politics section of the Le Monde Newspaper: https://www.lemonde.fr/politique/.
Newest new:     April 20th, 2023
Robots.txt:     Yes, allowed according to https://www.lemonde.fr/robots.txt
"""

# Required libraries 
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
root_url = "https://www.lemonde.fr/politique/"

# General info
source   = "LeMonde"
country  = "France"

# Defining an empty list to store the results of the provided URL
results = []

# Defining fetch/parse function to be used in the forthcoming loop
def getArticleInfo(thread):
        
    # We first identify the article relevant container
    cntr  = thread.find("section").find("a")

    # Then, we can target variables
    title = cntr.find("h3", class_ = "teaser__title").text.strip()
    desc  = cntr.find("p", class_ = "teaser__desc").text.strip()
    link  = cntr.get("href")

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
for page in range(1,3):
    
    # Target page URL
    target_url = root_url + f"{page}"

    # Fetching/parsening
    root_response = requests.get(target_url, 
                                 headers = headers)
    root_soup     = BeautifulSoup(root_response.text, "lxml")

    # Identifying the container that lists all the news articles from the politics section
    target_container = root_soup.find(id = "river")

    # Extracting information
    for article in target_container.findAll("div", class_ = "thread"):
        article_info = getArticleInfo(article)
        results.append(article_info)

# Saving data into a dataframe  
batch = datetime.date.today()  
path4saving = os.path.join(os.path.dirname(__file__), 
                           '..',
                           "Data",
                           "News-Headlines", 
                           f"FR_lemonde_{batch}.csv")
master_data = pd.DataFrame(results)
master_data.to_csv(path4saving, index = False, encoding = "utf-8")




    
 


