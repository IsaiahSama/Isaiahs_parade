import discord
from discord.ext import commands, tasks
from aiosqlite import connect
import asyncio
import random
from random import randint
from images import hugs, punches, kisses, slaps, knock, poses, flexes
from fight import FightMe, Fighter, questpro, enemy, FightingBeast, abilities, allabilities, passives, allpassives, raidingmonster, weaponlist, armourlist, gear, lilgear, allarmour, allweapons, BeastFight, fightdb
from items import Item, potlist, allpotlist
import math
import jobs
from teams import Team, ToAdv
from battle_functionality import train_emojis, TrainingHandler

emojiz = ["🤔", "🤫", "🤨", "🤯", "😎", "😓", "🤡", "💣", "🧛", "🧟‍♂️", "🏋️‍♂️", "⛹", "🏂"]
db_name = "iparadedb.sqlite3"


# Evolution of Fighter class

# def __init__(self, name, tag, level, health, mindmg, maxdmg, wins, losses, attackmsg=None):

# def __init__(self, name, tag, level, health, mindmg, maxdmg, wins, losses, pcoin, critchance=5, healchance=3, 
# ability=None, passive=None, weapon=fist, armour=linen):

# def __init__(self, name, tag, level, curxp, health, mindmg, maxdmg, wins, losses, pcoin, critchance=5, healchance=3, 
# ability=None, passive=None, weapon=fist, armour=linen, xpthresh=50, typeobj="player"):

# def __init__(self, name, tag, level, curxp, health, mindmg, maxdmg, wins, losses, pcoin, 
# critchance=5, healchance=3, ability=None, passive=None, weapon="Fist", armour="Linen", 
# xpthresh=50, typeobj="player", canfight=True):

# name tag level curxp health mindmg maxdmg wins losses pcoin critchance healchance ability passive weapon armour xpthresh typeobj
# canfight inteam invation weapon2 armour2 curbuff buffdur inventory, reborn

class Fight(commands.Cog):
    """FIGHT COMMANDS!!!"""
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.async_init())

    
    users = []
    teamlist = []

    async def async_init(self):
        await self.bot.wait_until_ready()
        self.homeguild = self.bot.get_guild(739229902921793637)
        
        async with connect(db_name) as db:
            await fightdb.setup(db)
            self.users = await fightdb.query_all_fighters(db)

        await self.setup_fighters()

        # self.teamlist = await Saving().loaddata("teamdata")
        # if not self.teamlist: self.teamlist = []
        self.update_fighters.start()
        print("Let's begin.")

    modlist = [347513030516539393, 527111518479712256, 493839592835907594, 315619611724742656, 302071862769221635]
          

    # Commands

    @commands.command(aliases=["pcoin", "pcoins"], brief="Used to view your currency", help="Check your balance")
    async def paradecoins(self, ctx):
        user = await self.getmember(ctx.author)
        
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return
        else:
            await ctx.send(f"{ctx.author.mention} has {user.pcoin} Parade Coins. Check out <>upgrade")

    
    @commands.command(brief="Donate to a friend... no overfeeding though", help="Use this to give money to someone. Cooldown: 10 minutes", usage="@user amount")
    @commands.cooldown(1, 600, commands.BucketType.user)
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

        if user1 == user2:
            user1.takecoin(arg)
            user2.addcoin(1/2 * arg)
            await ctx.send("Successful... But it seems you dropped and lost some in the process")

        if len(str(arg)) > user2.getTier() + 1:
            await ctx.send("You are trying to give too much money for that person's tier :face_with_monocle:")
            return

        if user1.pcoin >= arg:
            user1.takecoin(arg)
            user2.addcoin(arg)
            await ctx.send("Successful")

        else:
            await ctx.send("You don't have enough to give.")

    @commands.command(brief="View yourself at your FULL POWER!!", help="Your profile, but includes buffs from gear.", usage="option[@user]")
    async def powprofile(self, ctx, member: discord.Member=None):
        if await self.getmember(ctx.author):
            await ctx.send("Now shine... In your true form")
            await self.profile(ctx, member, True)
            return 0
        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command(aliases=["p"], usage="optional[@user]", brief="See your profile", help="Use this to view your fight profile")
    async def profile(self, ctx, member: discord.Member=None, powpof=False):
        if not member:
            target = await self.getmember(ctx.author)

        else:
            target = await self.getmember(member)

        if not target:
            await self.denied(ctx.channel, ctx.author)
            return

        
        if powpof:
            target = await self.fightuser(target)
            sword, shield = target.weapon, target.armour
            if target.weapon.name == "Plague Doctors Scepter":
                target.weapon.damage = math.floor(target.maxdmg * 0.5)
        
        else:
            sword, shield = target.getgear()
            if ctx.author.id in self.modlist and target.tag == ctx.author.id:
                await self.modcheck(ctx, target)
            
        profileEmbed = discord.Embed(
            title=f"Profile for {target.name}",
            color=randint(0, 0xffffff)
        )

        if not member:
            profileEmbed.set_thumbnail(url=ctx.author.avatar_url)
        else:
             profileEmbed.set_thumbnail(url=member.avatar_url)
        
        if ctx.guild == self.homeguild and not powpof:
            if ctx.author.id == target.tag:
                role = [x for x in ctx.author.roles if x.name == f"Tier{target.getTier()}"]
                if not role:
                    role = discord.utils.get(ctx.guild.roles, name=f"Tier{target.getTier()}")
                    await ctx.author.add_roles(role)
                    await ctx.send(f"You have received your ranking role of {role.name}")
                if target.hasreborn():
                    role = [x for x in ctx.author.roles if x.name == "The Reborn"]
                    if not role:
                        role = discord.utils.get(ctx.guild.roles, name="The Reborn")
                        await ctx.author.add_roles(role)
                        await ctx.send("You Have received your role of The Reborn")

        await self.fixvalues(target)

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
            profileEmbed.add_field(name="Weapon:", value=f"{sword.name}")
            profileEmbed.add_field(name="Armour:", value=f"{shield.name}")
            if target.hasActive():
                profileEmbed.add_field(name=f"Ability:", value=f"{target.ability.name}")

            else:
                profileEmbed.add_field(name="Ability:", value=f"None... Yet")
            
            if target.hasPassive():
                profileEmbed.add_field(name=f"Passive:", value=f"{target.passive.name}")
            else:
                profileEmbed.add_field(name="Passive:", value=f"None... Yet")
        else:
            
            profileEmbed.add_field(name="Weapon:", value=f"{sword.name}")
            profileEmbed.add_field(name="Armour:", value=f"{shield.name}")
            if target.hasActive():
                profileEmbed.add_field(name=f"Ability:", value=f"{target.getabilpassname(target.ability)}")
            else:
                profileEmbed.add_field(name="Ability:", value=f"None... Yet")

            if target.hasPassive():

                profileEmbed.add_field(name=f"Passive:", value=f"{target.getabilpassname(target.passive)}")
            else:
                profileEmbed.add_field(name="Passive:", value=f"None... Yet")
            
        profileEmbed.add_field(name="Parade Coins:", value=f"{target.pcoin}")
        profileEmbed.add_field(name="Crit Chance:", value=f"{target.critchance}%")
        profileEmbed.add_field(name="Self Heal Chance:", value=f"{target.healchance}%")
        
        if target.hasreborn():
            profileEmbed.add_field(name="Number of times Reincarnated", value=target.reborn)

        await ctx.send(embed=profileEmbed)

    @commands.command(brief="Ready to become a parader... Just run this command", help="So you want to become one of us? Well... this command is your first step.")
    async def createprofile(self, ctx):
        user = await self.getmember(ctx.author)
        channel = self.bot.get_channel(739266609264328786)
        if user:
            await ctx.send("You already have a profile. View with <>profile")
            await ctx.send("Did you mean <>createsocial to create a Social Profile?")
            return
        else:
            acc = Fighter(ctx.author.name, ctx.author.id, 0, 0, 170, 10, 20, 0, 0, 100)
            self.users.append(acc)
            await ctx.send("Profile Created. View with <>profile")
            await channel.send(f"{ctx.author.name} from {ctx.guild.name} is now a parader")
            role = [p for p in ctx.guild.roles if p.name == "Parader"]
            if not role:return
            role = role[0]
            await ctx.author.add_roles(role)
        
        async with connect(db_name) as db:
            await fightdb.insert_or_replace(db, acc)

    @commands.command(aliases=["q6"], brief="A quest for those who have reborn or are tier 6", help="A bonus quest for those who are Tier 6 or reborn. Cooldown: 2 uses, 5 minutes")
    @commands.cooldown(2, 300, commands.BucketType.user)
    async def quest6(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if user.reborn > 1 or user.getTier() == 6:
                await self.quest(ctx, True)
            else:
                await ctx.send("You can not use this as you are not tier 6")
        else:
            await self.denied(ctx.channel, ctx.author)
            return

    inquest = []
    @commands.command(aliases=["q"], brief="The standard quest to get you started", help="Embark on a quest for GLORY!! or glorious death")
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def quest(self, ctx, q6=False):
        if self.aboutupdate:
            await ctx.send("Cannot Do a Quest/Fight Right now as bot is about to go offine")
            return
        user = await self.getmember(ctx.author)

        if not user:
            await self.denied(ctx.channel, ctx.author)
            return

        if user.tag in self.channeling:
            await ctx.send("Cannot quest now as you are channeling")
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

        
        if user.reborn > 1 and not q6:
            await ctx.send("You can no longer do these quests. Do <>quest6 Instead")
            return


        self.inquest.append(user.tag)
    
        await ctx.send(embed=embed)
        try:
            if q6 and tier == 6 or q6 and user.reborn >= 1:
                await self.fight(ctx, None, False, True, True)
            else:
                await self.fight(ctx, None, False, True)
        except Exception as err:
            await ctx.send(err)
            self.inquest.remove(user.tag)
            raise err

    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def clrquest(self, ctx):
        self.inquest.clear()
        await ctx.send("Reset All Quests") 

    async def upgradebot(self, ctx):
        toupgrade = random.choice(["health", "min_dmg", "max_dmg"])
        await ctx.send(f"<>upgrade {toupgrade} 1")
        await self.upgrade(ctx, toupgrade, 1)

    @commands.command(brief="Used to upgrade your stats.", help="Get stronger by upgrading your stats", usage="optional[stat_to_upgrade] optional[amount_of_times_to_upgrade]")
    async def upgrade(self, ctx, arg=None, amount:int = 1):
        user = await self.getmember(ctx.author)
        
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return

        if not arg:
            user2 = await self.fightuser(user)
            statembed = discord.Embed(
                title=f"Stat Table for {ctx.author.display_name}",
                color=randint(0, 0xffffff)
            )

            await self.fixvalues(user)

            statembed.add_field(name="Tier:", value=f"{user.getTier()}")
            statembed.add_field(name="Level:", value=f"{user.level}", inline=False)
            statembed.add_field(name=f"Health: {user.health}", value=f"+20 = {user.healthprice()} Parade Coins", inline=False)
            statembed.add_field(name=f"Min_Dmg: {user.mindmg}", value=f"+5 = {user.mindmgprice()} Parade Coins", inline=False)
            statembed.add_field(name=f"Max_Dmg: {user.maxdmg}", value=f"+5 = {user.maxdmgprice()} Parade Coins", inline=False)
            statembed.add_field(name=f"Crit_chance: {user.critchance}%", value=f"+2% = {user.critchanceprice()} Parade Coins")
            statembed.add_field(name=f"Heal_Chance: {user.healchance}%", value=f"+3% = {user.healchanceprice()} Parade Coins", inline=False)
            if user.hasPassive():
                statembed.add_field(name=f"Passive: {user2.passive.name}", value=f"{user2.passive.description}")
            elif user.level >= 40 and not user.hasPassive():
                statembed.add_field(name="Passive:", value="You are strong enough to wield a passive. Get one with <>passive")
            else:
                statembed.add_field(name="Passive:", value="Unlocked at level 40")
            if user.hasActive():
                statembed.add_field(name=f"Active Ability: {user2.ability.name}", value=f"{user2.ability.description}")
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
            msg = user.uphealth(amount)
        elif arg == "min_dmg":
            msg = user.upmin(amount)
        elif arg == "max_dmg":
            msg = user.upmax(amount)
        elif arg == "crit_chance":
            msg = user.upcrit()
        elif arg == "heal_chance":
            msg = user.upheal()
        else:
            await ctx.send(f"{arg} is not a valid stat. Use <>upgrade by itself to see the stat names")
            return

        await ctx.send(msg)

    @commands.command(brief="Shows your passive if you have one", help="Shows your passive if you have one")
    async def mypassive(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if user.hasPassive():
                embed = discord.Embed(
                    title="Passive",
                    description=f"Showing Passive for {user.name}",
                    color=randint(0, 0xffffff)
                )
                abil = [x for x in allpassives if x.tag == user.passive]
                if abil:
                    abil = abil[0]
                    embed.add_field(name=abil.name, value=abil.description)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send("Something went wrong")
            else:
                await ctx.send("You do not have a passive")
            
        else:
            await self.denied(ctx.channel, ctx.author)

    @commands.command(brief="Shows the list of reborn passives. Must have reborned", help="If you have already reborned, you can use this command to take a look at passives available for your level of reborn")
    async def rpassive(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if user.hasreborn():
                await self.passive(ctx, rb=True)
            else:
                await ctx.send("You are not reborn")
        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command(brief="Get a passive or view the list of passives", help="This command is used to get your first passive, and also to change it to one you may one... for a price", usage="optional[True name_of_passive]")
    async def passive(self, ctx, arg=False, *, name_of_passive=None, rb=False, isbot=False):
        user = await self.getmember(ctx.author)
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return

        if user.level < 40:
            await ctx.send("You must be at least level 40 to get a passive")
            return

        if not user.hasPassive():
            pash = random.choice(passives)
            await ctx.send(f"Congratulations, your passive ability is {pash.name}. Check with <>profile")
            user.passive = pash.tag
            return
        if isbot: return
        if user.hasPassive() and not arg:
            passconfirm = discord.Embed(
                title=f"Passive Change. Your passive is {user.getabilpassname(user.passive)}",
                description="This will allow you to choose your passive. It will cost you dearly... 15 000 Parade Coins to be exact",
                color=randint(0, 0xffffff)
            )

            if rb:
                lowpass = [passi for passi in passives if passi.reborn]
            else:
                lowpass = [passi for passi in passives if not passi.reborn]
 
            for passi in lowpass:
                passconfirm.add_field(name=f"{passi.name}:", value=f"{passi.description}. Reborn: {passi.reborn}")

            passconfirm.set_footer(text="Continue... If you wish to continue, use <>passive True {Name of Passive}")

            await ctx.send(embed=passconfirm)
            return

        if user.hasPassive() and arg:
            if name_of_passive == None:
                await ctx.send("You did not enter the name of the passive you wanted")
                return
            value = None
            for passi in passives:
                if name_of_passive.lower() == passi.name.lower():
                    value = passi
                    break

            if value == None:
                await ctx.send(f"{value} is not a Passive, or is not available")
                return

            if value.isreborn():
                if not user.reborn >= value.reborn:
                    await ctx.send("This passive requires a higher reborn level to get.")
                    return
     
            msg = user.passchange(value)

            await ctx.send(msg)

    @commands.command(aliases=["myactive"], brief="Shows your ability if you have it.", help="Used to view your ability.")
    async def myability(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if user.hasActive():
                embed = discord.Embed(
                    title="Ability",
                    description=f"Showing Ability for {user.name}",
                    color=randint(0, 0xffffff)
                )
                abil = [x for x in allabilities if x.tag == user.ability]
                if abil:
                    abil = abil[0]
                    embed.add_field(name=abil.name, value=abil.description)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send("Something went wrong")

            else:
                await ctx.send("You do not have an ability.")
                return
        else:
            await self.denied(ctx.channel, ctx.author)

    @commands.command(aliases=["ractive"], brief="Used to view reborn abilities", help="Use this to get a list of all reborn abilities available for your reborn level.")
    async def rability(self, ctx):
        user = await self.getmember(ctx.author)
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return

        if user.hasreborn():
            await self.active(ctx, rb=True)
            return

        else:
            await ctx.send("You are not reborn")

    @commands.command(aliases=["ability"], brief="Get your first ability or switch it out", help="Use this to view a list of the abilities, get your first one or change it to a new one", usage="optional[True name_of_ability]")
    async def active(self, ctx, arg=False, *, act=None, rb=False):
        user = await self.getmember(ctx.author)

        if not user:
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
                title=f"Your ability is {user.getabilpassname(user.ability)}",
                description="Going any further with this command will cost you 25 000 Parade Coins and will allow you to choose your ability",
                color=randint(0, 0xffffff)
            )

            if not rb:
                abils = [acci for acci in abilities if not acci.reborn]
            else:
                abils = [acci for acci in abilities if acci.reborn]
                
            for acci in abils:
                accheck.add_field(name=f"{acci.name}", value=f"{acci.description}. Reborn: {acci.reborn}")

            accheck.set_footer(text="\nContinue... If you wish to continue, use <>active True {Name of Active}")

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
            
            if not target:
                await ctx.send(f"That is either not an active ability, or must be obtained by special means")
                return

            if target.isreborn():
                if not user.reborn >= target.reborn:
                    await ctx.send("Your reborn Levels are too low for this ability.")
                    return

            msg = user.actichange(target)

            await ctx.send(msg)

    
    raidon = False
    raiding = False
    raiders = []
    raidbeast = None
    winner = None

    @commands.command(brief="A RAID!!! Join it with <>raid", help="This command is to be used to join an existing pending raid.")
    async def raid(self, ctx):
        if ctx.guild == None:
            await ctx.send("You can't do that here :facepalm:")
            return

        channel = self.homeguild.get_channel(740764507655110666)

        user = await self.getmember(ctx.author)
        for raider in self.raiders:
            if raider.tag == user.tag:
                await ctx.send("You are already in the raid")
                return
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return

        if user.tag in self.channeling:
            await ctx.send("You cannot join a raid now since you are channeling")
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
        
    @commands.command(brief="Gives you a random reward", help="Receives a random reward. Cooldown: 1 hour")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def reward(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            msg = await self.getreward(user)
            if not msg:
                item = random.choice(allpotlist)
                if len(user.inventory) < 25:
                    user.inventory.append(item.tag)
                    msg = f"You have received {item.name}. Return in 1 hour"
            await ctx.send(f"{msg}. Come back in 1 hour")
            return

        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command(brief="Toggle your Parader role", help="Use this to toggle your Parader role.")
    async def readd(self, ctx):
        user = await self.getmember(ctx.author)

        if not user:
            await self.denied(ctx.channel, ctx.author)
            return

        yes = discord.utils.get(ctx.author.roles, name="Parader")
        if not yes:
            role = discord.utils.get(ctx.guild.roles, name="Parader")

            await ctx.author.add_roles(role)

            await ctx.send(f"{ctx.author.display_name} now has back their Parader role")
        
        else:
            await ctx.author.remove_roles(yes)

            await ctx.send(f"Removed Parader role from {ctx.author.name}. Do this command again to get it back")

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def train(self, ctx):
        player = await self.getmember(ctx.author)
        if not player:
            await self.denied(ctx.channel, ctx.author)
            return 

        train_embed = discord.Embed(
            title="Training",
            description=f"What do you want to train?\n💢: `Damage`\n🛡️: `Defense`\n💙: `Health`\n💥: `Crit_Chance`",
            color=randint(0, 0xffffff)
        )

        msg = await ctx.send(embed=train_embed)

        for emoji in train_emojis.keys():
            await msg.add_reaction(emoji)
        
        def check(reaction, user):
            return str(reaction.emoji) in list(train_emojis.keys()) and user == ctx.author

        try:
            reaction = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(":x:Took too long to respond to me. :x:")
            return

        choice = train_emojis[str(reaction[0].emoji)]

        train_embed.description = f"Training {choice}"
        await msg.edit(embed=train_embed)

        trainHandler = TrainingHandler()

        if choice == "Damage":
            player = await trainHandler.handle_damage(self.bot, ctx, player)
        elif choice == "Defense":
            player = await trainHandler.handle_defense(self.bot, ctx, player)
        elif choice == "Health":
            player = await trainHandler.handle_health(self.bot, ctx, player)
        else:
            player = await trainHandler.handle_crit(self.bot, ctx, player)

        if await self.didlevel(player):
            await ctx.send(f"{player.name} has reached level {player.level}")

    # Main
    infight = []
    aboutupdate = False
    @commands.command(brief="FIGHT SOMEONE!!", help="This is used to start a fight with someone", usage="@user")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fight(self, ctx, member: discord.Member, isbot=False, isquest=False, q6=False):
        iparade = self.bot.user
        if self.aboutupdate:
            await ctx.send("Cannot Do a Quest/Fight Right now as bot is about to go offine")
            return

        if isbot:
            account = await self.getmember(iparade)
        else:
            account = await self.getmember(ctx.author)
        
        if not account: await ctx.send("You need to create your own user profile with <>createprofile first"); return
        
        user1 = await self.fightuser(account)

        if not isquest:
            victim = await self.getmember(member)
            if not victim: await ctx.send(f"{member} does not have a fight profile. Let them make one with <>createprofile"); return
            user2 = await self.fightuser(victim)
            if member.status == discord.Status.offline:
                await ctx.send(f"{member.display_name} is offline so cannot be fought")
                return

            if not user1.fightable() or not user2.fightable():
                await ctx.send(f"One of you has disabled pvp. Turn it on with <>togglefight")
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

            if user1.tag in self.channeling or user2.tag in self.channeling:
                await ctx.send("You can not fight as you are channeling")
                return

            self.infight.append(user1.tag)
            self.infight.append(user2.tag)

            fightembed = discord.Embed(
                title="Fighting...",
                description=f"Fight Between {user1.name} and {user2.name}",
                color=randint(0, 0xffffff)
            )

            botmsg = await ctx.send(embed=fightembed)

        else:
            user2 = await self.get_enemy(user1, q6)          

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
            

        if user1.weapon.tag == 3601:
            user1.weapon.damage = math.floor(user1.maxdmg * 0.5)

        elif user2.weapon.tag == 3601:
            user2.weapon.damage = math.floor(user2.maxdmg * 0.5)

        user1.oghealth, user2.oghealth, user1.slag, user2.slag = user1.health, user2.health, 0, 0

        attacker, defender = random.sample([user1, user2], 2)

        fighting = True

        # Checking for Armour Weapon Pairs
        if attacker.armour.getpair():
            if attacker.weapon.tag == attacker.armour.pairs:
                msg = attacker.buff()
                await ctx.send(f"Set Bonus {msg}")
                

        if defender.armour.getpair():
            if defender.weapon.tag == defender.armour.pairs:
                msg = defender.buff()
                await ctx.send(f"Set Bonus {msg}")
                if not isquest:
                    await asyncio.sleep(3)


        if defender.hasPassive():
                if defender.passive.tag == 7006:
                    attacker, defender = defender, attacker
                    await ctx.send(f"{attacker.name} attacks first because of speed boost")

        """if user2.tag == 493839592835907594 and user1.tag in [315619611724742656, 347513030516539393, 315632232666759168]:
            user1.health = -999999
            await ctx.send(f"{user2.name} shut down {user1.name}'s attempt at betryal")
            attacker, defender = defender, attacker
            fighting = False"""
            
        psned = []
        turns = 1

        battlebed = discord.Embed(
                title=f"FIGHT... Turn {turns}",
                color=randint(0, 0xffffff)
            )
        
        slagged = False
        psn = False
        ts = False
        cts = False

        if user1.hasbuff():
            main1 = await self.getmain(user1)
            main1.bdur -= 1
            msg = await self.buffuse(user1)
                  
            await ctx.send(f"{user1.name}: {msg}")

            if user1.bdur <= 0:
                user1.bdur = 0
                await ctx.send("Your buff has expired")
                main1.curbuff = None
            else:
                await ctx.send(f"You have {main1.bdur} fights remaining with this buff")
        
        if not isquest:
            if user2.hasbuff():
                main2 = await self.getmain(user1)
                main2.bdur -= 1
                msg = await self.buffuse(user2)
                  
                await ctx.send(f"{user2.name}: {msg}")

                if user2.bdur <= 0:
                    user2.bdur = 0
                    await ctx.send("Your buff has expired")
                    user2.curbuff = None
                else:
                    await ctx.send(f"You have {main2.bdur} fights remaining with this buff")

        battle = await ctx.send("Battle will begin shortly.")

        while fighting:   
            await battle.edit(content="FIGHT!!!")         
            
            if attacker.hasPassive():
                if attacker.health <= (attacker.oghealth / 3):
                    if attacker.passive.tag == 7004:
                        attacker.passuse(0)
                        await ctx.send(f"New mindamage is {attacker.mindmg}")
                        await ctx.send(f"New Max Damage is {attacker.maxdmg}")
                        battlebed.add_field(name=f"{attacker.name}", value=f"{attacker.passive.usename}: {attacker.passive.effect}")


            if attacker.health >= 65000:
                attacker.weapon.lifesteal = 0
                attacker.armour.regen = 0
                if attacker.passive.tag == 7003:
                    attacker.passive.tag = None
                if attacker.ability.tag == 5009:
                    attacker.ability.tag = None
                await ctx.send(f"All regen has been Disabled for {attacker.name}")

            if attacker.mindmg > attacker.maxdmg:
                attacker.mindmg = attacker.maxdmg - 1
                
            power = randint(round(attacker.mindmg), round(attacker.maxdmg))

            critnum = randint(0, 100)
            healnum = randint(0, 100)

            if slagged:
                if attacker.ability.tag == 5012:
                    if defender.slag == 0:
                        pass
                    else:
                        defender.slag -= 1
                        power *= 1.5
                        battlebed.add_field(name=f"{attacker.ability.usename}", value=f"{defender.name} {attacker.ability.effect} {defender.slag} turns")

            power += attacker.weapon.damage

            if turns == 1:
                if attacker.hasPassive():
                    if attacker.passive.tag == 7006:
                        power *= 1.5
                        
            if attacker.hasPassive():
                if attacker.passive.tag == 7010:
                    if attacker.armour.tag == 2602:
                        if attacker.armour.getpair():
                            if attacker.weapon.tag == attacker.armour.Pairs:
                                power = await self.cantruehaki(defender, attacker, power, battlebed)
                        
                    elif attacker.weapon.tag == 1602:
                        power = await self.canhaki(defender, attacker, power, battlebed)
                    
                if attacker.passive.tag == 9101:
                    tob = 0.02 + (attacker.reborn / 100)
                    attacker.mindmg += math.ceil(tob * attacker.mindmg)     
                    attacker.maxdmg += math.ceil(tob * attacker.maxdmg)
                    attacker.health += math.ceil(tob * attacker.health)
                    battlebed.add_field(name=f"{attacker.name}: {attacker.passive.usename}", value=f"{attacker.passive.effect} by {tob * 100}%")

                if attacker.passive.name == "Pride of Balance":
                    if attacker.armour.getpair():
                        if attacker.armour.tag == 2603:
                            power = await self.canbalance(defender, attacker, power, battlebed)

            if defender.hasPassive():
                if defender.passive.tag == 9101:
                    tob = 0.02 + (defender.reborn / 100)
                    defender.mindmg += math.ceil(tob * defender.mindmg)     
                    defender.maxdmg += math.ceil(tob * defender.maxdmg)
                    defender.health += math.ceil(tob * defender.health)
                    battlebed.add_field(name=f"{defender.name}: {defender.passive.usename}", value=f"{defender.passive.effect} by {tob * 100}%")

            
            if attacker.hasActive():
                power, abiltag = await self.useability(defender, attacker, power, battlebed)
                if abiltag == 5012:
                    slagged = True

                if abiltag == 5001:
                    ts = True
                if abiltag == 6002:
                    ts = True
                    cts = True
                if abiltag == 6001:
                    psned.append(defender)
                    psn = True
                if abiltag == 5004:
                    if attacker.armour.getpair():
                        if attacker.weapon.tag == attacker.armour.pairs:
                            battlebed.add_field(name=f"{attacker.ability.usename}", value="Having armour set increases damage by 1.3 + 70")
                            power *= 1.3
                            power += 70

                if abiltag == 9001:
                    extradmg = 60
                    extrahp = 300
                    for _ in range(attacker.reborn): extradmg += 20
                    for _ in range(attacker.reborn): extrahp += 50

                    attacker.mindmg += extradmg
                    attacker.maxdmg += extradmg
                    attacker.health += extrahp
                    battlebed.add_field(name=attacker.ability.usename, value=f"Increased Min and Max damage by {extradmg} and health by {extrahp}")

            if ts or hasattr(defender, "flinch"):
                
                if hasattr(defender, "flinch"):
                    battlebed.add_field(name=attacker.ability.usename, value=f"{attacker.name} rolled a 4 and caused {defender.name} to flinch and did {power} damage.")
                else:
                    battlebed.add_field(name="In Stopped Time", value=f"{attacker.name} {attacker.attackmsg} {defender.name} for {power} damage")
                
                if cts:
                    defender.attack(power)
                    battlebed.add_field(name="In Stopped Time", value=f"{attacker.name} {attacker.attackmsg} {defender.name} for {power} damage")
                ts = False
                cts = False

                defender.attack(power)       
                power = randint(attacker.mindmg, attacker.maxdmg)
                critnum = randint(0, 100)
                healnum = randint(0, 100)

                power += attacker.weapon.damage
                
                if hasattr(defender, "flinch"):
                    delattr(defender, "flinch")

            if attacker.hasPassive():
                if attacker.passive.tag == 7005:
                    power = await self.cansharpeye(defender, attacker, power, battlebed)

            if critnum > 0 and critnum <= attacker.critchance:
                battlebed.add_field(name="Critical Hit", value=f"{attacker.name} got a crit")
                power *= 1.5
                if defender.hasPassive():
                    if defender.passive.tag == 7007:
                        power = await self.cancritblock(defender, attacker, power, battlebed)

            if healnum > 0 and healnum <= attacker.healchance:
                healin = randint(10, 20)
                battlebed.add_field(name="Self Heal", value=f"{attacker.name} heals {healin} hp")
                attacker.heal(healin)

            if defender.hasPassive():
                if defender.passive.tag == 7001:
                    power = await self.candodge(defender, attacker, power, battlebed)

            if attacker.typeobj == "player":
                if attacker.hasbuff():
                    buffitem = await self.getbuff(attacker.curbuff)
                    if buffitem.pup > 0:
                        power += buffitem.pup
                        battlebed.add_field(name=f"{buffitem.name}", value=f"{buffitem.effect}")
                    if turns in [1, 2]:
                        if buffitem.tag == 601:
                            rnum = randint(0, 100)
                            if rnum >= 25 and rnum <= 30:
                                battlebed.add_field(name=buffitem.name, value=buffitem.effect)
                                power = 99999999999999999
                                temp = await self.getmain(attacker)
                                temp.curbuff = None
                                temp.bdur = 0
            
            try:
                if defender.cursuf > 0:
                    todeal = 5/100 * defender.health
                    defender.attack(todeal)
                    battlebed.add_field(name=attacker.ability.usename, value=attacker.ability.effect)
                    defender.cursuf -= 1
                if defender.cursuf == 0:
                    del defender.cursuf
            
            except AttributeError:
                pass

            if attacker.hasPassive():
                if attacker.passive.tag == 8001:
                    attacker.dmgdone = power
                    battlebed.add_field(name=attacker.passive.usename, value="Damage done has been Noted")
                    try:
                        if attacker.dmgtaken > attacker.dmgdone:
                            power += attacker.dmgtaken - attacker.dmgdone
                            battlebed.add_field(name=attacker.passive.usename, value=attacker.passive.effect)
                    except AttributeError:
                        pass

                if attacker.passive.tag == 9102:
                    value = attacker.maxdmg - attacker.mindmg
                    if value > 6000: value = 6000
                    power += value
                    battlebed.add_field(name=attacker.passive.usename, value=f"{attacker.passive.effect} {value}")

            if power >= 7000:
                if defender.hasPassive():
                    if defender.passive.tag == 8002:
                        power -= 0.30 * power
                        battlebed.add_field(name=defender.passive.usename, value=defender.passive.effect)
            
            if attacker.weapon.tag == 1606:
                num = randint(1, 100)
                if num in range(20, 40):
                    power += 0.10 * power
                    battlebed.add_field(name=attacker.weapon.name, value=f"Cursed flames increase damage by 10% dealing {power} damage")

            if defender.hasActive():
                if defender.ability.tag == 9003:
                    num = random.choice([1, 2, 3, 0, 0, 6])
                    power = await self.dicing(attacker, defender, power, battlebed, num)


            defender.attack(power)

            if defender.hasPassive():
                if defender.passive.tag == 8001:
                    defender.dmgtaken = power
                    battlebed.add_field(name=defender.passive.name, value="Your damage has been noted")

            if power >= 1:
                if attacker.weapon.islifesteal():
                    x = math.floor((attacker.weapon.lifesteal / 100) * power)
                    attacker.heal(x)
                    battlebed.add_field(name=f"{attacker.weapon.name}", value=f"heals {attacker.name} for {x} hp")

            await botmsg.add_reaction(random.choice(emojiz))

            battlebed.add_field(name="Notif:", value= f"{attacker.name} {attacker.attackmsg} {defender.name} for {power} damage", inline=False)
            battlebed.add_field(name=f"{attacker.name}:", value=f"Health: {attacker.health}", inline=False)
            battlebed.add_field(name=f"{defender.name}:", value=f"Health: {defender.health}", inline=False)

            if psn:
                psndmg = 100
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

            if defender.typeobj == "player":
                if turns in [1, 2] and defender.health <= 0:
                    if defender.hasbuff():
                        if defender.curbuff == 401:
                            buffitem = await self.getbuff(defender.curbuff)
                            battlebed.add_field(name=buffitem.name, value=buffitem.effect)
                            defender.health = 100
                            temp = await self.getmain(defender)
                            temp.curbuff = None
                            temp.bdur = 0

            if defender.hasActive():
                if defender.ability.tag == 9002:
                    if defender.health >= 1000 and defender.health <= 0:
                        battlebed.add_field(name=defender.ability.usename, value=defender.ability.effect)
                        defender.health = 8000
                        defender.mindmg -= 0.40 * defender.mindmg
                        defender.maxdmg -= 0.40 * defender.maxdmg

            if defender.health <= 0:
                fighting = False
                if len(battlebed) >= 1024:
                    await ctx.send("Fight Log was too long")
                else:
                    await ctx.send(embed=battlebed)
                break

            if defender.hasPassive():
                if defender.passive.tag == 7002:
                    await self.cancounter(defender, attacker, power, battlebed)
            
            if attacker.hasPassive():
                if attacker.passive.tag == 7003:
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
                await battle.edit(embed=battlebed)
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
            rnum = randint(0, 100)
            if rnum in [5, 45, 68]:
                umain = await self.getmain(attacker)
                if len(umain.inventory) < 25:
                    umain.inventory.append(999)
                    await ctx.send("You have received Kevin's Secret Candy from your battle")

        if attacker.typeobj == "player" and defender.typeobj == "player":
            attacker = await self.getmain(attacker)
            defender = await self.getmain(defender)
            try:
                coin = randint(math.floor(defender.pcoin / 10), math.floor(defender.pcoin / 3))
            except ValueError:
                coin = 100
                await ctx.send(f"{defender.name} is a bit poor... so just take this 100 coins")
            await ctx.send(f"{attacker.name}: You have received {coin} Parade Coins from {defender.name}")
            attacker.addcoin(coin)
            defender.takecoin(coin)

        if attacker.typeobj == "player" and defender.typeobj == "npc":
            attacker = await self.getmain(attacker)
            if defender.mincoin > defender.maxcoin:
                defender.mincoin, defender.maxcoin = defender.maxcoin, defender.mincoin
            coin = randint(defender.mincoin, defender.maxcoin)

            if attacker.hasbuff():
                buffitem = await self.getbuff(attacker.curbuff)
                if buffitem.tag == 501:
                    coin *= 1.5
                    await ctx.send(f"{buffitem.name}: {buffitem.effect}")

            # coin *= 2

            attacker.addcoin(round(coin))
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

    @commands.command(brief="Shows the first 25 people to have reached Tier 6", help="USe this to view the first 25 members who have reached Tier 6")
    async def gods(self, ctx):
        embed = discord.Embed(
            title="First 25 Tier 6 gods",
            color=randint(0, 0xffffff)
        )

        warriors = [warrior for warrior in self.users if warrior.getTier() == 6]

        for warrior in warriors[:25]:
            embed.add_field(name=f"{warrior.name}", value=f"Level: {warrior.level}")

        embed.description=f"Number of Tier 6 gods are {len(warriors)}"

        await ctx.send(embed=embed)

    @commands.command(brief="Starts a Tier 6 raid", help="Can be used by members who are Tier 6 or who have been reborn at least thrice. Cooldown: 10 minutes")
    @commands.cooldown(2, 600, commands.BucketType.guild)
    async def paraid6(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if user.getTier() == 6 or user.reborn > 2:
                await self.paraid(ctx)
            else:
                await ctx.send("You have to be at least tier 6 to use this")
        else:
            await self.denied(ctx.channel, ctx.author)

    @commands.command(brief="Starts a raid", help="Use this to begin a raid in the current channel. Cooldown: 30 minutes")
    @commands.cooldown(1, 1800, commands.BucketType.guild)
    async def paraid(self, ctx):
        if self.raidon or self.raiding:
            await ctx.send("A raid is already in progress")
            return

        if self.aboutupdate:
            await ctx.send("An update is about to begin. So hold your raid until after")
            return

        if ctx.guild == None:
            await ctx.send("You can't use that command here")
            return
                
        user = await self.getmember(ctx.author)
        if user:
            if user.hasreborn() or user.level >= 40 :
                self.raidon = True
                if ctx.guild == self.homeguild:
                    ctx.channel = ctx.guild.get_channel(740764507655110666)
                else:
                    rmention = discord.utils.get(self.homeguild.roles, name="Raider")
                    channel = self.bot.get_channel(740764507655110666)
                    await channel.send(f"Attention {rmention.mention}: {ctx.author.name} from {ctx.guild.name} has started a raid. Come let us raid their raid. We only have 3 minutes")
                
                await ctx.channel.send(f"{ctx.author.name} has started a raid.")
                await self.startRaid(ctx.guild, ctx.channel, user)
            else:
                await ctx.send("You must be at least level 40 to start a raid")

    @commands.command(brief="Toggle your ability to fight/ be fought", help="Don't want to be fought? Toggle it with this. If you are offline, you cannot be fought. For now. Cooldown: 10 minutes")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def togglefight(self, ctx):
        user = await self.getmember(ctx.author)
        if not user:
            await ctx.send("Join us first with <>createprofile")
            return
        
        if user.fightable():
            user.canfight = "False"
            await ctx.send(f"{ctx.author.display_name} can no longer be fought")
            if ctx.guild.id == 739229902921793637:
                role = discord.utils.get(ctx.guild.roles, name="Pacifist")
                await ctx.author.add_roles(role)
        else:
            user.canfight = "True"
            await ctx.send(f"{ctx.author.display_name} is now available for fighting")
            if ctx.guild.id ==739229902921793637:
                role = discord.utils.get(ctx.guild.roles, name="Pacifist")
                await ctx.author.remove_roles(role)
        
        return

    async def getstrongest(self, value, items, botuser):
        canbuy = [item for item in items if item.tierz == botuser.getTier() and botuser.pcoin >= item.cost]
            
        if not canbuy: return None
        else: return canbuy[-1]

    async def upgradegear(self, ctx):
        botuser = await self.getmember(ctx.author)
        for value in ["weapon", "armour"]:
            await ctx.send(f"<>shop {value}")
            await self.shop(ctx, value)
            await asyncio.sleep(2)
            strongest = await self.getstrongest(value, eval(f"{value}list"), botuser)
            if not strongest: await ctx.send("Not enough Parade Coins"); continue
            if strongest.cost < eval(f"botuser.get{value}().cost"): await ctx.send(f"{strongest.name} is weaker than my current {value}"); continue
            await ctx.send(f"<>buy {strongest.name}")
            await self.buy(ctx, arg=strongest.name)


    # Weapon Stuff
    @commands.command(brief="Opens the shop", help="Time to spend your money to get stronger, use this to open your shop", usage="optional[weapons / armour / items]")
    async def shop(self, ctx, arg=None):
        if not arg:
            await ctx.send("Welcome to the shop, Here, you can purchase weapons armours and items. use <>shop weapons/armour/items")
            return
        user = await self.getmember(ctx.author)
        if user:
            if arg.lower() == "armour" or arg.lower() == "armour":
                await self.loadarmour(ctx, user)
                return
            
            if arg.lower() == "weapons" or arg.lower() == "weapon":
                await self.loadweapon(ctx, user)
                return
            
            if arg.lower() == "items":
                await self.loaditems(ctx)
                return

            else:
                await ctx.send(f"{arg} must be weapons, armour or armour or items. not {arg}")
        
        else:
            await ctx.send("You can not view the store without an adventurer's license. Do <>createprofile")

    @commands.command(brief="Shows your gear", help="Shows your current weapon and armour loadout")
    async def gear(self, ctx):
        user = await self.getmember(ctx.author)
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return

        sword, shield = user.getgear()
        if sword.name == "Plague Doctors Scepter":
            sword.damage = math.floor(user.maxdmg * 0.5)

        thing = discord.Embed(
            title=f"Gear for {user.name}",
            color=randint(0, 0xffffff)
        )
        if user.reborn > 0:
            tuser = await self.fightuser(user)
            sword.damage = tuser.weapon.damage
            sword.critplus = tuser.weapon.critplus
            sword.lifesteal = tuser.weapon.lifesteal
            shield.hpup = tuser.armour.hpup
            shield.pup = tuser.armour.pup

        thing.add_field(name=f"Weapon: {sword.name}", value=f"Damage: +{sword.damage}, Critchance: +{sword.critplus}%, Lifesteal: +{sword.lifesteal}",
        inline=False)
        thing.add_field(name=f"Armour: {shield.name}", value=f"Health up: +{shield.hpup}, Power Up: +{shield.pup}")
        if shield.getpair():
            fuser = await self.fightuser(user)
            thing.add_field(name=f"{shield.name} pairs well with {shield.getpair().name}", value=f"{fuser.buff()}", inline=False)
            

        await ctx.send(embed=thing)

    @commands.command(brief="Use this to view an item you find interesting", help="Use this to view detailed information on an item of your choice", usage="optional[name_of_item]")
    async def view(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Enter the name of a weapon, armour, or potion you would like to view"); return
        item = None
        for t in gear:
            if t.name.lower() == arg.lower():
                item = t
        
        if item == None:
            for t in potlist:
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
            weaponbed.add_field(name="Description:", value=f"{item.description}")
            weaponbed.add_field(name="Damage:", value=f"+{item.damage}")
            weaponbed.add_field(name="Crit Chance:", value=f"+{item.critplus}% chance")
            weaponbed.add_field(name="Lifesteal:",value=f"+{item.lifesteal}%")
            weaponbed.add_field(name="Cost:", value=f"{item.cost} Parade Coins")
            weaponbed.add_field(name="Tier:", value=f"{item.tierz}")
            

            msg = await ctx.send(embed=weaponbed)
        
        elif item.typeobj == "Armour":
            armourbed = discord.Embed(
            title="Here is the info you requested",
            color=randint(0, 0xffffff)
            )

            armourbed.add_field(name="Name:", value=f"{item.name}")
            armourbed.add_field(name="Description:", value=f"{item.description}")
            armourbed.add_field(name="Health Up:", value=f"+{item.hpup}")
            armourbed.add_field(name="Max Dmg Up:", value=f"+{item.pup}")
            if item.regen != 0:
                armourbed.add_field(name="Regen Amount:", value=f"{item.regen}%")
            armourbed.add_field(name="Cost:", value=f"{item.cost} Parade Coins")
            armourbed.add_field(name="Tier:", value=f"{item.tierz}")


            msg = await ctx.send(embed=armourbed)

        elif item.typeobj == "item":
            infobed = discord.Embed(
                title="Here is the info you requested",
                color=randint(0, 0xffffff)
            )

            infobed.add_field(name="Name:", value=f"{item.name}")
            infobed.add_field(name="Description:", value=f"{item.description}")
            infobed.add_field(name="ID:", value=f"{item.tag}")
            infobed.add_field(name="Health Up:", value=f"+{item.hup}")
            infobed.add_field(name="Min Dmg Up:", value=f"+{item.minup}")
            infobed.add_field(name="Max Dmg Up:", value=f"+{item.maxup}")
            infobed.add_field(name="Power Up:", value=f"+{item.pup}")
            infobed.add_field(name="Crit Increase:", value=f"+{item.critup}")
            infobed.add_field(name="Cost:", value=f"{item.cost} Parade Coins")
            infobed.add_field(name="Tier:", value=f"{item.tierz}")
            infobed.add_field(name="Duration:", value=f"{item.duration}")

            msg = await ctx.send(embed=infobed)

        else: return
            
        await asyncio.sleep(60)
        await msg.delete()


    @commands.command(brief="Use this to purchase an item of your choice", help="See something you like? Buy it with this command... Once you have the funds >:)",usage="name_of_item")
    async def buy(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("You did not tell me what you wanted to buy")

        user = await self.getmember(ctx.author)
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return

        req = None
        
        for item in lilgear:
            if item.name.lower() == arg.lower():
                req = item
                break
        
        if not req:
            for item in potlist:
                if item.name.lower() == arg.lower():
                    req = item
                    break

        if not req:
            await ctx.send(f"Sorry, I don't have any {arg} in stock") 
            return
        
        
        canget = await self.canbuy(user, req)
        

        await ctx.send(canget)

    # Job
    @commands.command(aliases=["j"], brief="Get a Job.", help="Don't want to fight and risk it all in a battle? Then get a Job. Cooldown: 2 uses every minute")
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def job(self, ctx, isbot=False):
        user = await self.getmember(ctx.author)
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return
        
        tier = user.getTier()

        await self.getjob(ctx.channel, user, tier)

    @commands.command(brief="Sell an item you no longer need", help="Use this to sell an item for some cash back", usage="True [weapon/armour/itemid]")
    async def sell(self, ctx, selly=False, arg=None):
        user = await self.getmember(ctx.author)
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return
        
        if selly == False and arg == None:
            await ctx.send(f"{ctx.author.mention} needs to do '<>sell True' in order to sell an item")
            await self.gear(ctx)
            return

        uwep, uarm = user.getgear()
        if uwep not in weaponlist or uarm not in armourlist:
            await ctx.send("You can not sell a weapon that does not exist in the shop")
            return

        if selly and arg == None:
            await ctx.send(f"Do <>sell True armour/weapon/itemid to sell your armour, weapon or item resepectively")
            return

        if selly:
            if arg.lower() == "armour" or arg.lower() == "armour":
                cost = math.ceil((3/4) * uarm.cost)
                await ctx.send(f"Sold {uarm.name} for {cost} Parade Coins")
                user.addcoin(cost)
                user.armour = 2101

            elif arg.lower() == "weapon":
                cost = math.ceil((3/4) * uwep.cost)
                await ctx.send(f"Sold {uwep.name} for {cost} Parade Coins")
                user.addcoin(cost)
                user.weapon = 1101

            else:
                try:
                    arg = int(arg)
                except ValueError: 
                    pass
                
                if type(arg) == int:
                    tosell = [x for x in user.inventory if x == arg]
                    if not tosell:
                        await ctx.send("You do not have an item matching that id")
                        return
                    else:
                        tosell = tosell[0]
                        buffitem = await self.getbuff(tosell)
                        cost = math.ceil((3/4) * buffitem.cost)
                        user.inventory.remove(tosell)
                        user.addcoin(cost)
                        await ctx.send(f"Sold {buffitem.name} for {cost} Parade coins")

                else:
                    await ctx.send(f"{arg} is neither 'armour', 'armour', 'weapon' or itemid")
                    return

            await ctx.send("Completed")


    @commands.command(brief="Reveals the number of paraders that exist", help="Shows how many other Paraders exist")
    async def paradercount(self, ctx):
        await ctx.send(f"There are currently {len(self.users)} Paraders")   


    @commands.command(brief="For help on tiers", help="Explains how tiers work")
    async def tier(self, ctx):
        user = await self.getmember(ctx.author)
        tierbed = discord.Embed(
            title="Tiers",
            description="Tiers determine the amount of money you will get from a job, which players you can fight, and the difficulty of your quests",
            color=randint(0, 0xffffff)
        )     

        if user:
            tierbed.add_field(name="Tier:", value=f"You are currently Tier {user.getTier()}", inline=False)
        
        tierbed.add_field(name="How they work", 
        value="""Your tier is determined based on your level. Levels 0-50 are Tier 1, 50-100 Tier 2
100-150 Tier3, 150-200 Tier 4, 200-300 Tier5 and level 300+ and 10k+ hp for Tier 6 """)
        tierbed.add_field(name="Weapons and Armour", 
        value="Weapons and Armours also have tiers. Because of this, when you open the shop, you will only see items at your tier and lower. Tier 5's, 6's and reborns get their own unique stores")

        await ctx.send(embed=tierbed)

    @commands.command(brief="FIGHT ME!!", help="Shows all users in your server that are available to be fought")
    async def search(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            usertier = user.getTier()
            fight_users = [await self.getmember(x) for x in ctx.guild.members if await self.getmember(x)]
            sametier = [x for x in fight_users if x.getTier() == usertier]
            canfight = [x.name for x in sametier if x.fightable()]

            fightbed = discord.Embed(
                title=f"Members able to be fought by {ctx.author.display_name}",
                description=f"{', '.join(canfight)}",
                color=randint(0, 0xffffff)
            )

            await ctx.send(embed=fightbed)

        else:
            await ctx.send("You do not have a fight profile. Do <>createprofile")


    # Teams
    @commands.command(brief="Shows teams made in your server", help="Shows the teams that exist in your server.")
    async def teams(self, ctx):
        serverteams = [x for x in self.teamlist if x.guildid == ctx.guild.id]
        if serverteams:
            teambed = discord.Embed(
                title="Team list",
                description=f"List of teams in {ctx.guild}",
                color=randint(0, 0xffffff)
            )

            for item in serverteams:
                leader = self.bot.get_user(item.leaderid)
                teambed.add_field(name=f"{item.name}", value=f"Lead by {leader.name}", inline=False)

            await ctx.send(embed=teambed) 
        else:
            await ctx.send("Your server has no teams currently registered. Make one with <>register {teamname}")

    
    @commands.command(brief="Registers a team", help="Use this to form allies with your fellow paraders. Cooldown: 5 minutes", usage="team_name")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def register(self, ctx, *, teamname):
        user = await self.getmember(ctx.author)
        if user:
            if not user.is_teammate():
                if len(teamname.strip()) <= 2:
                    await ctx.send("You cannot have a team name with less than 3 letters")
                    return

                if " " in teamname:
                    await ctx.send("Your team name cannot contain spaces. Use dashes or underscores instead")
                    return

                if len(teamname) > 20:
                    await ctx.send("Your team name cannot be more than 20 characters")
                    return

                guild_teams = [x for x in self.teamlist if x.guildid == ctx.guild.id]
                if guild_teams == 25:
                    await ctx.send("Your guild already has the max number of teams")
                    return
                curteams = [x for x in guild_teams if x.name.lower() == teamname.lower()]
                
                if not curteams:
                    await ctx.send("Making your team now")
                    nteam = Team(teamname, ctx.guild.id, user.tag, f"*{user.tag}5")
                    self.teamlist.append(nteam)
                    user.inteam = True
                    await ctx.send("Completed. View it with <>myteam")
                    await self.updateteam()
                    return
                else:
                    await ctx.send("There is already a team with this name. Please select a new one")
                    return

            else:
                await ctx.send("You are already part of a team. Please leave this one before creating a new one")
        else:
            await self.denied(ctx.channel, ctx.author)
            return


    @commands.command(aliases=["team"], help="Shows information on the team you are in", brief="View your team")
    async def myteam(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            await self.doublecheck(user)
            if user.is_teammate():
                
                userteam = [x for x in self.teamlist if ctx.author.id in x.teammates or ctx.author.id == x.leaderid]
                userteam = userteam[0]
                teamguild = self.bot.get_guild(userteam.guildid)
                teambed = discord.Embed(
                    title=userteam.name,
                    description=f"Showing team {userteam.name} of {teamguild.name}",
                    color=randint(0, 0xffffff)
                )
                tleader = self.bot.get_user(userteam.leaderid)
                teambed.set_thumbnail(url=tleader.avatar_url)
                tleader = await self.getmember(tleader)
                teambed.add_field(name="Lead by", value=f"{tleader.name}, Tier {tleader.getTier()}")
                teambed.add_field(name="Member Count", value=len(userteam.teammates))
                names = [self.bot.get_user(x).name for x in userteam.teammates]
                if names:
                    teambed.add_field(name="Members", value=', '.join(names), inline=False)

                await ctx.send(embed=teambed)
            else:
                await self.tdeny(ctx)
        else:
            await ctx.send("You do not have an account. Create one with <>createprofile")


    @commands.command(brief="Change your teams base to the current guild", help="Changes your teams home server to the one you are currently in")
    async def rebase(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if user.is_teammate():
                userteam = [x for x in self.teamlist if user.tag == x.leaderid]
                if userteam:
                    userteam = userteam[0]
                    userteam.guildid = ctx.guild.id
                    await ctx.send(f"Successfully changed your base guild to {ctx.guild}")
                else:
                    await ctx.send("You must be team leader to use this command")
                    return
            else:
                await self.tdeny(ctx)
                return
        else:
            await self.denied(ctx.channel, ctx.author)
            return


    inadventure = []
    @commands.command(brief="Take an adventure with your teammates.", help="Use this to go on an adventure with your teammates for scaling rewards. This command can only be done by team leaders")
    async def adventure(self, ctx):
        if self.aboutupdate:
            await ctx.send("Cannot start an adventure now. Going offline soon")
            return
            
        user = await self.getmember(ctx.author)
        if user:
            await self.doublecheck(user)
            if user.is_teammate():
                userteam = [x for x in self.teamlist if user.tag in x.teammates or user.tag == x.leaderid]
                userteam = userteam[0]
                canjoin = [x for x in self.inadventure if x.teamid == userteam.teamid]
                if len(userteam.teammates) < 1:
                    await ctx.send("You need at least 1 other teammate in order to start an adventure")
                    return
                
                if canjoin:
                    canjoin = canjoin[0]
                    if user.tag in canjoin.inadv:
                        await ctx.send("You are already part of this adventure")
                        return

                    canjoin.inadv.append(user.tag)
                    await ctx.send("Joined the adventure. Waiting for it to begin")
                    leader = self.bot.get_user(userteam.leaderid)
                    await leader.send(f"{ctx.author.name} has joined the adventure")
                    return
                else:
                    if user.tag == userteam.leaderid:
                        await ctx.send("Inviting your members")
                        for mate in userteam.teammates:
                            target = self.bot.get_all_members()
                            target = [member for member in target if member.id == mate]
                            target = target[0]
                            if target.status == discord.Status.offline:
                                continue
                            await target.send(f"{user.name} is preparing to go on an adventure. Join with <>adventure")
                        
                        pendingadv = ToAdv(userteam.teamid, True)
                        pendingadv.inadv.append(user.tag)
                        self.inadventure.append(pendingadv)
                        await ctx.send("You have 5 minutes before it begins. Make sure you have at least 1 other member by then")
                        await asyncio.sleep(60 * 5)
                        await self.prepadv(ctx, pendingadv)
                    else:
                        await ctx.send("For now, only the leader can start adventures.")
                        return                   
                    
            else:
                await self.tdeny(ctx)
        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command(brief="Invite someone to your team", help="Invite a member to your team. Can only be done by team leaders", usage="@user")
    async def invite(self, ctx, member: discord.Member):
        user, target = await self.getmember(ctx.author), await self.getmember(member)

        if user and target:
            if target.is_teammate():
                await ctx.send("The person you wish to invite is already in a team")
                return

            if not user.is_teammate():
                await self.tdeny(ctx)
                return

            userteam = [x for x in self.teamlist if ctx.author.id == x.leaderid]

            if not userteam:
                await ctx.send("Only the leader can invite a member to the team")
                return
            
            userteam = userteam[0]

            target.invitation = userteam.teamid
            await ctx.send("Your invitation has been sent")

            await member.send(f"You have been invited to {userteam.name} by {user.name}. Do <>accept {userteam.name} to accept")
        else:
            await ctx.send("Either you or the person you mentioned do not have a profile. Make one with <>createprofile")

    @commands.command(brief="Accept a team invitation", help="Use this to accept an invitation to a team", usage="team_name_that_invited_you")
    async def accept(self, ctx, *, teamname):
        user = await self.getmember(ctx.author)
        if user:
            if user.invitation:
                targetguild = [x for x in self.teamlist if user.invitation == x.teamid]
                targetguild = targetguild[0]
                targetguild.teammates.append(user.tag)
                user.inteam = True
                await ctx.send(f"Joined {targetguild.name}")
                leader = self.bot.get_user(targetguild.leaderid)
                await leader.send(f"{ctx.author.name} has joined your team")
                user.invitation = None
                await self.updateteam()

            else:
                await ctx.send("You have no current invitation")
        else:
            await ctx.send("No. Do <>createprofile")

    @commands.command(brief="Deny a team invitation", help="Use this to decline a team invitation", usage="team_name_that_invited_you")
    async def deny(self, ctx, *, teamname):
        user = await self.getmember(ctx.author)
        if user:
            if user.invitation:
                user.invitation = None
                await ctx.send("You have rejected your invitation")

            else:
                await ctx.send("You have no current invitation")
        else:
            await ctx.send("No. Do <>createprofile")

    @commands.command(brief="Use this to leave your current team", help="Leaves the team that you are currently in. If a leader is the only one remaining and leaves, then the team will be deleted immediately")
    async def leaveteam(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if user.is_teammate():
                userteam = [x for x in self.teamlist if user.tag in x.teammates or user.tag == x.leaderid]

                userteam = userteam[0]

                await ctx.send(f"Leaving {userteam.name}")
                if user.tag == userteam.leaderid:
                    if len(userteam.teammates) == 0:
                        self.teamlist.remove(userteam)
                        await ctx.send("As you are the leader leaving with no one else. Your team has been deleted")
                        
                    else:
                        victim = random.choice(userteam.teammates)
                        userteam.leaderid = victim
                        victimain = self.bot.get_user(victim)
                        await victimain.send(f"You are now the leader of {userteam.name}")
                        await ctx.send("Completed")

                else:
                    userteam.teammates.remove(user.tag)
                    user.inteam = False
                    await ctx.send(f"Successfully left {userteam.name}")

                user.inteam = False
                await self.updateteam()


        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command(brief="Kicks a team member", help="Use this to remove a member from your team", usage="@user True")
    async def kickmember(self, ctx, member: discord.Member, confirm=False):
        user1, user2 = await self.getmember(ctx.author), await self.getmember(member)
        if user1 and user2:
            if user1.is_teammate() and user2.is_teammate():
                userteam = [x for x in self.teamlist if x.leaderid == ctx.author.id]
                if not userteam:
                    await ctx.send("Only the leader can kick someone from a team")
                    return
                else:
                    userteam = userteam[0]
                    if user2.tag not in userteam.teammates:
                        await ctx.send(f"{member.name} is not a part of your team '-'")
                        return
                    
                    else:
                        userteam.teammates.remove(user2.tag)
                        user2.inteam = False
                        await ctx.send(f"Successfully removed {member.name} from {userteam.name}")
                        await self.updateteam()
                        return
            else:
                await ctx.send("You or the person you mentioned is not in a team")
                return
        else:
            await ctx.send("Either you, or the person you mentioned does not have profile. Make one with <>createprofile")

    @commands.command(brief="Switch your gear loadout", help="Use this to switch between your 2 gear loadouts")
    async def switch(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            _, _, s2, ss2 = user.getallgear()
            if user.hasreborn():
                if [s2.tierz == 6, ss2.tierz == 6] and user.getTier() < (6 - user.reborn):
                    await ctx.send(f"You have not yet reached the ability to wield god gear. You must be Tier {6 - user.reborn}")
                    return
                
            user.weapon, user.armour, user.weapon2, user.armour2 = user.weapon2, user.armour2, user.weapon, user.armour
            await ctx.send("Successfully switched your gear")
        else:
            await self.denied(ctx.channel, ctx.author)

    @commands.command(aliases=["i"], brief="Checks your inventory where items are stored", help="Views your inventory where items are stored")
    async def inventory(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if len(user.inventory) == 0:
                await ctx.send("Your inventory is empty. Get stuff with <>shop items")
                return
            if len(user.inventory) >= 1:
                invenbed = discord.Embed(
                    title="Inventory",
                    description=f"Showing inventory for {user.name}",
                    color=randint(0, 0xffffff)
                )

                for item in user.inventory:
                    x = await self.getbuff(item)
                    invenbed.add_field(name=f"{x.name}", value=f"{x.description} ID: {x.tag}\n")

                await ctx.send(embed=invenbed)

        else:
            await self.denied(ctx.channel, ctx.author)

    hasbuff = []

    @commands.command(brief="Uses an item from your inventory", help="Consumes an item from your inventory", usage="item_tag optional[True]")
    async def use(self, ctx, itag=None, confirm=False):
        try:
            itag = int(itag)
        except ValueError:
            await ctx.send("You must tell me the ID of the item you wish to use")
            return
        user = await self.getmember(ctx.author)
        if user:
            if len(user.inventory) == 0:
                await ctx.send("You do not have any items to use")
                return

            if itag is None:
                await ctx.send("You did not tell me the id of the item you wanted")
                return
            
            if not confirm and user.hasbuff():
                await ctx.send(f"This will replace will replace your current buff. Do <>use {itag} True to proceed")
                return

            itemtouse = [x for x in user.inventory if x == itag]

            if itemtouse:
                itemtouse = itemtouse[0]
                itemtouse = await self.getbuff(itemtouse)
                user.inventory.remove(itag)
                if itemtouse.untype == "pot":
                    await ctx.send(f"You drink {itemtouse.name}")
                elif itemtouse.untype == "item":
                    await ctx.send(f"You equip {itemtouse.name}")

                if itag == 999:
                    for _ in range(6):
                        await self.didlevel(user, True)
                    await ctx.send("The secret candy has increased your levels by 5")
                else:
                    user.curbuff = itemtouse.tag
                    user.bdur = itemtouse.duration

            else:
                await ctx.send("You do not have this item in your inventory")
                return
        
        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command(brief="Views your current buff", help="If you have a buff, this command shows it")
    async def buff(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            if user.hasbuff():
                item = await self.getbuff(user.curbuff)
                await ctx.send(f"Your current buff is {item.name} which you have for {user.bdur} more turns")
            else:
                await ctx.send("You do not have a buff")
        else:
            await self.denied(ctx.channel, ctx.author)
            return

    @commands.command(brief='Start once again... but stronger', help="Sends you back to level one with slightly higher stats, and allows you to unlock new abilities and passives", usage="True optional[(In order to reach reborn 5) a_goodbye_message_of_your_choice]")
    async def reborn(self, ctx, confirm=False, x="No"):
        user = await self.getmember(ctx.author)
        if user:
            if user.getTier() == 6:
                if not confirm:
                    await ctx.send("This will send you back to tier 1. Do <>reborn True to confirm")
                    return

                if user.reborn == 4 and x == "No":
                    await ctx.send("Warning. From reborn 5 forward, all enemies will scale based on your stats. And will all have tier 5+ weapons. Therefore, if you haven't already, I strongly recommend purchasing god gear, as you will be able to access it from the start. Do <>reborn True {something of your choice} to continue")
                    return
                
                await ctx.send("Heading back to Tier 1... Best of luck progressing again")
                sword1, shield1, sword2, shield2 = user.getallgear()
                if sword1.tierz == 6:
                    sword1, sword2 = sword2, sword1
                if shield1.tierz == 6:
                    shield1, shield2 = shield2, shield1

                user.rtz()

                await ctx.send("And it was done")
            else:
                await ctx.send("You must be tier 6 to use this")
                return
        else:
            await self.denied(ctx.channel, ctx.author)

    @commands.command(brief="See how much exp is needed to reach a level", help="Curious about how much exp you need to reach a certain level? use this command to view it", usage="level")
    async def expfor(self, ctx, level):
        try:
            level = int(level)
        except ValueError:
            await ctx.send(f"{level} is not a number")
            return False
        user = await self.getmember(ctx.author)
        if user:
            ulevel = await self.getcurxp(user.level, user.curxp)
            tlist = []
            if user.level > level:
                await ctx.send("You have already passed this level")
                return False

            if level in range(0, 600):
                base = 50
                for _x in range(level):
                    tlist.append(base)
                    base += 30

                tlist.pop()

                await ctx.send(f"To reach level {level} you need a total of {sum(tlist) - ulevel} more exp points")
            else:
                await ctx.send("That is out of range")

    @commands.command(brief="Your experience", help="Shows your total accumulated exp points")
    async def exp(self, ctx):
        user = await self.getmember(ctx.author)
        if user:
            curxp = await self.getcurxp(user.level, user.curxp)
            await ctx.send(f"{ctx.author.mention} has a total of {curxp} exp points")
        
        else:
            await self.denied(ctx.channel, ctx.author)

    @commands.command(help="Toggles your raider role. This is the role that will be used to notify you of raids", brief="Toggles your raider role")
    async def raider(self, ctx):
        if ctx.guild == self.homeguild:
            role = discord.utils.get(ctx.guild.roles, name="Raider")
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.send("Removed Raider role")
            else:
                await ctx.author.add_roles(role)
                await ctx.send("You now have Raider role")
        else:
            await ctx.send("This command cannot be used outside of The Parade. Get the link with <>parade")
    
    channeling = []

    @commands.command(brief="Channel for power", help="For those who are reborn 5. Channel for an hour with increased effects. Cooldown: 2 hours")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def rchannel(self, ctx):
        await self.channel(ctx, True)
        
    @commands.command(help="Channel power for 30 minutes. You cannot do quests or fights while channeling. Cooldown: 2 hours", brief="Channel for power.")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def channel(self, ctx, conf=False):
        user = await self.getmember(ctx.author)
        if user:
            if user.reborn < 2:
                await ctx.send("You must be reborn level 2 or higher in order to channel")
                return
            if user.mindmg > 3000 and user.maxdmg > 3000 and user.health > 6000:
                if user.reborn > 4 and not conf:
                    await ctx.send("Channeling above reborn 4 lasts for 1 hour instead of 30 minutes. Do <>rchannel instead")
                    return

                self.channeling.append(user.tag)
                await ctx.send(f"{user.name} has started channeling")

                if user.tag in self.channeling:
                    timer = 0
                    while user.tag in self.channeling:
                        user.mindmg += 15
                        user.maxdmg += 15
                        user.health += 15
                        await asyncio.sleep(60)
                        timer += 1
                        if user.reborn > 2:
                            user.curxp += 10
                        
                        if user.reborn > 3:
                            user.mindmg += 5
                            user.maxdmg += 5
                            user.health += 5
                            user.curxp += 10
                            user.pcoin += 100

                        if user.reborn > 4:
                            user.curxp += 80
                            user.pcoin += 500
                            user.health += 30
                            user.maxdmg += 35
                            user.mindmg += 35

                        if timer == 30 and user.reborn < 5:
                            self.channeling.remove(user.tag)
                            await ctx.send(f"{user.name} has finished channeling")
                            break

                        if timer == 60 and user.reborn >= 5:
                            self.channeling.remove(user.tag)
                            await ctx.send(f"{user.name} has finished channeling")
                            break

            else:
                await ctx.send("Health must be at least 6000 and Mindmg and Maxdmg must be at least 3000 in order to channel")
                return

        else:
            await self.denied(ctx.channel, ctx.author)

    @commands.command(brief="Shows a list of enemies in your tier", help="Shows information on the enemies in your tier that you can fight.")
    async def enemies(self, ctx):
        user = await self.getmember(ctx.author)
        if not user:
            await self.denied(ctx.channel, ctx.author)
            return
        
        else:
            targets = await self.get_enemy(user, False, True)
            embed = discord.Embed(
                title=f"Showing Enemies in Tier {user.getTier()}",
                color=randint(0, 0xffffff)
            )

            for enemy in targets:
                embed.add_field(name=enemy.name, value=f"Health: {enemy.health}\n Min Damage: {enemy.mindmg}\n Max Damage: {enemy.maxdmg}")
            
            await ctx.send(embed=embed)
            

    # Functions

    async def dicing(self, defender, attacker, power, embed, num):
        """Function used with the Dice ability."""
        if num == 0:
            embed.add_field(name=attacker.ability.usename, value=f"{attacker.name} couldn't get a valid dice roll")
        
        elif num == 1:
            embed.add_field(name=attacker.ability.usename, value=f"{attacker.name} rolled a 1... But nothing Happened")

        elif num == 2:
            power /= 2
            power = int(power)
            embed.add_field(name=attacker.ability.usename, value=f"{attacker.name} rolled a 2... Reduced incoming damage by 50%")

        elif num == 3:
            power = 0
            embed.add_field(name=attacker.ability.usename, value=f"{attacker.name} rolled a 3... Dodged all incoming damage")
        
        elif num == 4:
            setattr(defender, "flinch", True)

        elif num == 5:
            power *= 2
            embed.add_field(name=attacker.ability.usename, value=f"{attacker.name} rolled a 5, and doubled their power")
        
        elif num == 6:
            if not attacker.health >= 0.75 * attacker.oghealth:
                attacker.health = 0.75 * attacker.oghealth
                embed.add_field(name=attacker.ability.usename, value=f"{attacker.name} rolled a 6 and healed to 3/4 health")
        return power



    async def fixvalues(self, user):
        """Function which accepts a Fighter or FightMe object, and removes all floating points for their values"""
        user.health = math.ceil(user.health)
        user.mindmg = math.ceil(user.mindmg)
        user.maxdmg = math.ceil(user.maxdmg)
        user.pcoin = math.ceil(user.pcoin)
        user.curxp = math.ceil(user.curxp)

    async def getcurxp(self, level, curxp):
        base = 50
        tlist = []
        for _x in range(level):
            tlist.append(base)
            base += 30

        tlist.pop()

        return math.ceil(sum(tlist) + curxp)


    async def modcheck(self, ctx, target):
        """Function used to check if a user is a moderator of Isaiah Parade, and checks if they are strong enough to receive their gear"""
        if target.tag == 347513030516539393:
                if target.level < 300 and not target.hasreborn():
                    await ctx.send("Hello Trxsh. Reach level 300 to achieve your True Power")
                else:
                    if not target.armour == 4603 and not target.armour2 == 4603:
                        target.weapon2 = 3603
                        target.armour2 = 4603
                    if target.passive != 8001:
                        target.passive = 8001 
                        await ctx.send("Now... Embrace your true power")
       
        elif target.tag == 527111518479712256:
                if target.level < 300 and not target.hasreborn():
                    await ctx.send("Congratulations on being the first non-mod to reach Tier 5. Now just reach Tier 6 >:).")
                else:
                    if not target.weapon == 3604 and not target.weapon2 == 3604:
                        await ctx.send("So back into power I see CelestialG")
                        target.weapon2 = 3604
                        target.armour2 = 4604

        elif target.tag == 493839592835907594:
            if not target.hasreborn() and target.getTier() != 6:
                await ctx.send("Reach Tier 6 for your mod gear")
            else:
                if not target.weapon == 3602 and not target.weapon2 == 3602:
                    await ctx.send("Welcome my Parade Creator")
                    target.weapon2 = 3602
                    target.armour2 = 4601

        elif target.tag == 302071862769221635:
            if not target.hasreborn() and target.getTier() != 6 :
                await ctx.send("Reach Tier 6 for your God Gear")
            else:
                if not target.weapon == 3605 and not target.weapon2 == 3605:
                    await ctx.send("Well Biggums. Let's get Bigger")
                    target.weapon2 = 3605
                    target.armour2 = 4605
                    target.ability = "Mass increase"
                    target.passive = "Belly Protection"       


    async def buffuse(self, user):
        item = await self.getbuff(user.curbuff)
        user.health += item.hup
        user.mindmg += item.minup
        user.maxdmg += item.maxup
        user.critchance += item.critup

        msg = item.effect

        return msg

    async def getbuff(self, idtoget):
        item = [x for x in allpotlist if x.tag == idtoget]
        return item[0]
    
    async def tdeny(self, ctx):
        await ctx.send("You are not part of a team.\
            Do <>teams to see available ones and ask to be invited, or do <>register {teamname} to make your own")

    async def doublecheck(self, user):
        userteam = [x for x in self.teamlist if user.tag in x.teammates or user.tag == x.leaderid]
        if userteam:
            user.inteam = True
        else:
            user.inteam = False


    async def startRaid(self, guild=None, channel=None, user=None):

        if guild == None and channel == None:
            guild = self.bot.get_guild(739229902921793637)
            channel = guild.get_channel(740764507655110666)
        
        guild2 = self.bot.get_guild(739229902921793637)
        
        channel2 = self.homeguild.get_channel(740764507655110666)
        
        currole = discord.utils.get(guild.roles, name="Parader")
        if channel == channel2:
            currole = discord.utils.get(guild.roles, name="Raider")
            await channel.send(f"Attention {currole.mention}. A Raid Boss is on it's way to you. Join the raid with <>raid. We have 3 minutes until it starts")
        else:
            await channel.send(f"Attention {currole.name}. A Raid Boss is on it's way to you. Join the raid with <>raid. We have 3 minutes until it starts")

        await asyncio.sleep(150)
        await channel.send("We have info on the beast. 30 seconds remain")
        if channel != channel2:
            currole2 = discord.utils.get(guild2.roles, name="Raider")
            await channel2.send(f"{currole2.name} 30 Seconds remain and we have our info")
        
        await self.spawnraid(user)
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
                if player.weapon.name == "Plague Doctors Scepter":
                    player.weapon.damage = math.floor(player.maxdmg * 0.5)

            if self.raidbeast.weapon.name == "Plague Doctors Scepter":
                self.raidbeast.weapon.damage = math.floor(self.raidbeast.maxdmg * 0.5)
            
            self.raidbeast.oghealth = self.raidbeast.health
            await self.raidStart(channel)
        
        else:
            await channel.send("Not enough members for the Assault... The giant beast turned around and vanished... We need at least 1 brave hero")
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
            if person.hasActive():
                person.ability.reset()
        # Checking for Armour Weapon Pairs
            if person.armour.getpair():
                if person.weapon.name == person.armour.pairs.name:
                    msg = person.buff()
                    await channel.send(f"Set Bonus {msg}")
                    await asyncio.sleep(2)
            if person.hasbuff():
                main1 = await self.getmain(person)
                main1.bdur -= 1
                msg = await self.buffuse(person)
                    
                await channel.send(f"{person.name}: {msg}")

                if person.bdur <= 0:
                    person.bdur = 0
                    await channel.send("Your buff has expired")
                    main1.curbuff = None
                else:
                    await channel.send(f"You have {main1.bdur} fights remaining with this buff")

        if self.raidbeast.hasActive():
            self.raidbeast.ability.reset()

        if self.raidbeast.armour.getpair():
            if self.raidbeast.weapon.name == self.raidbeast.armour.pairs.name:
                msg = self.raidbeast.buff()
                await channel.send(f"Set Bonus {msg}")
                await asyncio.sleep(2)
        
        if self.raidbeast.weapon.tag == 3601:
            self.raidbeast.weapon.damage = 0.5 * self.raidbeast.maxdmg

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
                if player.hasbuff():
                    buffitem = await self.getbuff(player.curbuff)
                    if buffitem.tag == 501:
                        coin *= 1.5
                        await channel.send(f"{buffitem.name}: {buffitem.effect}")
                # coin *= 2
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


    async def spawnraid(self, user):
        if not user or user.getTier() < 6:
            rbeast = random.choice(raidingmonster)
        
        elif user.getTier() == 6:
            strong = [beast for beast in raidingmonster if beast.level >= 800]
            rbeast = random.choice(strong)
        else: return
        
        rbeast = FightingBeast(rbeast.name, rbeast.health, rbeast.mindmg, rbeast.maxdmg, 
        rbeast.mincoin, rbeast.maxcoin, rbeast.entrymessage, rbeast.minxp, rbeast.critchance, rbeast.healchance,
        rbeast.ability, rbeast.passive, rbeast.attackmsg, rbeast.weapon, rbeast.armour, rbeast.level, rbeast.tier,
        rbeast.reborn, rbeast.typeobj)
        
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
        cts = None
        for player in self.raiders:
            raidbed = discord.Embed(
            title=f"Raid battle against {self.raidbeast.name}",
            color=randint(0, 0xffffff)
        )

            power = player.maxdmg
            if self.raidbeast.hasPassive():
                if self.raidbeast.passive.tag == 7006:
                    raidbed.add_field(name=f"{self.raidbeast.name}", value=f"attacks first because of speed boost")
                    await self.turngo2(channel)
                    self.raidbeast.passive = None

            
            if player.hasPassive():
                if player.health <= (player.oghealth / 3):
                    if player.passive.tag == 7004:
                        player.passuse(0)
                        raidbed.add_field(name=f"{player.name}", value=f"{player.passive.usename}: {player.passive.effect}")

                if player.passive.tag == 7010:
                    if player.armour.name == "Haki":
                        if player.armour.getpair():
                            if player.weapon.name == player.armour.pairs.name:
                                power = await self.cantruehaki(self.raidbeast, player, power, raidbed)
                        
                    elif player.weapon.name == "Conqueror Haki":
                        power = await self.canhaki(self.raidbeast, player, power, raidbed)
                    
                    else:
                        pass

                if player.passive.name == "Pride of Balance":
                    if player.armour.getpair():
                        if player.armour.name == "Yang":
                            power = await self.canbalance(self.raidbeast, player, power, raidbed)

                if player.passive.tag == 9101:
                    tob = 0.02 + (player.reborn / 100)
                    player.mindmg += math.ceil(tob * player.mindmg)     
                    player.maxdmg += math.ceil(tob * player.maxdmg)
                    player.health += math.ceil(tob * player.health)
                    raidbed.add_field(name=f"{player.name}: {player.passive.usename}", value=f"{player.passive.effect} by {tob * 100}%")
        
            critnum = randint(0, 100)
            healnum = randint(0, 100)

            if self.rslagged == True:
                power *= 1.5
                raidbed.add_field(name=f"Slag is in effect", value=f"{self.raidbeast.name} takes 1.5x dmg because of slag ")


            power += player.weapon.damage

            if player.hasActive():
                if player.ability.name == "Slag":
                    num = randint(1,6)
                    if num == 3:
                        self.rslagged = True
                        self.raidbeast.slag = 2
                        raidbed.add_field(name=f"{player.ability.usename}", value=f"{self.raidbeast.name} {player.ability.effect} {self.raidbeast.slag} turns")
                else:
                    power, abiltag = await self.useability(self.raidbeast, player, power, raidbed)
                    if abiltag == 5001:
                        self.rts = True
                    if abiltag == "Celestial's Za Warudo":
                        self.rts = True
                        cts = True
                    if abiltag == 6001:
                            self.rpsned.append(self.raidbeast)
                            self.rpsn = True
                            self.rpsndmg = 100

                    if abiltag == 9001:
                        extradmg = 60
                        extrahp = 300
                        for _ in range(player.reborn): extradmg += 20
                        for _ in range(player.reborn): extrahp += 50

                        player.mindmg += extradmg
                        player.maxdmg += extradmg
                        player.health += extrahp
                        raidbed.add_field(name=player.ability.usename, value=f"Increased Min and Max damage by {extradmg} and health by {extrahp}")


            if player.hasPassive():
                if player.passive.tag == 7005:
                    power = await self.cansharpeye(self.raidbeast, player, power, raidbed)

                if player.passive.tag == 9102:
                    value = player.maxdmg - player.mindmg
                    power += value
                    raidbed.add_field(name=player.passive.usename, value=f"{player.passive.effect} {value}")

            if self.rts or hasattr(self.raidbeast, "flinch"):
                self.raidbeast.attack(power)
                power = player.maxdmg
                critnum = randint(0, 100)
                healnum = randint(0, 100)

                power += player.weapon.damage
                
                if hasattr(self.raidbeast, "flinch"):
                    player.ability.effect = f"Caused {self.raidbeast.name} to flinch"
                    delattr(self.raidbeast, "flinch")

                raidbed.add_field(name=player.ability.usename, value=player.ability.effect)
                if cts:
                    self.raidbeast.attack(power)
                    raidbed.add_field(name=player.ability.usename, value=player.ability.effect)
                    power = player.maxdmg
                    critnum = randint(0, 100)
                    healnum = randint(0, 100)

                    power += player.weapon.damage
                    cts = False
                self.rts = False

            if power >= 1:
                if player.weapon.islifesteal():
                    x = math.floor((player.weapon.lifesteal / 100) * power)
                    player.heal(x)
                    raidbed.add_field(name=f"{player.weapon.name}", value=f"heals {player.name} for {x} hp")
            

            if critnum > 0 and critnum <= player.critchance:
                raidbed.add_field(inline=False,name="Critical Hit", value=f"{player.name} got a crit")
                power *= 1.5
                if self.raidbeast.hasPassive():
                    if self.raidbeast.passive.tag == 7007:
                        power = await self.cancritblock(self.raidbeast, player, power, raidbed)

            if healnum > 0 and healnum <= player.healchance:
                healin = randint(10, 20)
                raidbed.add_field(inline=False,name="Self Heal", value=f"{player.name} heals {healin} hp")
                player.heal(healin)

            if self.raidbeast.hasPassive():
                if self.raidbeast.passive.tag == 7008:
                    power -= 50
                    raidbed.add_field(inline=False,name=f"{self.raidbeast.passive.usename}", value=f"{self.raidbeast.passive.effect}")

                if self.raidbeast.passive.tag == 7001:
                    power = await self.candodge(self.raidbeast, player, power, raidbed)
            
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
                if self.raidbeast.passive.tag == 7002:
                    await self.cancounter(self.raidbeast, player, power, raidbed)
                
                if self.raidbeast.passive.tag == 7003:
                    await self.canregen(self.raidbeast, raidbed)
            
            if player.hasPassive():
                if player.passive.tag == 7003:
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
                power, abiltag = await self.useability(target, self.raidbeast, power, raidbed)
                if abiltag in ["Stop Time", "Celestial's ZA WARUDO"]:
                    self.rts = True
                if abiltag == 6001:
                    self.rpsned.append(target)
                    self.rpsn = True
                    self.rpsndmg = 100

                if abiltag == 9001:
                    extradmg = 300
                    extrahp = 100

                    self.raidbeast.mindmg += extradmg
                    self.raidbeast.maxdmg += extradmg
                    self.raidbeast.health += extrahp
                    raidbed.add_field(name=self.raidbeast.ability.usename, value=f"Increased Min and Max damage by {extradmg} and health by {extrahp}")


        if self.rts:
            target.attack(power)
            power = randint(self.raidbeast.mindmg, self.raidbeast.maxdmg)
            critnum = randint(0, 100)
            healnum = randint(0, 100)

            power += self.raidbeast.weapon.damage

            self.rts = False

        if self.raidbeast.hasPassive():
            if self.raidbeast.passive.tag == 7004:
                if self.raidbeast.health <= 500:
                    self.raidbeast.passuse(0)
                    raidbed.add_field(name=f"{self.raidbeast.name}", value=f"{self.raidbeast.passive.usename}: {self.raidbeast.passive.effect}")
            
            if self.raidbeast.passive.tag == 7010:
                if self.raidbeast.armour.name == "Haki":
                    if self.raidbeast.armour.getpair():
                        if self.raidbeast.weapon.name == self.raidbeast.armour.pairs.name:
                            power = await self.cantruehaki(target, self.raidbeast, power, raidbed)
                        
                elif self.raidbeast.weapon.name == "Conqueror Haki":
                    power = await self.canhaki(target, self.raidbeast, power, raidbed)
                    
                else:
                    pass

                if self.raidbeast.passive.name == "Pride of Balance":
                    if self.raidbeast.armour.getpair():
                        if self.raidbeast.armour.name == "Yang":
                            power = await self.canbalance(target, self.raidbeast, power, raidbed)

        if critnum > 0 and critnum <= self.raidbeast.critchance:
            raidbed.add_field(inline=False,name="Critical Hit", value=f"{self.raidbeast.name} got a crit")
            power *= 1.5
            if target.hasPassive():
                    if target.passive.tag == 7007:
                        power = await self.cancritblock(target, self.raidbeast, power, raidbed)

        if healnum > 0 and healnum <= self.raidbeast.healchance:
            healin = randint(10, 20)
            raidbed.add_field(inline=False,name="Self Heal", value=f"{self.raidbeast.name} heals {healin} hp")
            self.raidbeast.heal(healin)

        if target.hasPassive():
            if target.passive.tag == 7001:
                power = await self.candodge(target, self.raidbeast, power, raidbed)
            if target.passive.tag == 7008:
                power -= 50
                raidbed.add_field(inline=False,name=f"{target.passive.usename}", value=f"{target.passive.effect}")

            if target.passive.tag == 9101:
                tob = 0.02 + (target.reborn / 100)
                target.mindmg += math.ceil(tob * target.mindmg)     
                target.maxdmg += math.ceil(tob * target.maxdmg)
                target.health += math.ceil(tob * target.health)
                raidbed.add_field(name=f"{target.name}: {target.passive.usename}", value=f"{target.passive.effect} by {tob * 100}%")
            
            if power >= 10000:
                if target.hasPassive():
                    if target.passive.tag == 8002:
                        power -= 0.30 * power
                        raidbed.add_field(name=f"{target.name}: {target.passive.usename}", value=target.passive.effect)
        
        power = math.floor(power)
       
        target.attack(power)
        if target.health <= 0:
            await channel.send(f"{target.name} has been slain")
            self.raiders.remove(target)

        if target.hasPassive():
            if target.passive.tag == 7002:
                await self.cancounter(target, self.raidbeast, power, raidbed)
                
            if self.raidbeast.health <= 0:
                return
                
            if target.passive.tag == 7003:
                await self.canregen(target, raidbed)

            raidbed.add_field(inline=False,name="Notif:", value= f"{self.raidbeast.name} {self.raidbeast.attackmsg} {target.name} for {power} damage")
            raidbed.add_field(inline=False,name=f"{self.raidbeast.name}:", value=f"Health: {self.raidbeast.health}")
            raidbed.add_field(inline=False,name=f"{target.name}:", value=f"Health: {target.health}")
            await self.rembed(raidbed, channel)

            

            await asyncio.sleep(3)
        if self.raidbeast.hasPassive():
            if self.raidbeast.passive.tag == 7003:
                await self.canregen(self.raidbeast, raidbed)

        
    async def getmember(self, member):
        """Function which accepts a guild member as an argument, and searches the list of registered fighters, and returns their Fighter Instance if it exists"""
        for user in self.users:
            if user.tag == member.id:
                return user

        return None

    async def denied(self, chan, person):
        """Function which accepts a channel and member object, and is called when a given member does not have a fight profile."""
        await chan.send(f"{person.mention}, or the person you @mentioned does not have a profile. Create one with <>createprofile")

    async def expgain(self, winner, loser):
        """Function called to reward exp after a battle. Is called when the winner is a player. Accepts 2 fighter objects, or a Fighter and a Beast"""
        winner = await self.getmain(winner)
        if loser.typeobj == "npc":
            exp = randint(loser.minxp, loser.maxxp)
        else:
            exp = loser.xpthresh / 3
        
        if winner.hasbuff():
            if winner.curbuff == 402:
                exp += 0.20 * exp

        # exp *= 2
        
        winner.curxp += math.floor(exp)
        
        winner.wins += 1

        levelup = await self.didlevel(winner)

        if levelup:
            return True
        if winner.hasbuff():
            if winner.curbuff == 402:
                irl = await self.getirl(winner)
                return f"{irl.mention} has gained an increased {exp} exp points from defeating {loser.name}"

        irl = await self.getirl(winner)
        return f"{irl.mention} has gained {exp} exp points from defeating {loser.name}"    

    async def getirl(self, user):
        everyone = self.bot.get_all_members()
        person = [x for x in everyone if x.id == user.tag]
        person = person[0]
        return person


    async def didlevel(self, x, val=False):
        if x.curxp >= x.xpthresh:
            while x.curxp >= x.xpthresh:
                x.curxp -= x.xpthresh
                await self.leveling(x)
            
            return True

        elif val:
            await self.leveling(x)

        else:
            return False

    async def leveling(self, x):
        x.xpthresh += 30
        x.level += 1
        x.health += randint(3, 8)
        x.mindmg += randint(1, 4)
        x.maxdmg += randint(3, 8)
        if x.hasreborn():
            x.addcoin(x.level * 50)

        if x.getTier() == 1:
            x.addcoin(20 * x.level)
        elif x.getTier() == 2:
            x.addcoin(50 * x.level)
        elif x.getTier() == 3:
            x.addcoin(70 * x.level)
        elif x.getTier() == 4:
            x.addcoin(120 * x.level)
        elif x.getTier() == 5:
            x.addcoin(150 * x.level)
        else:
            x.addcoin(300 * x.level)

    async def lost(self, arg):
        if arg in enemy:
            return
        arg.losses += 1

    async def get_enemy(self, user, q6, checkin=False):
        yes = []

        for vanillian in enemy:
            if not q6:
                if vanillian.tier == user.getTier(): yes.append(vanillian)
            else:
                if user.getTier() == 6 and user.reborn >= 3:
                    if vanillian.tier == 6: yes.append(vanillian)

                elif user.getTier() < 6:
                    if vanillian.tier >= 4: yes.append(vanillian)
                else:
                    if vanillian.tier >= 5: yes.append(vanillian)

        if checkin: return yes

        villain = random.choice(yes)

        if user.reborn >= 5:
            villain = await self.getmirror(user)

        villain = FightingBeast(villain.name, villain.health, villain.mindmg, villain.maxdmg, 
        villain.mincoin, villain.maxcoin, villain.entrymessage, villain.minxp, villain.critchance, villain.healchance,
        villain.ability, villain.passive, villain.attackmsg, villain.weapon, villain.armour, villain.level, villain.tier,
        villain.reborn, villain.typeobj)
        
        return villain

    async def getmirror(self, user):
        name = f"{user.name}'s Dark Copy"
        health = await self.vary(max(user.mindmg, user.health, user.maxdmg))
        mindmg = await self.vary(user.mindmg)
        maxdmg = await self.vary(user.maxdmg)
        mincoin = await self.vary(40000)
        maxcoin = await self.vary(80000)
        entrymessage = "Your Dark Copy Has Arrived"
        minxp = int(user.xpthresh / 4)
        critchance = user.critchance
        healchance = user.healchance
        ability = random.choice(allabilities)
        passive = random.choice(allpassives)
        weapons = [x for x in allweapons if x.tierz >= 5]
        armours = [x for x in allarmour if x.tierz >= 5]
        weapon = random.choice(weapons)
        armour = random.choice(armours)
        attackmsg = weapon.effect
        level = await self.vary(user.level)
        tier = user.getTier()
        try:
            reborn = int(user.reborn)
        except ValueError:
            reborn = 5
        
        villain = BeastFight(name, health, mindmg, maxdmg, mincoin, maxcoin, entrymessage, minxp,
        critchance, healchance, ability, passive, attackmsg, weapon, armour, level, tier, reborn)

        return villain

    async def vary(self, value):
        num = randint(10, 50)
        pon = randint(1, 2)
        if pon == 1:
            value -= num
        else:
            value += num

        return value

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

    
    async def botquest(self, ctx, member: discord.Member):
        embed = discord.Embed(
                title="Time for quest",
                description="Isaiah's Parade sets out on a quest",
                color=randint(0, 0xffffff)
            )

        await ctx.send("<>quest")
        await ctx.send(embed=embed)
        self.inquest.append(member.id)
        await self.fight(ctx, member, True, True)


    async def rembed(self, embed, channel):
        channel2 = self.bot.get_channel(740764507655110666)
        if channel == channel2:
            await channel.send(embed=embed)
        else:
            await channel.send(embed=embed)
            await channel2.send(embed=embed)


    # Adventure
    async def prepadv(self, ctx, squad):
        if len(squad.inadv) > 1:
            await self.teammsg(squad, "Member requirement has been met. Setting out for adventure now")
            squad.pending = False
            await self.startadv(squad)
        else:
            await ctx.send("Not enough Members to start an adventure")
            self.inadventure.remove(squad)
            return

    async def startadv(self, squad):
        timetocomplete = randint(1, 5)
        await self.teammsg(squad, f"Seems like adventure will take around {timetocomplete} minutes to complete")
        await asyncio.sleep(timetocomplete * 60)
        suceeded = randint(1, 10)
        end = 4
        for person in squad.inadv:
            end += 1
        if end > 9:
            end = 9
        if suceeded >= 1 and suceeded <= end:
            await self.teammsg(squad, "Congratulationsss, You have passed. You will now receive your rewards")
            for person in squad.inadv:
                nperson = self.bot.get_user(person)
                uperson = await self.getmember(nperson)
                xptoget, cashtoget = await self.advreward(uperson)
                uperson.curxp += xptoget
                uperson.pcoin += cashtoget
                await nperson.send(f"You have received {xptoget} xp and {cashtoget} parade coins")
        else:
            await self.teammsg(squad, "You have failed the adventure")

        self.inadventure.remove(squad)

    async def teammsg(self, team, msg):
        for user in team.inadv:
            target = self.bot.get_user(user)
            await target.send(f"{msg}")
            

    async def advreward(self, toreward):
        rewardxp = (toreward.xpthresh / 5)
        rewardcash = (toreward.pcoin / 10)
        return rewardxp, rewardcash

    # Isaiah

    @commands.command(hidden=True)
    @commands.is_owner()
    async def terrorize(self, ctx, member: discord.Member):
        while True:
            await self.botquest(ctx, member)
            ctx.author = self.bot.user
            await self.job(ctx, True)
            await self.job(ctx, True)
            await asyncio.sleep(5)
            await self.upgradebot(ctx)
            await self.upgradegear(ctx)
            await asyncio.sleep(6 * 60)


    @tasks.loop(minutes=5)
    async def update_fighters(self):
        if not self.users: return
        async with connect(db_name) as db:
            [await fightdb.insert_or_replace(db, user) for user in self.users]
        

    # async def updateteam(self):
    #     if not self.teamlist: return
    #     await Saving().save("teamdata", self.teamlist)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def createbot(self, ctx):
        iparade = self.bot.user
        ParadeMaster = Fighter(iparade.display_name, iparade.id, 0, 0, 200, 12, 30, 0, 0, 60)
        self.users.append(ParadeMaster)
        await ctx.send(f"Successfully Created Profile for {iparade.display_name}")


    async def useability(self, defender, attacker, power, embed):
        if attacker.ability.tag == 9003:
            num = random.choice([1, 0, 0, 4, 5, 6])
            power = await self.dicing(defender, attacker, power, embed, num)
            return power, 9003

        if not attacker.ability.oncd():
            if attacker.ability.tag == 5012:
                num = randint(1,6)
                if num == 3:
                    defender.slag = 2
                    embed.add_field(name=f"{attacker.ability.usename}", value=f"{defender.name} {attacker.ability.effect} {defender.slag} turns")
                    return power, attacker.ability.tag
                return power, 6969

            else:
                useabil = randint(0, 100)
                if useabil >= 25 and useabil <= 50:
                    if attacker.ability.tag == 9002:
                        return power, None
                    power = attacker.abiluse(power)
                    if attacker.ability.name == "The Plague":
                        defender.ptime = 3
                    if attacker.ability.name == "Suffocation":
                        defender.sufturn = 4
                    embed.add_field(name=f"{attacker.ability.usename}", value=f"{attacker.name} {attacker.ability.effect} {defender.name} for {power} damage",inline=False)
                    attacker.ability.cdreduce()
                    return power, attacker.ability.tag
 
        else:
            attacker.ability.cdreduce()
            embed.add_field(name="Ability Failed", value=f"{attacker.name} tried to use their ability. But it's on Cooldown", inline=False)
            if attacker.ability.tempcd == 0:
                attacker.ability.reset()

        return power, None
        
    async def canhaki(self, defender, attacker, power, embed):
        attacker.mindmg += 20
        attacker.maxdmg += 20
        embed.add_field(name=f"{attacker.passive.usename}:", value=f"{attacker.name} {attacker.passive.effect}")
        return power

    async def cantruehaki(self, defender, attacker, power, embed):
        attacker.mindmg += 30
        attacker.maxdmg += 30
        embed.add_field(name=f"{attacker.passive.usename}:", value=f"{attacker.name} {attacker.passive.effect}")
        if defender.level <= attacker.level - 30:
            defender.health -= 100
            embed.add_field(name=f"{attacker.passive.usename}:", value=f"{defender.name} lost 100 health to {attacker.passive.name}")
        
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

    async def fightuser(self, account:Fighter):
        """Function which accepts a Fighter class, and converts it to a FightMe class."""
        person = FightMe(*tuple(account.__dict__.values()))
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
        

    async def loadarmour(self, ctx, user):
        armourbed = discord.Embed(
            title="Welcome to my Armour Store",
            description="To buy an item, use <>buy {item name}, or use <>view {item name} for details",
            color=randint(0, 0xffffff)
        )

        if user.getTier() == 5:
            for item in armourlist:
                if item.tierz >= 4:
                    armourbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")  

        elif user.getTier() == 6:
            for item in armourlist:
                if item.tierz >= 6:
                    armourbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")           

        else:
            for item in armourlist:
                if item.tierz <= user.getTier():
                    armourbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")            
        
        await ctx.send(embed=armourbed)



    async def loadweapon(self, ctx, user):
        weaponbed = discord.Embed(
            title="Welcome to my Weapon Store",
            description="To buy an item, use <>buy {item name}, or use <>view {item name} for details",
            color=randint(0, 0xffffff)
        )

        if user.getTier() == 5:
            for item in weaponlist:
                if item.tierz >= 4:
                    weaponbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")
        
        elif user.getTier() == 6:
            for item in weaponlist:
                if item.tierz >= 6:
                    weaponbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")

        else:
            for item in weaponlist:
                if item.tierz <= user.getTier():
                    weaponbed.add_field(name=f"Name: {item.name}", value=f"Cost: {item.cost} Parade Coins")

        await ctx.send(embed=weaponbed)

    async def loaditems(self, ctx):
        itembed = discord.Embed(
            title="Welcome to the item store",
            description="To buy an item, use <>buy {itemname} or use <>view {itemname} for details",
            color=randint(0, 0xffffff)
        )
        
        for valuable in potlist:
            itembed.add_field(name=f"{valuable.name}", value=f"{valuable.description} \nCost: {valuable.cost}\nTier:{valuable.tierz}")
                
        await ctx.send(embed=itembed)

    
    async def canbuy(self, user, arg):
        if user.weapon == arg.tag or user.armour == arg.tag:
            msg = "You already have this equipped"
            return msg

        if user.getTier() < arg.tierz:
            return "You are too weak to wield this item"

        if arg.tierz == 6 and arg.typeobj.lower() != "item":
            _,_f, sword2, shield2 = user.getallgear()
            if arg.typeobj.lower() == "weapon":
                if sword2.tierz == 6:
                    return "You already have a Tier 6 weapon"

            if arg.typeobj.lower() == "armour":
                if shield2.tierz == 6:
                    return "You already have Tier 6 Armour"
            
        if user.pcoin >= arg.cost:
            if arg.typeobj.lower() == "weapon":
                user.weapon = arg.tag
            elif arg.typeobj.lower() == "armour":
                user.armour = arg.tag
            
            elif arg.typeobj.lower() == "item":
                if len(user.inventory) == 25:
                    return "Your inventory is full, therefore you cannot buy this item"
                else:
                    user.inventory.append(arg.tag)

            user.pcoin -= arg.cost            

            msg = f"Successfully bought {arg.name}"

            return msg
        
        return f"Now that won't do. You don't have enough Parade Coins to buy {arg.name}"


    async def getjob(self, channel, user, tier):
        jobbed = discord.Embed(
            title=f'Tier {tier} job:',
            color=randint(0, 0xffffff)
        )
        jobdesc = random.choice(eval(f"jobs.jtier{tier}"))
        if tier == 1:
            reward = randint(30, 70)
            loss = randint(5, 15)
            
        elif tier == 2:
            reward = randint(120, 170)
            loss = randint(30, 50)
            
        elif tier == 3:
            reward = randint(2000, 2300)  
            loss = randint(80, 160)
            
        elif tier == 4:
            reward = randint(10000, 15000)
            loss = randint(1000, 1450)

        elif tier == 5:
            reward = randint(30000, 40000)
            loss = randint(3600, 4000)

        elif tier == 6:
            await channel.send("You no longer take jobs")
            return
            
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
                user.addcoin(reward)
        else:
            jobbed.add_field(name="How unfortunate", value=f"You had to pay {loss} parade coins for your failure")
            jobbed.add_field(name="Sigh", value=f"{random.choice(jobs.badresp)}")
            user.takecoin(loss)

    async def setup_fighters(self):
        """Function which turns all tuples from the db into Fighter instances"""
        self.users = [Fighter(*user) for user in self.users]


    @commands.command(hidden=True)
    @commands.is_owner()
    async def botrestart(self, ctx):
        await ctx.message.delete()
        self.aboutupdate = True

        await asyncio.sleep(5)

        counter = 0

        while len(self.infight) > 0 or len(self.raiders) > 0 or len(self.inquest) > 0 or len(self.inadventure) > 0:
            counter += 1
            await asyncio.sleep(15)

        async with connect(db_name) as db:
            [await fightdb.insert_or_replace(db, user) for user in self.users]
        
        await ctx.send("Restarting bot")

        await asyncio.sleep(3)
        raise SystemExit     

    @commands.Cog.listener()
    async def on_disconnect(self):
        await asyncio.sleep(2)
        async with connect(db_name) as db:
            [await fightdb.insert_or_replace(db, user) for user in self.users]
        
        
def setup(bot):
    bot.add_cog(Fight(bot))