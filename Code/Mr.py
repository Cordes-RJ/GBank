# -*- coding: utf-8 -*-
"""
Mr. contains the manager class which handles the interactions between
the many scripts and the flow of the program itself
"""
import logger
import parameters
import warehouse
import bagnonSoup

class Manager:
    def __init__(self):
        logger.Start() # begin Logging
        # instantiate parameters
        self.paramLedger = parameters.Ledgerman() # instantiate parameters
        #self.warehouseLedger = warehouse.Build(self.paramLedger.GetWarehousePath())
    def Test(self):
        return warehouse.Build(self.paramLedger.GetWarehousePath())
    # BagUpdate grabs items from bagbrother and updates the ledger
    def BagUpdate(self):
        return bagnonSoup.Parser().Parse(self.paramLedger.GetBagPath(),self.paramLedger.characterWL)

#%%
m = Manager()
