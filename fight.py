import math
from dataclasses import dataclass
import copy

@dataclass
class Ability:
    name: str
    desc: str
    usename: str
    effect: str
    power: int
    powertick: int
    health: int
    lodmg: int
    hidmg: int
    abilcd: int = 4
    tempcd: abilcd = 4
    perhealth: int = 0

    def oncd(self):
        if self.abilcd == self.tempcd:
            return False
        else:
            return True

    def cdreduce(self):
        self.tempcd -= 1
        if self.tempcd == 0:
            self.tempcd = self.abilcd


    def reset(self):
        self.tempcd = self.abilcd


    def use(self):
        return self.power, self.powertick, self.health, self.lodmg, self.hidmg, self.perhealth

class Passive(Ability):
    def use(self):
        return self.power, self.powertick, self.health, self.lodmg, self.hidmg, self.perhealth

# Actives

theworld = Ability("Stop Time", "An ability which freezes time and allows the user to attack twice",
"ZA WARUDO!", "has stopped time, and attacked", 1, 0, 0, 0, 0)

swarm = Ability("Swarm", "Creates multiple versions of the user, and increases their power by x1.5 and their health by +30",
"KAGE BUNSHIN NO JUTSU", "'s Shadow clones have arrived. Power increased by x1.5, and health increased by +30. Attacks",
1.5, 0, 30, 0, 0)

blast = Ability("Blast", "Blasts the enemy with a powerful attack increasing dmg by 1.75 and dealing an extra 5 tick dmg. Health reduced by 40",
 "Outer... BLAST!", "'s health is reduced by 40. Power increased by x1.75 and +5 extra damage. Summons a powerful blast and blasts", 1.75, 5, -40,
 0, 0)

deadlygrasp = Ability("Deadly Grasp", "Reaches for the enemy with hands of death dealing an extra 70 damage, and healing for 15 hp",
"Let me grab you with death itself", "'s hands of death emerge, increasing health by 15, and dealing +70 damage to",
1, 70, 15, 0, 0)

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

slag = Ability("Slag", "Has a 1 in 6 chance of applying Slag to the target, causing them to take 1.5x damage for 2 turns",
"You... have been slagged", "now takes 1.5x damage for the next", 1.5, 0, 0, 0, 0)


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

haohaki = Passive("Haoshoku Haki", "Conqueror's Haki: Increases min and max damage by 40 for each passing turn.\nSet Bonus: Anyone below 30 levels of the user loses 100 hp every turn\nOtherwise. No effect"
, "Know the power of one who is worthy", "Increases min and max damage by 50", 1, 0, 0, 50, 50)

balancepride = Passive("Pride of Balance", "Requires: Yin Blade and Yang Armour set. Increases power of attack by 100 (100 True Damage) and heals for 100 hp on user's turn. Otherwise: No Effect"
,"The emodiment of Balance I am", "Increases power by 100. Heals for 200", 1, 100, 200, 0, 0)

# Unique
plague = Ability("The Plague", "Poisons the victim. Has a base damage of 100 increases by 100, Unique to ...?", "wishes death upon You",
"Summons The Plague and infects",1, 100, 0, 0, 0)

# Raid Enemies
bebebeslam = Ability("BBB slam!", "Giant King B B B, belly flops dealing 1.3x dmg and hitting 3 people", "BE BE BE... SLAM!", 
"belly flops dealing 1.3x dmg, healing for 10hp and hitting up to 3 people. Them being:", 1.3, 0, 10, 0, 0)

harder = Passive("Chubby", "Chub absorption", "CHUB ABSORPTION", "large size acts as a shock absorber, and your attacks do -10 damage",
1, -10, 0, 0, 0)

# Gargen
ssuck = Ability("Soul Sucker", "A powerful move which sucks the soul of the enemy dealing 2x dmg and healing for 15hp", "SOUL SUCKER!",
"sucks the soul of", 2, 0, 15, 0, 0)

nlove = Passive("Nightmare Lover", "Feeds off of the memories of your nightmares and heals itself. Increases it's max damage by 5 each time",
"Lover of Nightmares", "gets energies from nightmares within", 1, 0, 10, 5, 5, 0)

# Biggums
bellybump = Ability("Belly Belly Bounce", "Massive user dashes at an immense speed and bounces the enemy", "Belly... Belly... BOUNCE!",
"charges gaining x1.4 strength increasing min and max damage by 10, and then bounces", 1.4, 0, 0, 10, 10)

# NME
nmareterror = Ability("Nightmare Terror", "Places the target into a sleep, causing them to miss a turn, and dealing massive damage", 
"Know the terror of nightmares", "Casts a sleep spell then causes nightmares to", 1.4, 20, 0, 0, 0)

abilities = [theworld, swarm, blast, deadlygrasp, critstrike, pickelize, sonic, jajanken, uheal, slag]
allabilities = [plague]
for thing in abilities:
    allabilities.append(thing)

passives = [dodge, counter, regeneration, rage, sharpeye, sboost, critblock, haohaki, balancepride]

# Weapons
@dataclass
class Weapons:
    name: str
    desc: str
    effect: str
    damage: int= 0
    critplus: int=0
    healplus: int=0
    cost: int=0
    tierz: int=1
    typeobj: str="Weapon"

    def islifesteal(self):
        if self.healplus >= 1:
            return True
        return False

fist = Weapons("Fist","The original method of attacking (default)", "punches")
katana = Weapons("Katana", "Then, they were katanas.", "slices", 5, 2, cost=250)
bow = Weapons("Bow", "This one doesn't need arrows", "shoots", 6, 1, cost=255)
pistol = Weapons("Pistol", "Pew pew", "shoots", 8, 3, cost=300)
sword = Weapons("Sword", "Sword > Pistol", "slices", 10, 3, cost=320)
dagger = Weapons("Dagger", "Dagger = Sword??", "stabs", 10, 3, cost=320)
slime = Weapons("Baby Slime", "\"Summons a baby slime to fight for you\"", "bounces on", 9, 7, cost=320)
vampknives = Weapons("Vampire Knives", "Blood Draining Knives just for you", "drains", 20, 5, 5, cost=700)
fishrod = Weapons("Fishing Rod", "Gon has lent you his trusty Fishing Rod", "hooks and cuts", 35, 3, cost=450)
axe = Weapons("Axe", "Axe goes schwing", "slashes", 45, 6, cost=650)
fpan = Weapons("Frying Pan", "Not a drying pan", "bonks the head of", 27, 20, cost=660)
miracles = Weapons("Miracle Sword", "Straight from Slimenia", "slashes", 50, 5, 7, 1600, tierz=2)
blaster = Weapons("Blaster", "Pew Pew times 2", "blasts", 65, 4, cost=1100, tierz=2)
dsword = Weapons("Diamond Sword", "Has a pixelated edge for bonus damage", "slashes", 67, 5, cost=1100, tierz=2)
bomb = Weapons("Buh-Bomb", "A souvenir from those Buh-Bombs I had you fight", "explodes on",
85, 8, cost=1400, tierz=2)
crossbow = Weapons("Charged Crossbow", "Not your average Cross bow", "shocks and shoots", 88, 6, cost=1450, tierz=2)
bsuckler = Weapons("Blood Suckler", "A strange creature known for draining the blood of enemies", "sucks the blood of", 70, 3, 20, 4000, tierz=3)
sancspear = Weapons("Sanctum Spear", "Sanctum spear go boom", "pierces", 80, 25, 12, 15000, tierz=3)
stormbreaker = Weapons("Stormbreaker", "A gift from Thor himself. A replica at best", "slashes and zaps", 100, 25, cost=20000, tierz=3)
hcard = Weapons("Playing Cards", "Wait... aren't these Hisoka's?", "slices", 120, 15, 0, 23000, tierz=3)
seruption = Weapons("Solar Eruption", "Made with 100% Solar Fragments", "pierces",
130, 10, cost=25000, tierz=3)
vibechk = Weapons("The Vibe Check", "Yuh need to relax", "Checks the vibe on", 20, 70, 0, 40000, tierz=3)
tsummon = Weapons("Tank Summon", "Wait... what?", "summons a tank which blasts", 370, 25, 0, 300000, tierz=4)
sfknife = Weapons("Shadow Flame Knife", "Crafted from sorcery", "stabs and burns", 430, 15, 5, 300000, tierz=4)
srifle = Weapons("Sniper Rifle", "Never miss a shot", "Snipes", 300, 40, 4, cost=300000, tierz=4)

# Tier 5
evampknife = Weapons("Enchanted Vamp Knife", "Vampire knife, but enchanted with the blood of many", "drains the blood of", 600, 7, 20, 1000000, 5)
dreamsword = Weapons("Dream Sword", "Crafted from the essence of the light side of sleep", "steals the dreams of", 700, 15, 2, 1000000, 5)
cqhaki = Weapons("Conqueror Haki", "A physical manifestation of the ability. Allows the user to use the ability Haoshoku Haki.",
"controls", 2000, 16, 5, 5400000, 5)
yin = Weapons("Yin Blade", "The physical manifestation of darkness, destruction and negative energy", "alters the existence of", 1800, 20, 5, 5300000, 5)

weaponlist = [fist, katana, bow, pistol, sword, dagger, slime, fishrod, axe, fpan, vampknives, miracles, 
blaster, dsword, bomb, crossbow, bsuckler, sancspear, stormbreaker, hcard, vibechk, seruption, tsummon, sfknife, srifle,
evampknife, dreamsword, cqhaki, yin]

# Unique
pds = Weapons("Plague Doctors Scepter", "Soulbound to ...?", "infects", 0, 10, 15, 0, 5)
parblade = Weapons("Staff of the Parade", "The Chosen weapon of the Parade Creator", "moderates", 3370, 20, 25, 99999999999, 5)

allweapons = [pds, parblade]
for weapon in weaponlist:
    allweapons.append(weapon)



# Armour
@dataclass
class Armour:
    name: str
    desc: str
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


linen = Armour("Linen", "Some extremely basic and lightweight armour. (default)")
chain = Armour("Chainmail", "The Typical first set to buy", 5, cost=140)
hunters = Armour("Ranger", "Blends in with background. Gains set bonus with bow", 7, 2, cost=160)
iron = Armour("Iron", "Often the go to in Minecraft Speedruns", 10, 2, 270)
gold = Armour("Gold", "Is gold really better than iron though?", 15, 4, 400)
slimearm = Armour("Slime", "It's almost like attacks slide right off. Gains set bonus with Baby Slime", 20, 4, 550, 4, slime)
assas = Armour("Assassins", "Shh, Sneaky. Gains set bonus with Dagger", 20, 4, 550, 3, dagger)
valkryie = Armour("Valkryie", "Straight from ValHalla. Don't ask. Gains set bonus with axe", 30, 6, 600, pairs=axe)
diamond = Armour("Diamond", "What's a Diamond Sword, Without Diamond Armor. Gains set bonus with Diamond Sword", 40, 7, 720, 0, dsword)
saiyanguc = Armour("Saiyan Gucchi", "Special Edition it would seem", 40, 10, 700)
abyss = Armour("Abyss Walker", "Not from this world", 55, 15, 3000, tierz=2)
paladium = Armour("Paladium", "Increases life regen", 60, 20, 5500, 15, tierz=2)
cranger = Armour("Charged Ranger", "An upgrade to Ranger. Shocking I know", 90, 25, 7000, 0, crossbow, tierz=3)
solarflare = Armour("Solar Flare", "Made from Solar Fragments and Luminite Ore. Gains set bonus with Solar Eruption", 120, 35, 8000, pairs=seruption, tierz=2)
elitist = Armour("Elitist", "Said to be made for the elites", 150, 40, 10000, tierz=3)
wood = Armour("Wooden", "Pfft, you *wood* n't get it. Gains set bonus with The Vibe Check", 160, 45, 30000, 7, vibechk, 3)
hierro = Armour("Hierro", "Hard", 200, 50, 50000, 10, tierz=3)
plaguearm = Armour("Plague Doctors Uniform", "A copy of the original owned by ...?", 200, 50, 50000, 4, tierz=3)
vknight = Armour("Valhalla Knight", "Again, Don't ask where I got this from", 100, 30, 500000, 25, tierz=4)
shadowflame = Armour("Shadow Flame", 
"A sorcerer's creation created by shadows and flames of darkness. Gains set bonus with Shadow Flame Knife",
510, 200, 500000, 5, sfknife, 4)
artillery = Armour("Master General", "mhm yes. Tank uniform. Gains set bonus with Tank Summon", 660, 150, 500000, 0, tsummon, 4)
sranger = Armour("Tundra Ranger", "Gained from surviving the depth of the Tundra. Gains set bonus with Sniper Rifle", 570, 160, 500000, 4, srifle, 4)
# Tier 5
vampcloak = Armour("Vampiric Cloak", "Makes it easier to drain blood. Pairs well with Enchanted Vamp Knives", 800, 300, 1100000, 18, evampknife, 5)
nightmare = Armour("Nightmare", "Woven together from the essence of the dark side of sleep. Gains set bonus with Dream Sword",
800, 420, 1100000, 0, dreamsword, 5)
haki = Armour("Haki", "Makes it easier to absorb this mysterious energy. Gains set bonus with Conqueror Haki",
1200, 1200, 5000000, 5, cqhaki, 5)
yang = Armour("Yang", "The physical manifestation of creation, light and positive energy", 1500, 1000, 5000000, 30, yin, 5)

# unique
paraders = Armour("Parade Creators Outfit", "Identifies the creator of the Parade", 5900, 1370, 99999999, 10, parblade, 5)
pdr = Armour("True Plague Doctors Uniform", "Identifies ...? as a Parade Leader", 4050, 900, 9999999999, 25, pds, 5)
vmaster = Armour("Vibe Master", "Identifies Trxsh as a Parade Leader", 2700, 1000, 99999999999, 6, vibechk, 5)


armorlist = [linen, chain, hunters, iron, gold, slimearm, assas, valkryie, diamond, saiyanguc, abyss, paladium, cranger,
solarflare, elitist, wood, hierro, plaguearm, vknight, shadowflame, artillery, sranger, vampcloak, nightmare, haki, yang]

allarmor = [paraders, pdr, vmaster]
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
    weapon: str="Fist"
    armour: str="Linen"
    xpthresh: int=50
    typeobj: str="player"
    canfight: bool=True

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
        if self.getTier() >= 4:
            cost = 16000 + (self.health * 1.5)
        else:
            cost = 400 + (self.health * 1.5)
        return cost

    def mindmgprice(self):
        if self.getTier() >= 4:
            cost = 13000 + (self.mindmg * 1.5)
        else:
            cost = 200 + (self.mindmg * 1.5)
        return cost

    def maxdmgprice(self):
        if self.getTier() >= 4:
            cost = 14000 + (self.mindmg * 1.5)
        else:
            cost = 220 + (self.maxdmg * 1.75)
        return cost

    def critchanceprice(self):
        cost = 400 + (self.level * 3)
        return cost

    def healchanceprice(self):
        cost = 500 + (self.level * 3)
        return cost

    def uphealth(self):
        cost = self.healthprice()
        cando = self.cashchk(cost)
        if cando:
            self.health += 20
            self.health = math.ceil(self.health)
            return "Successfully increased max Health by 20"
        else:
            return "You do not have enough Funds"

    def upmin(self):
        cost = self.mindmgprice()
        cando = self.cashchk(cost)
        if self.mindmg + 5 > 1100 and self.getTier() < 5:
            return "Reach Tier 5 in order to upgrade your min damage some more"
        if cando:
            self.mindmg += 5
            self.mindmg = math.ceil(self.mindmg)
            return "Successfully increased Min Damage by 5"
        
        else:
            return "You do not have enough Funds"
    
    def upmax(self):
        cost = self.maxdmgprice()
        cando = self.cashchk(cost)
        if self.maxdmg + 5 > 1100 and self.getTier() < 5:
            return "Reach Tier 5 in order to upgrade your max damage some more"
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
        weapon = self.getweapon()
        if self.critchance - weapon.critplus >= 65:
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
        value = [w for w in allweapons if w.name == self.weapon]
        return value[0]

    def getgear(self):
        weapon = [w for w in allweapons if w.name == self.weapon]
        armor = [t for t in allarmor if t.name == self.armour]

        return weapon[0], armor[0]

    def getTier(self):
        if self.health <= 249:
            return 1
        elif self.health >= 250 and self.health <= 350:
            return 2
        elif self.health >= 351 and self.health <= 950:
            return 3
        elif self.health >= 951 and self.health <= 2999:
            return 4
        else:
            return 5


class FightMe(Fighter):

    def instantize(self):
        if self.ability == None:
            pass
        else:
            value = [x for x in allabilities if x.name == self.ability]
            self.ability = value[0]
        

        if self.passive == None:
            pass
        else:
            value = [x for x in passives if x.name == self.passive]
            self.passive = value[0]

        weapon = [w for w in allweapons if w.name == self.weapon]
        armor = [t for t in allarmor if t.name == self.armour]

        self.weapon, self.armour = copy.copy(weapon[0]), copy.copy(armor[0])

        
        self.buffup()

    def buffup(self):
        self.attackmsg = self.weapon.effect
        self.health += self.armour.hpup
        self.maxdmg += self.armour.pup
        self.critchance += self.weapon.critplus

    def buff(self):
        if self.armour.name == "Solar Flare":
            self.weapon.damage += 20
            self.health += 50
            msg = "Increased damage of Solar Flare by 20 and health by 50"

        elif self.armour.name == "Shadow Flame":
            self.weapon.damage += 60
            self.health += 100
            self.mindmg += 15
            msg = "Increased damage of Shadow Flame Knife by 60, Increased health by 100, and increased mindmg by 15"

        elif self.armour.name == "True Plague Doctors Uniform":
            self.health += 100
            self.weapon.damage += 45
            self.critchance += 5
            self.weapon.healplus += 6
            msg = "Increased Damage of Plague Doctors Scepter by 45. Increased Health by 100. Increased Critchance by 5%. Increased lifesteal by 6%"

        elif self.armour.name == "Valkryie":
            self.health += 40
            self.weapon.damage += 5
            msg = "Increased Damge of Axe by 5, and increased health by 40"

        elif self.armour.name == "Assassins":
            self.health += 10
            self.weapon.damage += 15
            msg = "Increased Damage of Dagger by 15, added 3% lifesteal and +10 health"

        elif self.armour.name == "Charged Ranger":
            self.weapon.damage += 30
            self.armour.regen += 5
            self.mindmg += 10
            msg = "Increased Weapon damage by 30, 5% regen and increase min damage by 10"       

        elif self.armour.name == "Diamond":
            self.health += 35
            self.weapon.damage += 15
            msg = "Increased Weapon Damage by 15, and increased health by 35"     

        elif self.armour.name == "Wooden":
            self.health += 200
            self.weapon.critplus += 3
            self.weapon.damage += 15
            msg = "Increased Health by 200, increased weapon damage by 15, and critchance by 3%"

        elif self.armour.name == "Slime":
            self.health += 20
            self.weapon.damage += 15
            self.weapon.critplus += 4
            msg = "Increased Health by 20, increased Damage of Baby Slime by 15, and increased crit chance by 4"

        elif self.armour.name == "Parade Creators Outfit":
            self.health += 60
            self.weapon.damage += 40
            self.weapon.critplus += 2
            self.weapon.healplus += 2
            self.mindmg += 40
            self.maxdmg += 40
            msg = "Increased Health by 60. Increased Min, max and weapon damage by 40. Increased Crit Chance and heal% by 2%"
        
        elif self.armour.name == "Master General":
            self.health += 220
            self.weapon.damage += 20
            msg = "Increased health by 220. Increased weapon damage by 20"

        elif self.armour.name == "Tundra Ranger":
            self.health += 150
            self.critchance += 15
            self.weapon.damage += 15
            self.weapon.healplus += 3
            msg = "Increased health by 150. Increased Critchance and weapon damage by 15. Increased weapon lifesteal by 3%"
        
        elif self.armour.name == "Vibe Master":
            self.critchance += 100
            self.weapon.damage += 30
            msg = "Increased crit chance by 100. Increased weapon damage by 30"

        elif self.armour.name == "Vampiric Cloak":
            self.health += 200
            self.weapon.healplus += 5
            self.armour.regen += 2
            self.weapon.damage += 40
            msg = "Increased Health by 200, lifesteal on ENC Vamp Knives by 5%, damage on ENC Vamp Knives by 40 and regen on Vamp Cloak by 2%"

        elif self.armour.name == "Nightmare":
            self.health += 120
            self.weapon.damage += 120
            self.attackmsg = "Sealed the dreams of"
            return "Increased health and weapon damage by 120"

        elif self.armour.name == "Haoshoku Haki":
            self.health += 500
            self.weapon.damage += 400
            self.weapon.healplus += 4
            self.armour.regen += 4
            self.critchance += 10
            self.mindmg += 20
            self.maxdmg += 20
            self.attackmsg = "manipulates the existence of"
            return "This is your birthrite. Increased health by 500, Damage of Conquerors by 400, increased lifesteal on both Haki and Conquerors Haki by 4%,increased crit chance by 10% and increased min and max damage by 20. Able to use Haoshoku Haki passive"

        elif self.armour.name == "Yang":
            self.health += 500
            self.weapon.damage += 400
            self.weapon.healplus += 4
            self.armour.regen += 4
            self.critchance += 10
            self.mindmg += 50
            self.maxdmg += 50
            self.attackmsg = "manipulates the mind and soul of"
            return "Perfect balanced has been achieved. Increased health by 500, Damage of Yin Blade by 400, increased lifesteal on both Yang and Yin by 4%,increased crit chance by 10% and increased min and max damage by 50. Able to use Pride of Balance Passive"
        
        else:
            return "Something went wrong"

        return msg


    def hpcheck(self):
        return self.health

    def attack(self, dmg):
        self.health -= dmg

    def heal(self, amount):
        self.health += amount
    
    

    def abiluse(self, power):
        powerinc, powerticinc, healthinc, lodmginc, hidmginc, perhealth = self.ability.use()
        power *= powerinc
        power += powerticinc
        self.health += healthinc
        self.mindmg += lodmginc
        self.maxdmg += hidmginc
        perhealth = math.ceil((perhealth/ 100) * self.health)
        self.health += perhealth

        return power

    def passuse(self, power):
        powerinc, powerticinc, healthinc, lodmginc, hidmginc, perhealth = self.passive.use()
        power *= powerinc
        power += powerticinc
        self.health += healthinc
        self.mindmg += lodmginc
        self.maxdmg += hidmginc
        perhealth = math.ceil((perhealth/ 100) * self.health)
        self.health += perhealth

        return power

class BeastFight:
    def __init__(self, name, tag, health, mindmg, maxdmg, mincoin, maxcoin, entrymessage, minxp, critchance=5, healchance=3, ability=None, passive=None, attackmsg=None, weapon=fist, armour=linen, typeobj="npc"):
        self.name = name
        self.tag = tag
        self.health = health
        self.mindmg = mindmg 
        self.maxdmg = maxdmg
        self.mincoin = mincoin
        self.maxcoin = maxcoin
        self.entrymessage = entrymessage
        self.minxp = minxp
        self.maxxp = minxp + 25
        self.critchance = critchance
        self.healchance = healchance
        self.ability = ability
        self.passive = passive
        self.attackmsg = attackmsg
        self.weapon = copy.copy(weapon)
        self.armour = copy.copy(armour)
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
        powerinc, tickpow, healthinc, lodmginc, hidmginc, perhealth= self.ability.use()
        power *= powerinc
        power += tickpow
        self.health += healthinc
        self.mindmg += lodmginc
        self.maxdmg += hidmginc
        perhealth = math.ceil((perhealth/ 100) * self.health)
        self.health += perhealth

        return power

    def passuse(self, power):
        powerinc, powerticinc, healthinc, lodmginc, hidmginc, perhealth = self.passive.use()
        power *= powerinc
        power += powerticinc
        self.health += healthinc
        self.mindmg += lodmginc
        self.maxdmg += hidmginc
        perhealth = math.ceil((perhealth/ 100) * self.health)
        self.health += perhealth

        return power

    def buff(self):
        if self.armour.name == "Solar Flare":
            self.weapon.damage += 20
            self.health += 50
            msg = "Increased damage of Solar Flare by 20 and health by 50"

        elif self.armour.name == "Shadow Flame":
            self.weapon.damage += 60
            self.health += 100
            self.mindmg += 15
            msg = "Increased damage of Shadow Flame Knife by 60, Increased health by 100, and increased mindmg by 15"

        elif self.armour.name == "Plague Doctors Uniform":
            self.health += 25
            self.weapon.damage += 15
            self.critchance += 2
            self.weapon.healplus += 4
            msg = "Increased Damage of Plague Doctors Scepter by 15. Increased Health by 25. Increased Critchance by 2%. Increased lifesteal by 4%"

        elif self.armour.name == "Valkryie":
            self.health += 40
            self.weapon.damage += 5
            msg = "Increased Damge of Axe by 5, and increased health by 40"

        elif self.armour.name == "Assassins":
            self.health += 10
            self.weapon.damage += 15
            msg = "Increased Damage of Dagger by 15, added 3% lifesteal and +10 health"

        elif self.armour.name == "Charged Ranger":
            self.weapon.damage += 30
            self.armour.regen += 5
            self.mindmg += 10
            msg = "Increased Weapon damage by 30, 5% regen and increase min damage by 10"       

        elif self.armour.name == "Diamond":
            self.health += 35
            self.weapon.damage += 15
            msg = "Increased Weapon Damage by 15, and increased health by 35"     

        elif self.armour.name == "Wooden":
            self.health += 200
            self.weapon.critplus += 3
            self.weapon.damage += 15
            msg = "Increased Health by 200, increased weapon damage by 15, and critchance by 3%"

        elif self.armour.name == "Slime":
            self.health += 20
            self.weapon.damage += 15
            self.weapon.critplus += 4
            msg = "Increased Health by 20, increased Damage of Baby Slime by 15, and increased crit chance by 4"

        elif self.armour.name == "Parade Creators Outfit":
            self.health += 60
            self.weapon.damage += 5
            self.weapon.critplus += 2
            self.weapon.healplus += 2
            self.mindmg += 5
            self.maxdmg += 5
            msg = "Increased Health by 60. Increased Min, max and weapon damage by 5. Increased Crit Chance and heal% by 2%"
        
        elif self.armour.name == "Master General":
            self.health += 220
            self.weapon.damage += 10
            msg = "Increased health by 220. Increased weapon damage by 10"

        elif self.armour.name == "Tundra Ranger":
            self.health += 150
            self.critchance += 10
            self.weapon.damage += 10
            self.weapon.healplus += 3
            msg = "Increased health by 150. Increased Critchance and weapon damage by 10. Increased weapon lifesteal by 3%"
        
        elif self.armour.name == "Vibe Master":
            self.critchance += 100
            self.weapon.damage += 30
            msg = "Increased crit chance by 100. Increased weapon damage by 30"

        elif self.armour.name == "Vampiric Cloak":
            self.health += 200
            self.weapon.healplus += 5
            self.armour.regen += 2
            self.weapon.damage += 40
            msg = "Increased Health by 200, lifesteal on ENC Vamp Knives by 5%, damage on ENC Vamp Knives by 40 and regen on Vamp Cloak by 2%"

        elif self.armour.name == "Nightmare":
            self.health += 120
            self.weapon.damage += 120
            self.attackmsg = "Sealed the dreams of"
            return "Increased health and weapon damage by 120"

        elif self.armour.name == "Yang":
            self.health += 500
            self.weapon.damage += 400
            self.weapon.healplus += 4
            self.armour.regen += 4
            self.critchance += 10
            self.mindmg += 50
            self.maxdmg += 50
            self.attackmsg = "manipulates the mind and soul of"
            return "Perfect balanced has been achieved. Increased health by 500, Damage of Yin Blade by 400, increased lifesteal on both Yang and Yin by 4%,increased crit chance by 10% and increased min and max damage by 50"
        
        else:
            return "Something went wrong"

        return msg

        

# Low Level below 200 hp and Magikarp
easy1 = BeastFight("The Cat",10000, 40, 6, 30, 10, 15, "Uh... What harm could a harmless little... oh my...", 10, attackmsg="raises up and scratches")
easy2 = BeastFight("ZombieMan",10002, 60, 5, 15, 15, 25, "Ah... the typical zombie is chasing you",15, attackmsg="tickles the brains of")
easy3 = BeastFight("Magikarp",10003, 120, 1, 2, 2, 5, "No challenge... Let's make it quick",25, attackmsg="flops on")
easy4 = BeastFight("Random Meme",10005, 45, 1, 20, 20, 40, "Some one has sent you a random powerful meme...", 60, attackmsg="memes on")
easy5 = BeastFight("Robloxian Army", 10007, 60, 4, 13, 20, 60, "First their pets, now themeselves? sigh...",40, attackmsg="gangs up on")
easy6 = BeastFight("Mr.Skeleton", 10008, 70, 7, 12, 10, 30, "Mr. Skeleton has spawned.", 15, attackmsg="aims their bow and shoots")
easy7 = BeastFight("Goblin Tinkerer", 10009, 120, 10, 21, 50, 90, "Wait, I thought the Goblin Tinkerer was on our side?", 25,
 attackmsg="throws spike balls at")
easy8 = BeastFight("Annoying Discord Spammer", 10010, 120, 8, 15, 2, 10, 
"There's always that one person that loves to spam @mentions... Found him", 10, attackmsg="spams on")

easy9 = BeastFight("Possessed Friend", 10011, 125, 12, 28, 20, 40, "I can't believe your friend got possessed... again", 70, attackmsg="slashes")
easy10 = BeastFight("Baby Shark", 10012, 130, 10, 30, 30, 50, "Baby shark doo doo doo oops...",60, attackmsg="sings then bites")

# Mid Level between 200 and 300 hp
mid1 = BeastFight("Cherry Blossom", 10013, 260, 30, 50, 30, 60,"Sakur- Cherry Blossom? \"WHO YOU CALLING USELESS...\"", 360,
attackmsg="charges chakra then punches")
mid2 = BeastFight("Buh-bomb", 10014, 330, 40, 80, 45, 90, "Look who came not from Mario's world", 340, weapon=bomb,
attackmsg="says \"My main goal, is to blow up\" and explodes on")
mid3 = BeastFight("Big Rock", 10015, 345, 10, 120, 60, 100, "*Smiles*", 350 , attackmsg="Jumps then lands on")
mid4 = BeastFight("Isaiah's Parade", 10016, 324, 40, 70, 40, 70, "Parade?... no... Just a clone", 320, attackmsg="slashes")
mid5 = BeastFight("Angel Statue", 10017, 300, 70, 115, 20, 50, "An Angel Statue feel from the sky... Nice?", 310, attackmsg="Pounds on")
mid6 = BeastFight("Azoth", 10018, 320, 40, 80, 40, 70, "Straight from Valhalla, Azoth is here", 330, ability=deadlygrasp, weapon=axe,
attackmsg="swings his axe at")

mid7 = BeastFight("Valkryie", 10019, 330, 40, 70, 100, 120, "Uh... I think she found out we stole their armour", 440, 8, ability=critstrike, weapon=axe,
armour=valkryie, attackmsg="swings her axes and slashes")

mid8 = BeastFight("Rick Sanchez", 10020, 325, 45, 70, 80, 130,"Guess who just popped out of a portal ready to attack", 470,
 ability=pickelize, attackmsg="blasts", weapon=blaster)

mid9 = BeastFight("Slivial", 10021, 325, 50, 76, 120, 250, "Straight from Slimenia, He summons his tank", 500, 6, 5, blast, regeneration,
"Shoots some ammo from his cannon at", weapon=miracles)

mid10 = BeastFight("Sanic", 10022, 340, 60, 90, 125, 150, "Gotta go fast", 430, 15, ability=sonic, attackmsg="zooms around then hits")






# High Level between 300 and 950 hp
hard1 = BeastFight("DRAGON!",10001, 400, 70, 110, 220, 400, "Dragon goes rawr but no 'XD'",500, ability=blast, attackmsg="Breathes on", armour=iron)
hard2 = BeastFight("Dio",10004, 449, 90, 160, 350, 600, "Oh no... It's dio... Quick, take him out. (Not on a date mind you)",700, ability=theworld, passive=regeneration,
weapon=vampknives,armour=gold, attackmsg="Barrages on")
hard3 = BeastFight("Red Paladins", 10006, 510, 115, 300, 250, 300, "The Red Paladins have arrived.",450, ability=swarm, weapon=axe, attackmsg="Gather and attack")
hard4 = BeastFight("Queen Bee", 10025, 545, 180, 290, 300, 370, "Queen Bee has Awoken", 430, ability=swarm, attackmsg="Rams into") 
hard5 = BeastFight("Kairo", 10026, 449, 200, 230, 250, 320, "Out of the trash, the Racoon has emerged", 450, ability=swarm,
attackmsg="bites")
hard6 = BeastFight("Money Tree", 10029, 700, 270, 320, 1000, 1200, "Who said money doesn't grow on trees.",
500, attackmsg="Blows money on")
hard7 = BeastFight("The Story Teller", 10031, 650, 330, 470, 1100, 1300, "The story Teller is angry you slept through his story",
450, attackmsg="Reads to", passive=dodge)

# tier 4 mofos
ut1 = BeastFight("DIO!", 10024, 1100, 400, 550, 19000, 20950, "Dio... no... it's DIO", 1000, 15, 60, theworld, regeneration,"Attacks", vampknives, gold)
ut2 = BeastFight("Robloxian Lord", 10023, 940, 200, 250, 15050, 17000, "Uh oh... A big one", 540, ability=swarm, passive=dodge, attackmsg="Memes on",
weapon=blaster, armour=saiyanguc)
ut3 = BeastFight("Ender Dragon", 10027, 1000, 450, 480, 17000, 18050, "Uh, Something was wrong with the respawn system, and now it's in your world", 500,
ability=blast, attackmsg="Breathes on")
ut4 = BeastFight("Moon Lord", 10028, 2000, 750, 800, 17000, 20000, "Impending Doom Approaches", 1000,10,20,
critstrike, regeneration, "Summons a Phantasmal Deathray and blasts", armour=abyss)
ut5 = BeastFight("Young Flame Handler", 10037, 1020, 500, 600, 17000, 19000, "His job... defeat you", 800, 5, 3, critstrike, attackmsg="strikes",
weapon=sfknife, armour=shadowflame)

# Tier 5
nme = BeastFight("NME", 10031, 7000, 1100, 1300, 42400, 52800, "NME is the enemy and he's come to prove that", 4000, 
20, 25, nmareterror, sboost, "devours the nightmares of", sfknife, shadowflame)
isama = BeastFight("Isaiah-Sama", 10030, 5500, 600, 800, 31400, 35600, "Isaiah has Arrived, but is nerfed", 1200, 15,20, theworld, regeneration,
 "fires at", seruption, solarflare)
uksniper = BeastFight("Unknown Sniper", 10032, 5000, 700, 900, 32000, 38000, "You feel someone watching you", 
4000, 5, 3, critstrike, sharpeye, "snipes", srifle, sranger)
sfass = BeastFight("Shadow Flame Assassin", 10033, 6000, 900, 1000, 40000, 44000, "You glimpse a shadow following you",
3500, 25, 10, critstrike, dodge, "slashes at", sfknife, shadowflame)
kdono = BeastFight("Kevin not Kevin", 10034, 8000, 1000, 1200, 58000, 64000, "KEVIN!!!", 5000, 5, 20, uheal, regeneration,
"menacingly approaches", hcard, vknight)
tmaster = BeastFight("Tank Master", 10035, 9000, 1000, 1200, 58000, 64000, "have you ever seen a tank up close?", 5000, 5,3,
blast, sharpeye, "Summons his tank, aims it, and fires", tsummon, artillery)
rebdio = BeastFight("DIO Reborn", 10036, 10500, 1600, 1800, 64000, 670000, "It's like he never dies.", 6000, 20,5, uheal, regeneration,
"flash freezes then drains", evampknife, vampcloak)

# Lists

enemy = [
easy1, easy2, easy3, easy4, easy5, easy6, easy7, easy8, easy9, easy10, 
mid1, mid2, mid3, mid4, mid5, mid6, mid7, mid8, mid9, mid10,
hard1, hard2, hard3, hard4, hard5, hard6, hard7,
ut1, ut2, ut3, ut4, ut5,
isama, nme, uksniper, sfass, kdono, tmaster, rebdio
]

# def __init__(self, name, tag, health, mindmg, maxdmg, mincoin, maxcoin, entrymessage, minxp, 
# critchance=5, healchance=3, ability=None, passive=None, attackmsg=None, weapon=fist, armour=linen, 
# typeobj="npc"):

# Raid Monster
bebebe = BeastFight("Giant King Be Be Be", 90001, 6000, 200, 300, 8000, 10000, "Giant King Be Be Be has been awoken... and is very angry",1000,
30, 25, bebebeslam, harder, "BE BE BE STRIKE!")

giggeng = BeastFight("Giant Gargen", 90002, 9000, 450, 700, 9000, 12000, "A wild Giantified Gargen Has Appeared", 1500, 20, 20, ssuck, nlove, "Attacks", armour=gold)

biggums = BeastFight("Biggums", 90003, 11000, 650, 750, 25000, 30000, "Biggums is rising out of the earth. Isn't as big as we were told however.", 2000,
20, 40, bellybump, harder, "kicks a giant foot at")

oogabooga = BeastFight("Ooga Booga", 90004, 14000, 800, 900, 40000, 50000, "Music plays as this giant tribal Man falls from the sky", 2500, 5, 3, swarm, sboost,
"dances then attacks", vibechk, wood)

anansi = BeastFight("Anansi", 90005, 16000, 1000, 1100, 50000, 60000, "Anansi is a spider, Anansi is a man. Now he's big and giant, and your head is his demand.",
3000, 2, 10, swarm, rage, "Transforms then attacks", armour=assas)

pdoctor = BeastFight("Plague Doctor", 90006, 20000, 1300, 1400, 60000, 72000, "...?", 4000, 3, 20, plague, sharpeye, "Spreads the plague to", pds,
plaguearm)

slimeraid = BeastFight("Prince Slime", 90007, 30000, 400, 500, 25000, 29000, "Prince Slime has awoken", 2000,
attackmsg="Bounces on", weapon=slime, armour=slimearm)

loc = BeastFight("Lord Of Creation and Destruction", 90008, 100000, 6000, 8000, 100000, 400000, "1 force descends from heaven, the other from the underworld. Now... they are one",
10000, 40, 30, None, critblock, "manipulates the existence of", yin, yang)



raidingmonster = [bebebe, giggeng, biggums, oogabooga, anansi, pdoctor, slimeraid, loc]

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

