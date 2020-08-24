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

    def info(self):
        return f"{self.category}: {self.name} - {self.desc}"


class HelpCom(commands.Cog):
    
    @commands.command()
    async def help(self, ctx, param=None):
        pass
        

barrage = Help("Action", "Barrage", "<>barrage {@mention}", "An action command which allows you to barrage the one you mention")
blush = Help("Action", "Blush", "<>blush", "A self action that can be used to indictate you are blushing")
clown = Help("Action", "Clown", "<>clown", "Sends an image. To be used when someone is clowning")
condescend = Help("Action", "Condescend", "<>condescend {@mention}", "To be used when someone does something very questionable")



"""Action
barrage blush clown condescend cry dance fistbump flex hug kiss pat poke pose punch slap
Afkmake
afk back leaveguild resetnick suggest
Call
endcall intercom
FullFight
accept active adventure botrestart buy clrquest createbot createprofile deny fight gear gods grant invite job kickmember leaveteam meadd myteam paradecoins paradercount paraid paraid6 passive powprofile profile quest quest6 raid readd rebase register resetstats reward search sell shop switch teams terrorize tier togglefight upgrade view
Gaming
endgame endstory startgame startstory wordadd wordremove wordshow
General
add allseeing chosenone divide heavens_door me multiply no online subtract timer yes
GroupCall
gcall gjoin gleave
HelpCom
help
Miscgen
emoji fdeathnote hme mentioned nohide ping
Moderator
deathnote freeze3 ger ger_rtz impactrevive killerqueen kingcrimson mute relax relog rnotif shadowrealm wipe zahando zawarudo
Namegen
namegen soulmate
ProfanFilter
profane
Relamain
acceptbff acceptfr acceptlove acceptparent addfriend addlove createsocial delpet denybff denyfr denylove denyparent dump feed getpet newbff newchild pet play save showfriends socialprofile updatesocial viewall
Special
byakugan completed csteal delmistake failure fotd notif observer rolecheck rolecreateparade stfu update updatelog
​No Category
help2 parade

commandlist = [barrage, blush, clown, condescend, cry, dance, fistbump, flex, hug, kiss, pat, poke, pose, punch,
slap, afk, back, leaveguild, resetnick, suggest, intercom, endcall, accept, active, adventure, buy, createprofile,
deny, fight, gear, gods, grant, invite, job, kickmember, leaveteam, myteam, paradecoins, paradercount, paraid,
paraid6, passive, powprofile, profile, quest, quest6, raid, readd, rebase, register, reward, search, sell, shop,
switch, teams, tier, togglefight, upgrade, view, endgame, endstory, startgame, startstory, wordadd, wordremove,
wordshow, add, allseeing, chosenone, divide, heavens_door, me, multiply, no, online, subtract, timer, yes,
gcall, gjoin, gleave, help, emoji, fdeathnote, mentioned, nohide, ping, deathnote, freeze3, ger, ger_rtz, 
impactrevive, killerqueen, kingcrimson, mute, relog, shadowrealm, wipe, zahando, zawarudo, namegen, soulmate,
profane, acceptbff, acceptfr, acceptlove, acceptparent, addfriend, addlove, createsocial, delpet, denybff,
denylove, denyparent, dump, feed, getpet, newbff, newchild, pet, play, showfriends, socialprofile,
updatesocial, parade]"""


def setup(bot):
    bot.add_cog(HelpCom(bot))
