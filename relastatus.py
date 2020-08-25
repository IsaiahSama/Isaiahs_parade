import random
class relauser:
    def __init__(self, guild, name, tag, friendcount=0, hasbff=False, bfid=None, pid=None,rela=False, friends=[], parents=[], children=[], petid=None, petexp=0,
    pendingfr=None, pendinglove=None, pendingbf = None, pendingpar=None, petnick=None):
        self.guild = guild
        self.name = name
        self.tag = tag
        self.friendcount = friendcount
        self.hasbff = hasbff
        self.bfid = bfid
        self.pid = pid
        self.rela = rela
        self.friends = friends
        self.parents = parents
        self.children = children
        self.petid = petid
        self.petexp = petexp
        self.pendingfr = pendingfr
        self.pendinglove = pendinglove
        self.pendingbf = pendingbf
        self.pendingpar = pendingpar
        self.petnick = petnick

    def haspet(self):
        if self.petid == None:
            return False
        else:
            return True


class Pet:
    def __init__(self, name, desc, tag, type, stages, expreq, stage=0, evolvesinto=None, playmessage=None, feedmsg=None):
        self.name = name
        self.desc = desc
        self.tag = tag
        self.type = type
        self.stages = stages
        self.expreq = expreq
        self.stage = stage
        self.evolvesinto = evolvesinto
        self.playmessage = playmessage
        self.feedmsg = feedmsg

    def evolve(self):
        if self.name == "Egg":
            x = random.choice(petlist)
            msg = f"Congratulations. Your Egg hatched into a {x.name}. View with <>pet"
            return msg, x.tag
        
        if self.canevolve():
            msg = f"Congratulations, Your {self.name} evolved into {self.evolvesinto.name} view with <>pet"
            return msg, self.evolvesinto.tag

        else:
            return

    def canevolve(self):
        if self.evolvesinto == None:
            return False
        
        return True



# Tier 3 Pets
trex = Pet("T-Rex", "*ROARS*, It shows you it's full affection in it's own way", 20003, "Reptillian",3, 0, 3, playmessage="roars, and lets you get on it's back",
feedmsg="swallows it whole and looks at you for more")
raven = Pet("Raven", "It sits quietly on your shoulder occassionally rubbing against you", 20006, "Bird",3,
0, 3, playmessage="flies away and brings back a live worm and drops it on your lap and looks at you with a gleam in it's eyes",
feedmsg="screeches then gulps down")
luxray = Pet("Luxray", "It's loyalty to you sparks fiercely", 20009, "Mammal", 3, 0, 3,
 playmessage="purrs as you rub it, casually discharging electricity. But you are used to it by now",
 feedmsg="makes a mess and constantly discharges electricity")
sbeast = Pet("Shadow Beast", "Your seemingly omniscent friend can change their form at will, and likes to hover around you",
20012, "Unknown", 3, 0, 3, playmessage="encases you in itself and goes jumping through shadows with you", feedmsg="puts it in it's hands, clasps them together, and it vanishes")
eagle = Pet("Eagle", "A majestic bird of prey. Likes flying around you while hunting", 20015, "Bird", 3, 0, 3, playmessage="screeches and sits casually on your shoulder",
feedmsg="rapidly devours it")
tstiger = Pet("Transforming Tiger", "It's sleek black fur feels extremely nice against your skin, and it can now freely change it's shape for 5 minutes",
20018, "Mammal", 3, 0, 3, playmessage="Transforms, knocks you down, and licks you", feedmsg="feeds slowly, savouring the taste")
dragon = Pet("Dodongo", "It's powerful, you can ride on it, it's cool, what else could you want?", 20023, "Reptile",
3, 0, 3, playmessage="Puts you on it's back and runs at amazing speeds", feedmsg="inhales all of it")
nymph = Pet("Earth Nymph", "Are known to be quite the tricksters.",
20028, "Spirit", 3, 0, 3, playmessage="( ͡° ͜ʖ ͡°)", feedmsg="absorbs some of the earth's energy.")

# Tier 2 Pets
bbdino = Pet("Bigger Dinosaur", "It has quite the apetite", 20002, "Reptillian", 3, 1200, 2, trex, "roars and lifts you up with its head", "roars and devours it whole")
lilraven = Pet("Chick", "Can't help but to rub it's black sleek feathers", 20005, "Bird", 3, 800, 2, 
raven, "stares at you as you stare at it, then chirps", "raises it's head and gulps it down")
luxio = Pet("Luxio", "It's sooooo cool. It surges with energy", 20008, "Mammal", 3, 1000, 2, luxray, "discharges electricty and tackles you affectionately","shocks you and it while feeding")
seye = Pet("Shadow Eye", "You feel it gazing passionately into your eyes", 20011, "Unknown", 3, 1200, 2, sbeast, "floats around vanishing into random shadows then reappearing around you",
"makes it vanish. Still don't know where it goes though")
meagle = Pet("Chick", "It's power is growing at a rapid rate, Likes wild meat", 20014, "Bird", 3, 900, 2, eagle, "Extends it's growing wings and rubs your hand",
"occassionally nips your finger in it's haste")
tstig = Pet("Transforming Cub", "Changes shape from time to time while playing with you", 20017, "Mammal",
3, 800, 2, tstiger, "transforms into various creatures in it's excitement and circles you.", "devours")
tree = Pet("Groot", "A large tree with facial features not needing water. It's leaves look fun to ride on", 20020, "Plant",
2, 0, 2, playmessage="Picks you up, places you on it's powerful large leaves, and walks around", 
feedmsg="Extends it's leaves covering you and takes in light")
lizard = Pet("Lizard", "It's become fairly large and... these scales feel so nice?", 20022, "Reptile", 3, 1100, 2, dragon, "Roars and rubs against you",
"quickly swallows it")
monkey = Pet("Monkey de mimicry", "Likes to mimic you", 20025, "Mammal", 2, 0, 2, playmessage="claps it's hands and begins to mimic you",
feedmsg="splits it and gives you 1/3")
elmnt = Pet("Earth Elemental", "Known to frequent forests and converse with the wildlife.", 20027, "Spirit", 3,
 1000, 2, nymph, "builds a magnificent rock sculpture.", "eats some rocks.")

# Tier 1 Pets
bdino = Pet("Baby Dinosaur", "I'm the baby, gotta love me", 20001, "Reptilian", 3, 350, 2, bbdino, "bites your hand and smiles, but it doesn't have teeth", "devours it")
bird = Pet("Hatchling", "Awww, isn't it the cutest", 20004, "Bird",3, 225, 1, lilraven, "ruffles it's feathers at your touch", "gulps it down")
shinx = Pet("Shinx", "Powerfully shocking. Who would have guessed", 20007, "Mammal", 3, 250,1, luxio, "Zaps you with stored electricity, careful not to hurt you", "tears into it")
speceye = Pet("Specter Eye", "Gives off an eerie sense on omniscience", 20010, "Unknown", 3, 900, 1, seye, "Floats around then stares at you. It's almost like it's trying to smile",
"causes it to vanish, where... who knows")
bbeag = Pet("Hatchling", "There's a kind of menacing look in it's eyes", 20013, "Bird", 3, 700, 1, meagle, "screeches and gently nips your finger", "gulps it down")
tcub = Pet("Tiger Cub", "Extremely playful and energetic", 20016, "Mammal", 3, 200, 1, tstig, "rubs against your leg", "sits on your lap while eating")
sapling = Pet("Sapling", "Wait... what? It's so cool though. Uses leaves to hover around", 20019, "Plant", 2, 1000, 1, tree,
"floats up and hovers around your head", "moves away and basks in the sunlight")
bblizard = Pet("Baby Lizard", "It's little legs scuttle around so quickly over your body", 20021, "Reptile", 3,
400, 1, lizard, "excitedly runs around in circles", "eats small bites")
bbmonkey = Pet("Little Monkey","Such an appetite for one so small", 20024, "Mammal", 2, 800, 1, monkey, "smiles and dances", 
"tries to eat it whole then ask for more")
wisp = Pet("Wisp", "An energetic little ball of energy", 20026, "Spirit", 3, 300, 1, elmnt, "makes a little mud doll. How cute.", "absorbs mud.")

# Egg
egg = Pet("Egg", "The origin pet. No one knows what will emerge until it does", 20000, "Unknown", 1, 100, playmessage="shakes. It might hatch soon", 
feedmsg="Remains unmoving. Maybe it appreciated the thought tho")


allpets = [egg, monkey, lizard, tree, tstig, meagle, seye, luxio, lilraven, bbdino, dragon,
tstiger, eagle, sbeast, luxray, raven, trex, elmnt, nymph]
petlist = [bdino, bird, shinx, speceye, bbeag, tcub, sapling, bblizard, bbmonkey, wisp]

for animal in petlist:
    allpets.append(animal)