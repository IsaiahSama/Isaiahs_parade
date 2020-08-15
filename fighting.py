import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
from random import randint
from images import hugs, punches, kisses, slaps, knock, poses, flexes
from fight import FightMe, Fighter, questpro, enemy, FightingBeast, abilities, allabilities, passives, raidingmonster, weaponlist, armorlist, gear, lilgear
import json
import math
import jobs

emojiz = ["🤔", "🤫", "🤨", "🤯", "😎", "😓", "🤡", "💣", "🧛", "🧟‍♂️", "🏋️‍♂️", "⛹", "🏂"]


class FullFight(commands.Cog):
    if os.path.exists("fightdata.json"):
        with open("fightdata.json") as h:
            data = json.load(h)

        tempuser = []
        
        for dictobj in data:
            templist = []
            for v in dictobj.values():
                templist.append(v)
            tempuser.append(templist)

        loadedacc = []

        # def __init__(self, name, tag, level, health, mindmg, maxdmg, wins, losses, attackmsg=None):
        # def __init__(self, name, tag, level, health, mindmg, maxdmg, wins, losses, pcoin, critchance=5, healchance=3, 
        # ability=None, passive=None, weapon=fist, armour=linen):
        # def __init__(self, name, tag, level, curxp, health, mindmg, maxdmg, wins, losses, pcoin, critchance=5, healchance=3, 
        # ability=None, passive=None, weapon=fist, armour=linen, xpthresh=50, typeobj="player"):
        # def __init__(self, name, tag, level, curxp, health, mindmg, maxdmg, wins, losses, pcoin, 
        # critchance=5, healchance=3, ability=None, passive=None, weapon="Fist", armour="Linen", 
        # xpthresh=50, typeobj="player", canfight=True):
        
        
        for fightmaster in tempuser:
            acc = Fighter(fightmaster[0], fightmaster[1], fightmaster[2], fightmaster[3], fightmaster[4], fightmaster[5], 
            fightmaster[6], fightmaster[7], fightmaster[8], fightmaster[9], fightmaster[10], fightmaster[11], fightmaster[12],
            fightmaster[13], fightmaster[14], fightmaster[15], fightmaster[16], fightmaster[17], fightmaster[18])
            
            loadedacc.append(acc)

        users = loadedacc

    else:
        users = []

    def __init__(self, bot):
        self.bot = bot
        self.updlist.start()
        bot.loop.create_task(self.async_init())

    async def async_init(self):
        await self.bot.wait_until_ready()
        self.homeguild = self.bot.get_guild(739229902921793637)


    # Commands

    @commands.command(aliases=["pcoin", "pcoins"])
    async def paradecoins(self, ctx):
        user = await self.getmember(ctx.author)
        
        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return
        else:
            await ctx.send(f"{ctx.author.mention} has {user.pcoin} Parade Coins. Check out <>upgrade")

    
    @commands.command()
    async def grant(self, ctx, member: discord.Member, arg: int):
        if arg <= 0:
            await ctx.send(f"You can't give {member.display_name} {arg} Parade Coins... Baka.")
            return

        user1 = await self.getmember(ctx.author)
        user2 = await self.getmember(member)

        if user1 == None:
            await self.denied(ctx.channel, ctx.author)
            return
        if user2 == None:
            await self.denied(ctx.channel, member)
            return

        if user1.pcoin >= arg:
            user1.takecoin(arg)
            user2.addcoin(arg)
            await ctx.send("Successful")

        else:
            await ctx.send("You don't have enough to give.")

    @commands.command()
    async def powprofile(self, ctx, member: discord.Member=None):
        if await self.ismember(ctx.author):
            await ctx.send("Buffing you up...")
            await asyncio.sleep(2)
            await ctx.send("Measuring information...")
            await asyncio.sleep(2)
            await ctx.send("Done")
            await self.profile(ctx, member, True)
            return 0
        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command()
    async def profile(self, ctx, member: discord.Member=None, powpof=False):
        if member == None:
            target = await self.getmember(ctx.author)

        else:
            target = await self.getmember(member)

        if target == None:
            await self.denied(ctx.channel, ctx.author)
            return

        if powpof:
            target = await self.fightuser(target)
            if target.weapon.name == "Plague Doctors Scepter":
                target.weapon.damage = math.floor(target.maxdmg * 0.5)

        if target.tag == 493839592835907594:
            if target.level < 300:
                await ctx.send("Your armour is Ready Kevin. Just reach level 300 to claim it")
            else:
                await ctx.send("Now my creator, embrace your true power")
                target.armour = "Parade Creators Outfit"
                target.weapon = "Staff of the Parade"

        if target.mindmg > target.maxdmg:
            target.mindmg, target.maxdmg = target.maxdmg, target.mindmg
            
        profileEmbed = discord.Embed(
            title=f"Profile for {target.name}",
            color=randint(0, 0xffffff)
        )

        if member == None:
            profileEmbed.set_thumbnail(url=ctx.author.avatar_url)
        else:
             profileEmbed.set_thumbnail(url=member.avatar_url)
        
        if ctx.guild == self.homeguild:
            role = [x for x in ctx.author.roles if x.name == f"Tier{target.getTier()}"]
            if role:
                pass
            else:
                role = discord.utils.get(ctx.guild.roles, name=f"Tier{target.getTier()}")
                await ctx.author.add_roles(role)
                await ctx.send(f"You have received your ranking role of {role.name}")

        profileEmbed.add_field(name="Name:", value=f"{target.name}")
        profileEmbed.add_field(name="Level:", value=f"{target.level}")
        profileEmbed.add_field(name="Tier:", value=f"{target.getTier()}")
        profileEmbed.add_field(name="Exp:", value=f"{target.curxp}/{target.xpthresh}")
        profileEmbed.add_field(name="Health:", value=f"{target.health}")
        profileEmbed.add_field(name="Min Damage:", value=f"{target.mindmg}")
        profileEmbed.add_field(name="Max Damage:", value=f"{target.maxdmg}")
        profileEmbed.add_field(name="Wins:", value=f"{target.wins}")
        profileEmbed.add_field(name="Losses:", value=f"{target.losses}")
        if powpof:
            profileEmbed.add_field(name="Max Base Damage:", value=f"{target.maxdmg + target.weapon.damage}")
            profileEmbed.add_field(name="Weapon:", value=f"{target.weapon.name}")
            profileEmbed.add_field(name="Armour:", value=f"{target.armour.name}")
            if target.hasActive():
                profileEmbed.add_field(name=f"Ability:", value=f"{target.ability.name}")

            else:
                profileEmbed.add_field(name="Ability:", value=f"None... Yet")
            
            if target.hasPassive():
                profileEmbed.add_field(name=f"Passive:", value=f"{target.passive.name}")
            else:
                profileEmbed.add_field(name="Passive:", value=f"None... Yet")
        else:
            
            profileEmbed.add_field(name="Weapon:", value=f"{target.weapon}")
            profileEmbed.add_field(name="Armour:", value=f"{target.armour}")
            if target.hasActive():
                profileEmbed.add_field(name=f"Ability:", value=f"{target.ability}")
            else:
                profileEmbed.add_field(name="Ability:", value=f"None... Yet")

            if target.hasPassive():

                profileEmbed.add_field(name=f"Passive:", value=f"{target.passive}")
            else:
                profileEmbed.add_field(name="Passive:", value=f"None... Yet")
            
        profileEmbed.add_field(name="Parade Coins:", value=f"{target.pcoin}")
        profileEmbed.add_field(name="Crit Chance:", value=f"{target.critchance}%")
        profileEmbed.add_field(name="Self Heal Chance:", value=f"{target.healchance}%")

        await ctx.send(embed=profileEmbed)

    @commands.command()
    async def createprofile(self, ctx):
        user = await self.getmember(ctx.author)
        channel = self.bot.get_channel(739266609264328786)
        if user in self.users:
            await ctx.send("You already have a profile. View with <>profile")
            await ctx.send("Did you mean <>createsocial to create a Social Profile?")
            return
        else:
            acc = Fighter(ctx.author.name, ctx.author.id, 0, 0, 170, 10, 20, 0, 0, 100)
            self.users.append(acc)
            await ctx.send("Profile Created. View with <>profile")
            await channel.send(f"{ctx.author.name} from {ctx.guild.name} is now a parader")
            role = [p for p in ctx.guild.roles if p.name == "Parader"]
            role = role[0]
            await ctx.author.add_roles(role)

    inquest = []
    @commands.command(aliases=["q"])
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def quest(self, ctx):
        if self.aboutupdate:
            await ctx.send("Cannot Do a Quest/Fight Right now as bot is about to go offine")
            return
        user = await self.getmember(ctx.author)

        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return

        tier = user.getTier()

        embed = discord.Embed(
            title=f"Time for Quest. Tier {tier}",
            description=f"{ctx.author.display_name} {random.choice(questpro)}",
            color=randint(0, 0xffffff)
        )
        
        if user.tag in self.inquest:
            await ctx.send("You are already in a quest, please wait for it to complete")
            return

        self.inquest.append(user.tag)
    
        await ctx.send(embed=embed)
        await self.fight(ctx, None, False, True)

    
    @commands.command()
    @commands.is_owner()
    async def clrquest(self, ctx):
        self.inquest.clear()
        await ctx.send("Reset All Quests")  

    @commands.command()
    async def upgrade(self, ctx, arg=None):
        user = await self.getmember(ctx.author)
        
        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return

        if arg == None:
            user2 = await self.fightuser(user)
            statembed = discord.Embed(
                title=f"Stat Table for {ctx.author.display_name}",
                color=randint(0, 0xffffff)
            )

            statembed.add_field(name="Tier:", value=f"{user.getTier()}")
            statembed.add_field(name="Level:", value=f"{user.level}", inline=False)
            statembed.add_field(name=f"Health: {user.health}", value=f"+20 = {user.healthprice()} Parade Coins", inline=False)
            statembed.add_field(name=f"Min_Dmg: {user.mindmg}", value=f"+5 = {user.mindmgprice()} Parade Coins", inline=False)
            statembed.add_field(name=f"Max_Dmg: {user.maxdmg}", value=f"+5 = {user.maxdmgprice()} Parade Coins", inline=False)
            statembed.add_field(name=f"Crit_chance: {user.critchance}%", value=f"+2% = {user.critchanceprice()} Parade Coins")
            statembed.add_field(name=f"Heal_Chance: {user.healchance}%", value=f"+3% = {user.healchanceprice()} Parade Coins", inline=False)
            if user.hasPassive():
                statembed.add_field(name=f"Passive: {user2.passive.name}", value=f"{user2.passive.desc}")
            elif user.level >= 40 and not user.hasPassive():
                statembed.add_field(name="Passive:", value="You are strong enough to wield a passive. Get one with <>passive")
            else:
                statembed.add_field(name="Passive:", value="Unlocked at level 40")
            if user.hasActive():
                statembed.add_field(name=f"Active Ability: {user2.ability.name}", value=f"{user2.ability.desc}")
            elif user.level >= 60 and not user.hasActive():
                statembed.add_field(name="Active:", value="You are strong enough to wield an ability. Get one with <>active")
            else:
                statembed.add_field(name="Active Ability:", value="Unlocked at level 60")

            await ctx.send(embed=statembed)
            await ctx.send("""To increase a stat, first gather the amount of Parade Coins needed. And then use <>upgrade {stat name}. 
Stat names are the names that you see in the above embed, with the exception of Level. Not Case-Sensitive and without the colon (:)""")
            return

        arg = arg.lower()

        if arg == "health":
            msg = user.uphealth()
        elif arg == "min_dmg":
            msg = user.upmin()
        elif arg == "max_dmg":
            msg = user.upmax()
        elif arg == "crit_chance":
            msg = user.upcrit()
        elif arg == "heal_chance":
            msg = user.upheal()
        else:
            await ctx.send(f"{arg} is not a valid stat. Use <>upgrade by itself to see the stat names")
            return

        await ctx.send(msg)

    @commands.command()
    async def passive(self, ctx, arg=False, *, nop=None):
        user = await self.getmember(ctx.author)

        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return

        if user.level < 40:
            await ctx.send("You must be at least level 40 to get a passive")
            return

        if not user.hasPassive():
            pash = random.choice(passives)
            await ctx.send(f"Congratulations, your passive ability is {pash.name}. Check with <>profile")
            user.passive = pash.name
            return

        if user.hasPassive() and not arg:
            passconfirm = discord.Embed(
                title=f"Passive Change. Your passive is {user.passive}",
                description="This will allow you to choose your passive. It will cost you dearly... 15 000 Parade Coins to be exact",
                color=randint(0, 0xffffff)
            )

            for passi in passives:
                passconfirm.add_field(name=f"{passi.name}:", value=f"{passi.desc}")

            passconfirm.add_field(name="\nContinue...", value="If you wish to continue, use <>passive True {Name of Passive}")

            await ctx.send(embed=passconfirm)
            return

        if user.hasPassive() and arg:
            if nop == None:
                await ctx.send("You did not enter the name of the passive you wanted")
                return
            value = None
            for passi in passives:
                if nop.lower() == passi.name.lower():
                    value = passi
                    break

            if value == None:
                await ctx.send(f"{value} is not a Passive, or is not available")
                return
            
            msg = user.passchange(value)

            await ctx.send(msg)


    @commands.command()
    async def active(self, ctx, arg=False, *, act=None):
        user = await self.getmember(ctx.author)

        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return

        if user.level < 60:
            await ctx.send("You are too weak for an active ability. Come back when you are level 60")
            return

        if not user.hasActive():
            yes = random.choice(abilities)
            await ctx.send(f"CONGRATULATIONS... Your new ability is {yes.name}")
            user.ability = yes.name
            return

        if user.hasActive() and not arg:
            accheck = discord.Embed(
                title=f"Your ability is {user.ability}",
                description="Going any further with this command will cost you 25 000 Parade Coins and will allow you to choose your ability",
                color=randint(0, 0xffffff)
            )

            for acci in allabilities:
                accheck.add_field(name=f"{acci.name}", value=f"{acci.desc}")

            accheck.add_field(name="\nContinue...", value="If you wish to continue, use <>active True {Name of Active}")

            await ctx.send(embed=accheck)
            return

        if user.hasActive() and arg:
            if act == None:
                await ctx.send("You did not say which ability you wanted")
                return

            target = None
            for thing in abilities:
                if act.lower() == thing.name.lower():
                    target = thing
                    break
            
            if target == None:
                await ctx.send(f"That is not an Active Ability")
                return

            msg = user.actichange(target)

            await ctx.send(msg)

    
    raidon = False
    raiding = False
    raiders = []
    raidbeast = None
    winner = None

    @commands.command()
    async def raid(self, ctx):

        channel = self.homeguild.get_channel(740764507655110666)

        user = await self.getmember(ctx.author)
        for raider in self.raiders:
            if raider.tag == user.tag:
                await ctx.send("You are already in the raid")
                return
        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return

        if not self.raidon:
            await ctx.send("There is no Raid going on currently. You will know when one is occurring")
            return

        if self.raiding:
            await ctx.send("Sorry, you cannot join a raid while it is in progress.")
            return

        user = await self.fightuser(user)

        self.raiders.append(user)

        msg = f"{ctx.author.display_name} from {ctx.guild.name} has joined the raid"

        await channel.send(msg)     
        await ctx.send(msg)      
        
    @commands.command()
    async def reward(self, ctx):
        if await self.ismember(ctx.author):
            user = await self.getmember(ctx.author)
            if user.tag in self.hadreward:
                await ctx.send("You already had a reward. Only once every Hour, check back later")
                return
            
            self.hadreward.append(user.tag)
            
            msg = await self.getreward(user)
            await ctx.send(f"{msg}. Come back in 1 hour")
            await asyncio.sleep(60 * 60)

            await ctx.send(f"{ctx.author.mention}, you can now get another reward")
            self.hadreward.remove(user.tag)
            return

        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command()
    async def readd(self, ctx):
        user = await self.getmember(ctx.author)

        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return

        yes = discord.utils.get(ctx.author.roles, name="Parader")
        if yes == None:
            role = discord.utils.get(ctx.guild.roles, name="Parader")

            await ctx.author.add_roles(role)

            await ctx.send(f"{ctx.author.display_name} now has back their Parader role")
        
        else:
            await ctx.author.remove_roles(yes)

            await ctx.send(f"Removed Parader role from {ctx.author.name}. Do this command again to get it back")

    # Main
    infight = []
    aboutupdate = False
    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def fight(self, ctx, member: discord.Member=None, isbot=False, isquest=False):
        if self.aboutupdate:
            await ctx.send("Cannot Do a Quest/Fight Right now as bot is about to go offine")
            return
        
        user1 = None
        user2 = None

        bott = self.bot.user

        # If member is None, or the bot is using it. Let member be none
        if member == None or isbot:
            member = None

        if member is not None:
            if member.status == discord.Status.offline:
                await ctx.send(f"{member.display_name} is offline so cannot be fought")
                return

        # Loops through the list of users If any matches, instantinize them, else, keep them as None
        for account in self.users:
            # If the bot is the one using the command, User1 = Instance of the bot
            if isbot:
                account = await self.getmember(bott)
                user1 = await self.fightuser(account)
    
            # If the one using the command is a human, then User1 = Fight Instance of the Player
            if not isbot:
                account = await self.getmember(ctx.author)
                user1 = await self.fightuser(account)
            # If the command has an @Mention, then user2 = Fight Instance of that person
            if member is not None:
                yes = await self.ismember(member)
                if yes:
                    account = await self.getmember(member)
                    user2 = await self.fightuser(account)
                else:
                    await ctx.send(f"{member.name} does not have an account. Create one with <>createprofile")
                    return
 
        if user1 == None:
            await ctx.send(f"You need to create a profile with <>createprofile first {ctx.author.mention}")
            return False


        if not isquest:
            if not user1.canfight:
                await ctx.send(f"{user1.name} has off disabled pvp. Turn it on with <>togglefight")
                return

            if not user2.canfight:
                await ctx.send(f"{user2.name} has disabled pvp. Turn it on with <>togglefight")
                return

            if user1.tag in self.infight or user2.tag in self.infight:
                await ctx.send("You, or the person you want to fight is already in one")
                return

            if user1.tag == user2.tag:
                await ctx.send("You can't fight yourself... You ok bud?")
                return

            if user1.getTier() > user2.getTier():
                await ctx.send("You are trying to fight someone weaker than yourself. Do you not have any shame or honour?")
                return

            elif user1.getTier() < user2.getTier():
                await ctx.send("I hope you know what you are getting yourself into. They are out of your tier... literally")

            self.infight.append(user1.tag)
            self.infight.append(user2.tag)


        if isquest:
            temp = await self.getmain(user1)
            tier = temp.getTier()
            user2 = await self.get_enemy(tier)
            
            rannum = randint(temp.level - 50, temp.level + 50)
            user2.level = rannum
            

            questembed = discord.Embed(
                title=f"Fighting {user2.name}",
                description=f"{user2.entrymessage}",
                color=randint(0, 0xffffff)
            )

            questembed.add_field(name="Health", value=f"{user2.health}")
            questembed.add_field(name="Level", value=f"{user2.level}")
            questembed.add_field(name="Damage Range", value=f"{user2.mindmg} - {user2.maxdmg}")
            questembed.add_field(name="Coin Range", value=f"{user2.mincoin} - {user2.maxcoin}")
            questembed.add_field(name="XP range", value=f"{user2.minxp} - {user2.maxxp}")
            if user2.hasActive():
                questembed.add_field(name="Ability", value=f"{user2.ability.name}")
            if user2.hasPassive():
                questembed.add_field(name="Passive", value=f"{user2.passive.name}")
            questembed.add_field(name="Weapon", value=f"{user2.weapon.name}")
            questembed.add_field(name="Armour", value=f"{user2.armour.name}")

            botmsg = await ctx.send(embed=questembed)
            
        else:
            fightembed = discord.Embed(
                title="Fighting...",
                description=f"Fight Between {user1.name} and {user2.name}",
                color=randint(0, 0xffffff)
            )

            botmsg = await ctx.send(embed=fightembed)

        if user1.weapon.name == "Plague Doctors Scepter":
            user1.weapon.damage = math.floor(user1.maxdmg * 0.5)

        elif user2.weapon.name == "Plague Doctors Scepter":
            user2.weapon.damage = math.floor(user2.maxdmg * 0.5)

        user1.oghealth = user1.health
        user2.oghealth = user2.health

        attacker = user1
        defender = user2

        fighting = True
  
        
        # Checking for Armour Weapon Pairs
        if attacker.armour.haspair():
            if attacker.weapon.name == attacker.armour.pairs.name:
                msg = attacker.buff()
                await ctx.send(f"Set Bonus {msg}")
                

        if defender.armour.haspair():
            if defender.weapon.name == defender.armour.pairs.name:
                msg = defender.buff()
                await ctx.send(f"Set Bonus {msg}")
                if not isquest:
                    await asyncio.sleep(3)


        if defender.hasPassive():
                if defender.passive.name == "Speed Boost":
                    attacker, defender = defender, attacker
                    await ctx.send(f"{attacker.name} attacks first because of speed boost")

        """if user2.tag == 493839592835907594 and user1.tag in [315619611724742656, 347513030516539393, 315632232666759168]:
            user1.health = -999999
            await ctx.send(f"{user2.name} shut down {user1.name}'s attempt at betryal")


            if user1.health <= 0:
                attacker, defender = defender, attacker
                fighting = False"""
            
        psned = []
        turns = 0

        battlebed = discord.Embed(
                title=f"FIGHT... Turn {turns}",
                color=randint(0, 0xffffff)
            )
        
        slagged = False
        psn = False
        ts = False

        while fighting:            
            
            if attacker.hasPassive():
                if attacker.health <= (attacker.oghealth / 3):
                    if attacker.passive.name == "Rage":
                        attacker.passuse(0)
                        await ctx.send(f"New mindamage is {attacker.mindmg}")
                        await ctx.send(f"New Max Damage is {attacker.maxdmg}")
                        battlebed.add_field(name=f"{attacker.name}", value=f"{attacker.passive.usename}: {attacker.passive.effect}")


            if attacker.health >= 65000:
                attacker.weapon.healplus = 0
                attacker.armour.regen = 0
                if attacker.passive.name == "Regeneration":
                    attacker.passive.name = None
                if attacker.ability.name == "Ultra Heal":
                    attacker.ability.name = None
                await ctx.send("All regen has been Disabled")

        
            power = randint(attacker.mindmg, attacker.maxdmg)
            critnum = randint(0, 100)
            healnum = randint(0, 100)

            if slagged:
                if attacker.ability.name == "Slag":
                    if defender.slag == 0:
                        battlebed.add_field(name=f"{attacker.ability.usename}", value=f"{defender.name} has been freed of Slag")
                        del defender.slag
                        slagged = False
                    else:
                        defender.slag -= 1
                        power *= 1.5
                        battlebed.add_field(name=f"{attacker.ability.usename}", value=f"{defender.name} {attacker.ability.effect} {defender.slag} turns")

            power += attacker.weapon.damage

            if turns == 1:
                if attacker.hasPassive():
                    if attacker.passive.name == "Speed Boost":
                        power *= 1.5
                        
            if attacker.hasPassive():
                if attacker.passive.name == "Haoshoku Haki":
                    if attacker.armour.name == "Haki":
                        if attacker.armour.haspair():
                            if attacker.weapon.name == attacker.armour.pairs.name:
                                power = await self.cantruehaki(defender, attacker, power, battlebed)
                        
                    elif attacker.weapon.name == "Conqueror Haki":
                        power = await self.canhaki(defender, attacker, power, battlebed)
                    
                    else:
                        pass

                if attacker.passive.name == "Pride of Balance":
                    if attacker.armour.haspair():
                        if attacker.armour.name == "Yang":
                            power = await self.canbalance(defender, attacker, power, battlebed)

            if defender.hasPassive():
                if defender.passive.name == "Haoshoku Haki":
                    if attacker.armour.name == "Haki":
                        if defender.armour.haspair():
                            if defender.weapon.name == defender.armour.pairs.name:
                                power = await self.cantruehaki(attacker, defender, power, battlebed)
                    
                    elif defender.weapon.name == "Conqueror Haki":
                        power = await self.canhaki(attacker, defender, power, battlebed)
                    
                    else:
                        pass

            
            if attacker.hasActive():
                if attacker.ability.oncd():
                    attacker.ability.cdreduce()
                else:
                    if attacker.ability.name == "Slag":
                        num = randint(1,6)
                        if num == 3:
                            slagged = True
                            defender.slag = 2
                            battlebed.add_field(name=f"{attacker.ability.usename}", value=f"{defender.name} {attacker.ability.effect} {defender.slag} turns")
                   
                    else:
                        power, abilname = await self.canability(defender, attacker, power, battlebed)
                        if abilname == "Stop Time":
                            ts = True
                        if abilname == "The Plague":
                            psned.append(defender)
                            psn = True
                            psndmg = 100          

            if ts:
                defender.attack(power)       
                power = randint(attacker.mindmg, attacker.maxdmg)
                critnum = randint(0, 100)
                healnum = randint(0, 100)

                power += attacker.weapon.damage

                battlebed.add_field(name="In Stopped Time", value=f"{attacker.name} {attacker.attackmsg} {defender.name}")

            if attacker.hasPassive():
                if attacker.passive.name == "Sharp Eye":
                    power = await self.cansharpeye(defender, attacker, power, battlebed)

            if critnum > 0 and critnum <= attacker.critchance:
                battlebed.add_field(name="Critical Hit", value=f"{attacker.name} got a crit")
                power *= 1.5
                if defender.hasPassive():
                    if defender.passive.name == "Critical Guard":
                        power = await self.cancritblock(defender, attacker, power, battlebed)

            if healnum > 0 and healnum <= attacker.healchance:
                healin = randint(10, 20)
                battlebed.add_field(name="Self Heal", value=f"{attacker.name} heals {healin} hp")
                attacker.heal(healin)

            if defender.hasPassive():
                if defender.passive.name == "Dodge":
                    power = await self.candodge(defender, attacker, power, battlebed)
                    
            defender.attack(power)

            if power >= 1:
                if attacker.weapon.islifesteal():
                    x = math.floor((attacker.weapon.healplus / 100) * power)
                    attacker.heal(x)
                    battlebed.add_field(name=f"{attacker.weapon.name}", value=f"heals {attacker.name} for {x} hp")

            await botmsg.add_reaction(random.choice(emojiz))

            battlebed.add_field(name="Notif:", value= f"{attacker.name} {attacker.attackmsg} {defender.name} for {power} damage", inline=False)
            battlebed.add_field(name=f"{attacker.name}:", value=f"Health: {attacker.health}", inline=False)
            battlebed.add_field(name=f"{defender.name}:", value=f"Health: {defender.health}", inline=False)

            if psn:
                for person in psned:
                    person.ptime -= 1
                    person.health -= psndmg
                    battlebed.add_field(name="The Plague", value=f"{person.name} loses {psndmg} hp because of the plague. {person.ptime} turns remain")
                    psndmg += 50
                    if person.ptime == 0:
                        battlebed.add_field(name="The Plauge", value=f"{person.name} was cured from the plague")
                        psned.remove(person)
                        if len(psned) == 0:
                            psn = False

            

            if defender.health <= 0:
                fighting = False
                if len(battlebed) >= 1024:
                    await ctx.send("Fight Log was too long")
                else:
                    await ctx.send(embed=battlebed)
                break

            if defender.hasPassive():
                if defender.passive.name == "Counter":
                    await self.cancounter(defender, attacker, power, battlebed)
            
            if attacker.hasPassive():
                if attacker.passive.name == "Regeneration":
                    await self.canregen(attacker, battlebed)

            if attacker.armour.hasregen():
                x = math.floor((attacker.armour.regen / 100) * attacker.oghealth) 
                attacker.health += x
                battlebed.add_field(name=f"{attacker.armour.name} effect:", value=f"heals {attacker.name} for {x} hp")

            if attacker.health <= 0:
                attacker, defender = defender, attacker
                fighting = False
                if len(battlebed) >= 1024:
                    await ctx.send("Fight Log was too long")
                else:
                    await ctx.send(embed=battlebed)
                break
            

            turns += 1

            if turns % 2 == 0:
                await ctx.send(embed=battlebed)
                battlebed = discord.Embed(
                    title=f"FIGHT... Turn {turns}",
                    color=randint(0, 0xffffff)
                )

            
            attacker, defender = defender, attacker
            

            await asyncio.sleep(2)
        
        ended = discord.Embed(
                title="It is finished",
                description=f"{attacker.name} has defeated {defender.name} with {attacker.health} health remaining",
                color=randint(0, 0xffffff)
            )
                
        await ctx.send(embed=ended)
        if isquest:
            self.inquest.remove(user1.tag)
        
        if attacker.hasActive():
            attacker.ability.reset()
        if defender.hasActive():
            defender.ability.reset()
        if attacker.typeobj == "player":
            lvl = await self.expgain(attacker, defender)
            if lvl == True:
                irl = await self.getirl(attacker)
                await ctx.send(f"{irl.mention} has leveled up")
            else:
                await ctx.send(f"{lvl}")

        if attacker.typeobj == "player" and defender.typeobj == "player":
            attacker = await self.getmain(attacker)
            defender = await self.getmain(defender)
            coin = randint(math.floor(defender.pcoin / 10), math.floor(defender.pcoin / 3))
            await ctx.send(f"{attacker.name}: You have received {coin} Parade Coins from {defender.name}")
            attacker.addcoin(coin)
            defender.takecoin(coin)

        if attacker.typeobj == "player" and defender.typeobj == "npc":
            attacker = await self.getmain(attacker)
            coin = randint(defender.mincoin, defender.maxcoin)
            attacker.addcoin(coin)
            await ctx.send(f"{attacker.name}: You have received {coin} Parade Coins for defeating {defender.name}")

                
        if defender.typeobj == "player":
            defender = await self.getmain(defender)
            await self.lost(defender)
            mula = math.ceil(defender.health / 7)
            await ctx.send(f"{defender.name} had to pay someone to heal their injuries, and they charged {mula} coins")
            defender.takecoin(mula)

        if not isquest:
            self.infight.remove(user1.tag)
            self.infight.remove(user2.tag)

        if self.aboutupdate:
            await ctx.send("Bot going offline shortly")

    @commands.command()
    @commands.cooldown(1, 1200, commands.BucketType.guild)
    async def paraid(self, ctx):
        if self.raidon:
            await ctx.send("A raid is already in progress")
            return
                
        ismem = await self.ismember(ctx.author)
        if ismem:
            user = await self.getmember(ctx.author)
            if user.level >= 40:
                self.raidon = True
                if ctx.guild == self.homeguild:
                    ctx.channel = ctx.guild.get_channel(740764507655110666)
                else:
                    rmention = discord.utils.get(self.homeguild.roles, name="Parader")
                    channel = self.bot.get_channel(740764507655110666)
                    await channel.send(f"Attention {rmention.name}: {ctx.author.name} from {ctx.guild.name} has started a raid. Come let us raid their raid. We only have 3 minutes")
                
                await ctx.channel.send(f"{ctx.author.name} has started a raid.")
                await self.startRaid(ctx.guild, ctx.channel)
            else:
                await ctx.send("You must be at least level 40 to start a raid")

    @commands.command()
    async def togglefight(self, ctx):
        user = await self.getmember(ctx.author)

        if user == None:
            await ctx.send("Join us first with <>createprofile")
            return
        
        if user.canfight:
            user.canfight = False
            await ctx.send(f"{ctx.author.display_name} can no longer be fought")
            if ctx.guild.id == 739229902921793637:
                role = discord.utils.get(ctx.guild.roles, name="Pacifist")
                await ctx.author.add_roles(role)
        else:
            user.canfight = True
            await ctx.send(f"{ctx.author.display_name} is now available for fighting")
            if ctx.guild.id ==739229902921793637:
                role = discord.utils.get(ctx.guild.roles, name="Pacifist")
                await ctx.author.remove_roles(role)
        
        return


    # Weapon Stuff
    @commands.command()
    async def shop(self, ctx, arg=None):
        if arg == None:
            await ctx.send("Welcome to the shop, Here, you can purchase weapons and armour. use <>shop weapons for weapons and <>shop armor for armor")
            return
        if await self.ismember(ctx.author):
            if arg.lower() == "armour" or arg.lower() == "armor":
                await self.loadarmour(ctx)
                return
            
            if arg.lower() == "weapons":
                await self.loadweapon(ctx)
                return

            else:
                await ctx.send(f"{arg} must be weapons, armour or armor. not {arg}")
        
        else:
            await ctx.send("You can not view the store without an adventurer's license. Do <>createprofile")

    @commands.command()
    async def gear(self, ctx):
        user = await self.ismember(ctx.author)
        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return

        user = await self.getmember(ctx.author)
        sword, shield = user.getgear()
        if sword.name == "Plague Doctors Scepter":
            sword.damage = math.floor(user.maxdmg * 0.5)

        thing = discord.Embed(
            title=f"Gear for {user.name}",
            color=randint(0, 0xffffff)
        )

        thing.add_field(name=f"Weapon: {sword.name}", value=f"Damage: +{sword.damage}, Critchance: +{sword.critplus}%, Lifesteal: +{sword.healplus}",
        inline=False)
        thing.add_field(name=f"Armour: {shield.name}", value=f"Health up: +{shield.hpup}, Power Up: +{shield.pup}")
        if shield.haspair():
            fuser = await self.fightuser(user)
            thing.add_field(name=f"{shield.name} pairs well with {shield.pairs.name}", value=f"{fuser.buff()}", inline=False)
            

        await ctx.send(embed=thing)

    @commands.command()
    async def view(self, ctx, *, arg=None):
        item = None
        for t in gear:
            if t.name.lower() == arg.lower():
                item = t

        if item == None:
            await ctx.send("Not a part of my stock")
            return
        
        if item.typeobj == "Weapon":
            weaponbed = discord.Embed(
            title="Here is the info you requested",
            color=randint(0, 0xffffff)
            )
            
            weaponbed.add_field(name="Name:", value=f"{item.name}")
            weaponbed.add_field(name="Description:", value=f"{item.desc}")
            weaponbed.add_field(name="Damage:", value=f"+{item.damage}")
            weaponbed.add_field(name="Crit Chance:", value=f"+{item.critplus}% chance")
            weaponbed.add_field(name="Lifesteal:",value=f"+{item.healplus}%")
            weaponbed.add_field(name="Cost:", value=f"{item.cost} Parade Coins")
            weaponbed.add_field(name="Tier:", value=f"{item.tierz}")
            

            msg = await ctx.send(embed=weaponbed)
        
        elif item.typeobj == "Armour":
            armorbed = discord.Embed(
            title="Here is the info you requested",
            color=randint(0, 0xffffff)
            )

            armorbed.add_field(name="Name:", value=f"{item.name}")
            armorbed.add_field(name="Description:", value=f"{item.desc}")
            armorbed.add_field(name="Health Up:", value=f"+{item.hpup}")
            armorbed.add_field(name="Max Dmg Up:", value=f"+{item.pup}")
            armorbed.add_field(name="Cost:", value=f"{item.cost} Parade Coins")
            armorbed.add_field(name="Tier:", value=f"{item.tierz}")


            msg = await ctx.send(embed=armorbed)

        else:
            pass
            
        await asyncio.sleep(60)
        await msg.delete()


    @commands.command()
    async def buy(self, ctx, *, arg=None):
        if arg == None:
            await ctx.send("You did not tell me what you wanted to buy")
        
        user = await self.getmember(ctx.author)
        if user == None:
            await self.denied(ctx.channel, ctx.author)
            return

        req = None
        
        for item in lilgear:
            if item.name.lower() == arg.lower():
                req = item
                break

        if req == None:
            await ctx.send(f"Sorry, I don't have any {req} in stock") 
            return
        
        
        canget = await self.canbuy(user, req)
        

        await ctx.send(canget)

    # Job
    @commands.command(aliases=["j"])
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def job(self, ctx):
        sure = await self.ismember(ctx.author)
        if not sure:
            await self.denied(ctx.channel, ctx.author)
            return
        user = await self.getmember(ctx.author)
        
        tier = user.getTier()

        await self.getjob(ctx.channel, user, tier)

    @commands.command()
    async def sell(self, ctx, selly=False, arg=None):
        yes = await self.ismember(ctx.author)
        if not yes:
            await self.denied(ctx.channel, ctx.author)
            return
        
        user = await self.getmember(ctx.author)
        
        if selly == False and arg == None:
            await ctx.send(f"{ctx.author.mention} needs to do '<>sell True' in order to sell an item")
            await self.gear(ctx)
            return

        uwep, uarm = user.getgear()
        if uwep not in weaponlist or uarm not in armorlist:
            await ctx.send("You can not sell a weapon that does not exist in the shop")
            return

        if selly and arg == None:
            await ctx.send(f"Do <>sell True armour or <>sell True weapon to sell your armour or weapon resepectively")
            return

        if selly:
            if arg.lower() == "armour" or arg.lower() == "armor":
                cost = math.ceil((3/4) * uarm.cost)
                await ctx.send(f"Sold {uarm.name} for {cost} Parade Coins")
                user.addcoin(cost)
                user.armour = "Linen"

            if arg.lower() == "weapon":
                cost = math.ceil((3/4) * uwep.cost)
                await ctx.send(f"Sold {uwep.name} for {cost} Parade Coins")
                user.addcoin(cost)
                user.weapon = "Fist"

            else:
                await ctx.send(f"{arg} is neither 'armour', 'armor' or 'weapon'")
                return

            await ctx.send("Completed")


    @commands.command()
    async def paradercount(self, ctx):
        await ctx.send(f"There are currently {len(self.users)} Paraders")   


    @commands.command()
    async def tier(self, ctx):
        yes = await self.ismember(ctx.author)
        tierbed = discord.Embed(
            title="Tiers",
            description="Tiers determine the amount of money you will get from a job, which players you can fight, and the difficulty of your quests",
            color=randint(0, 0xffffff)
        )     

        if yes:
            user = await self.getmember(ctx.author)
            tierbed.add_field(name="Tier:", value=f"You are currently Tier {user.getTier()}", inline=False)
        
        tierbed.add_field(name="How they work", 
        value="""Your tier is determined based on the amount of health you have. If your health is less than 250, You are tier 1. 
        Tier 2 is 250 to 350. Tier 3 is 351 to 950. Tier 4 is everthing 950-2999. And tier 5 is 3000+""")
        tierbed.add_field(name="Weapons and Armour", 
        value="Weapons and Armours also have tiers. Because of this, when you open the shop, you will only see items at your tier and lower. Tier 5's get a different Shop with tier 5 and 4 only")

        await ctx.send(embed=tierbed)

    @commands.command()
    async def search(self, ctx):
        if await self.ismember(ctx.author):
            user = await self.getmember(ctx.author)
            usertier = user.getTier()
            fmem = [x for x in ctx.guild.members if await self.ismember(x)]
            ffmem = [await self.getmember(x) for x in fmem]
            sametier = [x for x in ffmem if x.getTier() == usertier]
            canfight = [x.name for x in sametier if x.canfight]

            fightbed = discord.Embed(
                title=f"Members able to be fought by {ctx.author.display_name}",
                description=f"{', '.join(canfight)}",
                color=randint(0, 0xffffff)
            )

            await ctx.send(embed=fightbed)

        else:
            await ctx.send("You do not have a fight profile. Do <>createprofile")

    
    # Functions90
    async def startRaid(self, guild=None, channel=None):

        if guild == None and channel == None:
            guild = self.bot.get_guild(739229902921793637)
            channel = guild.get_channel(740764507655110666)
        
        guild2 = self.bot.get_guild(739229902921793637)
        
        channel2 = self.homeguild.get_channel(740764507655110666)
        
        currole = discord.utils.get(guild.roles, name="Parader")
        
        await channel.send(f"Attention {currole.name}. A Raid Boss is on it's way to you. Join the raid with <>raid. We have 3 minutes until it starts")

        await asyncio.sleep(150)
        await channel.send("We have info on the beast. 30 seconds remain")
        if channel != channel2:
            currole2 = discord.utils.get(guild2.roles, name="Parader")
            await channel2.send(f"{currole2.name} 30 Seconds remain and we have our info")
        
        await self.spawnraid()
        beastembed = discord.Embed(
            title=f"{self.raidbeast.name}",
            description=f"{self.raidbeast.entrymessage}",
            color=randint(0, 0xffffff)
        )
        await self.rembed(beastembed, channel)

        await asyncio.sleep(20)
        msg = f"{currole.name}, 10 Seconds Remain. The field of Empowerment is activated. Now you will always be doing max damage"
        await channel.send(msg)

        await asyncio.sleep(10)
        await channel.send("And so it began")
        if channel != channel2:
            await channel2.send("It has begun")

        if len(self.raiders) >= 1:
            self.raidon = False
            self.raiding = True
            for player in self.raiders:
                if player.hasActive():
                    player.ability.reset()
                player.oghealth = player.health

            self.raidbeast.oghealth = self.raidbeast.health
            await self.raidStart(channel)
        
        else:
            await channel.send("Not enough members for the Assault... The giant beast turned around and vanished... We need at least 3 players")
            await self.resetraid()
            return

    async def raidStart(self, channel):
        channel2 = self.homeguild.get_channel(740764507655110666)
        await channel.send(f"{self.raidbeast.entrymessage}")
        if channel != channel2:
            await channel2.send(f"{self.raidbeast.entrymessage}")

        await self.battlestart(channel)
        await self.resetraid()

    async def resetraid(self):
        self.raidon = False
        self.raiding = False
        self.raiders = []
        self.raidbeast = None
        self.winner = None


    
    async def battlestart(self, channel):
        for person in self.raiders:
        # Checking for Armour Weapon Pairs
            if person.armour.haspair():
                if person.weapon.name == person.armour.pairs.name:
                    msg = person.buff()
                    await channel.send(f"Set Bonus {msg}")
                    await asyncio.sleep(2)

        if self.raidbeast.hasActive():
            self.raidbeast.ability.reset()
        
        while self.raiding:

            await self.turngo(channel)

            self.raiding = await self.winchk()
            
            if not self.raiding:
                break
            await self.turngo2(channel)
            
            self.raiding = await self.winchk()
            
            if not self.raiding:
                break

            
        if self.winner == "players":
            channel2 = self.homeguild.get_channel(740764507655110666)
            if channel == channel2:
                pass
            else:
                await channel2.send(f"CONGRATULATIONS... {self.raidbeast.name} HAS BEEN DEFEATED!")
                await channel2.send(f"All players who managed to stay alive, will now be rewarded")
            
            await channel.send(f"CONGRATULATIONS... {self.raidbeast.name} HAS BEEN DEFEATED!")
            await channel.send(f"All players who managed to stay alive, will now be rewarded")
            for player in self.raiders:
                value = await self.expgain(player, self.raidbeast)
                player = await self.getmain(player)
                coin = randint(self.raidbeast.mincoin, self.raidbeast.maxcoin)
                player.addcoin(coin)
                if value:
                    await channel.send(f"{player.name} has leveled up")
                else:
                    await channel.send(f"{value}")
                await channel.send(f"{player.name} received {coin} from {self.raidbeast.name}")
            showoff = []
            for raider in self.raiders:
                showoff.append(raider.name)

            showoff = ", ".join(showoff)
            await channel.send(f"Rewards are finished being distributed. The surviving players were {showoff}. Thank you my brave heroes")
            if channel != channel2:
                await channel2.send(f"Rewards are finished being distributed. The surviving players were {showoff}. Thank you my brave heroes")
        else:
            await channel.send(f"Unfortunately, {self.raidbeast.name} wiped the floor with the young heroes.")


    async def spawnraid(self):
        rbeast = random.choice(raidingmonster)
        rbeast = FightingBeast(rbeast.name, rbeast.tag, rbeast.health, rbeast.mindmg, rbeast.maxdmg, 
        rbeast.mincoin, rbeast.maxcoin, rbeast.entrymessage, rbeast.minxp, rbeast.critchance, rbeast.healchance,
        rbeast.ability, rbeast.passive, rbeast.attackmsg, rbeast.weapon, rbeast.armour)
        
        self.raidbeast = rbeast
        self.raidbeast.slag = 0

        return True

    async def winchk(self):
        if self.raidbeast.health <= 0:
            self.winner = "players"
            return False
                

        elif len(self.raiders) == 0:
            self.winner = "beast"
            return False

        else:
            return True
                
    rpsned = []
    rpsn = False
    rts = False
    rpsndm = 100
    rslagged = False

    async def turngo(self, channel):
        for player in self.raiders:
            raidbed = discord.Embed(
            title=f"Raid battle against {self.raidbeast.name}",
            color=randint(0, 0xffffff)
        )

            if self.raidbeast.hasPassive():
                if self.raidbeast.passive.name == "Speed Boost":
                    raidbed.add_field(name=f"{self.raidbeast.name}", value=f"attacks first because of speed boost")
                    await self.turngo2(channel)
                    self.raidbeast.passive = None

            
            if player.hasPassive():
                if player.health <= (player.oghealth / 3):
                    if player.passive.name == "Rage":
                        player.passuse(0)
                        raidbed.add_field(name=f"{player.name}", value=f"{player.passive.usename}: {player.passive.effect}")

            
            power = player.maxdmg
            critnum = randint(0, 100)
            healnum = randint(0, 100)

            if self.rslagged:
                if player.hasActive():
                    if player.ability.name == "Slag":
                        if self.raidbeast.slag == 0:
                            raidbed.add_field(name=f"{player.ability.usename}", value=f"{self.raidbeast.name} has been freed of Slag")
                            del self.raidbeast.slag
                            self.rslagged = False
                        else:
                            self.raidbeast.slag -= 1
                            power *= 1.5
                            raidbed.add_field(name=f"{player.ability.usename}", value=f"{self.raidbeast.name} {player.ability.effect} {self.raidbeast.slag} turns")


            power += player.weapon.damage

            if player.hasActive():
                if player.ability.oncd():
                    player.ability.cdreduce()
                else:
                    if player.ability.name == "Slag":
                        num = randint(1,6)
                        if num == 3:
                            self.rslagged = True
                            self.raidbeast.slag = 2
                            raidbed.add_field(name=f"{player.ability.usename}", value=f"{self.raidbeast.name} {player.ability.effect} {self.raidbeast.slag} turns")
                    else:
                        power, abilname = await self.canability(self.raidbeast, player, power, raidbed)
                        if abilname == "Stop Time":
                            self.rts = True
                        if abilname == "The Plague":
                                self.rpsned.append(self.raidbeast)
                                self.rpsn = True
                                self.rpsndmg = 100

            if player.hasPassive():
                if player.passive.name == "Sharp Eye":
                    power = await self.cansharpeye(self.raidbeast, player, power, raidbed)

            if self.rts:
                self.raidbeast.attack(power)
                power = player.maxdmg
                critnum = randint(0, 100)
                healnum = randint(0, 100)

                power += player.weapon.damage
                self.rts = False

            if power >= 1:
                if player.weapon.islifesteal():
                    x = math.floor((player.weapon.healplus / 100) * power)
                    player.heal(x)
                    raidbed.add_field(name=f"{player.weapon.name}", value=f"heals {player.name} for {x} hp")
            

            if critnum > 0 and critnum <= player.critchance:
                raidbed.add_field(inline=False,name="Critical Hit", value=f"{player.name} got a crit")
                power *= 1.5
                if self.raidbeast.hasPassive():
                    if self.raidbeast.passive.name == "Critical Guard":
                        power = await self.cancritblock(self.raidbeast, player, power, raidbed)

            if healnum > 0 and healnum <= player.healchance:
                healin = randint(10, 20)
                raidbed.add_field(inline=False,name="Self Heal", value=f"{player.name} heals {healin} hp")
                player.heal(healin)

            if self.raidbeast.name == "Giant King Be Be Be":
                power -= 10
                raidbed.add_field(inline=False,name=f"{self.raidbeast.passive.usename}", value=f"{self.raidbeast.passive.effect}")

            
            self.raidbeast.attack(power)
            if self.rpsn:
                for person in self.rpsned:
                    person.ptime -= 1
                    person.health -= self.rpsndmg
                    raidbed.add_field(name="The Plague", value=f"{person.name} loses {self.rpsndmg} hp because of the plague. {person.ptime} turns remain")
                    self.rpsndmg += 50
                    if person.ptime == 0:
                        raidbed.add_field(name="The Plauge", value=f"{person.name} was cured from the plague")
                        self.rpsned.remove(person)
                        if len(self.rpsned) == 0:
                            del person.ptime
                            self.rpsn = False

            if self.raidbeast.hasPassive():
                if self.raidbeast.passive.name == "Counter":
                    await self.cancounter(self.raidbeast, player, power, raidbed)
                
                if self.raidbeast.passive.name == "Regeneration":
                    await self.canregen(self.raidbeast, raidbed)
            
            if player.hasPassive():
                if player.passive.name == "Regeneration":
                    await self.canregen(player, raidbed)

            if player.armour.hasregen():
                x = math.floor((player.armour.regen / 100) * player.health) 
                player.health += x
                raidbed.add_field(name=f"{player.armour.name} effect:", value=f"heals {player.name} for {x} hp")
            

            raidbed.add_field(inline=False,name="Notif:", value= f"{player.name} {player.attackmsg} {self.raidbeast.name} for {power} damage")
            raidbed.add_field(inline=False,name=f"{player.name}:", value=f"Health: {player.health}")
            raidbed.add_field(inline=False,name=f"{self.raidbeast.name}:", value=f"Health: {self.raidbeast.health}")


            await self.rembed(raidbed, channel)
            await asyncio.sleep(3)


    async def highhealth(self):
        hihp = 0
        victim = None
        for player in self.raiders:
            if player.health > hihp:
                victim = player
                hihp = player.health
            else:
                continue

        return victim


    async def turngo2(self, channel):
        raidbed = discord.Embed(
            title=f"Raid battle against {self.raidbeast.name}",
            color=randint(0, 0xffffff)
        )

        power = randint(self.raidbeast.mindmg, self.raidbeast.maxdmg)
        critnum = randint(0, 100)
        healnum = randint(0, 100)

        power += self.raidbeast.weapon.damage

        num = randint(0, 6)
        if num in [1, 3, 4]:
            target = await self.highhealth()
        else:
            target = random.choice(self.raiders)

        if self.raidbeast.hasActive():
            if self.raidbeast.ability.oncd():
                self.raidbeast.ability.cdreduce()
            else:
                power, abilname = await self.canability(target, self.raidbeast, power, raidbed)
                if abilname == "Stop Time":
                    self.rts = True
                if abilname == "The Plague":
                    self.rpsned.append(target)
                    self.rpsn = True
                    self.rpsndmg = 100


        if self.rts:
            target.attack(power)
            power = randint(self.raidbeast.mindmg, self.raidbeast.maxdmg)
            critnum = randint(0, 100)
            healnum = randint(0, 100)

            power += self.raidbeast.weapon.damage
            self.rts = False

        if self.raidbeast.hasPassive():
            if self.raidbeast.passive.name == "Rage":
                if self.raidbeast.health <= 500:
                    self.raidbeast.passuse(0)
                    raidbed.add_field(name=f"{self.raidbeast.name}", value=f"{self.raidbeast.passive.usename}: {self.raidbeast.passive.effect}")
            else:
                power = self.raidbeast.passuse(power)
                raidbed.add_field(name=f"{self.raidbeast.passive.usename}", value=f"{self.raidbeast.name} {self.raidbeast.passive.effect} {target.name}", inline=False)


        if critnum > 0 and critnum <= self.raidbeast.critchance:
            raidbed.add_field(inline=False,name="Critical Hit", value=f"{self.raidbeast.name} got a crit")
            power *= 1.5
            if target.hasPassive():
                    if target.passive.name == "Critical Guard":
                        power = await self.cancritblock(target, self.raidbeast, power, raidbed)

        if healnum > 0 and healnum <= self.raidbeast.healchance:
            healin = randint(10, 20)
            raidbed.add_field(inline=False,name="Self Heal", value=f"{self.raidbeast.name} heals {healin} hp")
            self.raidbeast.heal(healin)

        if target.hasPassive():
            if target.passive.name == "Dodge":
                power = await self.candodge(target, self.raidbeast, power, raidbed)
            
        power = math.floor(power)
        target.attack(power)
        if target.health <= 0:
            await channel.send(f"{target.name} has been slain")
            self.raiders.remove(target)

        if target.hasPassive():
            if target.passive.name == "Counter":
                await self.cancounter(target, self.raidbeast, power, raidbed)
                
            if self.raidbeast.health <= 0:
                return
                
            if target.passive.name == "Regeneration":
                await self.canregen(target, raidbed)

            raidbed.add_field(inline=False,name="Notif:", value= f"{self.raidbeast.name} {self.raidbeast.attackmsg} {target.name} for {power} damage")
            raidbed.add_field(inline=False,name=f"{self.raidbeast.name}:", value=f"Health: {self.raidbeast.health}")
            raidbed.add_field(inline=False,name=f"{target.name}:", value=f"Health: {target.health}")
            await self.rembed(raidbed, channel)

            

            await asyncio.sleep(3)
        if self.raidbeast.hasPassive():
            if self.raidbeast.passive.name == "Regeneration":
                await self.canregen(self.raidbeast, raidbed)

        
    async def getmember(self, x):
        for user in self.users:
            if user.tag == x.id:
                return user

        return None

    async def denied(self, chan, person):
        await chan.send(f"{person.mention}, or the person you @mentioned does not have a profile. Create one with <>createprofile")

    async def expgain(self, winner, loser):
        winner = await self.getmain(winner)
        if loser.typeobj == "npc":
            exp = randint(loser.minxp, loser.maxxp)
            winner.curxp += exp
        else:
            exp = loser.xpthresh / 2
            winner.curxp += exp
        
        winner.wins += 1

        levelup = await self.didlevel(winner)

        if levelup:
            return True
        else:
            irl = await self.getirl(winner)
            return f"{irl.mention} has gained {exp} exp points from defeating {loser.name}"    

    async def getirl(self, user):
        everyone = self.bot.get_all_members()
        person = [x for x in everyone if x.id == user.tag]
        person = person[0]
        return person



    async def didlevel(self, x):
        if x.curxp >= x.xpthresh:
            while x.curxp >= x.xpthresh:
                x.curxp -= x.xpthresh
                x.xpthresh += 50
                x.level += 1
                x.health += randint(3, 8)
                x.mindmg += randint(1, 4)
                x.maxdmg += randint(3, 8)
                x.addcoin(20 * x.level)
            
            return True

        else:
            return False
            

    async def lost(self, arg):
        if arg in enemy:
            return
        
        user = arg

        user.losses += 1

    async def get_enemy(self, tier):
        yes = []
        if tier == 1:
            min = 10
            max = 250
        elif tier == 2:
            min = 250
            max = 350
        elif tier == 3:
            min = 350
            max = 900
        elif tier == 4:
            min = 700
            max = 2999

        else:
            min = 3000
            max = 999999999

        for vanillian in enemy:
            if vanillian.health >= min and vanillian.health <= max:
                yes.append(vanillian)

        villain = random.choice(yes)


        villain = FightingBeast(villain.name, villain.tag, villain.health, villain.mindmg, villain.maxdmg, 
        villain.mincoin, villain.maxcoin, villain.entrymessage, villain.minxp, villain.critchance, villain.healchance,
        villain.ability, villain.passive, villain.attackmsg, villain.weapon, villain.armour, villain.typeobj)
        
        return villain

    hadreward = []
    # Daily

    async def getreward(self, user):
        rew = randint(0, 60)
        if rew >= 0 and rew <= 20:
            # Money reward
            amount = randint(math.ceil(user.health / 10), math.ceil(user.health / 3))
            user.addcoin(amount)
            msg = f"You received {amount} Parade Coins"
            return msg

        if rew >=21 and rew <= 40:
            # Health Reward
            amount = randint(5, 25)
            user.health += amount
            msg = f"Your health increased by {amount}"
            return msg
        
        if rew >= 41 and rew <= 50:
            # Power Reward
            amount = randint(1, 6)
            user.maxdmg += amount
            msg = f"Your max power has been increased by {amount}"
            return msg

        if rew >= 51 and rew <= 55:
            # Crit Reward
            amount = randint(1, 3)
            if user.critchance >= 65:
                await self.getreward(user)
                return
            user.critchance += amount
            msg = f"Your crit chance has been increased by {amount}%"
            return msg

        if rew >=56 and rew <= 60:
            # Health regain Chance reward
            amount = randint(1, 4)
            if user.healchance >= 50:
                await self.getreward(user)
                return
            user.healchance += amount
            msg = f"Your chance to heal has been increased by {amount}%"
            return msg

    
    async def botquest(self, ctx, victimchannel, member: discord.Member):
        member = member
        embed = discord.Embed(
                title="Time for quest",
                description="Isaiah's Parade sets out on a quest",
                color=randint(0, 0xffffff)
            )

        await victimchannel.send("<>quest")
        await victimchannel.send(embed=embed)
        ctx.channel = victimchannel
        await self.fight(ctx, member, True, True)


    async def rembed(self, embed, channel):
        channel2 = self.bot.get_channel(740764507655110666)
        if channel == channel2:
            await channel.send(embed=embed)
        else:
            await channel.send(embed=embed)
            await channel2.send(embed=embed)


    async def ismember(self, x):
        for user in self.users:
            if user.tag == x.id:
                return True

        return False

    @commands.command()
    @commands.is_owner()
    async def meadd(self, ctx):
        for server in self.bot.guilds:
            role = discord.utils.get(server.roles, name="Parader")
            for member in server.members:
                if await self.ismember(member):
                    await member.add_roles(role)
                else:
                    pass
            
            await ctx.send(f"Returned roles to all members in {server.name}")


    # Isaiah

    @commands.command()
    @commands.is_owner()
    async def terrorize(self, ctx, member: discord.Member):
        member = member
        while True:
            channel = ctx.guild.get_channel(739248277257715752)

            await self.botquest(ctx, channel, member)

            await asyncio.sleep(6 * 60)


    @tasks.loop(minutes=5.0)
    async def updlist(self):
        dumped = []
        for fighter in self.users:

            dumped.append(fighter.__dict__)

        with open("fightdata.json", "w") as f:
            json.dump(dumped, f, indent=4)

        print("Updated")

    




    @commands.command()
    @commands.is_owner()
    async def createbot(self, ctx):
        bott = self.bot.user
        ParadeMaster = Fighter(bott.display_name, bott.id, 0, 0, 200, 12, 30, 0, 0, 60)
        self.users.append(ParadeMaster)
        await ctx.send(f"Successfully Created Profile for {bott.display_name}")

    


    async def canability(self, defender, attacker, power, embed):
        useabil = randint(0, 100)
        if useabil >= 25 and useabil <= 50:
            if not attacker.ability.oncd():
                attacker.ability.cdreduce()
                power = attacker.abiluse(power)
                if attacker.ability.name == "The Plague":
                    defender.ptime = 3
                embed.add_field(name=f"{attacker.ability.usename}", value=f"{attacker.name} {attacker.ability.effect} {defender.name} for {power} damage",inline=False)
                return power, attacker.ability.name
            else:
                embed.add_field(name="Ability Failed", value=f"{attacker.name} tried to use their ability. But it's on Cooldown", inline=False)

        return power, None
        
    async def canhaki(self, defender, attacker, power, embed):
        attacker.mindmg += 50
        attacker.maxdmg += 50
        embed.add_field(name=f"{attacker.passive.usename}:", value=f"{attacker.name} {attacker.passive.effect}")
        return power

    async def cantruehaki(self, defender, attacker, power, embed):
        attacker.mindmg += 50
        attacker.maxdmg += 50
        embed.add_field(name=f"{attacker.passive.usename}:", value=f"{attacker.name} {attacker.passive.effect}")
        if defender.level <= attacker.level - 30:
            defender.health -= 100
            embed.add_field(name=f"{attacker.passive.usename}:", value=f"{defender.name} lost 100 health to {attacker.passive.usename}")
        
        return power

    async def canbalance(self, defender, attacker, power, embed):
        power += 100
        attacker.health += 100
        embed.add_field(name=f"{attacker.passive.usename}:", value=f"{attacker.name} {attacker.passive.effect}")
        return power

    async def candodge(self, defender, attacker, power, embed):
        usedodge = randint(0, 100)
        if usedodge >= 25 and usedodge <= 50:
            power = 0
            embed.add_field(name=f"{defender.passive.usename}:", value=f"{defender.name} {defender.passive.effect} {attacker.name}")
        
        return power

    async def cancounter(self, defender, attacker, power, embed):
        usecounter = randint(0, 100)
        if usecounter >= 10 and usecounter <= 25:
            embed.add_field(name=f"{defender.passive.usename}:", value=f"{defender.name} {defender.passive.effect} {attacker.name}")
            power = defender.passuse(power)
            attacker.attack(power)


    async def canregen(self, user, embed):
        regenamount = math.ceil((10/ 100) * user.health)
        embed.add_field(name=f"{user.passive.usename}:", value=f"{user.name} {user.passive.effect}: {regenamount}")
        user.passuse(0)

    async def cansharpeye(self, defender, attacker, power, embed):
        usesharpeye = randint(0, 100)
        if usesharpeye >= 50 and usesharpeye <= 75:
            embed.add_field(name=f"{attacker.passive.name}:", value=f"{attacker.name} {attacker.passive.effect} {defender.name}")
            power = attacker.passuse(power)

        return power

    async def cancritblock(self, defender, attacker, power, embed):
        usecritblock = randint(1,3)
        if usecritblock == 1 or usecritblock == 3:
            embed.add_field(name=f"{defender.passive.name}:", value=f"{defender.name} {defender.passive.effect} {attacker.name}")
            power /= 1.5
            power = defender.passuse(power)
        
        return power

    async def fightuser(self, account):
        person = FightMe(account.name, account.tag, account.level, account.curxp, account.health, account.mindmg, account.maxdmg, 
        account.wins, account.losses, account.pcoin, account.critchance, account.healchance, account.ability,
        account.passive, account.weapon, account.armour, account.xpthresh, account.typeobj, account.canfight)
        person.instantize()
        return person
        

    async def getmain(self, arg):
        for user in self.users:
            if user.tag == arg.tag:
                return user

        return None


    # Event
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if not self.raidon and not self.raiding:
            potraid = randint(0, 7000)
            if potraid >= 20 and potraid <= 40:
                self.raidon = True
                await self.startRaid()

    
    @commands.command()
    @commands.is_owner()
    async def resetstats(self, ctx, member: discord.Member):
        yes = await self.ismember(member)
        if yes:
            await self.profile(ctx, member)
            await asyncio.sleep(5)
            await ctx.send(f"Reset the stats for {member.name}")
        

    async def loadarmour(self, ctx):
        armorbed = discord.Embed(
            title="Welcome to my Armour Store",
            description="To buy an item, use <>buy {item name}, or use <>view {item name} for details",
            color=randint(0, 0xffffff)
        )

        user = await self.getmember(ctx.author)

        if user.getTier() == 5:
            for item in armorlist:
                if item.tierz >= 4:
                    armorbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")            

        else:
            for item in armorlist:
                if item.tierz <= user.getTier():
                    armorbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")            
        
        await ctx.send(embed=armorbed)



    async def loadweapon(self, ctx):
        weaponbed = discord.Embed(
            title="Welcome to my Weapon Store",
            description="To buy an item, use <>buy {item name}, or use <>view {item name} for details",
            color=randint(0, 0xffffff)
        )
        
        user = await self.getmember(ctx.author)

        if user.getTier() == 5:
            for item in weaponlist:
                if item.tierz >= 4:
                    weaponbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")

        else:
            for item in weaponlist:
                if item.tierz <= user.getTier():
                    weaponbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")

        await ctx.send(embed=weaponbed)



    
    async def canbuy(self, user, arg):
        if user.weapon == arg.name or user.armour == arg.name:
            msg = "You already have this equipped"
            return msg

        if user.getTier() < arg.tierz:
            return "You are too weak to wield this item"

        if user.pcoin >= arg.cost:
            user.pcoin -= arg.cost
            if arg.typeobj.lower() == "weapon":
                user.weapon = arg.name
            else:
                user.armour = arg.name

            msg = f"Successfully bought {arg.name}"

            return msg
        
        return f"Now that won't do. You don't have enough Parade Coins to buy {arg.name}"


    async def getjob(self, channel, user, tier):
        jobbed = discord.Embed(
            title=f'Tier {tier} job:',
            color=randint(0, 0xffffff)
        )
        if tier == 1:
            jobdesc = random.choice(jobs.jtier1)
            reward = randint(30, 70)
            loss = randint(5, 15)
            
        elif tier == 2:
            jobdesc = random.choice(jobs.jtier2)
            reward = randint(120, 170)
            loss = randint(30, 50)
            
        elif tier == 3:
            jobdesc = random.choice(jobs.jtier3)
            reward = randint(250, 360)  
            loss = randint(80, 160)
            
        elif tier == 4:
            jobdesc = random.choice(jobs.jtier4)
            reward = randint(10000, 15000)
            loss = randint(1000, 1450)

        elif tier == 5:
            jobdesc = random.choice(jobs.jtier5)
            reward = randint(30000, 40000)
            loss = randint(3600, 4000)
            
        else:
            await channel.send("An unknown error occured.")
            return

        yes = await self.didpass()
        await self.result(user, jobbed, yes, reward, loss)
        
        jobbed.description = jobdesc        

        await channel.send(embed=jobbed)

    async def didpass(self):
        num = randint(0, 100)
        if num >= 20 and num <= 80:
            return "Success"
        else:
            return "You Failed"

    async def result(self, user, jobbed, yes, reward, loss):
        jobbed.add_field(name="Done", value=f"{yes}")
        if yes.lower() == "success":
                jobbed.add_field(name="Here is your payment", value=f"You received {reward} parade coins")
                jobbed.add_field(name="Woop woop", value=f"{random.choice(jobs.responses)}")
        else:
            jobbed.add_field(name="How unfortunate", value=f"You had to pay {loss} parade coins for your failure")
            jobbed.add_field(name="Sigh", value=f"{random.choice(jobs.badresp)}")


    @commands.command()
    async def botrestart(self, ctx):
        await ctx.message.delete()
        self.aboutupdate = True

        print(len(self.infight))
        print(len(self.raiders))
        await asyncio.sleep(5)

        counter = 0

        while len(self.infight) > 0 or len(self.raiders) > 0 or len(self.inquest) > 0:
            print(len(self.infight))
            print(len(self.raiders))
            print(len(self.inquest))
            counter += 1
            await asyncio.sleep(10)

        self.updlist.restart()
        
        await ctx.send("Restarting bot")

        await asyncio.sleep(3)
        raise SystemExit     

        
def setup(bot):
    bot.add_cog(FullFight(bot))