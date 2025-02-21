# API key 932b29c2517bc4ab2c3ad585b0ff89ed
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from pdfminer.high_level import extract_text

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


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

def daily_devotional():
    # Path to your PDF file
    pdf_path = r"C:\Users\swpar\Desktop\Devontionals\_OceanofPDF.com_God_Is_with_You_Every_Day_365-Day_Devotional_-_Max_lucado.pdf"

    # Base page number for January 1st
    start_page = 8  

    # Get today's date
    today = datetime.today()
    # current_month = 1  # 1 = January, 2 = February, etc.
    # day_of_year = 1  # Day of year (1-365)
    current_month = today.month  # 1 = January, 2 = February, etc.
    day_of_year = today.timetuple().tm_yday  # Day of year (1-365)

    # Calculate extra pages using the direct formula
    if current_month % 2 == 0:  # Even month
        month_val = current_month // 2
        page_diff = (month_val - 1) * 2 + month_val
    else:  # Odd month
        month_val = current_month // 2  # floor division
        page_diff = month_val * 2 + month_val

    # Calculate the final page number
    page_number = start_page + (day_of_year) + page_diff - 2
    
    print(f"Looking for page number: {page_number}")
    
    # Extract text from the PDF file using PDFMiner's extract_text method
    # Note: PDFMiner works with page ranges, not page numbers
    # We extract the page in range and pass the extracted text for that page
    try:
        text = extract_text(pdf_path, page_numbers=[page_number])
        if text:
            return text
        else:
            print("No text found on the page.")
    except Exception as e:
        print(f"Error extracting text: {e}")

def online_daily_devotional():
    url = "https://seekinggodsface.org/"  # Replace with the target URL
    headers = {"User-Agent": "Mozilla/5.0"}  # Helps avoid getting blocked
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text  # The HTML content of the page

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract specific elements
        title = soup.title.text  # "Seeking Gods Face"
        paragraphs = [p.text for p in soup.find_all("p")]
        start_phrase = 'and universal prayer'
        end_phrase = "The Seeking God's Face website"

        # Initialize variables to control extraction
        collecting = False
        extracted_text = []
        cleaned_data = [line.strip() for line in paragraphs if line.strip()]
        for paragraph in cleaned_data:
            if start_phrase in paragraph:
                collecting = True
                continue
            if end_phrase in paragraph:
                break
            if collecting:
                extracted_text.append(paragraph.strip())
            

        format_text = "\n\n".join(extracted_text)

        return format_text
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")


def video_urls():
    urls = ["https://bibleproject.com/explore/book-overviews/?type=old", "https://bibleproject.com/explore/book-overviews/?type=new"]
    old_anchors = []
    new_anchors = []
    for url in urls:
        headers = {"User-Agent": "Mozilla/5.0"}  # Helps avoid getting blocked
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html_content = response.text  # The HTML content of the page
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract all anchor elements
            if url.endswith("old"):
                old_anchors = soup.find_all("a", class_="watch-testament-grid-item")
            else:
                new_anchors= soup.find_all("a", class_="watch-testament-grid-item")
        else:
            print(f"Failed to retrieve page. Status code: {response.status_code}")
            return []
        
    # Return the list of anchor elements
    return (old_anchors, new_anchors)

def get_video(url):
    video_url = None

    # Set up the Selenium WebDriver (using Chrome in this example)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening a browser window)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the iframe to be present and get the iframe element
        iframe = driver.find_element(By.CLASS_NAME, "video-container-video")
        if iframe:
            video_url = iframe.get_attribute("src")
        else:
            print("No iframe with class 'video-container-video' found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the WebDriver
        driver.quit()

    return video_url

# # Example usage
# verse_input = "Genesis 1:2"

# var = get_random_Verse()
# print(var)
# print('')
# print('')
# print(scrape_cross_references(var[0]))

#daily_devotional()
# print(online_daily_devotional() )  
# print(get_video("https://bibleproject.com/explore/video/leviticus/"))