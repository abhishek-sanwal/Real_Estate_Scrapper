
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException,\
    NoSuchElementException,WebDriverException
from selenium.webdriver.common.by import By
from collections import defaultdict
import pandas as pd
import time

from typing import List,DefaultDict
from .exception import CityCodeException, LocalityCodeException


# Image SideCard which contains all the data
card_div_class = ".tupleNew__contentWrap"

# Heading class of Society 
heading_class = ".tupleNew__locationName"

short_description_class = ".tupleNew__propertyHeading"
price_class =".tupleNew__priceValWrap>span"
sqft_class =".tupleNew__area1Type"
bhk_class =".tupleNew__area1Type"
description_class = ".tupleNew__descText"

'''
Function to get data document.querySelector(.${class}).textContent
'''
def get_data(node,class_:str)->str:
    
    # Default value
    data = "Not Available"
    
    try:
        # Get text content
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
        # Get data by css selector
        data = node.find_elements(By.CSS_SELECTOR,class_)
        
        # First Child Node data
        data1 = data[0].text.strip()
        
        # Second Child Node data
        data2 = data[1].text.strip()
        
    except StaleElementReferenceException as e:
        print(e,"Stale")
        
    except NoSuchElementException as e:
        print(e,"No such element")

    except WebDriverException as e:
        print(e,"Not able to connect to devtools,\
            window might be in sleep mode. Check pc settings.")
        
    return [data1, data2]


def process_results(url:str, type:str)->None:    
    
    # A mapp to store data
    mapp:DefaultDict[List] = defaultdict(list)
    
    # Loop over all pages
    for page_num in range(1,10):
        
        # Get Chrome driver
        # Driver should be compatible with your chrome version. 
        # Else you might face errors
        
        driver = webdriver.Chrome()
        time.sleep(3)
        
        # Load page
        driver.get(f"{url}&page={page_num}")

        #  Wait for loading
        time.sleep(5)
        
        # For each card-div
        for node in driver.find_elements(By.CSS_SELECTOR,
                                            card_div_class):
            
            heading = get_data(node,heading_class)
            short_description = get_data(node,short_description_class)
            price = get_data(node,price_class)
            description = get_data(node,description_class)
            sqft,bhk = get_tuple(node,sqft_class)
            
            
            mapp["society_name"].append(heading)
            mapp["short_description"].append(short_description)
            mapp["bhk"].append(bhk)
            mapp["square_feet"].append(sqft)
            mapp["price"].append(price)
            mapp["description"].append(description)
            
    df = pd.DataFrame(
        mapp
    )
    
    df.to_csv(
        f"{type}_99acres.csv",mode='a'
    )
    

def solve():
    
    # we can set more filters by adjusting query strings
    
    # Should be in lakhs
    min_budget = 10 # 10 Lakhs
    max_budget = 170 # 1 cr 170 lakhs
    bhk=2 # 2 for 2bhk, 3for 3bhk

    # Status of apartment you want
    available={
        "New":0,
        "Under_Construction":1,
        "Ready_to_move":2
    }

    av = available["Ready_to_move"]
    locality_code = 161
    city = "Noida"

    df = pd.read_csv(
        "99acres_city_code.csv",index_col=False
    )
    locality = "Sector 18 Noida"
    
    loc_df = pd.read_csv(
        "99acres_locality_code.csv",index_col=False
    )
    
    city_code_df = df[df["city"] == city]
    loc_df = loc_df[loc_df["locality"] == locality]
    
    # If no such city code exists
    if not len(loc_df):
        
        raise LocalityCodeException("Locality not found in df. To scrap that locality first add that locality code in csv manually or run script")
    
    # if not such locality code exists
    if not len(city_code_df) :
        raise CityCodeException("City not found in df. Please choose one of the city from the csv")
    
    # Get value
    city_code = city_code_df["code"].values[0]
    
    # Get value
    locality_code = loc_df["code"].values[0]
    
    '''
    For Scrapping data city wise Use this code
    '''
    # For scrapping results city wise
    # city_url = f"https://99acres.com/search/property/buy?city={city_code}&bedroom_num={bhk}&budget_max={max_budget}&budget_min={min_budget}&availability={av}"

    # process_results(url=city_url,city=city)
    
    '''
    For Scrapping data city + locality wise use this code
    '''
    # For scrapping results locality + city wise
    locality_url = f"https://99acres.com/search/property/buy?city={city_code}&locality={locality_code}&bedroom_num={bhk}&budget_max={max_budget}&budget_min={min_budget}&availability={av}"

    process_results(locality_url, locality)


if __name__== "__main__":
    solve()