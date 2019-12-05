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
        [103,'Consumables,Flasks'],
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
        [3000,'Trade Goods,Gemstones'], #custom
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

"""
refCode	main id	sub id	main type	sub type
97	-1	-3	Consumables	Item Enhancements (Temporary)
100	0	0	Consumables	Misc
101	0	1	Consumables	Potions
102	0	2	Consumables	Elixirs
104	0	4	Consumables	Scrolls
105	0	5	Consumables	Food & Drinks
106	0	6	Consumables	Item Enhancements (Permanent)
200	1	0	Containers	Bags
300	2	0	Weapons	One-Handed Axes
301	2	1	Weapons	Two-Handed Axes
302	2	2	Weapons	Bows
303	2	3	Weapons	Guns
304	2	4	Weapons	One-Handed Maces
305	2	5	Weapons	Two-Handed Maces
306	2	6	Weapons	Polearms
307	2	7	Weapons	One-Handed Swords
308	2	8	Weapons	Two-Handed Swords
310	2	10	Weapons	Staves
313	2	13	Weapons	Fist Weapons
314	2	14	Weapons	Miscellaneous (Weapons)
315	2	15	Weapons	Daggers
316	2	16	Weapons	Thrown
317	2	17	Weapons	Spear (shouldnt exist)
318	2	18	Weapons	Crossbows
319	2	19	Weapons	Wands
320	2	20	Weapons	Fishing Poles
492	3	-8	Armor	Shirts
493	3	-7	Armor	Tabards
494	3	-6	Armor	Cloaks
495	3	-5	Armor	Off-hand Frills
496	3	-4	Armor	Trinkets
497	3	-3	Armor	Amulets
498	3	-2	Armor	Rings
500	4	0	Armor	Miscellaneous (Armor)
501	4	1	Armor	Cloth Armor
502	4	2	Armor	Leather Armor
503	4	3	Armor	Mail Armor
504	4	4	Armor	Plate Armor
506	4	6	Armor	Shields
702	6	2	Projectiles	Arrows
703	6	3	Projectiles	Bullets
800	7	0	Trade Goods	Misc
801	7	1	Trade Goods	Parts
802	7	2	Trade Goods	Explosives
803	7	3	Trade Goods	Devices
805	7	5	Trade Goods	Cloth
806	7	6	Trade Goods	Leather
807	7	7	Trade Goods	Metal & Stone
808	7	8	Trade Goods	Meat
809	7	9	Trade Goods	Herbs
810	7	10	Trade Goods	Elemental
811	7	11	Trade Goods	Other (Trade Goods)
812	7	12	Trade Goods	Enchanting
1000	9	0	Recipes	Books
1001	9	1	Recipes	Leatherworking Patterns
1002	9	2	Recipes	Tailoring Patterns
1003	9	3	Recipes	Engineering Schematics
1004	9	4	Recipes	Blacksmithing Plans
1005	9	5	Recipes	Cooking Recipes
1006	9	6	Recipes	Alchemy Recipes
1007	9	7	Recipes	First Aid Books
1008	9	8	Recipes	Enchanting Formulae
1300	12	0	Quest	Misc
1400	13	0	Keys	Misc
1600	15	0	Miscellaneous	Junk
1601	15	1	Miscellaneous	Reagents
1602	15	2	Miscellaneous	Companions
1603	15	3	Miscellaneous	Holiday
1604	15	4	Miscellaneous	Other (Miscellaneous)
1605	15	5	Miscellaneous	Mounts
0	0	0	unmapped	unmapped
"""