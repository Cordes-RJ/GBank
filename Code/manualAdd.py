# -*- coding: utf-8 -*-

import utilFile
import logger
import utilParse

def getFileContent(path):
    Lines = utilFile.ReadIn_lines(path)
    if len(Lines) <= 0:
        # for readability
        errMessage = "Error getting manualAdd file|check parameters"
        logger.Log("manualAdd","getFileContent","Critical", errMessage, LogAndKill = True)
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
class Parser:
    def __init__(self):
        pass
    def Parse(self,FilePath,ItemMap):
        return addLinestoItemMap(getFileContent(FilePath),ItemMap)
        
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
