
from collections import defaultdict

import os
import pandas as pd
import time

from app.main import get_node,get_driver,LONG_WAIT

# Global Variables
# UrlS
CITY_URL :str = "https://99acres.com/search/property/buy?preference=&city="
LOCALITY_URL:str = f"{CITY_URL}7&locality="

# Class for fetching names
SEARCH_NAME_class_ = ".tags-and-chips__textOnly span:nth-child(2)"

BASE_DIR = os.path.dirname(__file__)

'''
A script to find city-code and locality code for all cities ,
Using this city code and locality code we can search data.
'''
def solve(url,start_count=1,end_count=50,name="city"):
    
    mapp:dict= defaultdict(list)
    
    # Run this loop more times to find more cityCode
    for i in range(start_count,end_count+1):
        
        driver = get_driver(url)
        time.sleep(LONG_WAIT)

        element = get_node(driver, SEARCH_NAME_class_)

        if element and element.text :
            print(i,element.text) 
            mapp[name].append(element.text)
            mapp["index"].append(i)
            print(mapp)
            
        # Server is blocking the 
        driver.close()
        
    print(mapp,"this is mapp.")
    df = pd.DataFrame(mapp)
    relative_path = os.path.join(BASE_DIR,f"../CSV/99acres_{name}_code.csv")
    df.to_csv(
        relative_path,mode="a",header=False,index=False
    )

    return "Done"


if __name__ =="__main__":
    
    url = LOCALITY_URL
    start_count = 156
    end_count = 205
    type_ = "locality"
    
    
    
    solve(url,start_count,end_count,type_)
    

    
    
    