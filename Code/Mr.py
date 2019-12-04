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

class Manager:
    def __init__(self):
        self.GoldFound = 0                                                      # needed for later
        logger.Start()                                                          # begin Logging
        # instantiate parameters
        self.paramLedger = parameters.Ledgerman()                               # instantiate parameters
        # ensure necessary files are available before continuing
        if self.AtomicityCheck():                                               # for readability
            pass
        # build warehouse ledger
        self.warehouseLedger = warehouse.Build(self.paramLedger.GetWarehousePath())
        # update for bag contents with new counts
        self.BagUpdate()
        # add itemIDs from manualAdd
        self.ManualAddUpdate()
        # do a price check on whitelisted items
        self.PriceCheck()
        # scrape WowheadInfo
        self.WowHeadScrape()
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
                self.warehouseLedger.m[itemID].LastPrice = priceList.Get(itemID)
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
        
#%%
x = [Manager()]
#%%
x[0].WowHeadScrape()

#%%
                
x = [Manager().BagUpdate()]
