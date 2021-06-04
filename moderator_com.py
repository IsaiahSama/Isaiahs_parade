import discord
from discord import utils, Embed
from discord.ext import commands
import asyncio
from random import randint, choice
import typing
import math
import traceback
from copy import copy
from tips import tips

class Moderator(commands.Cog):
    """Commands for all moderators"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = discord.utils.get(guild.text_channels, name="parade-room")
        if not channel:
            await guild.create_text_channel("parade-room")
            channel = discord.utils.get(guild.text_channels, name="parade-room")

        role = discord.utils.get(guild.roles, name="Parader")
        if not role:
            role = await guild.create_role(name="Parader")

        mchan = self.bot.get_channel(740414745252986970)
        await mchan.send(f"I have been invited to {guild.name}. {role.name} and {channel.name} Have been created successfully")
        
        role = discord.utils.get(guild.roles, name="shushed")
        if not role: 
            role = await guild.create_role(name="shushed")
        for channel in guild.text_channels:
            overwrites = channel.overwrites
            overwrites[role] = discord.PermissionOverwrite(send_messages=False)
            await channel.edit(overwrites=overwrites)
            
        joinbed = discord.Embed(
            title="I have Arrived",
            description=f"Thanks for inviting me to {guild.name}. I look forward to spending time with all of you",
            color=randint(0, 0xffffff)
        )

        joinbed.set_thumbnail(url=self.bot.user.avatar_url)
        joinbed.add_field(name="Help", value="You can view everything i'm capable of with <>help")
        joinbed.add_field(name="Main Server", value="Feel free to join my main server. Get the link with <>parade")
        joinbed.add_field(name="Positioning", value="As someone created to Moderate, be sure to give me a role high enough in order for you to use me to my full potential")
        joinbed.add_field(name="Extra", value="I have automatically setup a role called shushed, which is assigned when the <>mute command is used. For setting this role up for newly created channels, use <>silentnow")
        
        await channel.send(embed=joinbed)

    @commands.command(brief="Removes the roles of the mentioned person for x minutes.", help='Removes the roles of a member for x minutes. Returns them one by one', usage="@user duration")
    @commands.has_permissions(administrator=True)
    async def killerqueen(self, ctx, member: discord.Member, minutes: int=2):
        if member.id == 493839592835907594: 
            await ctx.send("Sorry... I can't go against my creator")
            return
        user_roles = [role for role in member.roles if not role == ctx.guild.default_role]
        for role in user_roles:
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

        for role in user_roles:
            await member.add_roles(role)
            await ctx.send(embed=reverse, delete_after=5)
            await asyncio.sleep(120)


    # Bans
    @commands.command(aliases=["ban"], brief='Used to ban a member', help="Bans the mentioned member", usage='@member optional[reason]')
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


    @commands.command(aliases=["unban"], brief="Unbands a user", help="Used to lift the ban on the user.", usage="@user optional[reason]")
    @commands.has_permissions(ban_members=True)
    async def impactrevive(self, ctx, userid: int, reason=None):
        user = await self.bot.fetch_user(userid)
        await ctx.guild.unban(user, reason=reason)
        embed = discord.Embed(
            title='Tsk...',
            color=randint(0, 0xffffff)
        )

        embed.add_field(name='I guess you are back', value=f"So you managed to escape {userid}!")
        await ctx.send(embed=embed)


    # Delete Messages
    @commands.command(aliases=["purge"], brief="Deletes X number of memories", help="Used to delete a specified number of messages", usage='amount_to_delete')
    @commands.has_permissions(manage_messages=True)
    async def zahando(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount, bulk=True)
        await asyncio.sleep(0.5)
        file=discord.File("./images/zahando.gif", filename="zahando.gif")

        deleted = discord.Embed(
            title="Messages Cleared",
            color=randint(0, 0xffffff)
        )
        
        deleted.set_image(url="attachment://zahando.gif")
        
        await ctx.send(file=file, embed=deleted, delete_after=4)


    # Target messages with a certain word
    @commands.command(help='Used to delete x number of messages containing the specified text', brief="Deletes messages containing text that you specify.", usage="amount_to_delete text-to-delete")
    @commands.has_permissions(manage_messages=True)
    async def wipehas(self, ctx, amount: typing.Optional[int] = 100, *, args):
        
        def check(m):
            return args.lower() in m.content.lower()

        await ctx.channel.purge(limit=amount, check=check)
        await ctx.send("Moderated", delete_after=5)


    @commands.command(brief="Deletes messages ending with the text specified", help="Deletes x number of messages ending with the text you specify.", usage="amount text-to-delete")
    @commands.has_permissions(manage_messages=True)
    async def wipeendswith(self, ctx, amount: typing.Optional[int] = 100, *, args):
       
        def check(m):
            return m.content.lower().endswith(args.lower())

        await ctx.channel.purge(limit=amount, check=check)
        await ctx.send("Moderated", delete_after=5)


    @commands.command(brief="Deletes messages starting with the text specified", help="Deletes x number of messages starting with the text you specify.", usage="amount text-to-delete")
    @commands.has_permissions(manage_messages=True)
    async def wipestartswith(self, ctx, amount: typing.Optional[int] = 100, *, args):
        
        def check(m):
            return m.content.lower().startswith(args.lower())
        
        await ctx.channel.purge(limit=amount, check=check)
        await ctx.send("Moderated")


    @commands.command(brief="Deletes messages sent by a user", help="Deletes X number of messages sent by the mentioned user.", usage="@user amount")
    @commands.has_permissions(manage_messages=True)
    async def kingcrimson(self, ctx, member: discord.Member, amount: int):
        
        def check(m):
           return m.author == member
        
        await ctx.channel.purge(limit=amount + 1, check=check)

        file = discord.File("./images/kc.gif", filename="kc.gif")

        embed = discord.Embed(
            title="KING CRIMSON NO NOURYOKU",
            description=f'It is only the results that remain in this world!All the actions you take in a world where time is erased are meaningless!.\n ***{member.mention} is now free of {amount} crimes***',
            color=randint(0, 0xffffff)
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(url="attachment://kc.gif")

        await ctx.send(file=file, embed=embed, delete_after=5)


    # Enables Slowmode
    @commands.command(aliases=["slow"], brief="Applies a slowmode to the current channel", help="Sets a slowmode on the current channel. The interval being the number specified", usage="seconds (set to 0 to disable slowmode)")
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
    @commands.command(aliases=["shhh"], brief="Just do it.")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def zawarudo(self, ctx, seconds: int=10):
        og = ctx.channel.overwrites or None
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

        changed_overwrites = copy(og) 
        changed_overwrites[ctx.guild.default_role] = discord.PermissionOverwrite(send_messages=False)

        await ctx.channel.edit(overwrites=changed_overwrites)
        await asyncio.sleep(seconds)
        await ctx.send("*Jikan desu... (Channel unfrozen)*")
        await ctx.channel.edit(overwrites=og)

    # Reverses zawarudo and 3freeze
    @commands.command(brief="Cancels Channel Freeze and and slowmode", help="Reverses the effect of zawarudo and slowmode")
    @commands.has_permissions(manage_channels=True)
    async def ger(self, ctx):
        og = ctx.channel.overwrites or None
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
        await ctx.channel.edit(overwrites=og)
        

    # Kicks a user
    @commands.command(aliases=["kick"], brief="Kicks a member", help="Removes a member from your server.", usage="@member")
    @commands.has_permissions(kick_members=True)
    async def deathnote(self, ctx, member: discord.Member):
        await ctx.send(content="***You're name has been written in my notebook... Now you have 5 seconds left...***",
        file=discord.File("./images/deathnote.gif"))
        await asyncio.sleep(1)
        await ctx.send(f"***It is done... goodbye {member.mention}. You were pathetic compared to L***")
        await asyncio.sleep(5)
        await member.kick()

    # Removes all roles permanately
    @commands.command(brief="Removes the roles from a user", help="Takes away all roles from a user", usage="@member")
    @commands.has_permissions(administrator=True)
    async def ger_rtz(self, ctx, member: discord.Member):
        for role in member.roles:
            if role == ctx.guild.default_role: continue
            member.remove_roles(role)

        await ctx.send(f"{member.display_name} has had their roles permanately stripped")

    @commands.command(brief="Mutes a user for x minutes", help="Mutes a member from typing for x minutes.", usage="@member duration [defaults to 5] optional[reason]")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time=5, *, reason="They should know"):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="shushed")
        if not role:
            await ctx.send("Could not get role 'shushed'. Create it and do <>silentnow")
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

    @commands.command(brief="Sets up permissions for the Mute role", help="Sets up permissions for the mute role.")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def silentnow(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="shushed")
        if not role: await ctx.send("Role does 'shushed' does not exist. Make sure it is in lower_case"); return

        for channel in ctx.guild.text_channels:
            overwrites = channel.overwrites
            overwrites[role] = discord.PermissionOverwrite(send_messages=False)
            await channel.edit(overwrites=overwrites)

    @commands.command(brief="Used to view all members with a specified role", help="Returns a list of all users that have a given role", usage="role_name/role_id")
    async def who_has_role(self, ctx, role:discord.Role):
        members = [member.name for member in ctx.guild.members if role in member.roles]
        if not members: await ctx.send("No one has that role as of yet")
        else: 
            await ctx.send(f"Showing all members that have the {role.name} role.")
            await ctx.send(', '.join(members))

    @commands.command(brief="Used to view all members without a specified role", help="Returns a list of all users that do not have a given role", usage="role_name/role_id")
    async def not_who_has_role(self, ctx, role:discord.Role):
        members = [member.name for member in ctx.guild.members if role not in member.roles]
        if not members: await ctx.send("Everyone seems to have that role")
        else: 
            await ctx.send(f"Showing all members that do not the {role.name} role.")
            await ctx.send(', '.join(members))

    @commands.command(brief="Changes the topic of the current channel", help="Used to change the topic of the current channel", usage="new_topic")
    @commands.has_permissions(manage_channels=True)
    async def change_channel_topic(self, ctx, *, new_topic):
        await ctx.channel.edit(topic=new_topic)

    @commands.command(brief="Changes all channel topics", help="This will allow you to change all channel topics as you please")
    @commands.has_permissions(manage_channels=True)
    async def change_all_channel_topics(self, ctx):
        check_dict = {"✅": "yes", "❌": "no"}
        
        def react_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in list(check_dict.keys())

        def message_check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for channel in ctx.guild.channels:
            if not hasattr(channel, "topic"): continue
            msg = await ctx.send(f"Would you like to change the topic for {channel.name}? ✅/❌")
            for key in list(check_dict.keys()):
                await msg.add_reaction(key)

            try:
                response = await self.bot.wait_for("reaction_add", check=react_check, timeout=60)
        
                answer = check_dict[str(response[0].emoji)]
                if answer == "no":
                    await ctx.send("Okay, moving on")
                    continue

                await ctx.send(f"The current topic for this channel is {channel.topic}. What would you like to change it to?")
                response = await self.bot.wait_for('message', check=message_check, timeout=60)
                await channel.edit(topic=response.content)
                await ctx.send(f"The new channel topic for {channel.name} is {channel.topic}")
            except asyncio.TimeoutError:
                await ctx.send("You took too long")
                return

    @commands.command()
    @commands.is_owner()
    async def botrestart(self, ctx):
        await ctx.send("Turning off bot now")
        raise SystemExit

    # Events

    @commands.Cog.listener()
    async def on_command(self, ctx):
        chosen = choice(list(range(4)))
        value = randint(0, 3)
        
        if chosen == value:
            embed = Embed(
                title="A Tip For You",
                description=choice(tips),
                color=randint(0, 0xffffff)
            )
        
            await ctx.send(embed=embed, delete_after=10)

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
                
    # On leaving
    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        if member.guild.id == 739229902921793637:
            channel = member.guild.get_channel(739255078229377054)
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

            await ctx.send(f"Just take it easy {ctx.author.name}. You are on Cooldown for {math.floor(error.retry_after)} more seconds")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Could not find that command. Remember they are case sensitive. Use <>help for a list")
        else:
            await ctx.send(error)    

        channel = self.bot.get_channel(740337325971603537)
        await channel.send(f"{ctx.author.name}: {error}")
        print(error)

    @commands.command(brief="Moves all members in the user's vc to another one", help="Used to move all members in the same vc as the user to another vc, whose id is specified", usage="name or id of vc to move to")
    @commands.has_guild_permissions(move_members=True)
    async def move_members_to(self, ctx, *, name_or_id_of_vc):
        if not ctx.author.voice.channel:
            await ctx.send("You are not currently connected to a voice channel")
            return 
        
        if not name_or_id_of_vc.isnumeric():
            vc_name = name_or_id_of_vc
            channels = [channel for channel in ctx.guild.channels if hasattr(channel, "connect") and vc_name.lower() in channel.name.lower()]
            if not channels:
                await ctx.send("Could not find any channels with that name. Double check spelling.")
                return

            if len(channels) > 1:
                await ctx.send("You have more than one channel matching the name given. Use the command again, but use the id of the channel instead provided below")
                channel_msg = ""
                for channel in channels:
                    channel_msg += f"`{channel.name}: {channel.id}`\n"
                
                await ctx.send(channel_msg)
                return

            channel = channels[0]
            
        elif name_or_id_of_vc.isnumeric():
            vc_id = int(name_or_id_of_vc)
            channel = utils.get(ctx.guild.channels, id=vc_id)
            if not channel:
                await ctx.send("There is no channel in this server with that id.")
                return

        else:
            await ctx.send("The text you entered, I do not recognise.")
            return 

        confirmation = ["✅", "❌"]

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in confirmation

        msg = await ctx.send(f"Are you sure you want to move all {len(ctx.author.voice.channel.members)} members of your voice channel to {channel.name}")
        for emoji in confirmation:
            await msg.add_reaction(emoji)

        try:
            reaction = await self.bot.wait_for("reaction_add", check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("Took too long. Cancelled operation")
            return

        emoji = str(reaction[0].emoji)

        if not emoji == "✅":
            await ctx.send("Maybe next time. Move has been cancelled")
            return

        for person in ctx.author.voice.channel.members:
            await person.move_to(channel)
            

    noprofane = []

    @commands.command(brief="Toggles profanity filter", help="Toggles profanity filter")
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
        msg = msg.replace("cum ", "sexual fluid")
        msg = msg.replace("nigger", "handsome black person")
        return msg
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.guild in self.noprofane:
            for sword in self.badword:
                if sword in message.content.lower():
                    newmsg = await self.regulate(message.content.lower())
                    await message.channel.send(f"{message.author.display_name}: {newmsg}")
                    await message.delete()
                    return
        
        # if not message.channel.is_nsfw():
        #     if message.attachments:
        #         image = [img for img in message.attachments if hasattr(img, "height")]
        #         if not image: return
        #         async with aiohttp.ClientSession() as session:
        #             s = await session.post("https://api.deepai.org/api/nsfw-detector", data={'image': image[0].url,},headers={'api-key': "557a24bd-0ea9-47b3-bb06-98e0d0be6347"})
        #             sjson = await s.json()
        #             try:
        #                 if sjson["output"]['nsfw_score'] > 0.5:
        #                     await message.delete()
        #                     await message.channel.send(f"OII... NO PORN HERE!!!. {sjson}", delete_after=10)
        #             except KeyError: print("Sus image... but idk what happened"); print(sjson)

def setup(bot):
    bot.add_cog(Moderator(bot))
