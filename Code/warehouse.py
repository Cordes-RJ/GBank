# -*- coding: utf-8 -*-

import pandas as pd
import utilMap
import utilFile
import itemTypeRefCodes as itemRef
import logger
import wowhead




# assumes input of attribute strings
    
class Item:
    def __init__(self):
        self.itemID = 0
        self.new = True
        self.Name = ""
        self.Rarity = -1
        self.IconName = ""
        self.itemRefCode = 0
        self.LastPrice = 0
        self.Ct = 0
    def INITviaDFrow(self,dfRow):
        self.itemID = dfRow['itemID']
        self.Name = (dfRow['Name']).encode('utf-8')
        self.Rarity = dfRow['Rarity']
        self.IconName = (dfRow['IconName']).encode('utf-8')
        self.itemRefCode = itemRef.getRefCodefromString(dfRow['Type'] +"," +dfRow['Subtype'])
        self.LastPrice = dfRow['LastPrice']
        self.Ct = 0
        self.new = False # was found in a previous update
        return self
    def ToCSVrow(self):
        name = self.Name.decode('utf-8')
        typeAndSubtype = itemRef.getStringFromRefCode(self.itemRefCode)
        iconName = self.IconName.decode('utf-8')
        link = wowhead.makeDisplayURLfromItemID(self.itemID)
        attList = [self.itemID,name,link,self.Rarity,iconName,typeAndSubtype,self.LastPrice,self.Ct,self.ct * self.LastPrice]
        return utilFile.ListOfItemsToCSVRow(attList)
    def INITviaID(self, itemID):
        self.itemID = itemID
        return self
    def UpdateWoWheadInfo(self, winfo):
        winfo = wowhead.wowheadItemInfo()
        self.Name = (winfo.Name).encode('utf-8')
        self.Rarity = winfo.Rarity
        self.itemRefCode = winfo.RefCode
        self.IconName = (winfo.IconName).encode('utf-8')
    def UpdatePrice(self, price):
        self.LastPrice = price
    def UpdateCt(self,ct):
        self.Ct = ct
        

# take raw CSV path and return Pandas dataframe
# assumes header
def getFileContents(path):
    Lines =pd.read_csv(path)
    if len(Lines) <= 0:
        # for readability
        errMessage = "Error getting itemRef file|check parameters and itemref folder"
        logger.Log("warehouse","getFileContent","Critical", errMessage, LogAndKill = True)
        # exit program
    # clean the ropes of unneccessary control chars
    return Lines

def dfRowToAttributeList(dfRow):
    attributeStrings = ['itemID','Name','Link','Rarity','IconName','Type','Subtype','LastPrice','Ct']
    itemRow = []
    for attribute in attributeStrings:
        itemRow.append(dfRow[attribute])
    return itemRow
    
# returns dictionary of items 
def Build(Path):
    df = getFileContents(Path)
    items = []
    for i,i2 in df.iterrows():
        items.append(Item().INITviaDFrow(i2))
    itemDict = utilMap.Map(-1)
    for item in items:
        itemDict.Add(item.itemID,item)
    return itemDict
        


"""
#x= Build()
#for ID in x.ListKeys():
   # print(x.Get(ID).ToCSVrow())
"""


