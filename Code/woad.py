# -*- coding: utf-8 -*-

import utilParse
import logger

def scrapeFromBrackets(string):
    return utilParse.findStrangeDatum(string,"[\"", "\"]")

def getItemID(string):
    try:
        return int(scrapeFromBrackets(string))
    except Exception:
        logger.Log("woad","getItemID","Critical","failed to parse auc-stat-simple line, check woad and file", LogAndKill = True)

def getPrice(string):
    List = utilParse.findAllCharacters(string, ";")
    price = 0
    try:
        price = int(string[List[1]+1:List[2]])
    except Exception:
        pass
    return price

def getDataFromStatString(string):
    return getItemID(string), getPrice(string)
    
#%%
import utilParse

string = "[\"13931\"] = \"0@909046;239;3700;30\","
print(string)
itemID = getItemIDfromStatString(string)
List = utilParse.findAllCharacters(string, ";")
price = int(string[List[1]+1:List[2]])
#%%
for i in range(len(string)):
    print(i,string[i])

#%%
