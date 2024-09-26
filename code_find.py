
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from collections import defaultdict

import pandas as pd
import time

# Global Variables
# UrlS
city_url :str = "https://99acres.com/search/property/buy?preference=&city="
locality_url:str = f"{city_url}=7&locality="

# Class for fetching names
class_ = ".tags-and-chips__textOnly span:nth-child(2)"


'''
A script to find city-code and locality code for all cities ,
Using this city code and locality code we can search data.
'''
def solve(url,count,name):
    
    
    mapp:dict= defaultdict(list)
    
    # Run this loop more times to find more cityCode
    for i in range(1,count):
        
        try:
            
            driver = webdriver.Chrome()
            time.sleep(5)
            driver.get(url + str(i))
            time.sleep(5)

            element = driver.find_element(By.CSS_SELECTOR, class_)

            if element and element.text :
                print(i,element.text) 
                mapp["locality"].append(element.text)
                print(mapp)
            
        except Exception as e:
            print(e)
        
        # Server is blocking the 
        driver.close()
        time.sleep(2)
        
    print(mapp,"this is mapp.")
    df = pd.DataFrame(mapp)
    
    df.to_csv(
        f"99acres_{name}_code.csv",mode="a"
    )
    
    return "Done"


if __name__ =="__main__":
    
    solve(locality_url,100,"locality")
    

    
    
    