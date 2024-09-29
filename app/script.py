
from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import defaultdict
import pandas as pd
import time

from typing import List,DefaultDict
from ..exceptions.exception import CityCodeException, LocalityCodeException
from .main import process_results

CITY_CODE_CSV = "99acres_city_code.csv"
LOCALITY_CODE_CSV = "99acres_locality_code.csv"

def solve():
    
    # we can set more filters by adjusting query strings
    
    # Should be in lakhs
    min_budget = 10 # 10 Lakhs
    max_budget = 170 # 1 cr 170 lakhs
    bhk=2 # 2 for 2bhk, 3for 3bhk
    city = "Noida"
    locality = "Sector 18 Noida"
    type_ = "Ready_to_move"
    
    # Status of apartment you want
    available={
        "New":0,
        "Under_Construction":1,
        "Ready_to_move":2
    }

    av = available[type_]
    
    df = pd.read_csv(
        f"{CITY_CODE_CSV}",index_col=False
    )

    loc_df = pd.read_csv(
        f"{LOCALITY_CODE_CSV}",index_col=False
    )
    
    city_code_df = df[df["city"] == city]
    loc_df = loc_df[loc_df["locality"] == locality]
    
    # If no such city code exists
    if not len(loc_df):
        
        raise LocalityCodeException("Locality not found in df. \
                                    To scrap that locality first add \
                                    that locality code in csv manually or run script")
    
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

    process_results(locality_url, locality,True)


if __name__== "__main__":
    solve()