# -*- coding: utf-8 -*-
"""
Mr. contains the manager class which handles the interactions between
the many scripts and the flow of the program itself
"""

import utilMap
import logger
import parameters
import atomicity
import warehouse
import bagnonSoup
import manualAdd
import woad
import wowhead
import utilTime
import utilFile
import utilParse
import currency

class Manager:
    def __init__(self):
        self.Timer = utilTime.StopWatch()
        self.GoldFound = 0                                                      # needed later
        self.TotalCommoditiesValue = 0                                          # needed later
        logger.Start()                                                          # begin Logging
        # instantiate parameters
        self.paramLedger = parameters.Ledgerman()                              # instantiate parameters
        self.PrintToggle = self.paramLedger.GetPrintToggle()
        self.PrintUpdate("StartUp","File Check")
        # ensure necessary files are available before continuing
        if self.AtomicityCheck():                                               # for readability
            pass
        self.PrintUpdate("File Check","Warehouse Construction")
        # build warehouse ledger
        self.warehouseLedger = warehouse.Build(self.paramLedger.GetWarehousePath())
        self.PrintUpdate("Warehouse Construction","Bag Scrape")
        # update for bag contents with new counts
        self.BagUpdate()
        self.PrintUpdate("Bag Scrape","Scrape for manually added items")
        # add itemIDs from manualAdd
        self.ManualAddUpdate()
        self.PrintUpdate("Scrape for manually added items","Auction Data Scrape")
        # do a price check on whitelisted items
        self.PriceCheck()
        self.PrintUpdate("Auction Data Scrape", "Wowhead Scrape")
        # scrape WowheadInfo
        self.WowHeadScrape()
        self.PrintUpdate("Wowhead Scrape", "File Update Preparation")
        # Prepare file contents
        self.CalculateMarketValue()
        VaultEntry = self.CreateVaultEntry()
        Ledger = self.LedgerToCsvBlob()
        # check again to ensure the files are available
        if self.AtomicityCheck():                                               # for readability
            pass
        self.PrintUpdate("File Update Preparation", "Writing to GBank")
        self.WriteVaultEntry(VaultEntry)
        self.WriteWarehouseFile(Ledger)
        self.ClearManualAdd()
        self.PrintUpdate("Writing to GBank", "To prepare for closure")
        self.PrintFinal()
    def PrintUpdate(self,LastStage,CurrentStage):
        if self.PrintToggle:
            print("Completed " + LastStage + " after " + self.Timer.getLapTimeString(5) + ".\nStarting " + CurrentStage + "...")
    def PrintFinal(self):
        if self.PrintToggle:
            print("Finished update after " + self.Timer.getFullTimeString(5))
    def AtomicityCheck(self):
        return atomicity.Check(self.paramLedger)
    # BagUpdate grabs items from bagbrother and updates the ledger
    def BagUpdate(self):
        whiteList = bagnonSoup.WhiteList(self.paramLedger.GetServerName(),self.paramLedger.GetCharacters())
        foundInBag, self.GoldFound = bagnonSoup.Parser().Parse(self.paramLedger.GetBagPath(),whiteList)
        for itemID in foundInBag.ListKeys():
            if self.warehouseLedger.InMap(itemID):
                self.warehouseLedger.Get(itemID).UpdateCt(foundInBag.Get(itemID))
            else:
                self.warehouseLedger.Add(itemID,warehouse.Item().INITviaIDandCt(itemID,foundInBag.Get(itemID)))
    # Manual Add update grabs items from manualAdd file and adds them to ledger
    def ManualAddUpdate(self):
        IDlist = manualAdd.Parser().Parse(self.paramLedger.GetManualAddPath())
        for itemID in IDlist:
            if not self.warehouseLedger.InMap(itemID):
                self.warehouseLedger.Add(itemID,warehouse.Item().INITviaID(itemID))
    def PriceCheck(self):
        IDwhiteList =  utilMap.CreateMapofEmptyInterfaces(self.warehouseLedger.ListKeys())
        priceList = woad.Parser(IDwhiteList).Parse(self.paramLedger.GetAuctionDataPath(),self.paramLedger.GetServerName())
        for itemID in priceList.ListKeys():
            if self.warehouseLedger.InMap(itemID):
                self.warehouseLedger.m[itemID].UpdatePrice(priceList.Get(itemID))
    def WowHeadScrape(self):
        header = self.paramLedger.GetScrapeHeader()
        timeout = self.paramLedger.GetScrapeTimeout()
        itemList = []
        for itemID in self.warehouseLedger.ListKeys():
            if self.warehouseLedger.Get(itemID).new:
                itemList.append(itemID)
        whItems = wowhead.Scraper().Scrape(itemList,header,timeout)
        for item in whItems:
            if self.warehouseLedger.InMap(item.itemID):
                self.warehouseLedger.m[item.itemID].UpdateWoWheadInfo(item)
    def CalculateMarketValue(self):
        for itemID in self.warehouseLedger.ListKeys():
            self.TotalCommoditiesValue += self.warehouseLedger.m[itemID].CalcAndGetmarketValue()
    def CreateVaultEntry(self):
        self.GoldFound = currency.GoldFloat(self.GoldFound)
        List = [utilTime.getDateString(),self.GoldFound+self.TotalCommoditiesValue,self.GoldFound,self.TotalCommoditiesValue]
        return utilFile.ListOfItemsToCSVRow(List)
    def LedgerToCsvBlob(self):
        Blob = "index,itemID,Name,Link,Rarity,IconName,Type,Subtype,LastPrice,Ct,MrktVal"
        itemIDs = utilParse.DeepCopyList(self.warehouseLedger.ListKeys())
        currentIdx = 0
        for itemID in itemIDs:
            Blob += "\n" + self.warehouseLedger.m[itemID].ToCSVrow(currentIdx)
            self.warehouseLedger.Del(itemID)
            currentIdx += 1
        return Blob
    def WriteVaultEntry(self, VaultEntry):
        try:
            with open(self.paramLedger.GetVaultPath(), "a+") as Vault:
                Vault.write("\n"+VaultEntry)
                Vault.close()
        except Exception:
            errMessage = "Error in writing vaultEntry to vault|check vaultFile or Mr.Py"
            logger.Log("Mr","WriteVaultEntry","Critical", errMessage, LogAndKill = True)
            # exit program
    def WriteWarehouseFile(self, CSVblob):
        try:
            with open(self.paramLedger.GetWarehousePath(), "w") as Warehouse:
                Warehouse.write(CSVblob)
        except Exception:
            errMessage = "Error in writing to Warehouse|check warehouse file or Mr.Py"
            logger.Log("Mr","WriteWarehouseFile","Critical", errMessage, LogAndKill = True)
            # exit program
    def ClearManualAdd(self):
        utilFile.Erase(self.paramLedger.GetManualAddPath())

"""
Manager()
"""
