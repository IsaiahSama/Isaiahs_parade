import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from dataclasses import dataclass



@dataclass
class Help:
    category: str
    name: str
    usage: str
    desc: str
    alias: str=None
    cooldown: str=None

    def info(self):
        return f"{self.category}: {self.name} - {self.desc}"


class HelpCom(commands.Cog):
    
    @commands.command()
    async def help(self, ctx, param=None):
        pass
        

barrage = Help("Action", "Barrage", "<>barrage @mention", "An action command which allows you to barrage the one you mention")
blush = Help("Action", "Blush", "<>blush", "A self action that can be used to indictate you are blushing")
clown = Help("Action", "Clown", "<>clown", "Sends an image. To be used when someone is clowning")
condescend = Help("Action", "Condescend", "<>condescend @mention", "To be used when someone does something very questionable")
cry = Help("Action", "Cry", "<>cry", "Aww...")
dance = Help("Action", "Dance", "<>dance", "Just vibin'")
fistbump = Help("Action", "Fistbump", "<>fistbump", "Brotherhood")
flex = Help("Action", "Flex", "<>flex @mention", "Generally used to flex on someone")
hug = Help("Action", "Hug", "<>hug @mention", "We all need one sometimes... probably")
kiss = Help("Action", "Kiss", "<>kiss @mention", "Just a lil love and affection")
pat = Help("Action", "Pat", "<>pat @mention", "There there.")
poke = Help("Action", "Poke", "<>poke @mention", "Good for getting someone's attention")
pose = Help("Action", "Pose", "<>pose", "JO-JO... POSE!!!")
punch = Help("Action", "Punch", "<>punch @mention", "Always that one person that just deserves it")
slap = Help("Action", "Slap", "<>slap @mention", "They probably earned it :shrug:")

afk = Help("Misc", "Afk", "<>afk optionalReason", "Generally used to indicate you going afk. When you are mentioned, the reason will be displayed along with the fact that you are afk")
back = Help("Misc", "Back", "<>back", "Used to announce your return from being afk")
resetnick = Help("Misc", "Resetnick", "<>resetnick", "Used to reset your nickname for that server")
suggest = Help("Misc", "Suggest", "<>suggest [suggestion]", "Used to make a suggestion for the bot")
emoji = Help("Misc", "Emoji", "<>emoji [emoji name]", "Useless... but hey. Requires exact emoji name")
me = Help("Misc", "Me", "<>me message", "Used to send your message as an embed >:)")
mentioned = Help("Misc", "Mentioned", "<>mentioned", "Looks through the last 700 messages to see if you were pinged\
If true, then it sends the message in which you were pinged")
nohide = Help("Misc", "Nohide", "<>nohide", "Cheeky little command that show a deleted message within 3 minutes")
ping = Help("Misc", "Ping", "<>ping", "Used to view the bot's Ping")
intercom = Help("Misc", "Intercom", "<>intercom", "Used to open a channel for another server/channel to join nice for meeting strangers")
endcall = Help("Misc", "endcall", "<>endcall", "Used to end an intercom")
gcall = Help("Misc", "Group Call", "<>gcall", "Used to create a multi-server call with any servers that join")
gjoin = Help("Misc", "Group Join", "gjoin", "Used to join an existing multi server call")
gleave = Help("Misc", "Group Leave", "<>gleave", "Used to leave the multi-server call you are in")
namegen = Help("Misc", "Name generator", "<>namegen number", "Generates a name with the amount of letters you specified. Max is 11 for sake of it still making a bit of sense")
soulmate = Help("Misc", "Soulmate", "<>soulmate", "Reveals the first letter of your soulmate... probably")
parade = Help("Misc", "Parade", "<>parade", "Gets the invite link to the bot's discord")

accept = Help("Battle", "accept", "<>accept teamname", "Used to accept a team invite")
active = Help("Battle", "Active", "<>active", "Used to view the Ability table.", "ability")
adventure = Help("Battle", "Adventure", "<>adventure", "Currently only available for the leader of a team. Invites teammates to take part in adventures")
buy = Help("Battle", "Buy", "<>buy itemname", "Used to purchase an item")
createprofile = Help("Battle", "Create Profile", "<>createprofile", "Used to create a profile to use Battle Commands")
deny = Help("Battle", "deny", "<>deny teamname", "Used to reject a team invite")
fight = Help("Battle", "Fight", "<>fight @mention", "Used to fight someone who also has a battle profile", cooldown="30 seconds")
gear = Help("Battle", "Gear", "<>gear", "Used to view your current equipment loadout")
gods = Help("Battle", "Gods", "<>gods", "Used to view the first 25 Tier 6 legends")
grant = Help("Battle", "Grant", "<>grant @mention amount", "Used to give the one you mentioned the amount of cash you specify")
invite = Help("Battle", "Invite", "<>invite @mention", "Used by the leader of a team to invite a member to their team")
job = Help("Battle", "Job", "<>job", "Used to do a job for some quick cash", "<>j", "1 minute")
kickmember = Help("Battle", "Kick Member", "<>kickmember @mention", "Used by team leaders to kick someone from thier team")
leaveteam = Help("Battle", "Leave Team", "<>leaveteam", "Used to leave your team")
myteam = Help("Battle", "My team", "<>myteam", "Used to view your team", "<>team")
paradecoins = Help("Battle", "Parade Coins", "<>paradecoins", "used to view your parade coins. The currency of Battle", "pcoins")
paraid = Help("Battle", "Paraid", "<>paraid", "Used by anyone above level 40 to start a raid", cooldown="20 minutes per guild")
paraid6 = Help("Battle", "Paraid6", "<>paraid6", "Usable by all members in Tier 6. Starts a raid", cooldown="10 minutes")
passive = Help("Battle", "Passive", "<>passive", "Used to view the passive table")
powprofile = Help("Battle", "Power Profile", "<>powprofile", "Used to view your profile in it's buffed state as it would be during a fight")
profile = Help("Battle", "Profile", "<>profile", "Used to view your stat profile")
quest = Help("Battle", "Quest", "<>quest", "Used to do a quest for exp and cash", "<>q", "3 minutes")
quest6 = Help("Battle", "Quest6", "<>quest6", "Usable only by members in Tier 6", "<>q6", "1 minute")
raid = Help("Battle", "Raid", "<>raid", "Used to join a raid. Raids only naturally occur in the home server. Get the invite with <>parade")
readd = Help("Battle", "Re-add", "<>readd", "Used to toggle your Parader role.")
rebase = Help("Battle", "Rebase", "<>rebase", "Used to change your team's home server to the one you are currently in")
register = Help("Battle", "Register", "<>register teamname", "Used to create a team")
reward = Help("Battle", "Reward", "<>reward", "Gives you a reward", cooldown="1 hour")
search = Help("Battle", "Search", "<>search", "Looks for other Paraders who are in your tier that have their fight enabled")
sell = Help("Battle", "Sell", "<>sell true weapon/armour/item", "Sells your Weapon, armour or item")
shop = Help("Battle", "Shop", "<>shop weapons/armor/items", "Opens the respective store")
switch = Help("Battle", "Switch", "<>switch", "Used to switch your current gear loadout")
teams = Help("Battle", "Teams", "<>teams", "Shows the first 25 teams in the server you are in")
tier = Help("Battle", "Tier", "<>tier", "Shows the information on how tiers work")
togglefight = Help("Battle", "Toggle Fight", "<>togglefight", "used to toggle whether or not you can be fought")
upgrade = Help("Battle", "Upgrade", "<>upgrade", "Shows your stat table")
upgrade2 = Help("Battle", "Upgrade", "<>upgrade statname", "Upgrades the stat which you specify")
view = Help("Battle", "View", "<>view itemname", "Shows more information on the item/weapon/armour you said")

startgame = Help("Word Games", "Start Game", "<>startgame", "Used to start a game of hangman")
endgame = Help("Word Games", "End Game", "<>endgame", "Used to end a hangman game early")
endstory = Help("Word Games", "End Story", "<>endstory", "Used to end and display your story")
startstory = Help("Word Games", "Start Story", "<>startstory", "Activates Story mode")
wordadd = Help("Word Games", "Word add", "<>wordadd word(s)", "Used to add words for the hangman game to use")
wordremove = Help("Word Games", "Word Remove", "<>wordremove word", "Used to remove a word from hangman's mind")
wordshow = Help("Word Games", "Word Show", "<>wordshow", "Used to show all words that hangman has in memory")

add = Help("General", "Add", "<>add number1 number2", "Adds the 2 numbers")
subtract = Help("General", "Subtract", "<>subtract number1 number2", "Subtracts the 2 numbers")
divide = Help("General", "Divide", "<>divide number1 number2", "Divides the 2 numbers")
multiply = Help("General", "Multiply", "<>multiply number1 number2", "Multiplies the 2 numbers")
allseeing = Help("General", "All Seeing", "<>allseeing", "Shows information on server you are in")
heavens_door = Help("General", "Heaven's Door", "<>heavens_door @mention", "Used to show information on the person you mention")
me = Help("General", "Me", "<>me message", "Used to send your message as an embed")
no = Help("General", "No", "<>no", "It has it's uses")
yes = Help("General", "Yes", "<>yes", "Also has it's uses")
timer = Help("General", "Timer", "<>timer time", "Sets a timer for the specified amount of minutes. Bot Still restarts fairly often, so don't set one for too long")
chosenone = Help("General", "Chosen One", "<>choseone", "Picks a random person from the server you are in")
online = Help("General", "Online", "<>online", "Used to check if the bot is online")

deathnote = Help("Mod", "Deathnote", "<>deathnote @mention", "Kicks the mentioned user.")
freeze3 = Help("Mod", "3 Freeze", "<>freeze3 time", "Turns on slowmode for the channel in the intervals specified by 'time'. So <>freeze3 5 will allow a user to send messages once every 5 seconds")
ger = Help("Mod", "Golden Experience Requiem", "<>ger", "Used to turn off slowmode and unfreeze a channel muted with <>zawaurdo")
ger_rtz = Help("Mod", "Golden Experience Requiem, Return to zero",
"<>ger_rtz @mention", "Used to strip a user of all of their roles")
impactrevive = Help("Mod", "Impact Revive", "<>impactrevive userid", "Used to unban a user. You must get their id and use it in the command")
killerqueen = Help("Mod", "Killer Queen", "<>killerqueen @mention duration", "Strips the mentioned user of their roles for the duration specified. After duration, the mentioned user will get back their roles 1 by 1 in minute intervals")
kingcrimson = Help("Mod", "King Crimson", "<>kingcrimson @mention amount", "Deletes the amount of messages by the person mentioned")
mute = Help("Mod", "Mute", "<>mute @mention", "Mutes the mentioned user")
relog = Help("Mod", "Relog", "<>relog amount", "Creates a channel called logs, if it does not exist already, and sends the history of the audit log up to the specified amount")
shadowrealm = Help("Mod", "Shadow realm", "<>shadowrealm @mention", "Bans the mentioned user from your server")
wipe = Help("Mod", "Wipe", "<>wipe message", "Deletes messages containing the word you specify")
zahando = Help("Mod", "Za Hando", "<>zahando amount", "Deletes the amount of messages you specify")
zawarudo = Help("Mod", "ZA WARUDO", "<>zawarudo time", "Stops everyone without manage channel permissions from speaking in the channel for that duration. Essentially a channel mute")
profane = Help("Mod", "Profane", "<>profane", "Used to toggle whether you want profanity moderated or not")

acceptbff = Help("Social", "Accept bff", "<>acceptbff", "Accepts a pending best friend request. You can only have 1")
acceptfr = Help("Social", "Accept friend request", "<>acceptfr", "Accepts a pending friend request")
acceptlove = Help("Social", "Accept love", "<>acceptlove", "Accepts a pending friend request")
acceptparent = Help("Social", "Accept Parent", "<>acceptparent", "Accepts a pending parent request")
addfriend = Help("Social", "Add friend", "<>addfriend @mention", "sends a friend request to the mentioned user")
addlove = Help("Social", "Add Love", "<>addlove @mention", "Sends a love request to the mentioned user")
createsocial = Help("Social", "Create Social", "<>createsocial", "Creates a social profile to be used with Social commands")
delpet = Help("Social", "Delpet", "<>delpet True", "Used to delete your pet")
denybff = Help("Social", "Deny bff", "<>denybff", "Denies a pending best friend request. You can only have 1")
denyfr = Help("Social", "Deny friend request", "<>denyfr", "Denies a pending friend request")
denylove = Help("Social", "Deny love", "<>denylove", "Denies a pending friend request")
denyparent = Help("Social", "Deny Parent", "<>denyparent", "Denies a pending parent request")
dump = Help("Social", "Dump", "<>dump", "Used to break up with your partner")
feed = Help("Social", "Feed", "<>feed", "Used to feed your pet")
getpet = Help("Social", "Get Pet", "<>getpet", "Used to get a pet")
newbff = Help("Social", "New BFF", "<>newbff @mention", "Sends a best friend request to the person you mentioned")
newchild = Help("Social", "New Child", "<>newchild @mention", "Sends a request to the mentioned user request to be their parent")
pet = Help("Social", "Pet", "<>pet", "Used to view your pet")
play = Help("Social", "Play", "<>play", "Used to play with your pet")
showfriends = Help("Social", "Show friends", "<>showfriends", "Shows your friends")
updatesocial = Help("Social", "Update Social", "<>updatesocial", "Changes the name and guild on your social profile to match your nickname and guild name of the one you are in")
socialprofile = Help("Social", "Social profile", "<>socialprofile", "Displays your social profile", "<>sp")

commandlist = [barrage, blush, clown, condescend, cry, dance, fistbump, flex, hug, kiss, pat, poke, pose, punch,
slap, afk, back, resetnick, suggest, intercom, endcall, accept, active, adventure, buy, createprofile,
deny, fight, gear, gods, grant, invite, job, kickmember, leaveteam, myteam, paradecoins, paraid,
paraid6, passive, powprofile, profile, quest, quest6, raid, readd, rebase, register, reward, search, sell, shop,
switch, teams, tier, togglefight, upgrade, upgrade2, view, endgame, endstory, startgame, startstory, wordadd, wordremove,
wordshow, add, allseeing, chosenone, divide, heavens_door, me, multiply, no, online, subtract, timer, yes,
gcall, gjoin, gleave, help, emoji, mentioned, nohide, ping, deathnote, freeze3, ger, ger_rtz, 
impactrevive, killerqueen, kingcrimson, mute, relog, shadowrealm, wipe, zahando, zawarudo, namegen, soulmate,
profane, acceptbff, acceptfr, acceptlove, acceptparent, addfriend, addlove, createsocial, delpet, denybff,
denylove, denyparent, dump, feed, getpet, newbff, newchild, pet, play, showfriends, socialprofile,
updatesocial, parade]


def setup(bot):
    bot.add_cog(HelpCom(bot))
