# API key 932b29c2517bc4ab2c3ad585b0ff89ed
import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Search Bible versions
def get_data():
    # API endpoint
    url = "https://api.scripture.api.bible/v1/bibles/65eec8e0b60e656b-01"

    # Headers with API key included
    headers = {
        "api-key": '932b29c2517bc4ab2c3ad585b0ff89ed' # Add your API key here
    }

    # Making the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert response to JSON and print it
        data = response.json()
        print(data)
    else:
        print(f"Request failed with status code: {response.status_code}")

# Random Verse
def get_random_Verse():
    url = "https://bible-api.com/?random=verse"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert response to JSON and return the reference and text as a tuple
        data = response.json()
        return (data['reference'], data['text'])
    else:
        print(f"Request failed with status code: {response.status_code}")
        return ("Error", "Could not fetch verse")

def scrape_cross_references(verse):
    # Format the verse into a query string for the URL
    formatted_verse = verse.replace(" ", "+").replace(":", "%3A")
    url = f"https://www.openbible.info/labs/cross-references/search?q={formatted_verse}"
    
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        #print(response.text)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
                # Assume response.text contains your HTML response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example to find cross-reference section
        cross_refs = soup.find('div', class_='crossrefs')
        if cross_refs:
             # Split the string into verses
            lines = cross_refs.text.strip().split("\n")
            verses = []
            current_verse = ""

            for line in lines:
                if line.strip() == "":  # Skip empty lines
                    continue
                if ":" in line:  # Detect a new verse starting with a reference
                    if current_verse:
                        verses.append(current_verse.strip())
                    current_verse = line
                else:
                    current_verse += " " + line

            if current_verse:  # Add the last verse if present
                verses.append(current_verse.strip())
            verses.pop(0)
            return verses
        else:
            print("Cross-references not found.")
            
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
   

# # Example usage
# verse_input = "Genesis 1:2"

var = get_random_Verse()
print(var)
print('')
print('')
print(scrape_cross_references(var[0]))