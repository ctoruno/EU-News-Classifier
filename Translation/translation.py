"""
Module Name:    Translation routine for Nes Headlines
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  April 22nd, 2023
Description:    This module contains the code needed for translating all the webscrapped new headlines and descriptions from
                all the taargeted newspapers.
Latest:         May 4th, 2023
"""
# Immporting rquired libraries
from google.cloud import translate_v3 as translate
import os
import math
import numpy as np
import pandas as pd

# Load data
path2data  = os.path.join(os.path.dirname(__file__), 
                          "..",
                          "Data/News-Headlines/")
path2files = [path2data + x
              for x in os.listdir(path2data)]
CSVfiles   = [pd.read_csv(x) 
              for x in path2files]
master_data = pd.concat(CSVfiles)

# Set up the credentials
path2creds = os.path.join(os.path.dirname(__file__), 
                          '../..',
                          "API-keys",
                          "eu-news-classifier-4e899c829c3f.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path2creds

# Set up the client
client = translate.TranslationServiceClient()
parent = "projects/893319515159/locations/global"

# List of countries:
cntrs = master_data.country.unique().tolist()

# Defining a translation request function
def requestTrans(data, targetColumn, sourceLang, colName):

    # Extracting target column as list
    extracted_text = data[targetColumn].tolist()

    # Google only allows a maximum of 30,000 characters per request. 
    # Therefore, we need to split the target text into chunks

    # Defining number of chunks to divide the target text in
    total_chrs = sum([len(str(x)) for x in extracted_text])
    nchunks    = math.ceil(total_chrs/30000)

    # Splitting the target text into chunks
    target_chunks = np.array_split(extracted_text, nchunks)

    # Defining an empty list to store the results
    tr_results = []

    # Requesting translation for each target chunk
    for target_text in target_chunks:

        # Requesting translation through the Google API
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": target_text,
                "mime_type": "text/plain",
                "source_language_code": sourceLang,
                "target_language_code": "en",
            }
        )

        # Tranforming response to a list containing the translations
        translated_response = ["{}".format(translation.translated_text) 
                            for translation in response.translations] 
        
        # Appending results
        tr_results.extend(translated_response)

    # Assigning translated text a new column
    data[colName] = tr_results
    
    return data

# Defining a function to automaticaally translate a column using the Google Cloud API
def ggtranslate(cname):

    # Set up the source and target language codes
    target_language = "en"
    if cname == "Italy":
        source_language = "it"
    if cname == "France":
        source_language = "fr"
    if cname == "Spain":
        source_language = "es"
    if cname == "Germany":
        source_language = "de"

    # Subsetting data
    data_subset = master_data[master_data["country"] == cname]

    # Translating the headlines
    results = requestTrans(data         = data_subset,
                           targetColumn = "title",
                           sourceLang   = source_language,
                           colName      = "translatedTitle")    
    
    # Translating the descriptions
    results = requestTrans(data         = results,
                           targetColumn = "description",
                           sourceLang   = source_language,
                           colName      = "translatedDesc")

    return results

# Applying the translating function to the data
translated_corpus = [ggtranslate(x) for x in cntrs]

# Concatenating data frames into a single set
data4app = pd.concat(translated_corpus)

# Saving data
data4app.to_csv("data4app.csv")









