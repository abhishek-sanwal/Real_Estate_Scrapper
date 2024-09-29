
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, \
StaleElementReferenceException, WebDriverException

import exceptions.exception as exception

from collections import defaultdict
from typing import List, DefaultDict

# SOME CONSTANTS DEFINED
MAX_RETRIES = 3
SHORT_WAIT = 2
LONG_WAIT = 5
DEFAULT_PAGES = 10
# Link
URL = "https://www.99acres.com/"

# Image SideCard which contains all the data
CARD_DIV_CLASS = ".tupleNew__contentWrap"

# Heading class of Society 
HEADING_CLASS = ".tupleNew__locationName"

# short description
SHORT_DESCRIPTION_CLASS = ".tupleNew__propertyHeading"

# Price Class
PRICE_CLASS =".tupleNew__priceValWrap>span"

# Square feat class
SQFT_CLASS =".tupleNew__area1Type"

# Bhk 1,2,4,5 class
BHK_CLASS =".tupleNew__area1Type"

# Description Class
DESCRIPTION_CLASS = ".tupleNew__descText"

#page_class
PAGE_CLASS = ".Pagination__srpPagination .caption_strong_large"

#  suggestions class
SUGGESTION_CLASS  ="#suggestions_custom"




'''
    Function to get data document.querySelector(.${class}).textContent
'''

def get_data(node,class_:str)->str:
    
    # Default value
    data = "Not Available"
    
    # Total retries MAX_RETRIES times
    for i in range(MAX_RETRIES):
        
        try:
            data = node.find_element(By.CSS_SELECTOR,class_).text.strip()
            break
        
        except NoSuchElementException as e:
            print(e,f"Either Single page or class not found, Retrying, Total Retries {MAX_RETRIES} times, Retry:{i}")
            time.sleep(SHORT_WAIT)
            
        except StaleElementReferenceException as e:
            print(e,f"Stale element, element not in dom, Retrying, Total Retries {MAX_RETRIES} times, Retry:{i}")
            time.sleep(SHORT_WAIT)
            
        except WebDriverException as e:
            print(e,"Not able to connect to devtools,\
                window might be in sleep mode. Check pc settings.")
            break
        
        
    return data


'''
    Function to get data document.querySelector(.${class}).textContent
    check

'''

def get_list(node,class_:str)->List[str]:
    
    # Default Values
    data1 = data2 = "Not Available"
    
    # Retry 3 times
    for i in range(MAX_RETRIES):
            
        try:
            # Fetch by CSS selector
            data = node.find_elements(By.CSS_SELECTOR,class_)
            
            data1 = data[0].text.strip()
            data2 = data[1].text.strip()
            break
            
        except NoSuchElementException as e:
            print(e,f"Element not found, Retrying, Total Retries {MAX_RETRIES} times, Retry:{i}")
            time.sleep(SHORT_WAIT)
            
        except StaleElementReferenceException as e:
            print(e,f"Stale element, element not in dom, Retrying, Total Retries {MAX_RETRIES} times, Retry:{i}")
            time.sleep(SHORT_WAIT)
            
        except WebDriverException as e:
            print(e,"Not able to connect to devtools,\
                window might be in sleep mode. Check pc settings.")
            break
        
    return [data1, data2]


'''
    Function to get last page number
'''
def get_page_number(driver, PAGE_CLASS)->int:

    page_data = ""
    
    # Retry 3 times 
    for i in range(MAX_RETRIES):
            
        try:
            page_data = driver.find_element(By.CSS_SELECTOR,PAGE_CLASS)
            page_data = page_data.text.strip()
            print(page_data,"Page data here")
            if not page_data:
                continue
            break
            
        except NoSuchElementException as e:
            print(e,f"Either Single page or element not found, Retrying, Total Retries {MAX_RETRIES} times, Retry:{i}")
            time.sleep(SHORT_WAIT)
            
        except StaleElementReferenceException as e:
            print(e,f"Stale element, element not in dom, Retrying, Total Retries {MAX_RETRIES} times, Retry:{i}")
            time.sleep(SHORT_WAIT)
            
        except WebDriverException as e:
            print(e,"Not able to connect to dev tools Most probably window is in sleep mode")
            break
        
        
    if not page_data:
        print(f"Page class not loaded.Sending default {DEFAULT_PAGES} value")    
        return DEFAULT_PAGES
            
    print(page_data,"Page data after loop")
    
    return int(page_data[page_data.rfind(" ")+1:])


'''
Function to get paginated society Data
I am extracting limited fields but almost anything can be extracted
including pictures, links which has been revealed.


'''


def process_results(url:str, societyName:str,flag:bool)->None:    
    
    mapp:DefaultDict[List] = defaultdict(list)
    
    maxi_page = DEFAULT_PAGES
    page_num = 1
    while page_num <= maxi_page:
        
        # Get Chrome driver
        # Driver should be compatible with your chrome version. 
        # Else you might face errors
        driver = webdriver.Chrome()
        
        driver.get(f"{url}&page={page_num}")
        time.sleep(LONG_WAIT)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SHORT_WAIT)
        
        for node in driver.find_elements(By.CSS_SELECTOR,
                                            CARD_DIV_CLASS):
            
            heading = get_data(node,HEADING_CLASS)
            short_description = get_data(node,SHORT_DESCRIPTION_CLASS)
            price = get_data(node,PRICE_CLASS)
            description = get_data(node,DESCRIPTION_CLASS)
            sqft,bhk = get_list(node,SQFT_CLASS)
            
            if not flag and heading.find(societyName) != -1:
                print(heading)
                mapp["society_name"].append(heading)
                mapp["short_description"].append(short_description)
                mapp["bhk"].append(bhk)
                mapp["square_feet"].append(sqft)
                mapp["price"].append(price)
                mapp["description"].append(description)
        

        if maxi_page == DEFAULT_PAGES:
            
            maxi_page = get_page_number(driver,PAGE_CLASS)
            
        page_num += 1
            

    df = pd.DataFrame(
        mapp
    )
    # Remove duplicates rows
    df.drop_duplicates(keep="first",inplace=True)
    
    # Convert to csv and store
    df.to_csv(
        f"CSV/output/{societyName}_99acres.csv",mode='a'
    )


def get_url(url):
    
    for i in range(MAX_RETRIES):
        
        try:
            
            driver = webdriver.Chrome()
            
            driver.get(url)
            
            time.sleep(LONG_WAIT)
            
            if driver.title.lower().find("error") != -1:
                raise exception.LoadErrorException(f"Server side page load error")

            break
            
        except WebDriverException as e:
            print(e ,f"Retrying... \
                    Total retries {MAX_RETRIES}.Retry number{i}")
            
            time.sleep(SHORT_WAIT)
            
        except LoadErrorException as e:
            
            print(e,f"Retrying... \
                    Total retries {MAX_RETRIES}.Retry number{i}")
            
            time.sleep(SHORT_WAIT)
            
    return driver

'''
Extract Any apartment list data
'''
def extractSocietyData(societyName:str)->None:
    
    if not societyName:
        return ""
    
    driver = webdriver.Chrome()
    
    driver = get_url(url)
    
    # Extract title of page
    print(driver.title)
    
    # Scroll page by 1000px in y direction so that search bar will be
    # visible in viewport
    driver.execute_script("window.scrollBy(0, 1000);") 
    
    # Now searchbar is visible
    time.sleep(SHORT_WAIT)
    
    # Find search bar by its id
    search_bar = driver.find_element(By.CSS_SELECTOR,"#keyword") 
    
    # Print placeholder text
    print(search_bar.get_attribute('placeholder'))
    
    for i in range(MAX_RETRIES):
        
        try:    
            # Click search bar to enter data
            search_bar.click()
            break
            
        except StaleElementReferenceException as e:
            print(f"Stale element. Retrying, Retry number{i} Total retires=3")
            time.sleep(SHORT_WAIT)
            
        except NoSuchElementException as e:
            print(f"Element not found. Retrying, Total retires 3, retry number{i}")
            time.sleep(SHORT_WAIT)
            
        
    
    # Enter Society Name in search
    search_bar.send_keys(societyName)
    print("Data Entered")
    # Wait for suggestions
    time.sleep(LONG_WAIT)
    
    # Click first available suggestion Usually 
    # first suggestion is best suggestion So
    search_suggestions = driver.find_element(By.CSS_SELECTOR, SUGGESTION_CLASS)
                                            
    first_search_suggestion = search_suggestions.find_element(By.TAG_NAME, 
                                                              'li')
    first_search_suggestion.click()

    # Press enter search_bar
    search_bar.send_keys(Keys.RETURN)

    # Wait for redirecting to new page.
    time.sleep(LONG_WAIT)
    
    # Error occurs here
    # This page can not be loaded
    # Server side js has bot-detection scripts
    # So we need to close this driver
    # and reload a new one
    url = driver.current_url
    
    driver.close()
    
    process_results(url,societyName,False)

societyName = "Shree Ananth Nagar Layout"
# societyName = "Magarpatta Annex"
# societyName = "Jaypee Greens"
societyName = "Griha Pravesh"

print(extractSocietyData(societyName))