import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from dataclasses import dataclass



@dataclass
class MyHelp:
    def __init__(self, category, name, usage, desc, alias=None, cooldown=None):
        self.category = category
        self.name = name
        self.usage = usage
        self.desc = desc
        self.alias = alias
        self.cooldown = cooldown

    def info(self):
        cmdbed = discord.Embed(
            title=f"Help on {self.name}",
            description=f"{self.desc}",
            color=randint(0, 0xffffff)
        )

        cmdbed.add_field(name="Usage:", value=f"{self.usage}")
        cmdbed.add_field(name="cooldown:", value=f"{self.cooldown}")
        cmdbed.add_field(name="Aliases:", value=f"{self.alias}")

        return cmdbed

class HelpCom(commands.Cog):
    
    @commands.command()
    async def help(self, ctx, *, param=None):
        if param is None:
            await ctx.send("""Do <>help categoryname for the list of commands in that category
You can also do <>help commandname for more info on that command.
Available categories are Action, Battle, Mod, Misc, gaming, general and social""")
            return

        tosend = []
        categ = [x for x in mycommands if x.category.lower() == param.lower()] 
        templist = []

        if categ:
            for thing in categ:
                tosend.append(f"{thing.name}. Usage: {thing.usage}. Aliases: {thing.alias}")
            
            tosend = '\n# '.join(tosend)
            
            await ctx.send(f"""```md\n{tosend}\n```""")

        else:
            zacmd = [x for x in mycommands if param.lower() in x.name.lower() or param.lower() in x.usage.lower()]
            if zacmd:
                for thing in zacmd:
                    tosend.append(thing.info())
                
                for item in tosend:
                    msg = await ctx.send(embed=item)
                    templist.append(msg)
                
                await asyncio.sleep(30)
                for tmsg in templist:
                    await tmsg.delete()
            else:
                await ctx.send("Not a command or category")

barrage = MyHelp("Action", "Barrage", "<>barrage @mention", "An action command which allows you to barrage the one you mention")
blush = MyHelp("Action", "Blush", "<>blush", "A self action that can be used to indictate you are blushing")
clown = MyHelp("Action", "Clown", "<>clown", "Sends an image. To be used when someone is clowning")
condescend = MyHelp("Action", "Condescend", "<>condescend @mention", "To be used when someone does something very questionable")
cry = MyHelp("Action", "Cry", "<>cry", "Aww...")
dance = MyHelp("Action", "Dance", "<>dance", "Just vibin'")
fistbump = MyHelp("Action", "Fistbump", "<>fistbump", "Brotherhood")
flex = MyHelp("Action", "Flex", "<>flex @mention", "Generally used to flex on someone")
hug = MyHelp("Action", "Hug", "<>hug @mention", "We all need one sometimes... probably")
kiss = MyHelp("Action", "Kiss", "<>kiss @mention", "Just a lil love and affection")
pat = MyHelp("Action", "Pat", "<>pat @mention", "There there.")
poke = MyHelp("Action", "Poke", "<>poke @mention", "Good for getting someone's attention")
pose = MyHelp("Action", "Pose", "<>pose", "JO-JO... POSE!!!")
punch = MyHelp("Action", "Punch", "<>punch @mention", "Always that one person that just deserves it")
slap = MyHelp("Action", "Slap", "<>slap @mention", "They probably earned it :shrug:")

afk = MyHelp("Misc", "Afk", "<>afk optionalReason", "Generally used to indicate you going afk. When you are mentioned, the reason will be displayed along with the fact that you are afk")
back = MyHelp("Misc", "Back", "<>back", "Used to announce your return from being afk")
resetnick = MyHelp("Misc", "Resetnick", "<>resetnick", "Used to reset your nickname for that server")
suggest = MyHelp("Misc", "Suggest", "<>suggest [suggestion]", "Used to make a suggestion for the bot")
emoji = MyHelp("Misc", "Emoji", "<>emoji [emoji name]", "Useless... but hey. Requires exact emoji name")
me = MyHelp("Misc", "Me", "<>me message", "Used to send your message as an embed >:)")
mentioned = MyHelp("Misc", "Mentioned", "<>mentioned", "Looks through the last 700 messages to see if you were pinged\
If true, then it sends the message in which you were pinged")
nohide = MyHelp("Misc", "Nohide", "<>nohide", "Cheeky little command that show a deleted message within 3 minutes")
ping = MyHelp("Misc", "Ping", "<>ping", "Used to view the bot's Ping")
intercom = MyHelp("Misc", "Intercom", "<>intercom", "Used to open a channel for another server/channel to join nice for meeting strangers")
endcall = MyHelp("Misc", "endcall", "<>endcall", "Used to end an intercom")
gcall = MyHelp("Misc", "Group Call", "<>gcall", "Used to create a multi-server call with any servers that join")
gjoin = MyHelp("Misc", "Group Join", "gjoin", "Used to join an existing multi server call")
gleave = MyHelp("Misc", "Group Leave", "<>gleave", "Used to leave the multi-server call you are in")
namegen = MyHelp("Misc", "Name generator", "<>namegen number", "Generates a name with the amount of letters you specified. Max is 11 for sake of it still making a bit of sense")
soulmate = MyHelp("Misc", "Soulmate", "<>soulmate", "Reveals the first letter of your soulmate... probably")
parade = MyHelp("Misc", "Parade", "<>parade", "Gets the invite link to the bot's discord")

accept = MyHelp("Battle", "accept", "<>accept teamname", "Used to accept a team invite")
active = MyHelp("Battle", "Active", "<>active", "Used to view the Ability table.", "ability")
adventure = MyHelp("Battle", "Adventure", "<>adventure", "Currently only available for the leader of a team. Invites teammates to take part in adventures")
buy = MyHelp("Battle", "Buy", "<>buy itemname", "Used to purchase an item")
createprofile = MyHelp("Battle", "Create Profile", "<>createprofile", "Used to create a profile to use Battle Commands")
deny = MyHelp("Battle", "deny", "<>deny teamname", "Used to reject a team invite")
fight = MyHelp("Battle", "Fight", "<>fight @mention", "Used to fight someone who also has a battle profile", cooldown="30 seconds")
gear = MyHelp("Battle", "Gear", "<>gear", "Used to view your current equipment loadout")
gods = MyHelp("Battle", "Gods", "<>gods", "Used to view the first 25 Tier 6 legends")
grant = MyHelp("Battle", "Grant", "<>grant @mention amount", "Used to give the one you mentioned the amount of cash you specify")
invite = MyHelp("Battle", "Invite", "<>invite @mention", "Used by the leader of a team to invite a member to their team")
job = MyHelp("Battle", "Job", "<>job", "Used to do a job for some quick cash", "<>j", "1 minute")
kickmember = MyHelp("Battle", "Kick Member", "<>kickmember @mention", "Used by team leaders to kick someone from thier team")
leaveteam = MyHelp("Battle", "Leave Team", "<>leaveteam", "Used to leave your team")
myteam = MyHelp("Battle", "My team", "<>myteam", "Used to view your team", "<>team")
paradecoins = MyHelp("Battle", "Parade Coins", "<>paradecoins", "used to view your parade coins. The currency of Battle", "pcoins")
paraid = MyHelp("Battle", "Paraid", "<>paraid", "Used by anyone above level 40 to start a raid", cooldown="20 minutes per guild")
paraid6 = MyHelp("Battle", "Paraid6", "<>paraid6", "Usable by all members in Tier 6. Starts a raid", cooldown="10 minutes")
passive = MyHelp("Battle", "Passive", "<>passive", "Used to view the passive table")
powprofile = MyHelp("Battle", "Power Profile", "<>powprofile", "Used to view your profile in it's buffed state as it would be during a fight")
profile = MyHelp("Battle", "Profile", "<>profile", "Used to view your stat profile")
quest = MyHelp("Battle", "Quest", "<>quest", "Used to do a quest for exp and cash", "<>q", "3 minutes")
quest6 = MyHelp("Battle", "Quest6", "<>quest6", "Usable only by members in Tier 6", "<>q6", "1 minute")
raid = MyHelp("Battle", "Raid", "<>raid", "Used to join a raid. Raids only naturally occur in the home server. Get the invite with <>parade")
readd = MyHelp("Battle", "Re-add", "<>readd", "Used to toggle your Parader role.")
rebase = MyHelp("Battle", "Rebase", "<>rebase", "Used to change your team's home server to the one you are currently in")
register = MyHelp("Battle", "Register", "<>register teamname", "Used to create a team")
reward = MyHelp("Battle", "Reward", "<>reward", "Gives you a reward", cooldown="1 hour")
search = MyHelp("Battle", "Search", "<>search", "Looks for other Paraders who are in your tier that have their fight enabled")
sell = MyHelp("Battle", "Sell", "<>sell true weapon/armour/item", "Sells your Weapon, armour or item")
shop = MyHelp("Battle", "Shop", "<>shop weapons/armor/items", "Opens the respective store")
switch = MyHelp("Battle", "Switch", "<>switch", "Used to switch your current gear loadout")
teams = MyHelp("Battle", "Teams", "<>teams", "Shows the first 25 teams in the server you are in")
tier = MyHelp("Battle", "Tier", "<>tier", "Shows the information on how tiers work")
togglefight = MyHelp("Battle", "Toggle Fight", "<>togglefight", "used to toggle whether or not you can be fought")
upgrade = MyHelp("Battle", "Upgrade", "<>upgrade", "Shows your stat table")
upgrade2 = MyHelp("Battle", "Upgrade", "<>upgrade statname", "Upgrades the stat which you specify")
upgrade3 = MyHelp("Battle", "Upgrade", "<>upgrade statname amount", "Upgrades the stat the specified number of times")
view = MyHelp("Battle", "View", "<>view itemname", "Shows more information on the item/weapon/armour you said")
use = MyHelp("Battle", "Use", "<>use itemid", "Uses the buff item/potion")
reborn = MyHelp("Battle", "Reborn", "<>reborn", "Must be tier 6. Allows you to go back to tier 1 and progress again. You keep 1% hp and 3% of other stats added on to the base. Crit and Healchance remain unaffected")

startgame = MyHelp("Gaming", "Start Game", "<>startgame", "Used to start a game of hangman")
endgame = MyHelp("Gaming", "End Game", "<>endgame", "Used to end a hangman game early")
endstory = MyHelp("Gaming", "End Story", "<>endstory", "Used to end and display your story")
startstory = MyHelp("Gaming", "Start Story", "<>startstory", "Activates Story mode")
wordadd = MyHelp("Gaming", "Word add", "<>wordadd word(s)", "Used to add words for the hangman game to use")
wordremove = MyHelp("Gaming", "Word Remove", "<>wordremove word", "Used to remove a word from hangman's mind")
wordshow = MyHelp("Gaming", "Word Show", "<>wordshow", "Used to show all words that hangman has in memory")

add = MyHelp("General", "Add", "<>add number1 number2", "Adds the 2 numbers")
subtract = MyHelp("General", "Subtract", "<>subtract number1 number2", "Subtracts the 2 numbers")
divide = MyHelp("General", "Divide", "<>divide number1 number2", "Divides the 2 numbers")
multiply = MyHelp("General", "Multiply", "<>multiply number1 number2", "Multiplies the 2 numbers")
allseeing = MyHelp("General", "All Seeing", "<>allseeing", "Shows information on server you are in")
heavens_door = MyHelp("General", "Heaven's Door", "<>heavens_door @mention", "Used to show information on the person you mention")
me = MyHelp("General", "Me", "<>me message", "Used to send your message as an embed")
no = MyHelp("General", "No", "<>no", "It has it's uses")
yes = MyHelp("General", "Yes", "<>yes", "Also has it's uses")
timer = MyHelp("General", "Timer", "<>timer time", "Sets a timer for the specified amount of minutes. Bot Still restarts fairly often, so don't set one for too long")
chosenone = MyHelp("General", "Chosen One", "<>choseone", "Picks a random person from the server you are in")
online = MyHelp("General", "Online", "<>online", "Used to check if the bot is online")

deathnote = MyHelp("Mod", "Deathnote", "<>deathnote @mention", "Kicks the mentioned user.")
freeze3 = MyHelp("Mod", "3 Freeze", "<>freeze3 time", "Turns on slowmode for the channel in the intervals specified by 'time'. So <>freeze3 5 will allow a user to send messages once every 5 seconds")
ger = MyHelp("Mod", "Golden Experience Requiem", "<>ger", "Used to turn off slowmode and unfreeze a channel muted with <>zawaurdo")
ger_rtz = MyHelp("Mod", "Golden Experience Requiem, Return to zero",
"<>ger_rtz @mention", "Used to strip a user of all of their roles")
impactrevive = MyHelp("Mod", "Impact Revive", "<>impactrevive userid", "Used to unban a user. You must get their id and use it in the command")
killerqueen = MyHelp("Mod", "Killer Queen", "<>killerqueen @mention duration", "Strips the mentioned user of their roles for the duration specified. After duration, the mentioned user will get back their roles 1 by 1 in minute intervals")
kingcrimson = MyHelp("Mod", "King Crimson", "<>kingcrimson @mention amount", "Deletes the amount of messages by the person mentioned")
mute = MyHelp("Mod", "Mute", "<>mute @mention", "Mutes the mentioned user")
relog = MyHelp("Mod", "Relog", "<>relog amount", "Creates a channel called logs, if it does not exist already, and sends the history of the audit log up to the specified amount")
shadowrealm = MyHelp("Mod", "Shadow realm", "<>shadowrealm @mention", "Bans the mentioned user from your server")
wipein = MyHelp("Mod", "Wipe has", "<>wipehas amount text", "Deletes messages containing the text you specify")
wipestartswith = MyHelp("Mod", "Wipe Starts with", "<>wipestartswith amount text", "Deletes messages beginning with the text you specify")
wipeendswith = MyHelp("Mod", "Wipe Ends With", "<>wipeendswith amount text", "Deletes messages ending with the text you specify")
zahando = MyHelp("Mod", "Za Hando", "<>zahando amount", "Deletes the amount of messages you specify")
zawarudo = MyHelp("Mod", "ZA WARUDO", "<>zawarudo time", "Stops everyone without manage channel permissions from speaking in the channel for that duration. Essentially a channel mute")
profane = MyHelp("Mod", "Profane", "<>profane", "Used to toggle whether you want profanity moderated or not")
tmsg = MyHelp("Mod", "Track Joins and Leaves", "<>trackjoins", "Used to toggle whether I will track join and leaves or not")
tmsg2 = MyHelp("Mod", "Track Joins and Leaves", "<>trackjoins message", "Used when toggling to set a message to send when a user joins")

acceptbff = MyHelp("Social", "Accept bff", "<>acceptbff", "Accepts a pending best friend request. You can only have 1")
acceptfr = MyHelp("Social", "Accept friend request", "<>acceptfr", "Accepts a pending friend request")
acceptlove = MyHelp("Social", "Accept love", "<>acceptlove", "Accepts a pending friend request")
acceptparent = MyHelp("Social", "Accept Parent", "<>acceptparent", "Accepts a pending parent request")
addfriend = MyHelp("Social", "Add friend", "<>addfriend @mention", "sends a friend request to the mentioned user")
addlove = MyHelp("Social", "Add Love", "<>addlove @mention", "Sends a love request to the mentioned user")
createsocial = MyHelp("Social", "Create Social", "<>createsocial", "Creates a social profile to be used with Social commands")
delpet = MyHelp("Social", "Delpet", "<>delpet True", "Used to delete your pet")
denybff = MyHelp("Social", "Deny bff", "<>denybff", "Denies a pending best friend request. You can only have 1")
denyfr = MyHelp("Social", "Deny friend request", "<>denyfr", "Denies a pending friend request")
denylove = MyHelp("Social", "Deny love", "<>denylove", "Denies a pending friend request")
denyparent = MyHelp("Social", "Deny Parent", "<>denyparent", "Denies a pending parent request")
dump = MyHelp("Social", "Dump", "<>dump", "Used to break up with your partner")
feed = MyHelp("Social", "Feed", "<>feed", "Used to feed your pet")
getpet = MyHelp("Social", "Get Pet", "<>getpet", "Used to get a pet")
newbff = MyHelp("Social", "New BFF", "<>newbff @mention", "Sends a best friend request to the person you mentioned")
newchild = MyHelp("Social", "New Child", "<>newchild @mention", "Sends a request to the mentioned user request to be their parent")
pet = MyHelp("Social", "Pet", "<>pet", "Used to view your pet")
play = MyHelp("Social", "Play", "<>play", "Used to play with your pet")
showfriends = MyHelp("Social", "Show friends", "<>showfriends", "Shows your friends")
updatesocial = MyHelp("Social", "Update Social", "<>updatesocial", "Changes the name and guild on your social profile to match your nickname and guild name of the one you are in")
socialprofile = MyHelp("Social", "Social profile", "<>socialprofile", "Displays your social profile", "<>sp")
nickpet = MyHelp("Social", "Nick pet", "<>nickpet name", "Gives your pet a nickname")

mycommands = [barrage, blush, clown, condescend, cry, dance, fistbump, flex, hug, kiss, pat, poke, pose, punch,
slap, afk, back, resetnick, suggest, intercom, endcall, accept, active, adventure, buy, createprofile,
deny, fight, gear, gods, grant, invite, job, kickmember, leaveteam, myteam, paradecoins, paraid,
paraid6, passive, powprofile, profile, quest, quest6, raid, readd, rebase, register, reward, search, sell, shop,
switch, teams, tier, togglefight, upgrade, upgrade2, upgrade3, view, endgame, endstory, startgame, startstory, wordadd, wordremove,
wordshow, add, allseeing, chosenone, divide, heavens_door, me, multiply, no, online, subtract, timer, yes,
gcall, gjoin, gleave, emoji, mentioned, nohide, ping, deathnote, freeze3, ger, ger_rtz, 
impactrevive, killerqueen, kingcrimson, mute, relog, shadowrealm, wipein, wipestartswith, wipeendswith, zahando, zawarudo, namegen, soulmate,
profane, acceptbff, acceptfr, acceptlove, acceptparent, addfriend, addlove, createsocial, delpet, denybff,
denylove, denyparent, dump, feed, getpet, newbff, newchild, pet, play, showfriends, socialprofile,
updatesocial, parade, use, nickpet, reborn, tmsg, tmsg2]


def setup(bot):
    bot.add_cog(HelpCom(bot))
