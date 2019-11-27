# -*- coding: utf-8 -*-

import utilParse
import utilFile
import utilMap
import logger

def scrapeFromBrackets(string):
    return utilParse.findStrangeDatum(string,"[\"", "\"]")

def getItemID(string):
    try:
        return int(scrapeFromBrackets(string))
    except Exception:
        print(string)
        logger.Log("woad","getItemID","Critical","failed to parse auc-stat-simple line, check woad and file", LogAndKill = True)

def getPrice(string):
    List = utilParse.findAllCharacters(string, ";")
    price = 0
    try:
        if len(List) == 2:
            foundEnd = utilParse.findCharacter(string,"\"",startIndexAt=List[1])
            price = int(string[List[1]+1:foundEnd])
        elif len(List)== 3:
            print(string)
            price = int(string[List[1]+1:List[2]])
    except Exception:
        pass
    print(string, price, List)
    return price

def getDataFromStatString(string):
    return getItemID(string), getPrice(string)

def getFileContent(path):
    Lines = utilFile.ReadIn_lines(path)
    if len(Lines) <= 0:
        # for readability
        errMessage = "Error getting auc-stat-simple file|check parameters addons and saved variables"
        logger.Log("woad","getFileContent","Critical", errMessage, LogAndKill = True)
        # exit program
    # clean the ropes of unneccessary control chars
    return Lines

def findServer(Ropes, server):
    for idx in range(len(Ropes)):
        if Ropes[idx].type == 2:
            found = utilParse.findSubstring(Ropes[idx].string,server)
            if found != -1:
                return idx
            else:
                pass
    errMessage = "Error finding server in auc-stat-simple file|check parameters addons and saved variables"
    logger.Log("woad","findServer","Critical", errMessage, LogAndKill = True)

def isolateServer(Ropes, server):
    foundAt = findServer(Ropes,server)
    for idx in range(foundAt+1,len(Ropes)):
        if Ropes[idx].type == 2:
            return Ropes[foundAt+1:idx]
        else:
            pass
    errMessage = "Error isolating server in auc-stat-simple file|check parameters addons and saved variables"
    logger.Log("woad","isolateServer","Critical", errMessage, LogAndKill = True)

def findDailyPriceSection(Ropes):
    for idx in range(len(Ropes)):
        if Ropes[idx].type == 3:
            found = utilParse.findSubstring(Ropes[idx].string,"[\"daily\"]")
            if found != -1:
                return idx
            else:
                pass
    errMessage = "Error finding daily price section in auc-stat-simple file|check parameters addons and saved variables"
    logger.Log("woad","findDailyPriceSection","Critical", errMessage, LogAndKill = True)

def isolateDailyPrices(Ropes):
    foundAt = findDailyPriceSection(Ropes)
    for idx in range(foundAt+1,len(Ropes)):
        if Ropes[idx].type == 3:
            return Ropes[foundAt+1:idx]
        else:
            pass
    errMessage = "Error isolating daily prices in auc-stat-simple file|check parameters addons and saved variables"
    logger.Log("woad","isolateDailyPrices","Critical", errMessage, LogAndKill = True)
    
# returns dictionary of itemID:price
def grabDailyPrices(Ropes):
    itemMap = utilMap.Map(0)
    for Rope in Ropes:
        itemID, price = getDataFromStatString(Rope.string)
        itemMap.Add(itemID,price)
    return itemMap

def linesToRopeList(Lines):
    Ropes = []
    for i in range(len(Lines)):
        raw = rope(Lines[i])
        # removes empty lines and the highest level delimiter, which is useless
        if raw.type != 0 and raw.type != 1:
            Ropes.append(raw)
    return Ropes

class rope:
    def __init__(self, string):
        self.string = utilParse.removeControlCharacters(string)
        self.type =  utilParse.countCharacters(string,"\t")
        ##### types are indicated by tab count ^
        # 0 : useless
        # 1 : useless
        # 2 : server or server delimiter
        # 3 : type marker (recent daily vs mean)
        # 4 : item data

# raw parser returns a dictionary of daily prices
class rawParser:
    def __init__(self):
        pass
    def Parse(self,FilePath, ServerName):
        return grabDailyPrices(isolateDailyPrices(isolateServer(linesToRopeList(getFileContent(FilePath)),ServerName)))
    
# whiteList should be a Map of itemIDs
class Parser:
    def __init__(self, itemIDWhiteList):
        self.whiteList = itemIDWhiteList
    def whiteListedItemID(self,itemID):
        if self.whiteList.InMap(itemID):
            return True
        else:
            return False
    def grabDailyPrices(self,Ropes):
        itemMap = utilMap.Map(0)
        for Rope in Ropes:
            itemID = getItemID(Rope.string)
            if self.whiteListedItemID(itemID):
                itemMap.Add(itemID,getPrice(Rope.string))
            else: # for readability
                pass
        return itemMap
    def Parse(self,FilePath, ServerName):
        return self.grabDailyPrices(isolateDailyPrices(isolateServer(linesToRopeList(getFileContent(FilePath)),ServerName))) 

"""
----
Lines = getFileContent("test_Auc-Stat-Simple.lua")
A1ropes = linesToRopeList(Lines)
A2newRopes = isolateServer(A1ropes,"Kirtonos")
A3dailyPrices = isolateDailyPrices(A2newRopes)
A4dict = grabDailyPrices(A3dailyPrices)
-----
woadParser = Parser()
itemdict = woadParser.Parse("test_Auc-Stat-Simple.lua", "Kirtonos")
x = [itemdict]
----
woadParser = Parser()
itemdict = woadParser.Parse("test_Auc-Stat-Simple.lua", "Kirtonos")
x = [itemdict]
"""