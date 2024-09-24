
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from collections import defaultdict

urls = "https://www.99acres.com/"

society_class = ".tupleNew__locationName"
bhk_class = ".tupleNew__bOld"
price_class = ".tupleNew__priceValWrap>span"
squft_class = ".tupleNew__perSqftWrap"
area_class = ".tupleNew__areaType"
possession_class = ".tupleNew__possessionBy"
picture_class = ".CR__slideshowSlider"
description_id = "#srp_tuple_description"
rating_class = ".tupleNew__locRatings span"

def extract_data(url):

    default = "Nothing"
    # Get a chormedriver
    driver = webdriver.Chrome()
    
    driver.get(url)
    
    # Wait for 10 secs to load
    time.sleep(10)
    
    # Move 1000px in y-direction so data gets visible
    # website is dynamic so it is essential step
    driver.execute_script(
        "window.scrollTo(0, 1000);")
    
    # Create a dictionary
    mapp = defaultdict(list)
   
    # keys for our mapp    
    lis = ['society_name', "description", "area", "bhk", "square_ft",
           "price", "possession","rating"]
    
    
    index = 0
    
    # Go class by class
    for class_ in [society_class,description_id,area_class, bhk_class, 
                   squft_class, price_class, possession_class, 
                   rating_class]:
        
        # Fetch each element
        for element in driver.find_elements(By.CSS_SELECTOR,class_):
            
            # Fetch text and remove whitespaces around it
            text = element.text.strip()
            # If text exists
            if text:
                # Append to its key-list
                mapp[lis[index]].append(text)
                        


        index += 1
    
    # Fetch Maximum length of any list
    maxi = max(len(mapp[i]) for i in mapp)
   
    # Make each list length same    
    for lis in mapp:
        
        if len(mapp[lis]) != maxi:
            
            # Add a default word
            mapp[lis] += [default]*(maxi-len(mapp[lis]))
    
    # Convert to DF
    df = pd.DataFrame(mapp)
    
    # Convert to csv and store it
    df.to_csv('99acres.csv')
    
    # Task done
    print("Task completed")

def extractSocietyData(societyName:str)->None:
    
    driver = webdriver.Chrome()
    
    driver.get("https://www.99acres.com/")
    
    # Wait for page to get loaded
    time.sleep(5)
    
    # Extract title of page
    print(driver.title)
    
    # Scroll page by 1000px in y direction so that search bar will be
    # visible in viewport
    driver.execute_script("window.scrollBy(0, 1000);") 
    
    # Now searchbar is visible
    time.sleep(2)
    
    # Find search bar by its id
    search_bar = driver.find_element(By.ID,"keyword")
    
    # Print placeholder text
    print(search_bar.get_attribute('placeholder'))
    
    # Click search bar to enter data
    search_bar.click()
    
    # Enter Society Name in search
    search_bar.send_keys(societyName)
    
    # Wait for suggestions
    time.sleep(10)
    
    # Click first available suggestion
    search_suggestions =driver.find_element(By.CSS_SELECTOR,"#suggestions_custom")
    first_search_suggestion = search_suggestions.find_element(By.TAG_NAME, 'li')
    first_search_suggestion.click()

    # Press enter search_bar
    search_bar.send_keys(Keys.RETURN)

    # Wait for redirecting to new page.
    time.sleep(10)
    
    # Error occurs here
    # This page can not be loaded
    # Server side js has bot-detection scripts
    # So we need to close this driver
    # and reload a new one
    url = driver.current_url
    
    driver.close()
    
    extract_data(url)
    

societyName = "Sri Anjana Green layout"

print(extractSocietyData(societyName))