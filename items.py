from dataclasses import dataclass, field

@dataclass()
class Item:
    name: str
    tag: int
    description: str
    cost: int
    effect: str
    duration: int
    tierz: int
    hup: int=0
    pup: int=0
    minup: int=0
    maxup: int=0
    critup: int=0
    untype: str="pot"
    typeobj: str="item"
    

# Buff Potions
# name, tag, description, cost, effect, duration, tier, healthup, powerup, minup, maxup, critup, untype(pot or item)
ppot = Item("Power Potion", 100, "A basic potion which increases your attack power by 20 for 3 fights",
500, "increases attack power by 20", 3, 1, 0, 20, 0, 0, 0, "pot")
hpot = Item("Health Potion", 101, "A basic health potion which increases your health by 30 for 2 fights",
600, "Increases health by 30", 2, 1, 30, 0, 0, 0, 0, "pot")
lblet = Item("Lucky Bracelet", 102, "A bracelet which increases your crit chance by 10% for 2 fights",
650, "Increases Crit Chance by 10%", 2, 1, 0, 0, 0, 0, 10, "item")
mpot = Item("Mixa Pot", 201, "A potion carefully brewed increasing your power and health by 50 for 2 fights",
1100, "Increases health and power by 50", 2, 2, 50, 50, 0, 0, 0, "pot")
sring = Item("Special Ring", 202, "A ring which increases your min and max damage by 30 for 3 fights",
1200, "Increases min and max damage by 30", 3, 2, 0, 0, 30, 30, 0, "item")
mcloak = Item("Magic Cloak", 203, "Fairly dusty, but seems to increase all of your stats by 15 for 5 fights",
1000, "Increases all stats by 15", 5, 2, 15, 15, 15, 15, 15, "item")
gpapple = Item("Golden Pineapple", 301, "A golden pineapple that when it's juice is drunk, increases health by 150 and power by 40 for 2 fights",
2300, "Increases health by 150, and power by 40", 2, 3, 150, 40, 0, 0, 0, "pot")
fsash = Item("Sash of FOCUS", 401, "A sash worn around the forehead that helps you to survive an OHKO. Lasts until activated",
10000, "Ripped sash and survived an OHKO", 6666, 4, 0, 0, 0, 0, 0, "item")
boe = Item("Band Of Experience", 402, "A band said to increase exp gain by 20% from all sources",
50000, "Increases exp gain by 20% from all sources", 5, 4, 0, 0, 0,0, 0, "item")
lc = Item("Lucky Coin", 501, "A coin which increases money earned by 1.5", 200000, "increases money gain by 1.5x",
5,5, 0,0,0,0,0, "item")
ohkoscarf = Item("OHKO scarf", 601, "A sacred scarf that gives you a 5/100 chance to OHKO an enemy on first turn. Lasts until activated",
1200000, "Ripped scarf and One Hit KO enemy", 66666, 6, 0, 0, 0, 0, 0, "item")

ksc = Item("Kevin's Secret Candy", 999, "A rare item said to increase your levels by 5 when mixed with water. Has a 3% chance of dropping from defeated enemies",
0, "Increases level by 5", 1, 2, untype="pot")


potlist = [ppot, hpot, lblet, 
mpot, sring, mcloak,
gpapple, 
fsash, boe,
lc,
ohkoscarf]
allpotlist = [ksc]
for t in potlist:
    allpotlist.append(t)

