# -*- coding: utf-8 -*-
"""
Mr. contains the manager class which handles the interactions between
the many scripts and the flow of the program itself
"""
import logger
import parameters
import atomicity
import warehouse
import bagnonSoup

class Manager:
    def __init__(self):
        logger.Start()                                                          # begin Logging
        # instantiate parameters
        self.paramLedger = parameters.Ledgerman()                               # instantiate parameters
        # ensure necessary files are available before continuing
        if self.AtomicityCheck():                                               # for readability
            pass
        # build warehouse ledger
        self.warehouseLedger = warehouse.Build(self.paramLedger.GetWarehousePath())
        # update for bag contents with new counts
    def AtomicityCheck(self):
        return atomicity.Check(self.paramLedger)
    # BagUpdate grabs items from bagbrother and updates the ledger
    def BagUpdate(self):
        return bagnonSoup.Parser().Parse(self.paramLedger.GetBagPath(),self.paramLedger.characterWL)

#%%
#x = [Manager().BagUpdate()]
