# -*- coding: utf-8 -*-
import utilFile
import utilMap
import logger
import pandas as pd

def getFileContent(parameterPath,characterListpath):
    ParameterStrings = pd.read_csv(parameterPath)
    if len(ParameterStrings) <= 0:
        # for readability
        errMessage = "Error getting parameters file|check parameters"
        logger.Log("parameters","getFileContent","Critical", errMessage, LogAndKill = True)
        # exit program
    characters = utilFile.ReadIn_lines(characterListpath)
    if len(characters) <= 0:
        # for readability
        errMessage = "Error getting characters file|check character white list"
        logger.Log("parameters","getFileContent","Critical", errMessage, LogAndKill = True)
        # exit program
    return buildFromParameterStrings(ParameterStrings), characters

def buildFromParameterStrings(ParameterStrings):
    Map = utilMap.Map(-1)
    for i,i2 in ParameterStrings.iterrows():
        Map.Add(i2['Parameter'],i2['Value'])
    return Map

# Ledgerman keeps account of parameters and character whitelist
class Ledgerman:
    def __init__(self):
        self.params, self.characterWL = getFileContent("parameters.csv","characterWhiteList.csv")
    def GetServerName(self):
        return self.params['ServerName']
    def GetCharacters(self):
        return self.characterWL
    def BuildDrivePath(self,file):
        return self.params['DriveGBankPath']+"\\"+file
    def BuildSavedVarPath(self,file):
        return self.params['SavedVariablesPath']+"\\"+file
    def GetWarehousePath(self):
        return self.BuildDrivePath("warehouse.csv")
    def GetVaultPath(self):
        return self.BuildDrivePath("vault.csv")
    def GetManualAddPath(self):
        return self.BuildDrivePath("manualAdd.csv")
    def GetBagPath(self):
        return self.BuildSavedVarPath("BagBrother.LUA")
    def GetAuctionDataPath(self):
        return self.BuildSavedVarPath("Auc-Stat-Simple.LUA")

