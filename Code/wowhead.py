# -*- coding: utf-8 -*-

import utilParse
import itemTypeRefCodes as refcodes
import utilWeb

class wowheadItemInfo:
    def __init__(self):
        self.Name = "n/a"
        self.Link = "n/a"
        self.Rarity = -1
        self.RefCode = 0
        self.IconName = "n/a"

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
        item.Link = makeDisplayURLfromItemID(findID(XML))
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
        return utilWeb.politelyScrape(itemList,makeXMLURLfromItemID,requesterFunc,parseWowHeadXML,header,timeout)

