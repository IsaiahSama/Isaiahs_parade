import discord
from discord.ext import commands
import asyncio
import random
from random import randint


class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    isaiah = 493839592835907594
    # Guild list
    list_guild = []
    guild_members = []
    roles_guild = []
    guild_channels = []
    guild_channels_id = []
    curguild = None


    # Other
    target = None

    # Unique Commands
    # My commands
    @commands.command()
    @commands.is_owner()
    async def notif(self, ctx, *, text):
        for server in self.bot.guilds:
            channel = discord.utils.get(server.text_channels, name="parade-room")
            if channel == None:
                await server.create_text_channel("parade-room")
                for tchan in server.text_channels:
                    if tchan.name.lower() == "parade-room":
                        await tchan.send("Successfully Created")

                channel = discord.utils.get(server.text_channels, name="parade-room")  
            
            await channel.send(f"Notification: {text}")


    @commands.command()
    @commands.is_owner()
    async def updatelog(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title="Update Log",
            description="List of updates since last bot Restart",
            color=randint(0, 0xffffff)
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Battle", value="Changes", inline=False)
        embed.add_field(name="<>readd", value="Can now be used to remove the parader role from yourself", inline=False)
        embed.add_field(name="Moderator", value="Addition", inline=False)
        embed.add_field(name="<>profane", value="enables and disables the profanity filter for a guild")
        
        for server in self.bot.guilds:
            channel = discord.utils.get(server.text_channels, name="parade-room")
            if channel == None:
                await server.create_text_channel("parade-room")
                for tchan in server.text_channels:
                    if tchan.name.lower() == "parade-room":
                        await tchan.send("Successfully Created")

                channel = discord.utils.get(server.text_channels, name="parade-room")
            
            if server.id == 739229902921793637:
                channel = server.get_channel(739576238712160329)
            
            await channel.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx):
        for server in self.bot.guilds:
            channel = discord.utils.get(server.text_channels, name="parade-room")
            role = discord.utils.get(server.roles, name="Parader")
            if role == None:
                await channel.send("Heading off for an update in 1 minute")
            else:
                await channel.send(f"Hello there my lovely {role.mention}. Heading offline for updates in 1 minute")

        await asyncio.sleep(40)
        for server in self.bot.guilds:
            channel = discord.utils.get(server.text_channels, name="parade-room")
            await channel.send("20 seconds remain")
        await asyncio.sleep(19)
        for server in self.bot.guilds:
            channel = discord.utils.get(server.text_channels, name="parade-room")
            await channel.send("Bye Bye")
        
        await asyncio.sleep(5)
        exit()

    # Del mistake
    @commands.command()
    @commands.is_owner()
    async def delmistake(self, ctx, guildid:int,chanid:int, arg:int):
        if guildid == 0 and chanid == 0:
            for server in self.bot.guilds:
                for chan in server.text_channels:
                    counter = 0
                    if "parade-room" in chan.name:
                        for m in await chan.history().flatten():
                            if counter < arg:
                                if m.author == self.bot.user:
                                    await m.delete()
                                    counter += 1
        else:
            guild = self.bot.get_guild(guildid)
            channel = guild.get_channel(chanid)
            counter = 0
            for m in await channel.history().flatten():
                if counter < arg:
                    if m.author == self.bot.user:
                        await m.delete()
                        counter += 1

        await ctx.send("Yes")

    # Fact of the day
    @commands.command()
    @commands.is_owner()
    async def fotd(self, ctx, *,fact):
        await ctx.message.delete()
        for server in self.bot.guilds:
            if server.id == 469273564034498580:
                channel = server.get_channel(691991741896720474)
                await channel.send(f"Today's fact is: {fact}")

            if server.id == 739229902921793637:
                channel = server.get_channel(739266507090952282)
                await channel.send(f"Today's fact is: {fact}")
            
            channel = discord.utils.get(server.text_channels, name="parade-room")
            if channel == None:
                await server.create_text_channel("parade-room")
                for tchan in server.text_channels:
                    if tchan.name.lower() == "parade-room":
                        await tchan.send("Successfully Created")

                channel = discord.utils.get(server.text_channels, name="parade-room")                  
                        
            await channel.send(f"Today's fact is: {fact}")



    # Gets all servers bots are in
    @commands.command()
    @commands.is_owner()
    async def observer(self, ctx):
        self.list_guild.clear()
        introfile = discord.File("images/isaiah.gif", filename="isaiah.gif")
        intro = discord.Embed(
            title="Hacking into Database",
            description="Getting my Information",
            color=randint(0, 0xffffff)
        )

        intro.set_thumbnail(url=self.bot.user.avatar_url)
        intro.set_image(url="attachment://isaiah.gif")

        await ctx.send(file=introfile, embed=intro)

        await asyncio.sleep(5)

        await ctx.send("Almost done")

        await asyncio.sleep(4)

        await ctx.send("Done... Loading")

        await asyncio.sleep(2)
        guild_index = 0
        for guild in self.bot.guilds:
            self.list_guild.append(guild)
            guild_roles = [str(role) for role in guild.roles]
            guild_roles = guild_roles[1:]
            guild_roles = ", ".join(guild_roles)
            embed = discord.Embed(
                title="Guild Info",
                description="Info on Guilds relating to self.isaiah's Parade",
                color=randint(0, 0xffffff)
            )

            embed.set_thumbnail(url=guild.icon_url)
            embed.add_field(name="Guild Id:", value=f"{guild.id}")
            embed.add_field(name="Guild Number", value=f"{guild_index}")
            embed.add_field(name="Guild Name", value=guild.name)
            embed.add_field(name="Guild Owner", value=guild.owner)
            embed.add_field(name="Member Count", value=guild.member_count)
            embed.add_field(name="Guild Roles", value=guild_roles)
            embed.add_field(name="Date Created", value=guild.created_at.strftime("%d/%m/%y"))

            await ctx.send(embed=embed)
            guild_index += 1

        await ctx.send("```Moderated```")


    # GEt all members from a guild
    @commands.command()
    @commands.is_owner()
    async def byakugan(self, ctx, gindex: int):
        self.guild_members.clear()
        guild = self.list_guild[gindex]
        member_index = 0
        for member in guild.members:
            self.guild_members.append(member)
            user_roles = [str(role) for role in member.roles]
            user_roles = user_roles[1:]
            user_roles = ", ".join(user_roles)
            if member.activity is None:
                actividad = "None"
            else:
                actividad = member.activity.name
            memberembed = discord.Embed(
                title=f"{member}",
                description="My byakugan has seen their information",
                color=randint(0, 0xffffff)
            )
            memberembed.set_thumbnail(url=member.avatar_url)
            memberembed.set_image(url="attachment://hd1.gif")
            memberembed.add_field(name='User Number:', value=f"{member_index}")
            memberembed.add_field(name='Display Name:', value=f"{member.display_name}")
            memberembed.add_field(name='Current Activity:', value=f"{actividad}")
            memberembed.add_field(name='Current Status:', value=f"{member.status}")
            memberembed.add_field(name='On Mobile:', value=f"{member.is_on_mobile()}")
            memberembed.add_field(name='Date Joined Server:', value=f'{member.joined_at.strftime("%d/%m/%y")}')
            memberembed.add_field(name='Date Account Created:', value=f'{member.created_at.strftime("%d/%m/%y")}')
            memberembed.add_field(name='Highest Role:', value=f"{member.top_role}")
            memberembed.add_field(name='Roles:', value=f"{user_roles}")
            try:
                await ctx.send(embed=memberembed)
                member_index += 1
            except:
                member_index += 1
        await ctx.send("```Moderated```")


    # Get a Specific member
    # Maybe sometime in the future

    # Role Check Testing
    @commands.command()
    @commands.is_owner()
    async def rolecheck(self, ctx, gindex: int):
        guild = self.list_guild[gindex]
        self.roles_guild.clear()
        role_count = 0
        for role in guild.roles:
            self.roles_guild.append(role)
            idrole = role.id
            namerole = role.name

            therole = discord.Embed(
                title=f"Information on roles of {guild}",
                description="Found them",
                color=randint(0, 0xffffff)
            )

            therole.set_thumbnail(url=ctx.author.avatar_url)
            therole.add_field(name="Role Count:", value=f"{role_count}")
            therole.add_field(name="Role Name:", value=f"{namerole}")
            therole.add_field(name="Role Id:", value=f"{idrole}")

            await ctx.send(embed=therole)
            role_count += 1
        await ctx.send("```Moderated```")

    #  Channel view
    @commands.command()
    @commands.is_owner()
    async def csteal(self, ctx, gindex: int):
        global curguild
        self.guild_channels.clear()
        self.guild_channels_id.clear()
        curguild = self.list_guild[gindex]
        i = 0

        for channel in curguild.text_channels:
            self.guild_channels.append(channel)
            chanembed = discord.Embed(
                title=f"Channel of {curguild}",
                description="Here are the channels",
                color=randint(0, 0xffffff)
            )

            chanembed.set_thumbnail(url=curguild.icon_url)
            chanembed.add_field(name=f"{i}", value=f"{channel}")
            i += 1
            
            await ctx.send(embed=chanembed)

        await ctx.send("Moderated")

    @commands.command()
    @commands.is_owner()
    async def rolecreateparade(self, ctx):
        for server in self.bot.guilds:
            for role in server.roles:
                if role.name == "Parader":
                    await role.delete()

        await asyncio.sleep(10)

        for server in self.bot.guilds:
            await server.create_role(name="Parader")
            await ctx.send(f"Created Parader in {server.name}")

        await ctx.send("Completed")


    # Damani's Command
    @commands.command()
    async def stfu(self, ctx, member: discord.Member):
        guild = ctx.guild
        file = discord.File("images/damani.gif", filename="damani.gif")
        embed = discord.Embed(
            title=f"Silence {member.display_name}",
            description="Retard...",
            color=randint(0, 0xffffff)
        )

        if ctx.author.id == 347513030516539393:
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_image(url="attachment://damani.gif")
            for role in guild.roles:
                if role.name == "Victim":
                    await member.add_roles(role)
                    await ctx.send(file=file, embed=embed)

            overwrite = discord.PermissionOverwrite(send_messages=False)
            role_name = guild.get_role(721798925002080378)
            for channel in guild.text_channels:
                await channel.set_permissions(role_name, overwrite=overwrite)

            await asyncio.sleep(9)
            await ctx.send("Did you enjoy your break?")
            await member.remove_roles(role_name)
        elif ctx.author.id == self.isaiah:
            await ctx.send("Not even you can use this command my Creator")
        else:
            await ctx.send(f"Did you seriously think you could use this command? {ctx.author.mention}")


    # Adjes Command
    @commands.command()
    async def failure(self, ctx, member: discord.Member):
        if ctx.author.id == 315619611724742656:
            if ctx.author.guild_permissions.manage_roles:
                user_role = []
                for role in member.roles:
                    user_role.append(role)
                user_role = user_role[1:]
                for role in user_role:
                    await member.remove_roles(role)

                file=discord.File("images/adje.gif", filename="adje.gif")

                victim = discord.Embed(
                    title="Allow me to show you how much of a failure you truly are",
                    color=randint(0, 0xffffff)
                )

                victim.set_thumbnail(url=ctx.author.avatar_url)
                victim.set_image(url="attachment://adje.gif")
                
                await ctx.send(file=file, embed=victim)

                await asyncio.sleep(40)
                for role in user_role:
                    await member.add_roles(role)
                await ctx.send("Now you see what I see")
            else:
                target = member
                victim = discord.Embed(
                    title="Allow me to show you how much of a failure you really are...",
                    color=randint(0, 0xffffff)
                )

                victim.set_thumbnail(url=target.avatar_url)
                victim.add_field(name="Ha.", value=f"Look at this fool {target.mention}")
                
                await ctx.send(embed=victim)
        elif ctx.author.id == self.isaiah:
            await ctx.send("Come on my Creator, you are better than that")
        else:
            await ctx.send("This command is not for you human")



def setup(bot):
    bot.add_cog(Special(bot))