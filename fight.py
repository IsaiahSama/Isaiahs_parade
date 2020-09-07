import math
from dataclasses import dataclass, field
import copy

@dataclass
class Ability:
    name: str
    description: str
    usename: str
    effect: str
    power: int
    powertick: int
    health: int
    min_dmg_up: int
    max_dmg_up: int
    perhealth: int = 0
    reborn: bool=False
    cooldown: int = 4
    tempcd: cooldown = 4

    def oncd(self):
        if self.cooldown == self.tempcd:
            return False
        else:
            return True

    def cdreduce(self):
        self.tempcd -= 1
        if self.tempcd == 0:
            self.tempcd = self.cooldown


    def reset(self):
        self.tempcd = self.cooldown


    def use(self):
        return self.power, self.powertick, self.health, self.min_dmg_up, self.max_dmg_up, self.perhealth

    def isreborn(self):
        return self.reborn

class Passive(Ability):
    def use(self):
        return self.power, self.powertick, self.health, self.min_dmg_up, self.max_dmg_up, self.perhealth

# Actives

theworld = Ability("Stop Time", "An ability which freezes time and allows the user to attack twice",
"ZA WARUDO!", "has stopped time, and attacked", 1, 0, 0, 0, 0)

swarm = Ability("Swarm", "Creates multiple versions of the user, and increases their power by x1.5 and their health by +30",
"KAGE BUNSHIN NO JUTSU", "'s Shadow clones have arrived. Power increased by x1.5, and health increased by +30. Attacks",
1.5, 0, 30, 0, 0)

blast = Ability("Blast", "Blasts the enemy with a powerful attack increasing dmg by 1.75 and dealing an extra 5 tick dmg. Health reduced by 40",
 "Outer... BLAST!", "'s health is reduced by 40. Power increased by x1.75 and +5 extra damage. Summons a powerful blast and blasts", 1.75, 5, -40,
 0, 0)

deadlygrasp = Ability("Deadly Grasp", "Reaches for the enemy with hands of death dealing an extra 150 damage, and healing for 15 hp",
"Let me grab you with death itself", "'s hands of death emerge, increasing health by 15, and dealing +150 damage to",
1, 150, 15, 0, 0)

critstrike = Ability("Critical Strike", "Is a guaranteed critical hit that does 2x damage instead of 1.5", "Scared of my Guaranteed critical hit?",
"raises their crit chance to 100% and does double damage to", 2, 0, 0, 0, 0)

pickelize = Ability("Pickelize", "Stole Rick's Formula. Now turn into a pickle, heal up, and roll over enemies for x1.5 +10 dmg",
"IT'S PICKLE RICK", "turns into a giant pickle, heals 5 hp, increases dmg by x1.5 + 10 then rolls over", 1.5, 10, 5, 0,0)

sonic = Ability("Pocket Ring", "Learnt from the Hedgehog Sonic himself. Increases min and max dmg by 20", "Gotta go fast", 
"increases their min and max dmg by 20 and hit", 1, 5, 0, 20, 20)

jajanken = Ability("Jajanken", "After 5 months of training with Gon, you have now achieved a weaker jajanken. Increases damage by x2.3, but does 500 damage to the user.",
"SAISHO WA GUU... JAN... KEN...", "sacrifices 500 hp and blasts", 2.3, 0, -500, 0, 0)

uheal = Ability("Ultra Heal", "A sacred technique used to heal for 10% of your max health", "The gods have blessed me", "regains 10% of their max health and didn't attack",
1, 0, 0, 0, 0, 10)

ssuck = Ability("Soul Sucker", "A powerful move which sucks the soul of the enemy dealing 2x dmg and healing for 15hp", "SOUL SUCKER!",
"sucks the soul of", 2, 0, 15, 0, 0)

nmareterror = Ability("Nightmare Terror", "Finds the targets worse nightmare and strikes them with it dealing 1.6x damage + 50 damage", 
"Know the terror of nightmares", "Casts a sleep spell then causes nightmares to", 1.6, 50, 0, 0, 0)

slag = Ability("Slag", "Has a 1 in 6 chance of applying Slag to the target, causing them to take 1.5x damage for 2 turns",
"You... have been slagged", "now takes 1.5x damage for the next", 1.5, 0, 0, 0, 0)

psusanoo = Ability("Perfect Susanoo", "The perfected susanoo. Increases power of attack by 2.5x but reduces min and max damage by 20",
"Know the power, of my Perfect Susanoo", "exponentially increases power, steals 20 min and max damage from you then attacks", 2.5, 0, 0, 
20, 20)


# Passives

dodge = Passive("Dodge", "Has a 25% chance to dodge the attack of an enemy.", "You didn't miss me... I dodged it", "dodged",
0, 0, 0, 0 , 0)

counter = Passive("Counter", "Loses 30 hp. Attacks the enemy on their turn dealing 0.75x the damage they gave you. 15% chance", "FULL COUNTER",
"Lost 30 hp, but sent 1.3x the damage received to", 0.75, 0 , -30, 0, 0)

regeneration = Passive("Regeneration", "Gains 10% hp at the end of every turn", "Regen go brr", "Gained 10% hp", 0, 0, 0, 0, 0, 10)

rage = Passive("Rage", "Increases min damage and max damage by 25 each turn when hp is below 1/3 of their hp and heals for 5%", "GRRRR... NOW I'm ANGRY", "increased min and max damage by 25 and healed for 5% hp", 1, 0, 0, 25, 25,5)

sharpeye = Passive("Sharp Eye", "25% Proc Chance. Deals a critical hit for x1.2 damage. Can stack with regular crit", "Sharp Eye",
"has tightened their focus, increased their power by x1.2, then attacks", 1.2, 0,0,0,0)

sboost = Passive("Speed Boost", "Goes First and deals 1.2x dmg on first hit", "Speed Boost", "Attacks first and deals bonus dmg to", 1, 0, 0, 0, 0)

critblock = Passive("Critical Guard", "All critical hits against you deal x0.75 instead of x1.5. 2 in 3 chance of occuring", "Critical Guard","Reduces your critical damage to only 0.75x the original", 0.75,0,0,0,0)

chubz = Passive("Chubby", "large size acts as a shock absorber, and enemy attacks do -50 damage", "Absorbs 50 damage", "Feel my chubzzz",
1, -50, 0, 0, 0)

nlove = Passive("Nightmare Lover", "Feeds off of the memories of your nightmares and heals itself. Increases it's max damage by 5 each time",
"Lover of Nightmares", "gets energies from nightmares within", 1, 0, 10, 5, 5, 0)

haohaki = Passive("Haoshoku Haki", "Needs: Conqueror's Haki: Increases min and max damage by 20 (30 with set bonus) for each passing turn.\nSet Bonus: Anyone below 500 hp of the user loses 100 hp every turn\nOtherwise. No effect"
, "Know the power of one who is worthy", "Increases min and max damage by 20(30 with set bonus)", 1, 0, 0, 50, 50)

balancepride = Passive("Pride of Balance", "Requires: Yin Blade and Yang Armour set. Increases power of attack by 100 (100 True Damage) and heals for 100 hp on user's turn. Otherwise: No Effect"
,"The emodiment of Balance I am", "Increases power by 100. Heals for 200", 1, 100, 200, 0, 0)

tob = Passive("Tide Of Battle", "A Passive sprung from love of battle, and dominance on the battlefield. Increases min and max dmg by 3% every turn",
"The battle shifts in my favour", "Increases health, min and max dmg by 3%",0,0,0,0,0, reborn=True)

# Unique
plague = Ability("The Plague", "...?'s special abiltiy which poisons the victim. Has a base damage of 100 increases by 50 for 3 turns, Unique to ...?",
 "wishes death upon You", "Summons The Plague and infects",1, 100, 0, 0, 0)

czw = Ability("Celestial's ZA WARUDO", "CelestialG's special ability which stops time for 3 turns",
"THIS IS MY ZA WARUDO!", "has stopped time, and attacked", 1, 20, 0, 0, 0)

suffocation = Ability("Suffocation", "Ability of Trxsh. Has 4 in 10 chance of proccing. Removes 5% of opponents health for 4 turns",
"SHINE... BAKAYARO", "Removes 5% of health from",1, 0, 0, 0, 0, cooldown=5)

massinc = Ability("Mass increase", "The big one's ability... Bigger and bigger... Doubles damage and heals for 10% hp",
"BIGGUMS... BIG!!!", "enlarges, doubles power, then attacks", 2.5, 0, 0, 0, 0, 10)

nklk = Passive("No Kill Like Overkill", "A sacred ability belonging to Trxsh. All extra damage done to him is added on to his power for his next turn",
"NO KILL LIKE OVERKILL", "stole all extra power and overkilled", 1, 0, 0, 0, 0)

bproc = Passive("Belly Protection", "Won't be hurting this chub. Decreases all damage above 10k by 30% and heals for 4%hp",
"Jigglessss", "heals for 3%hp and reduces damage by 30%", 0, 0, 0, 0, 0, 3)


# Raid Enemies
bebebeslam = Ability("BBB slam!", "Giant King B B B, belly flops dealing 1.3x dmg and hitting 3 people", "BE BE BE... SLAM!", 
"belly flops dealing 1.3x dmg, healing for 10hp", 1.3, 0, 10, 0, 0)

# Biggums
bellybump = Ability("Belly Belly Bounce", "Massive user dashes at an immense speed and bounces the enemy", "Belly... Belly... BOUNCE!",
"charges gaining x1.4 strength increasing min and max damage by 10, and then bounces", 1.4, 0, 0, 10, 10)

abilities = [theworld, swarm, blast, deadlygrasp, critstrike, pickelize, sonic, jajanken, uheal, slag, ssuck, nmareterror]
allabilities = [plague, psusanoo, czw, suffocation, massinc]
for thing in abilities:
    allabilities.append(thing)

passives = [dodge, counter, regeneration, rage, sharpeye, sboost, critblock, nlove, chubz, tob]
allpassives = [haohaki, balancepride, nklk, bproc]
for thing in passives:
    allpassives.append(thing)

# Weapons
@dataclass
class Weapons:
    name: str
    tag: int
    description: str
    effect: str
    damage: int= 0
    critplus: int=0
    lifesteal: int=0
    cost: int=0
    tierz: int=1
    typeobj: str="Weapon"

    def islifesteal(self):
        if self.lifesteal != 0:
            return True
        return False

fist = Weapons("Fist", 1001, "The original method of attacking (default)", "punches")
katana = Weapons("Katana",1002, "Then, they were katanas.", "slices", 5, 2, cost=250)
bow = Weapons("Bow", 1003, "This one doesn't need arrows", "shoots", 6, 1, cost=255)
pistol = Weapons("Pistol", 1004, "Pew pew", "shoots", 8, 3, cost=300)
sword = Weapons("Sword", 1005, "Sword > Pistol", "slices", 10, 3, cost=320)
dagger = Weapons("Dagger", 1006, "Dagger = Sword??", "stabs", 10, 3, cost=320)
slime = Weapons("Baby Slime", 1007, "\"Summons a baby slime to fight for you\"", "bounces on", 9, 7, cost=320)
vampknives = Weapons("Vampire Knives", 1008, "Blood Draining Knives just for you", "drains", 20, 5, 5, cost=700)
fishrod = Weapons("Fishing Rod", 1009, "Gon has lent you his trusty Fishing Rod", "hooks and cuts", 35, 3, cost=450)
axe = Weapons("Axe", 1010, "Axe goes schwing", "slashes", 45, 6, cost=650)
fpan = Weapons("Frying Pan", 1011, "Not a drying pan", "bonks the head of", 27, 20, cost=660)
miracles = Weapons("Miracle Sword", 1012, "Straight from Slimenia", "slashes", 50, 5, 7, 1600, tierz=2)
blaster = Weapons("Blaster", 1013, "Pew Pew times 2", "blasts", 65, 4, cost=1100, tierz=2)
dsword = Weapons("Diamond Sword", 1014, "Has a pixelated edge for bonus damage", "slashes", 67, 5, cost=1100, tierz=2)
bomb = Weapons("Buh-Bomb", 1015, "A souvenir from those Buh-Bombs I had you fight", "explodes on",
85, 8, cost=1400, tierz=2)
crossbow = Weapons("Charged Crossbow", 1016, "Not your average Cross bow", "shocks and shoots", 88, 6, cost=1450, tierz=2)
bsuckler = Weapons("Blood Suckler", 1017, "A strange creature known for draining the blood of enemies", "sucks the blood of", 70, 3, 20, 14000, tierz=3)
sancspear = Weapons("Sanctum Spear", 1018, "Sanctum spear go boom", "pierces", 80, 25, 12, 15000, tierz=3)
stormbreaker = Weapons("Stormbreaker", 1019, "A gift from Thor himself. A replica at best", "slashes and zaps", 100, 25, cost=20000, tierz=3)
hcard = Weapons("Playing Cards", 1020, "Wait... aren't these Hisoka's?", "slices", 120, 15, 0, 23000, 3)
seruption = Weapons("Solar Eruption", 1021, "Made with 100% Solar Fragments", "pierces",
130, 10, cost=25000, tierz=3)
vibechk = Weapons("The Vibe Check", 1022, "Yuh need to relax", "Checks the vibe on", 350, 70, 0, 100000, tierz=4)
tsummon = Weapons("Tank Summon", 1023, "Wait... what?", "summons a tank which blasts", 370, 25, 0, 300000, tierz=4)
sfknife = Weapons("Shadow Flame Knife", 1024, "Crafted from sorcery", "stabs and burns", 430, 15, 5, 300000, tierz=4)
srifle = Weapons("Sniper Rifle", 1025, "Never miss a shot", "Snipes", 300, 40, 4, cost=300000, tierz=4)

# Tier 5
evampknife = Weapons("Enchanted Vamp Knife", 1026, "Vampire knife, but enchanted with the blood of many", "drains the blood of", 600, 7, 20, 1000000, 5)
dreamsword = Weapons("Dream Sword", 1027, "Crafted from the essence of the light side of sleep", "steals the dreams of", 700, 15, 2, 1000000, 5)
herorian = Weapons("The Herorian", 1028, "The prized Spinning Top of the legendary Herorian from Heroria", "spins into", 800, 3, 1, 1000500, 5)
daxe = Weapons("Deathly Axe", 1033, "Said to bring out the true power of Deadly Grasp, and linked directly to Azoth himself. But leeches off of 2% of the users hp",
"reveals death to", 750, 20, -2, 1100000, 5)
emace = Weapons("Energy Mace", 1034, "Made of concentrated chak-- energy", "slams into", 850, 5, 0, 1100000, 5)

# Tier 6
bblade = Weapons("Banana Blaster", 1032, "YAA HOO, not your typical exploding bananas", "fires at", 1800, 40, 3, 5300000, 6)
cqhaki = Weapons("Conqueror Haki", 1029, "A physical manifestation of the ability. Allows the user to use the ability Haoshoku Haki.",
"controls", 2000, 16, 5, 5400000, 6)
yin = Weapons("Yin Blade", 1030, "The physical manifestation of darkness, destruction and negative energy", "alters the existence of", 1800, 20, 5, 5300000, 6)
mhand = Weapons("Master Hand", 1031, "A mysterious floating hand with seemingly immense power used for offense", "sways then strikes", 2000, 30, 10, 5400000, 6)
tblade = Weapons("Tatsuki Blade", 1035, "Said to have the ability to quickly siphon the life force of all that touch it, you included", "drains", 2000, 15, -2, 5500000, 6)

weaponlist = [fist, katana, bow, pistol, sword, dagger, slime, fishrod, axe, fpan, vampknives, 
miracles, blaster, dsword, bomb, crossbow, bsuckler, sancspear, stormbreaker, hcard, seruption, vibechk, 
tsummon, sfknife, srifle, 
evampknife, dreamsword, herorian, daxe, emace,
bblade, cqhaki, yin, mhand, tblade]

# Unique
pds = Weapons("Plague Doctors Scepter", 3001, "Soulbound to ...?", "infects", 0, 10, 15, 0, 6)
parblade = Weapons("Staff of the Parade", 3002, "The Chosen weapon of the Parade Creator", "moderates", 5000, 20, 25, 0, 6)
uth = Weapons("『Unravel the Heavens』", 3003, "He's just standing there, menacingly, with the power of ∞ and ∅!", "shine barrages",
4200, 0, 10, 0, 6)
diowep = Weapons("Celestial's Dio", 3004, "The power of ZA WARUDO is overflowing", "poses then brutally barrages", 3800, 2, 15, 0, 6)
bhammer = Weapons("Biggums Sledge Hammer", 3005, "It's like a sledge hammer... But Bigger", "slams", 3500, 15, tierz=6)

allweapons = [pds, parblade, uth, diowep, bhammer]
for weapon in weaponlist:
    allweapons.append(weapon)

# Armour
@dataclass
class Armour:
    name: str
    tag: int
    description: str
    hpup: int=0
    pup: int=0
    cost: int=0
    regen: int=0
    pairs: object=None
    tierz: int=1
    typeobj: str="Armour"

    def hasregen(self):
        if self.regen == 0:
            return False
        else:
            return True

    def haspair(self):
        if self.pairs == None:
            return False
        else:
            return True


linen = Armour("Linen", 2001, "Some extremely basic and lightweight armour. (default)")
chain = Armour("Chainmail", 2002, "The Typical first set to buy", 5, cost=140)
hunters = Armour("Ranger", 2003, "Blends in with background. Gains set bonus with bow", 7, 2, cost=160)
iron = Armour("Iron", 2004, "Often the go to in Minecraft Speedruns", 10, 2, 270)
gold = Armour("Gold", 2005, "Is gold really better than iron though?", 15, 4, 400)
slimearm = Armour("Slime", 2006, "It's almost like attacks slide right off. Gains set bonus with Baby Slime", 20, 4, 550, 4, slime)
assas = Armour("Assassins", 2007, "Shh, Sneaky. Gains set bonus with Dagger", 20, 4, 550, 3, dagger)
valkryie = Armour("Valkryie", 2008, "Straight from ValHalla. Don't ask. Gains set bonus with axe", 30, 6, 600, pairs=axe)
diamond = Armour("Diamond", 2009, "What's a Diamond Sword, Without Diamond Armor. Gains set bonus with Diamond Sword", 40, 7, 720, 0, dsword)
saiyanguc = Armour("Saiyan Gucchi", 2010, "Special Edition it would seem", 40, 10, 700)
abyss = Armour("Abyss Walker", 2011, "Not from this world", 55, 15, 3000, tierz=2)
paladium = Armour("Paladium", 2012, "Increases life regen", 60, 20, 5500, 15, tierz=2)
cranger = Armour("Charged Ranger", 2013, "An upgrade to Ranger. Shocking I know", 90, 25, 7000, 0, crossbow, tierz=3)
solarflare = Armour("Solar Flare", 2014, "Made from Solar Fragments and Luminite Ore. Gains set bonus with Solar Eruption", 120, 35, 8000, pairs=seruption, tierz=2)
elitist = Armour("Elitist", 2015, "Said to be made for the elites", 150, 40, 10000, tierz=3)
hierro = Armour("Hierro", 2016, "Hard", 200, 50, 50000, 10, tierz=3)
plaguearm = Armour("Plague Doctors Uniform", 2017, "A copy of the original owned by ...?", 200, 50, 50000, 4, tierz=3)
wood = Armour("Wooden", 2018, "Pfft, you *wood* n't get it. Gains set bonus with The Vibe Check", 260, 45, 90000, 7, vibechk, 3)
vknight = Armour("Valhalla Knight", 2019, "Again, Don't ask where I got this from", 100, 30, 500000, 20, tierz=4)
shadowflame = Armour("Shadow Flame", 2020,
"A sorcerer's creation created by shadows and flames of darkness. Gains set bonus with Shadow Flame Knife",
510, 200, 500000, 5, sfknife, 4)
artillery = Armour("Master General", 2021, "mhm yes. Tank uniform. Gains set bonus with Tank Summon", 660, 150, 500000, 0, tsummon, 4)
sranger = Armour("Tundra Ranger", 2022, "Gained from surviving the depth of the Tundra. Gains set bonus with Sniper Rifle", 570, 160, 500000, 4, srifle, 4)

# Tier 5
vampcloak = Armour("Vampiric Cloak", 2023, "Makes it easier to drain blood. Pairs well with Enchanted Vamp Knives", 800, 300, 1100000, 18, evampknife, 5)
nightmare = Armour("Nightmare", 2024, "Woven together from the essence of the dark side of sleep. Gains set bonus with Dream Sword",
800, 420, 1100000, 0, dreamsword, 5)
hshield = Armour("Hero's Shield", 2031, "The shield of the legendary Herorian of Heroria. Gains set bonus with The Herorian", 750, 400, 1400000, 4, herorian, 5)
blastgear = Armour("Blasting", 2025, "Said to increase your power... Explosively. Gains set bonus with Tier 2 Buh-bomb", 700, 400, 1300000, 0, bomb, 5 )
vmaster = Armour("Vibe Master", 2026, "An upgrade to the previous Wooden Armor. Gains set bonus with The Vibe Check", 700, 250, 1100000 , 8, vibechk, 5)
loincloth = Armour("Loincloth", 2032, "Who knows where this came from. With Deathly Axe, increases effectiveness of Deadly Grasp",
500, 500, 1200000, 3, daxe, 6)
susanoo1 = Armour("Imperfect Susanoo", 2033, "Named after the shinto god of storms. It hurts. Loses 2%hp each turn Gains set bonus with Energy Mace", 900, 400,
1400000, -2, emace, 5)

# Tier 6 (God Tier)
mkgear = Armour("Monkey Suit", 2030, "An outfit made by the Monkey King. Gains set bonus with Banana Blaster", 1700, 800,
5000000, 6, bblade, 6)
haki = Armour("Haki", 2027, "Makes it easier to absorb this mysterious energy. Gains set bonus with Conqueror Haki",
1200, 1200, 5000000, 5, cqhaki, 6)
yang = Armour("Yang", 2028, "The physical manifestation of creation, light and positive energy", 1500, 1000, 5000000, 30, yin, 6)
ymr = Armour("YareYare Mirror",2034, "Said to be able to significantly reduce all incoming damage. Set bonus with Tatsuki Blade", 2500, 50, 5200000, 0, tblade, 6)
chand = Armour("Crazy Hand", 2029, "A mysterious floating with seemingly immense power used to defend", 1400, 1300, 5000000, 10, mhand, 6)


# unique
paraders = Armour("Parade Creators Outfit", 4001, "The cloak donned by the Creator of Isaiah's Parade", 5900, 4000, 0, 10, parblade, 6)
pdr = Armour("True Plague Doctors Uniform", 4002, "You don't want him doing your autopsy", 4050, 1900, 0, 25, pds, 6)
loin = Armour("Unusual Loincloth", 4003, "Wait, is that a monkey tail?", 5000, 2000, 0, 4, uth, 6)
jotarowep = Armour("Celestial Platinum", 4004, "The physical manifestation of CelestialG's fighting spirit",
5000, 1700, 0, 5, diowep, 6)
bigbel = Armour("Biggums' Belly", 4005, "It's so chubby.", 5500, 2000)

armorlist = [linen, chain, hunters, iron, gold, slimearm, assas, valkryie, diamond, saiyanguc, 
abyss, paladium, cranger,
solarflare, elitist, wood, hierro, plaguearm,
vknight, shadowflame, artillery, sranger, 
vampcloak, nightmare, hshield, blastgear, vmaster, loincloth, susanoo1,
mkgear, haki, yang, ymr, chand]

allarmor = [paraders, pdr, loin, jotarowep, bigbel]
for thing in armorlist:
    allarmor.append(thing)

gear = []
for item in allweapons:
    gear.append(item)
for item in allarmor:
    gear.append(item)

lilgear = []
for item in weaponlist:
    lilgear.append(item)
for item in armorlist:
    lilgear.append(item)

@dataclass
class Fighter:
    name: str
    tag: int
    level: int
    curxp: int
    health: int
    mindmg: int
    maxdmg: int
    wins: int
    losses: int
    pcoin: int
    critchance: int=5
    healchance: int=3
    ability: object=None
    passive: object=None
    weapon: int=1001
    armour: int=2001
    xpthresh: int=50
    typeobj: str="player"
    canfight: bool=True
    inteam: bool=False
    invitation: int= None
    weapon2: int=1001
    armour2: int=2001
    curbuff: int=None
    bdur: int=0
    inventory: list=field(default_factory=list)
    reborn: int=0

    def rtz(self):
        self.level = 0
        self.curxp = 0
        self.xpthresh = 50
        self.health = 170 + ((0.01 + (self.reborn / 100)) * self.health)
        self.mindmg = 10 + ((0.03 + (self.reborn / 100)) * self.mindmg)
        self.maxdmg = 20 + ((0.03 + (self.reborn / 100)) * self.maxdmg)
        self.reborn += 1
        self.pcoin = ((1/50) * self.pcoin) 
        self.weapon = 1001
        self.armour = 2001

    def hasreborn(self):
        if self.reborn == 0:
            return False
        return True

    def hasbuff(self):
        if self.curbuff is not None:
            return True
        
        return False

    def addcoin(self, coin):
        self.pcoin += coin
        self.pcoin = math.ceil(self.pcoin)

    def takecoin(self, coin):
        self.pcoin -= coin
        
    def hasPassive(self):
        if self.passive == None:
            return False
        else:
            return True

    def hasActive(self):
        if self.ability == None:
            return False
        else:
            return True

    def healthprice(self):
        if self.getTier() in [4, 5]:
            cost = 16000 + (self.health * 1.5)
        elif self.getTier() == 6:
            cost = 200000 + (self.health * 1.5)

        else:
            cost = 400 + (self.health * 1.5)

        if self.hasreborn():
            cost -= ((10 + (self.reborn * 2)) / 100) * cost
        
        return cost

    def mindmgprice(self):
        if self.getTier() in [4, 5]:
            cost = 13000 + (self.mindmg * 1.5)
        elif self.getTier() == 6:
            cost = 150000 + (self.mindmg * 1.5)
        else:
            cost = 200 + (self.mindmg * 1.5)
        
        if self.hasreborn():
            cost -= ((10 + (self.reborn * 2)) / 100) * cost
        return cost

    def maxdmgprice(self):
        if self.getTier() in [4, 5]:
            cost = 14000 + (self.maxdmg * 1.5)
        elif self.getTier() == 6:
            cost = 180000 + (self.maxdmg * 1.5)
        else:
            cost = 220 + (self.maxdmg * 1.75)
        if self.hasreborn():
            cost -= ((10 + (self.reborn * 2)) / 100) * cost
        return cost

    def critchanceprice(self):
        cost = 400 + (self.level * 3)
        return cost

    def healchanceprice(self):
        cost = 500 + (self.level * 3)
        return cost

    def uphealth(self, narg):
        cost = self.healthprice()

        if not self.hasreborn():
            if self.getTier() == 1 and self.health + 20 > 130 * 1.3:
                return "Reach Tier 2 to upgrade your health further"
            if self.getTier() == 2 and self.health + 20 > 345 * 1.3:
                return "Reach Tier 3 to upgrade your health further"
            if self.getTier() == 3 and self.health + 20 > 949 * 1.3:
                return "Reach Tier 4 to upgrade your health further"
            if self.getTier() == 4 and self.health + 20 > 2800 * 1.3:
                return "Reach Tier 5 to upgrade your health further"

        cando = self.cashchk(cost)
        at = 0

        if narg > 0:
            while cando and at < narg:
                at += 1
                cost = self.healthprice()
                cando = self.cashchk(cost)
                self.health += 20
                self.health = math.ceil(self.health)
            return f"You upgraded your health {at} times"
        
        if cando:
            self.health += 20
            self.health = math.ceil(self.health)
            return "Successfully increased max Health by 20"
        else:
            return "You do not have enough Funds"

    def upmin(self, narg):
        cost = self.mindmgprice()

        if not self.hasreborn():
            if self.mindmg + 5 > 50 * 1.5 and self.getTier() == 1:
                return "Reach Tier 2 to upgrade some more"

            elif self.mindmg + 5 > 160 * 1.5 and self.getTier() == 2:
                return "Reach Tier 3 to upgrade some more"

            elif self.mindmg + 5 > 600 * 1.5 and self.getTier() == 3:
                return "Reach Tier 4 to upgrade some more"

            elif self.mindmg + 5 > 1700 * 1.5 and self.getTier() == 4:
                return "Reach Tier 5 in order to upgrade your min damage some more"
            
            elif self.mindmg + 5 > 3500 * 1.5 and self.getTier() == 5:
                return "Reach Tier 6 in order to upgrade your min damage further"

        cando = self.cashchk(cost)
        at = 0

        if narg > 0:
            while cando and at < narg:
                at += 1
                cost = self.mindmgprice()
                cando = self.cashchk(cost)
                self.mindmg += 5
                self.mindmg = math.ceil(self.mindmg)
            return f"You upgraded your min damage {at} times"
        
        
        if cando:
            self.mindmg += 5
            self.mindmg = math.ceil(self.mindmg)
            return "Successfully increased Min Damage by 5"
        
        else:
            return "You do not have enough Funds"
    
    def upmax(self, narg):
        cost = self.maxdmgprice()

        if not self.hasreborn():
            if self.maxdmg + 5 > 90 * 1.5 and self.getTier() == 1:
                return "Reach Tier 2 to upgrade some more"

            elif self.maxdmg + 5 > 190 * 1.5 and self.getTier() == 2:
                return "Reach Tier 3 to upgrade some more"

            elif self.maxdmg + 5 > 700 * 1.5 and self.getTier() == 3:
                return "Reach Tier 4 to upgrade some more"

            if self.maxdmg + 5 > 1800 * 1.5 and self.getTier() == 4:
                return "Reach Tier 5 in order to upgrade your max damage some more"

            if self.maxdmg + 5 > 4200 * 1.5 and self.getTier() == 5:
                return "Reach Tier 6 in order to upgrade your max damage some more"

        cando = self.cashchk(cost)
        at = 0

        if narg > 0:
            while cando and at < narg:
                at += 1
                cost = self.maxdmgprice()
                cando = self.cashchk(cost)
                self.maxdmg += 5
                self.maxdmg = math.ceil(self.maxdmg)
            return f"You upgraded your max dmg {at} times"

        if cando:
            self.maxdmg += 5
            self.maxdmg = math.ceil(self.maxdmg)
            return "Successfully increased Max Damage by 5"
        
        else:
            return "You do not have enough Funds"

    def cashchk(self, x):
        if self.pcoin >= x:
            self.pcoin -= x
            return True
 
        else:
            return False

    def upcrit(self):
        cost = self.critchanceprice()
        if self.critchance >= 65:
            return "You already have your crit maxed"
        
        cando = self.cashchk(cost)
        if cando:
            self.critchance += 2
            self.critchance = math.ceil(self.critchance)
            return "Successfully increased Crit Chance by 2"
        
        else:
            return "You do not have enough Funds"

    def upheal(self):
        cost = self.healchanceprice()
        if self.healchance >= 35:
            return "Your Health % Chance is maxed"
        
        cando = self.cashchk(cost)

        if cando:
            self.healchance += 3
            self.healchance = math.ceil(self.healchance)
            return "Successfully increased Healh Chance by 3"
        else:
            return "You do not have enough Funds"


    def passchange(self, chg):
        if self.pcoin >= 15000:
            self.pcoin -= 15000
            self.passive = chg.name
            return "Successful... Check with <>profile or <>passive"

        else:
            return "You do not have enough Parade Coins for this transaction. You need at least 15 000"

    def actichange(self, chg):
        if self.pcoin >= 25000:
            self.pcoin -= 15000
            self.ability = chg.name
            return "Successful... Check with <>profile or <>active"

        else:
            return "You don't have enough Parade Coins for this"


    def getweapon(self):
        value = [w for w in allweapons if w.tag == self.weapon]
        return value[0]

    def getgear(self):
        weapon = [w for w in allweapons if w.tag == self.weapon]
        armor = [t for t in allarmor if t.tag == self.armour]

        return copy.copy(weapon[0]), copy.copy(armor[0])

    def getallgear(self):
        weapon = [w for w in allweapons if w.tag == self.weapon]
        armor = [t for t in allarmor if t.tag == self.armour]
        weapon2 = [w for w in allweapons if w.tag == self.weapon2]
        armor2 = [t for t in allarmor if t.tag == self.armour2]

        return copy.copy(weapon[0]), copy.copy(armor[0]), copy.copy(weapon2[0]), copy.copy(armor2[0])

    def getTier(self):
        if self.level >= 0 and self.level < 50:
            return 1
        elif self.level >= 50 and self.level < 100:
            return 2
        elif self.level >= 100 and self.level < 150:
            return 3
        elif self.level >= 150 and self.level < 200:
            return 4
        elif self.health >= 10000 and self.level >= 300:
            return 6
        elif self.level >= 200:
            return 5
        else:
            print("Something went wrong with the tiers")
            return 0

def buffing(tobuff):
    if tobuff.armour.name == "Solar Flare":
        tobuff.weapon.damage += 20
        tobuff.health += 50
        msg = "Increased damage of Solar Flare by 20 and health by 50"

    elif tobuff.armour.name == "Shadow Flame":
        tobuff.weapon.damage += 60
        tobuff.health += 100
        tobuff.mindmg += 15
        msg = "Increased damage of Shadow Flame Knife by 60, Increased health by 100, and increased mindmg by 15"

    elif tobuff.armour.name == "True Plague Doctors Uniform":
        tobuff.health += 100
        tobuff.weapon.damage += 45
        tobuff.critchance += 5
        tobuff.weapon.lifesteal += 6
        msg = "Increased Damage of Plague Doctors Scepter by 45. Increased Health by 100. Increased Critchance by 5%. Increased lifesteal by 6%"

    elif tobuff.armour.name == "Valkryie":
        tobuff.health += 40
        tobuff.weapon.damage += 5
        msg = "Increased Damge of Axe by 5, and increased health by 40"

    elif tobuff.armour.name == "Assassins":
        tobuff.health += 10
        tobuff.weapon.damage += 15
        msg = "Increased Damage of Dagger by 15, added 3% lifesteal and +10 health"

    elif tobuff.armour.name == "Charged Ranger":
        tobuff.weapon.damage += 30
        tobuff.armour.regen += 5
        tobuff.mindmg += 10
        msg = "Increased Weapon damage by 30, 5% regen and increase min damage by 10"       

    elif tobuff.armour.name == "Diamond":
        tobuff.health += 35
        tobuff.weapon.damage += 15
        msg = "Increased Weapon Damage by 15, and increased health by 35"     

    elif tobuff.armour.name == "Wooden":
        tobuff.health += 200
        tobuff.weapon.critplus += 3
        tobuff.weapon.damage += 15
        msg = "Increased Health by 200, increased weapon damage by 15, and critchance by 3%"

    elif tobuff.armour.name == "Slime":
        tobuff.health += 20
        tobuff.weapon.damage += 15
        tobuff.weapon.critplus += 4
        msg = "Increased Health by 20, increased Damage of Baby Slime by 15, and increased crit chance by 4"
        
    elif tobuff.armour.name == "Master General":
        tobuff.health += 220
        tobuff.weapon.damage += 20
        msg = "Increased health by 220. Increased weapon damage by 20"

    elif tobuff.armour.name == "Tundra Ranger":
        tobuff.health += 150
        tobuff.critchance += 15
        tobuff.weapon.damage += 15
        tobuff.weapon.lifesteal += 3
        msg = "Increased health by 150. Increased Critchance and weapon damage by 15. Increased weapon lifesteal by 3%"
        
    elif tobuff.armour.name == "Vibe Master":
        tobuff.critchance += 100
        tobuff.weapon.damage += 30
        msg = "Increased crit chance by 100. Increased weapon damage by 30"

    elif tobuff.armour.name == "Vampiric Cloak":
        tobuff.health += 200
        tobuff.weapon.lifesteal += 5
        tobuff.armour.regen += 2
        tobuff.weapon.damage += 40
        msg = "Increased Health by 200, lifesteal on ENC Vamp Knives by 5%, damage on ENC Vamp Knives by 40 and regen on Vamp Cloak by 2%"

    elif tobuff.armour.name == "Nightmare":
        tobuff.health += 120
        tobuff.weapon.damage += 120
        tobuff.attackmsg = "Sealed the dreams of"
        msg = "Increased health and weapon damage by 120"

    elif tobuff.armour.name == "Haki":
        tobuff.health += 500
        tobuff.weapon.damage += 400
        tobuff.weapon.lifesteal += 4
        tobuff.armour.regen += 4
        tobuff.critchance += 10
        tobuff.mindmg += 20
        tobuff.maxdmg += 20
        tobuff.attackmsg = "manipulates the existence of"
        msg = "This is your birthrite. Increased health by 500, Damage of Conquerors by 400, increased lifesteal on both Haki and Conquerors Haki by 4%,increased crit chance by 10% and increased min and max damage by 20. Able to use Haoshoku Haki passive"

    elif tobuff.armour.name == "Yang":
        tobuff.health += 500
        tobuff.weapon.damage += 400
        tobuff.weapon.lifesteal += 4
        tobuff.armour.regen += 4
        tobuff.critchance += 10
        tobuff.mindmg += 50
        tobuff.maxdmg += 50
        tobuff.attackmsg = "manipulates the mind and soul of"
        msg = "Perfect balanced has been achieved. Increased health by 500, Damage of Yin Blade by 400, increased lifesteal on both Yang and Yin by 4%,increased crit chance by 10% and increased min and max damage by 50. Able to use Pride of Balance Passive"
        
    elif tobuff.armour.name == "Blasting":
        tobuff.weapon.damage += 700
        tobuff.health += 200
        tobuff.critchance += 10
        msg = "Increased weapon damage by 700, health by 200 and crit chance by 10"
    
    elif tobuff.armour.name == "Monkey Suit":
        tobuff.health += 600
        tobuff.weapon.damage += 300
        tobuff.mindmg += 80
        tobuff.armour.regen += 4
        msg = "Your instincts run wild. Increases regen by 4%, health by 600, weapon damage by 300 and min damage by 80"

    elif tobuff.armour.name == "Hero's Shield":
        tobuff.health += 400
        tobuff.weapon.damage += 200
        tobuff.mindmg += 40
        tobuff.maxdmg += 40
        msg = "You are now the hero. Increased health by 400, damage by 200 and min and max dmg by 40"

    elif tobuff.armour.name == 'Crazy Hand':
        tobuff.ability = psusanoo
        msg = "You have awakened Perfect Susanoo"

    elif tobuff.armour.name == "YareYare Mirror":
        tobuff.weapon.damage += 100
        tobuff.weapon.lifesteal = 5
        tobuff.ability = psusanoo
        msg = "You have awakened the ability of Perfect Susanoo. Tatsuki blade no longer harms you, but instead heals you and has +100 dmg"

    elif tobuff.armour.name == "Imperfect Susanoo":
        tobuff.health += 200
        tobuff.weapon.damage += 50
        tobuff.weapon.lifesteal += 2
        msg = "Increases Health by 200, increases weapon damage by 50. Increased lifesteal of energy mace by 2%"

    elif tobuff.armour.name == "Loincloth":
        tobuff.ability = deadlygrasp
        msg = "Grants you the ability of deadly grasp and increases it's power."

    elif tobuff.armour.name == "Parade Creators Outfit":
        tobuff.health += 60
        tobuff.weapon.damage += 40
        tobuff.weapon.critplus += 2
        tobuff.weapon.lifesteal += 2
        tobuff.mindmg += 40
        tobuff.maxdmg += 40
        msg = "Increased Health by 60. Increased Min, max and weapon damage by 40. Increased Crit Chance and heal% by 2%"

    elif tobuff.armour.tag == 4003:
        tobuff.ability = suffocation
        tobuff.armour.hpup += 150
        tobuff.armour.pup += 150
        tobuff.weapon.damage += 150
        msg = "Now... Suffocate them. Increases all damage/health stats by 150"

    elif tobuff.armour.tag == 4004:
        tobuff.ability = czw
        tobuff.armour.hpup += 100
        tobuff.armour.pup += 100
        tobuff.weapon.damage += 100
        msg = "Awaken to your ZA WARUDO. Increases all stats by 100"

    else:
        msg = "Something went wrong"

    return msg

class FightMe(Fighter):

    def instantize(self):
        if self.ability != None:
            value = [x for x in allabilities if x.name == self.ability]
            self.ability = value[0]
        

        if self.passive != None:
            value = [x for x in allpassives if x.name == self.passive]
            self.passive = value[0]

        weapon, armour = self.getgear()

        self.weapon, self.armour = copy.copy(weapon), copy.copy(armour)
        if self.reborn > 0:
            self.incstats()

        self.buffup()

    def incstats(self):
        toinc = (3 + self.reborn) / 100
        twep = self.weapon.__dict__
        for k,v in twep.items():
            if type(v) == int:
                if k in ["tag", "cost", "tierz"]: continue
                twep[k] = math.ceil(v + (v * toinc))
            else: continue

        tarm = self.armour.__dict__
        for k,v in tarm.items():
            if type(v) == int:
                if k in ["tag", "cost", "tierz"]: continue
                tarm[k] = math.ceil(v + (v * toinc))
            else: continue

    def buffup(self):
        self.attackmsg = self.weapon.effect
        self.health += self.armour.hpup
        self.maxdmg += self.armour.pup
        self.critchance += self.weapon.critplus

    def buff(self):
        x = self
        msg = buffing(x)
        return msg

    def hpcheck(self):
        return self.health

    def attack(self, dmg):
        self.health -= dmg

    def heal(self, amount):
        self.health += amount
    

    def abiluse(self, power):
        powerinc, powerticinc, healthinc, min_dmg_upinc, max_dmg_upinc, perhealth = self.ability.use()
        power *= powerinc
        power += powerticinc
        self.health += healthinc
        self.mindmg += min_dmg_upinc
        self.maxdmg += max_dmg_upinc
        perhealth = math.ceil((perhealth/ 100) * self.health)
        self.health += perhealth

        return power

    def passuse(self, power):
        powerinc, powerticinc, healthinc, min_dmg_upinc, max_dmg_upinc, perhealth = self.passive.use()
        power *= powerinc
        power += powerticinc
        self.health += healthinc
        self.mindmg += min_dmg_upinc
        self.maxdmg += max_dmg_upinc
        perhealth = math.ceil((perhealth/ 100) * self.health)
        self.health += perhealth

        return power

class BeastFight:
    def __init__(self, name, health, mindmg, maxdmg, mincoin, maxcoin, entrymessage, minxp, critchance=5, healchance=3, ability=None, passive=None, attackmsg=None, weapon=fist, armour=linen, level=1, typeobj="npc"):
        self.name = name
        self.health = health
        self.mindmg = mindmg 
        self.maxdmg = maxdmg
        self.mincoin = mincoin
        self.maxcoin = maxcoin
        self.entrymessage = entrymessage
        self.minxp = minxp
        self.maxxp = minxp + 40
        self.critchance = critchance
        self.healchance = healchance
        self.ability = ability
        self.passive = passive
        self.attackmsg = attackmsg
        self.weapon = copy.copy(weapon)
        self.armour = copy.copy(armour)
        self.level = level
        self.typeobj = typeobj

    def hasPassive(self):
        if self.passive == None:
            return False
        else:
            return True

    def hasActive(self):
        if self.ability == None:
            return False
        else:
            return True

class FightingBeast(BeastFight):

    def hpcheck(self):
        return self.health

    def heal(self, amount):
        self.health += amount

    def attack(self, dmg):
        self.health = self.health - dmg

    def abiluse(self, power):
        powerinc, tickpow, healthinc, min_dmg_upinc, max_dmg_upinc, perhealth= self.ability.use()
        power *= powerinc
        power += tickpow
        self.health += healthinc
        self.mindmg += min_dmg_upinc
        self.maxdmg += max_dmg_upinc
        perhealth = math.ceil((perhealth/ 100) * self.health)
        self.health += perhealth

        return power

    def passuse(self, power):
        powerinc, powerticinc, healthinc, min_dmg_upinc, max_dmg_upinc, perhealth = self.passive.use()
        power *= powerinc
        power += powerticinc
        self.health += healthinc
        self.mindmg += min_dmg_upinc
        self.maxdmg += max_dmg_upinc
        perhealth = math.ceil((perhealth/ 100) * self.health)
        self.health += perhealth

        return power

    def buff(self):
        x = self
        buffing(x)
        msg = buffing(x)
        return msg

        

# Low Level below 200 hp and Magikarp
easy1 = BeastFight("The Cat", 40, 6, 30, 10, 15, "Uh... What harm could a harmless little... oh my...", 62, attackmsg="raises up and scratches", level=5)
easy2 = BeastFight("ZombieMan", 60, 5, 15, 15, 25, "Ah... the typical zombie is chasing you",65, attackmsg="tickles the brains of", level=5)
easy3 = BeastFight("Magikarp", 120, 1, 2, 2, 5, "No challenge... Let's make it quick",73, attackmsg="flops on", level=6)
easy4 = BeastFight("Random Meme", 45, 1, 20, 20, 40, "Some one has sent you a random powerful meme...", 95, attackmsg="memes on", level=10)
easy5 = BeastFight("Robloxian Army", 60, 14, 20, 20, 60, "First their pets, now themeselves? sigh...",112, attackmsg="gangs up on", level=11)
easy6 = BeastFight("Mr.Skeleton", 70, 17, 22, 10, 30, "Mr. Skeleton has spawned.", 148, attackmsg="aims their bow and shoots", level=12)
easy7 = BeastFight("Goblin Tinkerer", 120, 25, 31, 50, 90, "Wait, I thought the Goblin Tinkerer was on our side?", 212,
 attackmsg="throws spike balls at", level=23)
easy8 = BeastFight("Annoying Discord Spammer", 120, 18, 35, 2, 10, 
"There's always that one person that loves to spam @mentions... Found him", 237, attackmsg="spams on", level=34)

easy9 = BeastFight("Possessed Friend", 125, 32, 38, 20, 40, "I can't believe your friend got possessed... again", 246, attackmsg="slashes", level=35)
easy10 = BeastFight("Baby Shark", 130, 50, 90, 30, 50, "Baby shark doo doo doo oops...",258, attackmsg="sings then bites", level=46)

# Mid Level between 200 and 300 hp
mid1 = BeastFight("Cherry Blossom", 260, 60, 80, 30, 60,"Sakur- Cherry Blossom? \"WHO YOU CALLING USELESS...\"", 182,
attackmsg="charges chakra then punches", level=51)
mid2 = BeastFight("Buh-bomb", 330, 70, 90, 45, 90, "Look who came not from Mario's world", 227, weapon=bomb,
attackmsg="says \"My main goal, is to blow up\" and explodes on", level=55)
mid3 = BeastFight("Big Rock", 345, 10, 130, 60, 100, "*Smiles*", 300 , attackmsg="Jumps then lands on", level=57 )
mid4 = BeastFight("Isaiah's Parade", 324, 90, 100, 40, 70, "Parade?... no... Just a clone", 307, attackmsg="slashes", level=69)
mid5 = BeastFight("Angel Statue", 300, 110, 125, 20, 50, "An Angel Statue feel from the sky... Nice?", 335, attackmsg="Pounds on", level=80)
mid6 = BeastFight("Azoth", 320, 40, 120, 140, 70, "Straight from Valhalla, Azoth is here", 545, ability=deadlygrasp, weapon=axe,
attackmsg="swings his axe at", level=90)

mid7 = BeastFight("Valkryie", 330, 120, 142, 100, 120, "Uh... I think she found out we stole their armour", 677, 8, ability=critstrike, weapon=axe,
armour=valkryie, attackmsg="swings her axes and slashes", level=92)

mid8 = BeastFight("Rick Sanchez", 325, 145, 170, 80, 130,"Guess who just popped out of a portal ready to attack", 693,
 ability=pickelize, attackmsg="blasts", weapon=blaster, level=93)

mid9 = BeastFight("Slivial", 325, 150, 176, 120, 250, "Straight from Slimenia, He summons his tank", 703, 6, 5, blast, regeneration,
"Shoots some ammo from his cannon at", weapon=miracles, level=94)

mid10 = BeastFight("Sanic", 340, 160, 190, 125, 150, "Gotta go fast", 758, 15, ability=sonic, attackmsg="zooms around then hits", level=95    )


# High Level between 500 and 950 hp
hard1 = BeastFight("DRAGON!", 900, 270, 310, 2220, 2400, "Dragon goes rawr but no 'XD'",362, ability=blast, attackmsg="Breathes on", armour=iron, level=100)
hard2 = BeastFight("Dio", 700, 250, 360, 2350, 2600, "Oh no... It's dio... Quick, take him out. (Not on a date mind you)",454, ability=theworld, passive=regeneration,
weapon=vampknives,armour=gold, attackmsg="Barrages on", level=120)
hard3 = BeastFight("Red Paladins", 650, 215, 300, 1800, 2300, "The Red Paladins have arrived.",721, ability=swarm, weapon=axe, attackmsg="Gather and attack", level=121)
hard4 = BeastFight("Queen Bee", 900, 380, 490, 2000, 2370, "Queen Bee has Awoken", 722, ability=swarm, attackmsg="Rams into", level=125) 
hard5 = BeastFight("Kairo", 600, 200, 230, 2000, 3200, "Out of the trash, the Racoon has emerged", 801, ability=swarm,
attackmsg="bites", level=130)
hard6 = BeastFight("Money Tree", 800, 270, 320, 5000, 6200, "Who said money doesn't grow on trees.",
1048, attackmsg="Blows money on", level=140)
hard7 = BeastFight("The Story Teller", 700, 530, 670, 4100, 5300, "The story Teller is angry you slept through his story",
1184, attackmsg="Reads to", passive=dodge, level=143)
hard8 = BeastFight("Max Steal", 949, 600, 650, 5500, 6000, "GO TURBO", 1480, 20, 5, blast, sboost, "strikes", sancspear, elitist, 144)
hard9 = BeastFight("Thor not Thor", 900, 500, 600, 5000, 5500, "Something just came crashing down", 1498, 6, 10, blast, critblock, "Zaps", stormbreaker, hierro, 145)
hard10 = BeastFight("Kid", 800, 600, 700, 6000, 6200, "Clearly not an ordinary kid", 1508, 30, 5, passive=dodge,
attackmsg="sorts his cards then attack", weapon=hcard, armour=plaguearm, level=149)

# tier 4 mofos. Between 951 and 3k hp
ut1 = BeastFight("DIO!", 1100, 400, 550, 19000, 20950, "Dio... no... it's DIO", 602, 15, 60, theworld, regeneration,"Attacks", vampknives, gold, 150)
ut2 = BeastFight("Robloxian Lord", 960, 200, 250, 15050, 17000, "Uh oh... A big one", 1121, ability=swarm, passive=dodge, attackmsg="Memes on",
weapon=blaster, armour=saiyanguc, level=151)
ut3 = BeastFight("Ender Dragon", 1000, 450, 480, 17000, 18050, "Uh, Something was wrong with the respawn system, and now it's in your world", 1205,
ability=blast, attackmsg="Breathes on", level=152)
ut4 = BeastFight("Moon Lord", 2000, 750, 800, 17000, 20000, "Impending Doom Approaches", 1436 ,10,20,
critstrike, regeneration, "Summons a Phantasmal Deathray and blasts", armour=abyss, level=153)
ut5 = BeastFight("Young Flame Handler", 2020, 1700, 1800, 17000, 19000, "His job... defeat you", 1766, 5, 3, critstrike, attackmsg="strikes",
weapon=sfknife, armour=shadowflame, level=154)
ut6 = BeastFight("Young General", 2400, 1500, 1700, 17000, 18000, "You are simply practice for this rising star", 1815, 10, 3, blast, None,
"Aims and shoots at", tsummon, artillery, 155)
ut7 = BeastFight("Young Marksman", 2100, 1200, 1300, 15000, 16000, "ready... aim...", 1861, 30, 3, critstrike, None, "sets up and quickly snipes",
srifle, sranger, 156)
ut8 = BeastFight("Valhalla Knight", 2800, 800, 900, 16000, 19000, "This menacing warrior has arrived", 2060, 10, 20, uheal, rage,
"Swings his axe menacingly and then attacks", bsuckler, vknight, 157)
ut9 = BeastFight("Drippler", 952, 500, 550, 15000, 16000, "What is this strange multi-eyed floating creature", 2069, 10, 10,
swarm, dodge, "drains the blood of", bsuckler, hierro, 158)
ut10 = BeastFight("Magician", 980, 470, 600, 15000, 19000, "Come, let me show you a trick you won't forget", 2508, 5, 3,
uheal, dodge, "shuffles cards then attacks", hcard, vknight, 159)


# Tier 5 Between 3k and 10k hp
nme = BeastFight("NME", 6000, 1100, 1300, 42400, 52800, "NME is the enemy and he's come to prove that", 902, 
20, 25, nmareterror, sboost, "devours the nightmares of", sfknife, shadowflame, 220)
isama = BeastFight("Isaiah-Sama", 5500, 1600, 1800, 31400, 35600, "Isaiah has Arrived, but is nerfed", 1216, 15,20, theworld, regeneration,
 "fires at", seruption, solarflare, 240)
uksniper = BeastFight("Unknown Sniper", 5000, 1000, 1100, 32000, 38000, "You feel someone watching you", 
1591, 5, 3, critstrike, sharpeye, "snipes", srifle, sranger, 250)
sfass = BeastFight("Shadow Flame Assassin", 6000, 1300, 1400, 40000, 44000, "You glimpse a shadow following you",
1987, 25, 10, critstrike, dodge, "slashes at", sfknife, shadowflame, 270)
kdono = BeastFight("Kevin not Kevin", 8000, 1000, 1200, 58000, 64000, "KEVIN!!!", 2382, 5, 20, uheal, regeneration,
"menacingly approaches", hcard, vknight, 280)
herian = BeastFight("The Herorian", 7000, 1600, 1900, 20000, 21000, "The Herorian from Heroria?", 2953,
20, 10, slag, dodge, "expertly spins his top and throws it at", herorian, hshield, 300)
tmaster = BeastFight("Tank Master", 9300, 1000, 1200, 58000, 64000, "have you ever seen a tank up close?", 3734, 5,3,
blast, sharpeye, "Summons his tank, aims it, and fires", tsummon, artillery, 310)
rebdio = BeastFight("DIO Reborn", 10000, 1600, 1800, 64000, 67000, "It's like he never dies.", 4638, 20,5, uheal, regeneration,
"flash freezes then drains", evampknife, vampcloak, 320)
minmegu = BeastFight("Minmegu", 9600, 3000, 4000, 70000, 72000, "ECKS-PLOH-SHUN!!!", 4914, 10, 4, jajanken, counter, "quick casts an explosion and blows up",
bomb, blastgear, 350)
dmaster = BeastFight("Dream Master", 8500, 3500, 4200, 68000, 72000, "Your worst nightmare??", 5258, 5, 3, nmareterror, nlove, "gathers nightmares and strikes",
dreamsword, nightmare, 400)

# Tier 6 10k +
god1 = BeastFight("Gensuki Armada", 15000, 9000, 10000, 800000, 900000, "His eyes of decay stare at you", 10000, 5, 3, sharpeye, haohaki,
"stares and damages", cqhaki, haki, 550)
god2 = BeastFight("Weakened Parade Creator", 18000, 13000, 15000, 900000, 1200000, "Just who was he fighting to get him like this... Maybe you can beat him",
11000, 40, 20, jajanken, rage, "Twirls his staff then attacks", parblade, paraders, 570)

god3 = BeastFight("Monkey King", 40000, 20000, 23000, 1500000, 1700000, "Where did he even come from", 11000, 30, 10,
swarm, rage, "aims and fires at", bblade, mkgear, 640)

god4 = BeastFight("Haxiyuri Genko", 78000, 28000, 33000, 1800000, 2000000, "The ability to change materials and summon weapons at will... and you are his target",
12000, 10, 10, sharpeye, balancepride, "sighs and summons weapons and attacks", yin, yang, 670)

god5 = BeastFight("Hiro Kage", 80000, 30000, 35000, 2000000, 2300000, "His Kagekan is blazing", 14000, 20, 14, sharpeye, dodge,
"Summons his susanoo and strikes", mhand, chand, 700)

# Lists

enemybeta = [
easy1, easy2, easy3, easy4, easy5, easy6, easy7, easy8, easy9, easy10, 
mid1, mid2, mid3, mid4, mid5, mid6, mid7, mid8, mid9, mid10,
hard1, hard2, hard3, hard4, hard5, hard6, hard7, hard8, hard9, hard10,
ut1, ut2, ut3, ut4, ut5, ut6, ut7, ut8, ut9, ut10,
isama, nme, uksniper, sfass, kdono, tmaster, rebdio, herian, minmegu, dmaster,
god1, god2, god3, god4, god5
]

enemy = []
for thingie in enemybeta:
    enemy.append(copy.copy(thingie))

# def __init__(self, name, tag, health, mindmg, maxdmg, mincoin, maxcoin, entrymessage, minxp, 
# critchance=5, healchance=3, ability=None, passive=None, attackmsg=None, weapon=fist, armour=linen, 
# typeobj="npc"):

# Raid Monster
bebebe = BeastFight("Giant King Be Be Be", 6000, 200, 300, 8000, 10000, "Giant King Be Be Be has been awoken... and is very angry",1000,
30, 25, bebebeslam, chubz, "BE BE BE STRIKE!", level=500)

giggeng = BeastFight("Giant Gargen", 9000, 450, 700, 9000, 12000, "A wild Giantified Gargen Has Appeared", 1500, 20, 20, ssuck, nlove, "Attacks", armour=gold, level=520)

biggums = BeastFight("Biggums", 11000, 650, 750, 25000, 30000, "Biggums is rising out of the earth. Isn't as big as we were told however.", 2000,
20, 40, bellybump, chubz, "kicks a giant foot at", level=540)

oogabooga = BeastFight("Ooga Booga", 14000, 800, 900, 40000, 50000, "Music plays as this giant tribal Man falls from the sky", 2500, 5, 3, swarm, sboost,
"dances then attacks", vibechk, wood, 560)

anansi = BeastFight("Anansi", 16000, 1000, 1100, 50000, 60000, "Anansi is a spider, Anansi is a man. Now he's big and giant, and your head is his demand.",
3000, 2, 10, swarm, rage, "Transforms then attacks", armour=assas, level=565)

pdoctor = BeastFight("Plague Doctor", 20000, 1300, 1400, 60000, 72000, "...?", 4000, 3, 20, plague, sharpeye, "Spreads the plague to", pds,
plaguearm, 580)

slimeraid = BeastFight("Prince Slime", 30000, 400, 500, 25000, 29000, "Prince Slime has awoken", 2000,
attackmsg="Bounces on", weapon=slime, armour=slimearm, level=500)

dizawarudo = BeastFight("DIO ZA WARUDO", 35000, 1700, 2000, 60000, 70000, "What... He's just that good",
5000, 10, 20, theworld, regeneration, "strikes", evampknife, vampcloak, 600)

ruffy = BeastFight("RUFFY!", 80000, 7000, 8500, 120000, 140000, "RUFFY!!!", 12000, 40, 30,
None, haohaki, "gomi gomi no PUNCHU!", cqhaki, haki, 1000)

loc = BeastFight("Lord Of Creation and Destruction", 100000, 6000, 8000, 100000, 400000, "1 force descends from heaven, the other from the underworld. Now... they are one",
10000, 40, 30, None, balancepride, "manipulates the existence of", yin, yang, 1000)


raidingmonster = [bebebe, giggeng, biggums, oogabooga, anansi, pdoctor, slimeraid, loc, ruffy]

# Quest Prompts

sample1 = "has been summoned by Your Majesty to exterminate a Little problem... He says to make haste, or else he'll be late for dinner"

sample2 = "saw something that they shouldn't have. No way you are going to be able to get away. Time to fight"

sample3 = "has been requested by an innocent little girl to help her kidnapped father. Because you are such a great person, You accept"

sample4 = """has encountered Jotaro. 
Yare Yare daze, The great Jotaro himself is asking you for help defeating some small fry. Maybe he just wants to test you"""

sample5 = """is being asked by a suspicious Old Man near the temple to fight his curse... 
You really want to enter the dungeon so as it turns night... YOU FIGHT!"""

sample6 = ", you have been tasked with guarding Princess Sophia on her journey through Avalor. Whethere you want to or not, it's your job"

sample7 = "just has the urge to fight something. No one will stop you though."

sample8 = ", your mother wants you to buy some bread from the store 1 block away. Sounds easy doesn't it... But alas..."

sample9 = ", sorry to tell you, but You are unlucky enough to not have a structured quest of any sort"

sample10 = "hears word of creatures attacking a nearby village. You chug down your ale and head out to slay some mobs"

sample11 = """was just innocently driving along, and sees something strange in the ditch you were driving alongside. 
Your adventurer heart screams to you"""

sample12 = "The robloxians gathered up against you, with their pets. Let's not look weak now shall we?"

questpro = [sample1, sample2, sample3, sample4, sample5, sample6, sample7, sample8, sample9, sample10, sample11, sample12]

