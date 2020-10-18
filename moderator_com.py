import discord
from discord.ext import commands
import asyncio
import random
from random import randint
import typing
import math
import os
import json
import traceback


class Tracking:
    def __init__(self, guildid, msg=None):
        self.guildid=guildid
        self.msg=msg


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    jltracking = []
    if os.path.exists("jltracking.json"):
        with open("jltracking.json") as tjl:
            ttrack = json.load(tjl)

        for server in ttrack:
            server = Tracking(server["guildid"], server["msg"])
            jltracking.append(server)

    # Admin's Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def relax(self, ctx):
        guild = ctx.guild
        new_role = await guild.create_role(name="The Silent Ones")

        overwrite = discord.PermissionOverwrite(send_messages=False)

        await ctx.channel.set_permissions(new_role, overwrite=overwrite)

        overcheck = ctx.channel.overwrites_for(new_role)

        overcheck.update(send_messages=False)
        
        for member in guild.members:
            await member.add_roles(new_role)

        await ctx.send("You need to relax")
        await asyncio.sleep(5)
        await ctx.send("Continue")
        for role in guild.roles:
            if role.name == "The Silent Ones":
                await role.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def killerqueen(self, ctx, member: discord.Member, minutes: int=2):
        user_role = []
        for role in member.roles:
            user_role.append(role)
        user_role = user_role[1:]
        for role in user_role:
            await member.remove_roles(role)
        
        killer = discord.Embed(
            title="KIRU KUIN",
            description="BAITSA DASUTO",
            color=randint(0, 0xffffff)
        )

        killer.set_thumbnail(url=ctx.author.avatar_url)
        killer.set_image(url="https://media.tenor.co/images/a3d5892f2e8074c0f4631e457c7c534b/tenor.gif")

        await ctx.send(embed=killer)

        await asyncio.sleep(minutes * 60)

        reverse = discord.Embed(
            title="Kotoamtsukami",
            description="You slowly return... but good?",
            color=randint(0, 0xffffff)
        )

        reverse.set_thumbnail(url=ctx.author.avatar_url)
        reverse.set_image(url="https://pa1.narvii.com/6477/edfa062f367af4201c7f40637f97a72b013799e6_hq.gif")

        for role in user_role:
            await member.add_roles(role)
            await ctx.send(embed=reverse)
            await asyncio.sleep(120)


    # Bans
    @commands.command(aliases=["ban"])
    @commands.has_permissions(ban_members=True)
    async def shadowrealm(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(
            title="It's Time",
            description="I Summon Exodia in Attack Mode...",
            color=randint(0, 0xffffff)
        )
        embed.add_field(name="EXODIA... OBLITERATE!",
                        value=f'I, {ctx.author.display_name}, herby ban you to the shadow realm {member.mention}!')
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await member.ban(reason=reason)


    @commands.command(aliases=["unban"])
    @commands.has_permissions(ban_members=True)
    async def impactrevive(self, ctx, user: int, reason=None):
        user = await self.bot.fetch_user(user)
        await ctx.guild.unban(user, reason=reason)
        embed = discord.Embed(
            title='Tsk...',
            color=randint(0, 0xffffff)
        )

        embed.add_field(name='I guess you are back', value=f"So you managed to escape {user.mention}!")
        await ctx.send(embed=embed)


    # Delete Messages
    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def zahando(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await asyncio.sleep(0.5)
        file=discord.File("./images/zahando.gif", filename="zahando.gif")

        deleted = discord.Embed(
            title="Messages Cleared",
            color=randint(0, 0xffffff)
        )
        
        deleted.set_image(url="attachment://zahando.gif")
        
        thing = await ctx.send(file=file, embed=deleted)
        await asyncio.sleep(4)
        await thing.delete()


    # Target messages with a certain word
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def wipehas(self, ctx, amount: typing.Optional[int] = 100, *, args):
        counter = 0
        
        args = f"{args}"

        for message in await ctx.channel.history().flatten():
            if counter <= amount:
                if args.lower() in message.content.lower():
                    await message.delete()
                    counter += 1

        await ctx.send("Moderated")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def wipeendswith(self, ctx, amount: typing.Optional[int] = 100, *, args):
        counter = 0
        
        args = f"{args}"

        for message in await ctx.channel.history().flatten():
            if counter <= amount:
                if message.content.lower().endswith(args.lower()):
                    await message.delete()
                    counter += 1

        await ctx.send("Moderated")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def wipestartswith(self, ctx, amount: typing.Optional[int] = 100, *, args):
        counter = 0
        
        args = f"{args}"

        for message in await ctx.channel.history().flatten():
            if counter <= amount:
                if message.content.lower().startswith(args.lower()):
                    await message.delete()
                    counter += 1

        await ctx.send("Moderated")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def kingcrimson(self, ctx, member: discord.Member, amount: int):
        # def checking(m):
        #    return m.author == member
        # await ctx.channel.purge(limit=arg, check=checking)
        file = discord.File("./images/kc.gif", filename="kc.gif")
        counter = 0
        for m in await ctx.channel.history().flatten():
            if counter < amount:
                if m.author == member:
                    await m.delete()
                    counter += 1
        embed = discord.Embed(
            title="KING CRIMSON NO NOURYOKU",
            description=f'''**It is only the results that remain in this world!
    All the actions you take in a world where time is erased are meaningless!**
    ***{member.mention} is now free of {amount} crimes***''',
            color=randint(0, 0xffffff)
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(url="attachment://kc.gif")

        await ctx.send(file=file, embed=embed)


    # Enables Slowmode
    @commands.command(aliases=["slow"])
    @commands.has_permissions(manage_channels=True)
    async def freeze3(self, ctx, second: int):
        file = discord.File("./images/3_freeze.gif", filename="3_freeze.gif")
        embed = discord.Embed(
            title="3 FREEZE",
            description=f"Messages have been slowed down to {second} second intervals",
            color=randint(0, 0xffffff)
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(url="attachment://3_freeze.gif")

        await ctx.send(file=file, embed=embed)
        await ctx.channel.edit(slowmode_delay=second)


    # Overwrites channel permissions to stop @everyone from talking in chat
    @commands.command(aliases=["shhh"])
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def zawarudo(self, ctx, seconds: int=10):
        guild = ctx.guild

        role = discord.utils.get(guild.roles, name="The Silent Ones")

        for member in guild.members: await member.add_roles(role)

        file = discord.File("./images/zawarudo.gif", filename="zawarudo.gif")
        embed = discord.Embed(
            title="ZA... WARUDO!",
            description=f"""TOKI WO TOMARE!! 
    (Channel frozen) for {seconds} seconds""",
            color=randint(0, 0xffffff)
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(url="attachment://zawarudo.gif")

        await ctx.send(file=file, embed=embed)

        await asyncio.sleep(seconds)
        await ctx.send("*Jikan desu... (Channel unfrozen)*")

        for member in guild.members: await member.remove_roles(role)


    # Reverses zawarudo and 3freeze
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def ger(self, ctx):
        file = discord.File("./images/goldenexp.gif")

        embed = discord.Embed(
            title="GOLDEN EXPERIENCE REQUIEM",
            description="""You will never arrive at the reality that will occur! None who stand before me 
            shall ever do so, no matter what abilities they may wield!""",
            color=randint(0, 0xffffff)
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(url="attachment://goldenexp.gif")
        await ctx.send(file=file, embed=embed)
        await ctx.channel.edit(slowmode_delay=0)
        role = discord.utils.get(ctx.guild.roles, name="The Silent Ones")
        for member in ctx.guild.members: 
            if role in member.roles:
                await member.remove_roles(role)


    # Kicks a user
    @commands.command(aliases=["kick"])
    @commands.has_permissions(kick_members=True)
    async def deathnote(self, ctx, member: discord.Member):
        await ctx.send(content="***You're name has been written in my notebook... Now you have 5 seconds left...***",
        file=discord.File("./images/deathnote.gif"))
        await asyncio.sleep(1)
        await ctx.send(f"***It is done... goodbye {member.mention}. You were pathetic compared to L***")
        await asyncio.sleep(5)
        await member.kick()

    # Removes all roles permanately
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def ger_rtz(self, ctx, member: discord.Member):
        user_role = []
        for role in member.roles:
            user_role.append(role)
        user_role = user_role[1:]
        for role in user_role:
            await member.remove_roles(role)

        await ctx.send(f"{member.display_name} has had their roles permanately stripped")

    @commands.command()
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time=5, *, reason="They should know"):
        guild = ctx.guild

        role = discord.utils.get(guild.roles, name="The Silent Ones")
        if role == None:
            await ctx.send("Could not get role 'The Silent Ones'. Create it and do <>silentnow")
            return
        
        await member.add_roles(role)
        mutebed = discord.Embed(
            title="Muted",
            description=f"{member.mention} has been muted for {time} minutes. Reason: {reason}",
            color=randint(0, 0xffffff)
        )
        mutebed.set_thumbnail(url=ctx.author.avatar_url)
        mutebed.set_image(url="https://i.pinimg.com/originals/9a/72/9f/9a729f73546829f2e361087032dda1ba.gif")

        await ctx.send(embed=mutebed)
        await asyncio.sleep(time * 60)
        
        await ctx.send(f"{member.mention}. You have been Unmuted. Do your best to not have to be muted again")
        await member.remove_roles(role)

    @commands.command()
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def silentnow(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="The Silent Ones")
        if not role: await ctx.send("Role does 'The Silent Ones' does not exist"); return

        for channel in ctx.guild.text_channels:
            overwrites = {role: discord.PermissionOverwrite(send_messages=False)}
            await channel.edit(overwrites=overwrites)

    @commands.command()
    @commands.is_owner()
    async def rnotif(self, ctx, *, msg):
        for server in self.bot.guilds:
            role = discord.utils.get(server.roles, name="Parader")
            channel = discord.utils.get(server.text_channels, name="parade-room")
            if role == None or channel == None:
                continue
            await channel.send(f"Attention {role.mention}. {msg}")

        await ctx.send("Notified")

    @commands.command()
    @commands.has_permissions(view_audit_log=True)
    async def relog(self, ctx, amount=5):
        channel = discord.utils.get(ctx.guild.text_channels, name="logs")
        if channel == None:
            channel = await ctx.guild.create_text_channel("logs")
            await channel.send("An error occured and could not set channel perms. Please change them as you see fit")

        async for entry in ctx.guild.audit_logs(limit=amount):
            logbed = discord.Embed(
                title=f"Log Entry",
                description=f"{entry.action.name}: Done by {entry.user}\nTime: {entry.created_at.strftime('%b %a %H %M')}",
                color=randint(0, 0xffffff)
            )
            
            await channel.send(embed=logbed)

    tlist = []

    if len(jltracking) > 0:
        tlist = [gid.guildid for gid in jltracking]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def trackjoins(self, ctx, *, msg=None):

        if msg:
            if ctx.guild.id in self.tlist:
                toobj = await self.getguildobj(ctx.guild.id)
                toobj.msg = msg
                await ctx.send("Updated your guild message")

        if not msg:
            msg = f"Welcome to {ctx.guild.name}. I hope you enjoy your time here"


        if ctx.guild.id in self.tlist:
            toobj = await self.getguildobj(ctx.guild.id)
            self.jltracking.remove(toobj)
            self.tlist.remove(ctx.guild.id)
            await ctx.send("I will no longer track Joins and leaves from this server")
        else:
            tobj = Tracking(ctx.guild.id, msg)
            self.jltracking.append(tobj)
            self.tlist.append(ctx.guild.id)
            await ctx.send("I will be tracking joins and leaves from this server. If you so desire, you can add on a custom message using <>trackjoins message")

        await self.save()
    # Events

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        if member.guild.id == 722201014127820850:
            channel= discord.utils.get(member.guild.text_channels, name="parade-room")

            await channel.send(f"Welcome to {member.guild.name} {member.mention}... We look forward to having you serve in our domain :smiling_imp:")
            await channel.send("Please keep in mind that you only have 2 minutes here")
            await asyncio.sleep(120)
            await member.kick()
    
        elif member.guild.id == 739229902921793637:
            channel = member.guild.get_channel(739255078229377054)
            await channel.send(f"Welcome to {member.guild.name} {member.mention}... We look forward to having you serve in our domain :smiling_imp:. If you already have a profile. Do <>readd")
            role = discord.utils.get(member.guild.roles, name="Follower")

            await member.add_roles(role)

        elif member.guild.id in self.tlist:
            channel= discord.utils.get(member.guild.text_channels, name="welcome")
            if not channel:
                channel = discord.utils.get(member.guild.text_channels, name="parade-room")
                if not channel:
                    channel = await member.guild.create_text_channel("parade-room")
            else:
                channel = member.guild.system_channel

            ts = await self.getguildobj(member.guild.id)
            await channel.send(f"{member.mention} {ts.msg}")
                
    # On leaving
    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        if member.guild.id == 733822954034561065:
            return False
        elif member.guild.id == 739229902921793637:
            channel = member.guild.get_channel(739255078229377054)
        else:
            return

        await channel.send(f"I hope {member.mention} doesn't think that they will be missed. They made their choice")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # get data from exception
        etype = type(error)
        trace = error.__traceback__

        # the verbosity is how large of a traceback to make
        # more specifically, it's the amount of levels up the traceback goes from the exception source
        verbosity = 10

        # 'traceback' is the stdlib module, `import traceback`.
        lines = traceback.format_exception(etype, error, trace, verbosity)

        # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
        traceback_text = ''.join(lines)

        # now we can send it to the user
        # it would probably be best to wrap this in a codeblock via e.g. a Paginator
        print(traceback_text)

        if isinstance(error, commands.CommandOnCooldown):

            await ctx.send(f"You are on Cooldown for {math.floor(error.retry_after)} seconds")

        elif isinstance(error, commands.MissingPermissions):
            
            await ctx.send(error)
        
        elif isinstance(error, commands.CommandNotFound):
            
            await ctx.send(error)

        elif isinstance(error, commands.NotOwner):
            
            await ctx.send(error)

        elif isinstance(error, commands.MissingRequiredArgument):
            
            await ctx.send(error)     

        elif isinstance(error, commands.BadArgument):

            await ctx.send(error)    

        else:
            channel = self.bot.get_channel(740337325971603537)
            await channel.send(f"{ctx.author.name}: {error}")
            print(error)

    # Functions
    async def getguildobj(self, gid):
        for dic in self.jltracking:
            if dic.guildid == gid:
                return dic

    async def save(self):
        todump = []
        for thing in self.jltracking:
            todump.append(thing.__dict__)

        with open("jltracking.json", "w") as f:
            json.dump(todump, f, indent=4)


class ProfanFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    noprofane = []

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def profane(self, ctx):
        if ctx.guild not in self.noprofane:
            self.noprofane.append(ctx.guild)
            await ctx.send("Profanity is being moderated")
        else:
            self.noprofane.remove(ctx.guild)
            await ctx.send("Profanity is no longer being moderated")
    
    badword = ["fuck", "shit", "bitch", "cum", "nigger"]

    async def regulate(self, msg):
        msg = msg.replace("fuck", "fack")
        msg = msg.replace("shit", "shiz")
        msg = msg.replace("bitch", "beech")
        msg = msg.replace("cum ", "excrete my sexual fluid")
        msg = msg.replace("nigger", "handsome black person")
        return msg
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.guild not in self.noprofane:
            return
        else:
            for sword in self.badword:
                if sword in message.content.lower():
                    newmsg = await self.regulate(message.content.lower())
                    await message.channel.send(f"{message.author.display_name}: {newmsg}")
                    await message.delete()
                    return        

def setup(bot):
    bot.add_cog(Moderator(bot))
    bot.add_cog(ProfanFilter(bot))
