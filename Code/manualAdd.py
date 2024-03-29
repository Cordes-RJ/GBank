# -*- coding: utf-8 -*-

import utilFile
import logger
import utilParse

def getFileContent(path):
    Lines = utilFile.ReadIn_lines(path)
    if len(Lines) <= 0:
        # for readability
        errMessage = "Got blank return from ManualAdd"
        logger.Log("manualAdd","getFileContent","Note", errMessage)
        # exit program
    return Lines

# assumes input of a map[itemID]:ct, adds each itemID string to a item dict
def addLinestoItemMap(lines, anItemMap):
    itemMap = anItemMap.DeepCopy()
    try:
        for i in lines:
            itemID = int(utilParse.removeControlCharacters(i))
            print(itemID)
            if not itemMap.InMap(itemID):
                itemMap.Set(itemID, 0)
        return itemMap
    except Exception:
        errMessage = "Error adding ID from manualAdd file|check manualAddFile for non-integers"
        logger.Log("manualAdd","addLines","Critical", errMessage, LogAndKill = True)

# assumes input of a map[itemID]:ct, adds each itemID string to a item dict
class ParserOld:
    def __init__(self):
        pass
    def Parse(self,FilePath,ItemMap):
        return addLinestoItemMap(getFileContent(FilePath),ItemMap)

# just returns itemList
class Parser:
    def __init__(self):
        pass
    def Parse(self,FilePath):
        Lines = getFileContent(FilePath)
        # clean lines and replace with integers
        for idx in range(len(Lines)):
            Lines[idx] = int(utilParse.removeControlCharacters(Lines[idx]))
        return Lines
    
        
"""
Remember, map arguments are passed as pointers, the variable doesn't need to
be returned.
x1 = utilMap.Map(0)
x1.Add("a",0)
def inFunc(map):
    map.Add("b",1)
inFunc(x1)
print(x1.Get("b"))
> 1 
"""
