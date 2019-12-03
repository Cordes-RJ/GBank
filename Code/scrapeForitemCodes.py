# -*- coding: utf-8 -*-
"""
temp code meant to scrape wowhead for item type and subtype mapping
"""

"""


import utilWeb
import wowhead
import utilMap
import random
import utilParse

global itemCodes
itemCodes = utilMap.Map(-1)

def createRefCode(mainID, subID):
    code = mainID*100+subID+100
    return code

def refCodeToSplitCodes(refCode):
    subCode = refCode - (int(refCode/100)*100)
    mainCode = int(refCode/100)- 1
    return mainCode, subCode

def refCodeToSplitCodesCSV(refCode):
    subCode = refCode - (int(refCode/100)*100)
    mainCode = int(refCode/100)- 1
    return str(mainCode) + "," + str(subCode)

def generateRandomIDs(ct,minInc, maxInc, start):
    current = start
    List = []
    for i in range(ct):
        current += random.randint(1,maxInc)
        List.append(current)
    return List

class TempItemInfo:
    def __init__(self):
        self.Name = "n/a"
        self.itemID = -1
        self.Type = ""
        self.subType = ""
        self.typeCode = -1
        self.subTypeCode = -1

# a urlBuildFunc
def makeXMLURLfromItemID(ItemID):
       return "https://classic.wowhead.com/item=" +str(ItemID) + "&&xml"
   
def findName(XML):
    return utilParse.findStrangeDatum(XML,"<name><![CDATA[", "]")
    
def findID(XML):
    return int(utilParse.findStrangeDatum(XML,"<item id=\"", "\""))

def findClass(XML):
    a = utilParse.findSubstring(XML,"<class id")
    return utilParse.findStrangeDatum(XML,"<![CDATA[","]]>",startIndexAt=a)

def findSubClass(XML):
    a = utilParse.findSubstring(XML,"<subclass")
    return utilParse.findStrangeDatum(XML,"<![CDATA[","]]>",startIndexAt=a)

def findClassCode(XML):
    return int(utilParse.findStrangeDatum(XML,"<class id=\"", "\""))

def findSubClassCode(XML):
    return int(utilParse.findStrangeDatum(XML,"<subclass id=\"", "\""))

# a parseResponseFunc
def parseWowHeadXML(XML):
    item = TempItemInfo()
    check = utilParse.findSubstring(XML,"Item not found!")
    if check == -1:
        item.itemID = findID(XML)
        item.Name = findName(XML)
        item.Type = findClass(XML)
        item.subType = findSubClass(XML)
        item.typeCode = findClassCode(XML)
        item.subTypeCode = findSubClassCode(XML)
    return item
   
def requesterFunc(url,headerTxt,timeout):
    try:
        return utilWeb.getResponseText(url,headerTxt,timeout)
    except Exception:
        print("failed",url)
        return ""

def ScrapeforItemCodes():
    refCodes = {}
    randIDs = generateRandomIDs(3400,1,15, 500)
    itemList = utilWeb.politelyScrape(randIDs, makeXMLURLfromItemID,requesterFunc,parseWowHeadXML,"test2",0.5)
    for item in itemList:
        if item.itemID != -1:
            refCodes[createRefCode(item.typeCode,item.subTypeCode)] = item.Type + "," + item.subType
    csvBlob = ""
    for key in refCodes.keys():
        csvBlob += str(key) + ","+ refCodeToSplitCodesCSV(key)+","+ refCodes[key] + "\n"
    with open("itemrefs.csv", "w") as IntoLog:
        IntoLog.write(csvBlob)
        IntoLog.close()
"""