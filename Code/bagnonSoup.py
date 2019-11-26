# -*- coding: utf-8 -*-

import utilFile
import utilParse
import utilMap
import logger


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
        self.gold = Val
        
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
    return utilParse.findStrangeDatum(string," ", ",")

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
    if utilParse.findSubstring(string, "money") == -1:
        return -1
    return grabMoney(string)

# Tab Type C is for tab count 4 (items)
def parseTabC(string):
    if utilParse.findSubstring(string,"nil") == -1:
        return -1,0
    return grabItemData(string)

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
        potentialVal = parseTabB(string)
        if potentialVal == -1:
            return
        self.characterInFocus.SetGold(potentialVal)
    def handleTabFour(self, string):
        itemID, quantity = parseTabC(string)
        if itemID != -1:
            self.characterInFocus.AddToItemCount(itemID,quantity)
    def Parse(self,FilePath):
        ropeList = linesToRopeList(getFileContent(FilePath))
        for rope in ropeList:
            self.handler[rope.type](rope.string)
                
    

#%%
p = [Parser()]
p[0].Parse("BagBrother.LUA")
