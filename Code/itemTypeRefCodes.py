# -*- coding: utf-8 -*-
"""
ItemTypeRefCodes is a file which defines a two-way lookup for reference codes
in the interest of limiting the holding of large strings during other
operations prior to writing back to warehouse.csv
"""

import utilMap
global itemReferenceCodes


def createRefCode(mainID, subID):
    code = mainID*100+subID+100
    if code in itemReferenceCodes.ListKeys(True):
        return code
    return 0

def getRefCodefromString(string):
    return itemReferenceCodes.Get(False,string)
    
def getStringFromRefCode(refCode):
    return itemReferenceCodes.Get(True,refCode)
    
# define itemRefs
itemRefs = [
        [97,'Consumables,Item Enhancements (Temporary)'],
        [100,'Consumables,Misc'],
        [101,'Consumables,Potions'],
        [102,'Consumables,Elixirs'],
        [104,'Consumables,Scrolls'],
        [105,'Consumables,Food & Drinks'],
        [106,'Consumables,Item Enhancements (Permanent)'],
        [200,'Containers,Bags'],
        [300,'Weapons,One-Handed Axes'],
        [301,'Weapons,Two-Handed Axes'],
        [302,'Weapons,Bows'],
        [303,'Weapons,Guns'],
        [304,'Weapons,One-Handed Maces'],
        [305,'Weapons,Two-Handed Maces'],
        [306,'Weapons,Polearms'],
        [307,'Weapons,One-Handed Swords'],
        [308,'Weapons,Two-Handed Swords'],
        [310,'Weapons,Staves'],
        [313,'Weapons,Fist Weapons'],
        [314,'Weapons,Miscellaneous (Weapons)'],
        [315,'Weapons,Daggers'],
        [316,'Weapons,Thrown'],
        [317,'Weapons,Spear (shouldnt exist)'],
        [318,'Weapons,Crossbows'],
        [319,'Weapons,Wands'],
        [320,'Weapons,Fishing Poles'],
        [492,'Armor,Shirts'],
        [493,'Armor,Tabards'],
        [494,'Armor,Cloaks'],
        [495,'Armor,Off-hand Frills'],
        [496,'Armor,Trinkets'],
        [497,'Armor,Amulets'],
        [498,'Armor,Rings'],
        [500,'Armor,Miscellaneous (Armor)'],
        [501,'Armor,Cloth Armor'],
        [502,'Armor,Leather Armor'],
        [503,'Armor,Mail Armor'],
        [504,'Armor,Plate Armor'],
        [506,'Armor,Shields'],
        [702,'Projectiles,Arrows'],
        [703,'Projectiles,Bullets'],
        [800,'Trade Goods,Misc'],
        [801,'Trade Goods,Parts'],
        [802,'Trade Goods,Explosives'],
        [803,'Trade Goods,Devices'],
        [805,'Trade Goods,Cloth'],
        [806,'Trade Goods,Leather'],
        [807,'Trade Goods,Metal & Stone'],
        [808,'Trade Goods,Meat'],
        [809,'Trade Goods,Herbs'],
        [810,'Trade Goods,Elemental'],
        [811,'Trade Goods,Other (Trade Goods)'],
        [812,'Trade Goods,Enchanting'],
        [1000,'Recipes,Books'],
        [1001,'Recipes,Leatherworking Patterns'],
        [1002,'Recipes,Tailoring Patterns'],
        [1003,'Recipes,Engineering Schematics'],
        [1004,'Recipes,Blacksmithing Plans'],
        [1005,'Recipes,Cooking Recipes'],
        [1006,'Recipes,Alchemy Recipes'],
        [1007,'Recipes,First Aid Books'],
        [1008,'Recipes,Enchanting Formulae'],
        [1300,'Quest,Misc'],
        [1400,'Keys,Misc'],
        [1600,'Miscellaneous,Junk'],
        [1601,'Miscellaneous,Reagents'],
        [1602,'Miscellaneous,Companions'],
        [1603,'Miscellaneous,Holiday'],
        [1604,'Miscellaneous,Other (Miscellaneous)'],
        [1605,'Miscellaneous,Mounts'],
        [0,'unmapped,unmapped']
        ]

itemReferenceCodes = utilMap.TwoWayMap("Other,Misc",0)
for item in itemRefs:
    itemReferenceCodes.Set(True,item[0],item[1])

del itemRefs
"""
x = getRefCodefromString("Recipes,Cooking")
y = getStringFromRefCode(1004)
"""

