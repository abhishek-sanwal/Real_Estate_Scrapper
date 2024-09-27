
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
locality_url:str = f"{city_url}7&locality="

# Class for fetching names
class_ = ".tags-and-chips__textOnly span:nth-child(2)"


'''
A script to find city-code and locality code for all cities ,
Using this city code and locality code we can search data.
'''
def solve(url,start_count=1,end_count=50,name="city"):
    
    mapp:dict= defaultdict(list)
    
    # Run this loop more times to find more cityCode
    for i in range(start_count,end_count+1):
        
        try:
            
            driver = webdriver.Chrome()
            time.sleep(5)
            driver.get(url + str(i))
            time.sleep(5)

            element = driver.find_element(By.CSS_SELECTOR, class_)

            if element and element.text :
                print(i,element.text) 
                mapp[name].append(element.text)
                mapp["index"].append(i)
                print(mapp)
            
        except Exception as e:
            print(e)
        
        # Server is blocking the 
        driver.close()
        time.sleep(2)
        
    print(mapp,"this is mapp.")
    df = pd.DataFrame(mapp)
    
    df.to_csv(
        f"99acres_{name}_code.csv",mode="a",header=False,index=False
    )
    
    return "Done"


if __name__ =="__main__":
    
    solve(locality_url,156,205,"locality")
    

    
    
    