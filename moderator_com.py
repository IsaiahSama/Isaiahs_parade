import discord
from discord.ext import commands
import asyncio
import random
from random import randint
import typing
import math


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    @commands.command()
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


    @commands.command()
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
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def zahando(self, ctx, arg: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=arg)
        await asyncio.sleep(0.5)
        file=discord.File("images/zahando.gif", filename="zahando.gif")

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
    async def wipe(self, ctx, amount: typing.Optional[int] = 100, *, args):
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
    async def kingcrimson(self, ctx, member: discord.Member, arg: int):
        # def checking(m):
        #    return m.author == member
        # await ctx.channel.purge(limit=arg, check=checking)
        file = discord.File("images/kc.gif", filename="kc.gif")
        counter = 0
        for m in await ctx.channel.history().flatten():
            if counter < arg:
                if m.author == member:
                    await m.delete()
                    counter += 1
        embed = discord.Embed(
            title="KING CRIMSON NO NOURYOKU",
            description=f'''**It is only the results that remain in this world!
    All the actions you take in a world where time is erased are meaningless!**
    ***{member.mention} is now free of {arg} crimes***''',
            color=randint(0, 0xffffff)
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(url="attachment://kc.gif")

        await ctx.send(file=file, embed=embed)


    # Enables Slowmode
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def freeze3(self, ctx, arg: int):
        file = discord.File("images/3_freeze.gif", filename="3_freeze.gif")
        embed = discord.Embed(
            title="3 FREEZE",
            description=f"Messages have been slowed down to {arg} second intervals",
            color=randint(0, 0xffffff)
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(url="attachment://3_freeze.gif")

        await ctx.send(file=file, embed=embed)
        await ctx.channel.edit(slowmode_delay=arg)


    # Overwrites channel permissions to stop @everyone from talking in chat
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.has_permissions(manage_roles=True)
    async def zawarudo(self, ctx, arg: int=10):
        guild = ctx.guild
        new_role = await guild.create_role(name="The Silent Ones")

        file = discord.File("images/zawarudo.gif", filename="zawarudo.gif")
        embed = discord.Embed(
            title="ZA... WARUDO!",
            description=f"""TOKI WO TOMARE!! 
    (Channel frozen) for {arg} seconds""",
            color=randint(0, 0xffffff)
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(url="attachment://zawarudo.gif")

        silence_member = []
        for member in ctx.guild.members:
            if not member.guild_permissions.manage_channels:
                silence_member.append(member)

        overwrite = discord.PermissionOverwrite(send_messages=False)

        await ctx.channel.set_permissions(new_role, overwrite=overwrite)

        await ctx.send(file=file, embed=embed)

        overcheck = ctx.channel.overwrites_for(new_role)

        overcheck.update(send_messages=False)
        for role in guild.roles:
            if role.name == "The Silent Ones":
                for member in silence_member:
                    try:
                        await member.add_roles(role)
                    except:
                        continue
        await asyncio.sleep(arg)
        await ctx.send("*Jikan desu... (Channel unfrozen)*")
        for role in guild.roles:
            if role.name == "The Silent Ones":
                await role.delete()


    # Reverses zawarudo and 3freeze
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def ger(self, ctx):
        file = discord.File("images/goldenexp.gif")

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
        for role in ctx.guild.roles:
            if role.name == "The Silent Ones":
                await role.delete()


    # Kicks a user
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def deathnote(self, ctx, member: discord.Member):
        await ctx.send("***I've eaten my potato chip... Now you have 60 seconds left...***")
        await ctx.send(file=discord.File("images/deathnote.gif"))
        await asyncio.sleep(30)
        await ctx.send(f"***30 seconds remain {member.mention}***")
        await asyncio.sleep(25)
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

        role = discord.utils.get(guild.roles, name="The Silent One")
        if role == None:
            role = await guild.create_role(name="The Silent One")


        overwrite = discord.PermissionOverwrite(send_messages=False)

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(role, overwrite=overwrite)

            overcheck = channel.overwrites_for(role)

            overcheck.update(send_messages=False)
        
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



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):

            await ctx.send(f"You are on Cooldown for {math.floor(error.retry_after)} seconds")

        if isinstance(error, commands.MissingPermissions):
            
            await ctx.send(error)
        
        if isinstance(error, commands.CommandNotFound):
            
            await ctx.send(error)

        if isinstance(error, commands.NotOwner):
            
            await ctx.send(error)

        else:
            channel = self.bot.get_channel(740337325971603537)
            await channel.send(f"{ctx.author.name}: {error}")
            print(error)
                

def setup(bot):
    bot.add_cog(Moderator(bot))
