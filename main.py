'''
Scrappers are commonly deployed by search engines like Google that 
extract publicly available data from various websites over the internet 
so that a search solution can be built over it. Being a real estate internet 
company we also want to help our customers and in-house operations teams with 
similar data by making it available on their tips. For joining our tech team can
you write a Python program that takes a society's name as input and can extract 
all its publicly available data on 99acres.com
'''

import time,requests
import pandas as pd
from bs4 import BeautifulSoup
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

    time.sleep(5)
    
    driver = webdriver.Chrome()
    
    driver.get(url)
    
    time.sleep(10)
    driver.execute_script(
        "window.scrollTo(0, 1000);")
    
    mapp = defaultdict(list)
   
    lis = ['society_name', "description", "area", "bhk", "square_ft",
           "price", "possession","rating"]
    
    
    index = 0
    for class_ in [society_class,description_id,area_class, bhk_class, 
                   squft_class, price_class, possession_class, 
                   rating_class]:
        
        for element in driver.find_elements(By.CSS_SELECTOR,class_):
            
            
            text = element.text.strip()
            if text:
                mapp[lis[index]].append(text)
                        


        index += 1
    
    maxi = max(len(mapp[i]) for i in mapp)
   
    for lis in mapp:
        
        if len(mapp[lis]) != maxi:
            
            mapp[lis] += ['Nothing']*(maxi-len(mapp[lis]))
    
    df = pd.DataFrame(mapp)
    
    df.to_csv('99acres.csv')
    
    print("Task completed")

def extractSocietyData(societyName:str)->None:
    
    
    driver = webdriver.Chrome()
    
    driver.get("https://www.99acres.com/")
    
    time.sleep(5)
    
    print(driver.title)
    
    driver.execute_script("window.scrollBy(0, 1000);") 
    
    time.sleep(2)
    
    search_bar = driver.find_element(By.ID,"keyword")
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

    time.sleep(10)
    # Error occurs here
    # This page can not be loaded
    url = driver.current_url
    
    driver.close()
    
    extract_data(url)
    

societyName = "Ajnara Genx"

print(extractSocietyData(societyName))