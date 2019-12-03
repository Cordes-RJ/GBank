# -*- coding: utf-8 -*-
"""
ItemTypeRefCodes is a file which defines a two-way lookup for reference codes
in the interest of limiting the holding of large strings during other
operations prior to writing back to warehouse.csv
"""

import utilMap
global itemReferenceCodes


def createRefCode(mainID, subID):
    if mainID > 9: # odd items, just return an unknown
        return 0
    code = mainID*100+subID+100
    if code in itemReferenceCodes.keys():
        return code
    return 0

def getRefCodefromString(string):
    return itemReferenceCodes.Get(False,string)
    
def getStringFromRefCode(refCode):
    return itemReferenceCodes.Get(True,refCode)
    
# define itemRefs
itemRefs = [
        [100,"Consumable,Other"],
        [101,"Consumable,Potion"],
        [102,"Consumable,Elixir"],
        [103,"Consumable,Flask"],
        [104,"Consumable,Scroll"],
        [105,"Consumable,Food & Drink"],
        [106,"Item Enhancement,Item Enhancement"],
        [107,"Consumable,Bandage"],
        [108,"Consumable,Other"],
        [200,"Bag,Bag"],
        [201,"Bag,Soul Bag"],
        [202,"Bag,Herb Bag"],
        [203,"Bag,Enchanting Bag"],
        [204,"Bag,Engineering Bag"],
        [205,"Bag,Gem Bag"],
        [206,"Bag,Mining Bag"],
        [207,"Bag,Leatherworking Bag"],
        [208,"Bag,Inscription Bag"],
        [300,"Weapon,Axe"],
        [301,"Weapon,2hAxe"],
        [302,"Weapon,Bow"],
        [303,"Weapon,Gun"],
        [304,"Weapon,Mace"],
        [305,"Weapon,2hMace"],
        [306,"Weapon,Polearm"],
        [307,"Weapon,Sword"],
        [308,"Weapon,2hSword"],
        [309,"Weapon,Obsolete"],
        [310,"Weapon,Staff"],
        [311,"Weapon,Exotic"],
        [312,"Weapon,Exotic"],
        [313,"Weapon,Fist Weapon"],
        [314,"Weapon,Miscellaneous"],
        [315,"Weapon,Dagger"],
        [316,"Weapon,Thrown"],
        [317,"Weapon,Spear"],
        [318,"Weapon,Crossbow"],
        [319,"Weapon,Wand"],
        [320,"Trade Goods,Fishing"],
        [400,"Jewelcrafting,Red"],
        [401,"Jewelcrafting,Blue"],
        [402,"Jewelcrafting,Yellow"],
        [403,"Jewelcrafting,Purple"],
        [404,"Jewelcrafting,Green"],
        [405,"Jewelcrafting,Orange"],
        [406,"Jewelcrafting,Meta"],
        [407,"Jewelcrafting,Simple"],
        [408,"Jewelcrafting,Prismatic"],
        [500,"Gear,Miscellaneous"],
        [501,"Gear,Cloth"],
        [502,"Gear,Leather"],
        [503,"Gear,Mail"],
        [504,"Gear,Plate"],
        [505,"Gear,Buckler(OBSOLETE)"],
        [506,"Gear,Shield"],
        [507,"Item Enhancement,Libram"],
        [508,"Gear,Idol"],
        [509,"Gear,Totem"],
        [510,"Gear,Sigil"],
        [600,"Trade Goods,Reagent"],
        [700,"Gear,Wand(OBSOLETE)"],
        [701,"Ammo,Bolt(OBSOLETE)"],
        [702,"Ammo,Arrow"],
        [703,"Ammo,Bullet"],
        [704,"Ammo,Thrown(OBSOLETE)"],
        [800,"Trade Goods,Trade Goods"],
        [801,"Trade Goods,Parts"],
        [802,"Trade Goods,Explosives"],
        [803,"Trade Goods,Devices"],
        [804,"Trade Goods,Jewelcrafting"],
        [805,"Trade Goods,Cloth"],
        [806,"Trade Goods,Leather"],
        [807,"Trade Goods,Metal & Stone"],
        [808,"Trade Goods,Cooking"],
        [809,"Trade Goods,Herb"],
        [810,"Trade Goods,Elemental"],
        [811,"Trade Goods,Other"],
        [812,"Trade Goods,Enchanting"],
        [813,"Trade Goods,Materials"],
        [814,"Item Enhancement,Armor Enchantment"],
        [815,"Item Enhancement,Weapon Enchantment"],
        [900,"Other,Generic(OBSOLETE)"],
        [1000,"Tomes,Book"],
        [1001,"Recipes,Leatherworking"],
        [1002,"Recipes,Tailoring"],
        [1003,"Recipes,Engineering"],
        [1004,"Recipes,Blacksmithing"],
        [1005,"Recipes,Cooking"],
        [1006,"Recipes,Alchemy"],
        [1007,"Recipes,First Aid"],
        [1008,"Recipes,Enchanting"],
        [1009,"Recipes,Fishing"],
        [1010,"Recipes,Jewelcrafting"],
        [0,"Other,Misc"],
        ]

itemReferenceCodes = utilMap.TwoWayMap("Other,Misc",0)
for item in itemRefs:
    itemReferenceCodes.Set(True,item[0],item[1])

del itemRefs
"""
x = getRefCodefromString("Recipes,Cooking")
y = getStringFromRefCode(1004)
"""

"""
id	subid	primary	subclass
0	0	Consumable	Other
0	1	Consumable	Potion
0	2	Consumable	Elixir
0	3	Consumable	Flask
0	4	Consumable	Scroll
0	5	Consumable	Food & Drink
0	6	Item Enhancement	Item Enhancement
0	7	Consumable	Bandage
0	8	Consumable	Other
1	0	Bag	Bag
1	1	Bag	Soul Bag
1	2	Bag	Herb Bag
1	3	Bag	Enchanting Bag
1	4	Bag	Engineering Bag
1	5	Bag	Gem Bag
1	6	Bag	Mining Bag
1	7	Bag	Leatherworking Bag
1	8	Bag	Inscription Bag
2	0	Weapon	Axe
2	1	Weapon	2hAxe
2	2	Weapon	Bow
2	3	Weapon	Gun
2	4	Weapon	Mace
2	5	Weapon	2hMace
2	6	Weapon	Polearm
2	7	Weapon	Sword
2	8	Weapon	2hSword
2	9	Weapon	Obsolete
2	10	Weapon	Staff
2	11	Weapon	Exotic
2	12	Weapon	Exotic
2	13	Weapon	Fist Weapon
2	14	Weapon	Miscellaneous
2	15	Weapon	Dagger
2	16	Weapon	Thrown
2	17	Weapon	Spear
2	18	Weapon	Crossbow
2	19	Weapon	Wand
2	20	Trade Goods	Fishing
3	0	Jewelcrafting	Red
3	1	Jewelcrafting	Blue
3	2	Jewelcrafting	Yellow
3	3	Jewelcrafting	Purple
3	4	Jewelcrafting	Green
3	5	Jewelcrafting	Orange
3	6	Jewelcrafting	Meta
3	7	Jewelcrafting	Simple
3	8	Jewelcrafting	Prismatic
4	0	Gear	Miscellaneous
4	1	Gear	Cloth
4	2	Gear	Leather
4	3	Gear	Mail
4	4	Gear	Plate
4	5	Gear	Buckler(OBSOLETE)
4	6	Gear	Shield
4	7	Item Enhancement	Libram
4	8	Gear	Idol
4	9	Gear	Totem
4	10	Gear	Sigil
5	0	Trade Goods	Reagent
6	0	Gear	Wand(OBSOLETE)
6	1	Ammo	Bolt(OBSOLETE)
6	2	Ammo	Arrow
6	3	Ammo	Bullet
6	4	Ammo	Thrown(OBSOLETE)
7	0	Trade Goods	Trade Goods
7	1	Trade Goods	Parts
7	2	Trade Goods	Explosives
7	3	Trade Goods	Devices
7	4	Trade Goods	Jewelcrafting
7	5	Trade Goods	Cloth
7	6	Trade Goods	Leather
7	7	Trade Goods	Metal & Stone
7	8	Trade Goods	Cooking
7	9	Trade Goods	Herb
7	10	Trade Goods	Elemental
7	11	Trade Goods	Other
7	12	Trade Goods	Enchanting
7	13	Trade Goods	Materials
7	14	Item Enhancement	Armor Enchantment
7	15	Item Enhancement	Weapon Enchantment
8	0	Other	Generic(OBSOLETE)
9	0	Tomes	Book
9	1	Recipes	Leatherworking
9	2	Recipes	Tailoring
9	3	Recipes	Engineering
9	4	Recipes	Blacksmithing
9	5	Recipes	Cooking
9	6	Recipes	Alchemy
9	7	Recipes	First Aid
9	8	Recipes	Enchanting
9	9	Recipes	Fishing
9	10	Recipes	Jewelcrafting
10	0	Other	Money(OBSOLETE)
11	0	Bag	Quiver(OBSOLETE)
11	1	Bag	Quiver(OBSOLETE)
11	2	Bag	Quiver
11	3	Bag	Ammo Pouch
12	0	Other	Quest
13	0	Other	Key
13	1	Other	Lockpick
14	0	Other	Permanent
15	0	Other	Junk
15	1	Trade Goods	Reagent
15	2	Other	Pet
15	3	Other	Holiday
15	4	Other	Other
15	5	Other	Mount
16	1	Other	Warrior
16	2	Other	Paladin
16	3	Other	Hunter
16	4	Other	Rogue
16	5	Other	Priest
16	6	Other	Death Knight
16	7	Other	Shaman
16	8	Other	Mage
16	9	Other	Warlock
16	11	Other	Druid
"""