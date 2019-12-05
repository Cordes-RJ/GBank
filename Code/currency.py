# -*- coding: utf-8 -*-

class WoW:
    def __init__(self,gold,silver,copper):
        self.gold = int(gold)
        self.silver= int(silver)
        self.copper = int(copper)
    def toString(self):
        return ("g:"+str(self.gold)+"|"+str(self.silver)+"|"+str(self.copper))

def IntToGold(integer):
    copper = integer % 100
    integer = (integer-copper)/100
    silver = integer%100
    gold = (integer-silver)/100
    return WoW(gold,silver,copper)
    
def GoldFloat(integer):
    return round(integer/10000,4)
