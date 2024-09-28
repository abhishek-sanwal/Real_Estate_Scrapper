
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, \
StaleElementReferenceException, WebDriverException

from collections import defaultdict
from typing import List, DefaultDict


# Link
url = "https://www.99acres.com/"

# Image SideCard which contains all the data
card_div_class = ".tupleNew__contentWrap"

# Heading class of Society 
heading_class = ".tupleNew__locationName"

short_description_class = ".tupleNew__propertyHeading"

# Price Class
price_class =".tupleNew__priceValWrap>span"

# Square feat class
sqft_class =".tupleNew__area1Type"

# Bhk 1,2,4,5 class
bhk_class =".tupleNew__area1Type"

# Description Class
description_class = ".tupleNew__descText"

#page_class
page_class = ".Pagination__srpPagination .caption_strong_large"

'''
Function to get data document.querySelector(.${class}).textContent
'''

def get_data(node,class_:str)->str:
    
    # Default value
    data = "Not Available"
    
    try:
        data = node.find_element(By.CSS_SELECTOR,class_).text.strip()
        
    except StaleElementReferenceException as e:
        print(e,"stale element, element changed by js after selection")
        
    except NoSuchElementException as e:
        
        print(e,"No such elements exception")
        
    except WebDriverException as e:
        print(e,"Not able to connect to devtools,\
            window might be in sleep mode. Check pc settings.")
        
    return data


'''
Function to get data document.querySelector(.${class}).textContent
'''

def get_tuple(node,class_:str)->List[str]:
    
    # Default Values
    data1 = data2 = "Not Available"
    
    try:
        # Fetch by CSS selector
        data = node.find_elements(By.CSS_SELECTOR,class_)
        # First Child
        data1 = data[0].text.strip()
        # Second Child
        data2 = data[1].text.strip()
        
    except StaleElementReferenceException as e:
        print(e,"Stale")
        
    except NoSuchElementException as e:
        print(e,"No such element")

    except WebDriverException as e:
        print(e,"Not able to connect to devtools,\
            window might be in sleep mode. Check pc settings.")
        
    return [data1, data2]

'''
Function to get last page number
'''
def get_page_number(driver, page_class)->int:

    try:
        page_data = driver.find_element(By.CSS_SELECTOR,page_class)
        
    except NoSuchElementException as e:
        print(e,"Element not yet found")
        
    page_data = page_data.text.strip()
    return page_data[page_data.rfind(" ")+1:]


'''
Function to get paginated society Data
I am extracting limited fields but almost anything can be extracted
including pictures, links which has been revealed.


'''


def process_results(url:str, societyName:str)->None:    
    
    mapp:DefaultDict[List] = defaultdict(list)
    
    # Default value for page
    maxi_page = 10 
    
    for page_num in range(1,maxi_page+1):
        
        # Get Chrome driver
        # Driver should be compatible with your chrome version. 
        # Else you might face errors
        driver = webdriver.Chrome()
        
        driver.get(f"{url}&page={page_num}")
        time.sleep(5)
            
        for node in driver.find_elements(By.CSS_SELECTOR,
                                            card_div_class):
            
            heading = get_data(node,heading_class)
            short_description = get_data(node,short_description_class)
            price = get_data(node,price_class)
            description = get_data(node,description_class)
            sqft,bhk = get_tuple(node,sqft_class)
            
            if heading.find(societyName) != -1:
                print(heading)
                mapp["society_name"].append(heading)
                mapp["short_description"].append(short_description)
                mapp["bhk"].append(bhk)
                mapp["square_feet"].append(sqft)
                mapp["price"].append(price)
                mapp["description"].append(description)
        

        if maxi_page == 10:
            
            maxi_page = get_page_number(driver,page_class)
            
        print(maxi_page)
            

    df = pd.DataFrame(
        mapp
    )
    
    df.to_csv(
        f"{societyName}_99acres.csv",mode='a'
    )


'''

'''
def extractSocietyData(societyName:str)->None:
    
    if not societyName:
        return ""
    
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
    print("Data Entered")
    # Wait for suggestions
    time.sleep(5)
    
    # Click first available suggestion Usually 
    # first suggestion is best suggestion So
    search_suggestions =driver.find_element(By.CSS_SELECTOR,
                                            "#suggestions_custom")
    first_search_suggestion = search_suggestions.find_element(By.TAG_NAME, 
                                                              'li')
    first_search_suggestion.click()

    # Press enter search_bar
    search_bar.send_keys(Keys.RETURN)

    # Wait for redirecting to new page.
    time.sleep(5)
    
    # Error occurs here
    # This page can not be loaded
    # Server side js has bot-detection scripts
    # So we need to close this driver
    # and reload a new one
    url = driver.current_url
    
    driver.close()
    
    process_results(url,societyName)

societyName = "Griha Pravesh"

print(extractSocietyData(societyName))