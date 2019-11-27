# -*- coding: utf-8 -*-

import utilFile
import utilParse
import utilMap
import logger
from time import time as getTime


# gets file content from a bagbrother file
def getFileContent(path):
    Lines = utilFile.ReadIn_lines(path)
    if len(Lines) <= 0:
        # for readability
        errMessage = "Error getting bagbrother file|check parameters addons and saved variables"
        logger.Log("bagnonSoup","getFileContent","Critical", errMessage, LogAndKill = True)
        # exit program
    # clean the ropes of unneccessary control chars
    return Lines

def linesToRopeList(Lines):
    Ropes = []
    for i in range(len(Lines)):
        raw = rope(Lines[i])
        # removes empty lines and the highest level delimiter, which is useless
        if raw.type != 0:
            Ropes.append(raw)
    return Ropes

class Server:
    def __init__(self,name):
        self.name = name
        self.characters = []
    def addCharacter(self, char):
        self.characters.append(char)
    def GetName(self):
        return self.name

class Character:
    def __init__(self,name):
        self.name = name
        self.items = utilMap.Map(0)
        self.gold = 0
    def AddToItemCount(self,ID,ct):
        self.items.Set(ID,self.items.Get(ID)+ct)
    def GetName(self):
        return self.name
    def SetGold(self,Val):
        self.gold = int(Val)
    def getItemList(self):
        return self.items.ListKeys()
    def getItemCt(self,ID):
        return self.items.Get(ID)
    def getGold(self):
        return self.gold
        
class rope:
    def __init__(self, string):
        self.string = utilParse.removeControlCharacters(string)
        self.type =  utilParse.countCharacters(string,"\t")
        ##### types are indicated by tab count ^
        # 0 : useless
        # 1 : server or server delimiter
        # 2 : character or character delimiter
        # 3 : section delimiter or characteristic (race, faction, gold)
        # 4 : item or nil

def scrapeFromBrackets(string):
    return utilParse.findStrangeDatum(string,"[\"", "\"]")

def grabMoney(string):
    return utilParse.findStrangeDatum(string,"= ", ",")

def grabItemData(string):
    itemID = utilParse.findStrangeDatum(string,"\"",":")
    if itemID == "":
        return -1,0
    if utilParse.findCharacter(string, ";") == -1:
        return int(itemID), 1
    else:
        quantity = utilParse.findStrangeDatum(string,";","\"")
        return int(itemID), int(quantity)

# Tab Type A includes tab counts 1 and 2 (server and character)
def parseTabA(string):
    # return blank if it's a closing bracket
    if utilParse.findCharacter(string, "{") == -1:
        return ""
    # else return the server name
    return scrapeFromBrackets(string)

# Tab Type B is for tab count 3 (attributes like faction and money)
def parseTabB(string):
    if utilParse.findSubstring(string,"money") >= 0:
        return grabMoney(string)
    if utilParse.findSubstring(string, "equip") >= 0:
        return -2                      #* BUGFIX FOR EQUIPPED ITEMS
    if utilParse.findSubstring(string, "}") >= 0:
        return -3                      #* BUGFIX FOR EQUIPPED ITEMS
    return -1 # general failure to find money

# Tab Type C is for tab count 4 (items)
def parseTabC(string):
    if utilParse.findSubstring(string,"nil") != -1:
        return -1,0
    return grabItemData(string)


class WhiteList:
    def __init__(self, server, charList):
        self.server = server
        self.characters = utilMap.CreateMapofEmptyInterfaces(charList)
    def Check(self,char):
        if self.characters.InMap(char):
            return True
        return False

class subParser:
    def __init__(self):
        self.totalGold = 0
        self.items = utilMap.Map(0)
    def addToItemCt(self,ID,ct):
        self.items.Set(ID,self.items.Get(ID)+ct)
    def addToGold(self,val):
        self.totalGold += val
    def parseCharacter(self, char):
        self.addToGold(char.getGold())
        itemIDs = char.getItemList()
        for ID in itemIDs:
            self.addToItemCt(ID,char.getItemCt(ID))
    def parseCharacterList(self, charList):
        for char in charList:
            self.parseCharacter(char)
        return self.items.DeepCopy(), self.toGoldEntry()
    def toCsvLine(self, ID):
        return "\n"+str(ID)+"," +str(self.items.Get(ID))
    def toCsvBlob(self):
        blob = "ItemID,Ct"
        for ID in self.items.ListKeys():
            blob += self.toCsvLine(ID)
        return blob
    def toGoldEntry(self):
        t = str(getTime())
        return t + "," + str(self.totalGold)

class Parser:
    def __init__(self):
        self.servers = []
        self.serverInFocus = ""
        self.characterInFocus = ""
        self.handler = {
                1:self.handleTabOne,
                2:self.handleTabTwo,
                3:self.handleTabThree,
                4:self.handleTabFour
                }
        self.ignoreEquipped = False
        # is flipped to true when evaluating equipped items
    def closeServerInFocus(self):
        self.servers.append(self.serverInFocus)
    def closeCharacterInFocus(self):
        self.serverInFocus.addCharacter(self.characterInFocus)
    def setNewServerInFocus(self,name):
        self.serverInFocus = Server(name)
    def setNewCharacterInFocus(self,name):
        self.characterInFocus = Character(name)
    def handleTabOne(self,string):
        potentialServer = parseTabA(string)
        if potentialServer == "":
            self.closeServerInFocus()
        else:
            self.setNewServerInFocus(potentialServer)
    def handleTabTwo(self,string):
        potentialChar = parseTabA(string)
        if potentialChar == "":
            self.closeCharacterInFocus()
        else:
            self.setNewCharacterInFocus(potentialChar)
    def handleTabThree(self,string):
        #print("handling tabThree String:", string)
        potentialVal = parseTabB(string)
        if potentialVal == -1:
            #print("skipping")
            return # skip
        if potentialVal == -2:
            self.ignoreEquipped = True #* BUGFIX FOR EQUIPPED ITEMS
            #print("setting ignore on:")
            return
        if potentialVal == -3 and self.ignoreEquipped:
            self.ignoreEquipped = False #* BUGFIX FOR EQUIPPED ITEMS
            #print("setting ignore off:")
            return
        if potentialVal == -3:
            #print("skipping")
            return
        #print("setting value:", potentialVal)
        self.characterInFocus.SetGold(potentialVal)
    def handleTabFour(self, string):
        if self.ignoreEquipped:
            return                     #* BUGFIX FOR EQUIPPED ITEMS
        itemID, quantity = parseTabC(string)
        if itemID != -1:
            self.characterInFocus.AddToItemCount(itemID,quantity)
    def getServer(self,whitelist):
        for server in self.servers:
            if server.name == whitelist.server:
                return server
        logger.Log("BagnonSoup","Parser|getServer","Critical","Server Not Found", LogAndKill=True)
    def getCharacters(self,server, whitelist):
        newCharList = []
        for char in server.characters:
            if whitelist.Check(char.name):
                newCharList.append(char)
        if len(newCharList) == 0:
            logger.Log("BagnonSoup","Parser|getChars","Critical","No Characters Found", LogAndKill=True)
        return newCharList
    def getWhiteListedCharacters(self,whitelist):
        server = self.getServer(whitelist)
        return self.getCharacters(server, whitelist)
    # returns dictionary and goldCsvEntry
    def Parse(self,FilePath, whitelist):
        ropeList = linesToRopeList(getFileContent(FilePath))
        for rope in ropeList:
            self.handler[rope.type](rope.string)
        subparser = subParser()
        return subparser.parseCharacterList(self.getWhiteListedCharacters(whitelist))


    


