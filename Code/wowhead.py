# -*- coding: utf-8 -*-
"""
wowhead is used to scrape data from classic.wowhead and facilitate transfer of
the data found to other functions
"""


import utilParse
import itemTypeRefCodes as refcodes
import utilWeb
import logger

class wowheadItemInfo:
    def __init__(self):
        self.Name = ""
        self.itemID = 0
        self.Rarity = -1
        self.RefCode = 0
        self.IconName = ""

# a urlBuildFunc
def makeXMLURLfromItemID(ItemID):
       return "https://classic.wowhead.com/item=" +str(ItemID) + "&&xml"
   
# a urlBuildFunc
def makeDisplayURLfromItemID(ItemID):
       return "https://classic.wowhead.com/item=" +str(ItemID)
   
# a parseResponseFunc
def parseWowHeadXML(XML):
    item = wowheadItemInfo()
    check = utilParse.findSubstring(XML,"Item not found!")
    if check == -1:
        item.itemID = findID(XML)
        item.Name = findName(XML)
        item.RefCode = refcodes.createRefCode(findClass(XML),findSubClass(XML))
        item.IconName = findIcon(XML)
        item.Rarity = findQuality(XML)
    return item
    
def requesterFunc(url,headerTxt,timeout):
    return utilWeb.getResponseText(url,headerTxt,timeout)
    
def findName(XML):
    return utilParse.findStrangeDatum(XML,"<name><![CDATA[", "]")
    
def findID(XML):
    return int(utilParse.findStrangeDatum(XML,"<item id=\"", "\""))

def findQuality(XML):
    return int(utilParse.findStrangeDatum(XML,"<quality id=\"", "\""))

def findClass(XML):
    return int(utilParse.findStrangeDatum(XML,"<class id=\"", "\""))

def findSubClass(XML):
    return int(utilParse.findStrangeDatum(XML,"<subclass id=\"", "\""))

def findIcon(XML):
    a = utilParse.findSubstring(XML,"<icon displayId=\"")
    return utilParse.findStrangeDatum(XML,">","<",startIndexAt=a)

# takes list of itemIDs as input
# if it fails to find an item on wowhead, it will return it as a blank item
class Scraper:
    def __init__(self):
        pass
    def Scrape(self, itemList, header, timeout):
        List = utilWeb.politelyScrape(itemList,makeXMLURLfromItemID,requesterFunc,parseWowHeadXML,header,timeout)
        for item in List:
            if item.Name == "":
                logger.Log("wowhead","scraper","warning","failed to get data for: "+str(item))
        return List

"""
s = Scraper()
x = s.Scrape(['13968','341'], "test",10)
"""