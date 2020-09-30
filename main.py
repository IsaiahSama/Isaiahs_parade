# imports
import discord
from discord.ext import commands, tasks
import asyncio
import random
from random import randint
import os
import sqlite3
from dotenv import load_dotenv
load_dotenv()
import json


# Set Client
bot = commands.Bot(command_prefix='<>', case_insensitive=True)
bot.help_command = None


bot.load_extension("general_com")
bot.load_extension("gaming_com")
bot.load_extension("misc_com")
bot.load_extension("moderator_com")
bot.load_extension("action_com")
bot.load_extension("special_com")
bot.load_extension("fighting")
bot.load_extension("relacom")
bot.load_extension("calling")
bot.load_extension("bothelp")
# bot.load_extension("music_com")

# Events
# Creating On_ready event
@bot.event
async def on_ready():
    # on ready event called when bot finished logging in
    print("We have logged in as {0.user}".format(bot))
    # Sets Discord Status
    activity = discord.Activity(name='<>help', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    backup.start()
    # , status=discord.Status.dnd

@tasks.loop(hours=1)
async def backup():
    lis = ["fightdata.json", "relausers.json", "jltracking.json", "teams.json"]
    for files in lis:
        try:
            with open(files) as fdata:
                dataf = json.load(fdata)
        except json.JSONDecodeError:
            print("One of the Files Are Corrupt and therefore will not be backed up")
            return
        
        with open(f"backups/{files}", "w") as t:
            json.dump(dataf, t, indent=4)

    print("Backed up")    

@bot.command()
@commands.is_owner()
async def refresh(ctx):
    bot.reload_extension("general_com")
    bot.reload_extension("gaming_com")
    bot.reload_extension("misc_com")
    bot.reload_extension("moderator_com")
    bot.reload_extension("action_com")
    bot.reload_extension("special_com")
    bot.reload_extension("fighting")
    bot.reload_extension("relacom")
    bot.reload_extension("calling")
    bot.reload_extension("bothelp")

    
# when bot joins a guild
@bot.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.text_channels, name="parade-room")
    if channel == None:
        await guild.create_text_channel("parade-room")
        channel = discord.utils.get(guild.text_channels, name="parade-room")

    role = discord.utils.get(guild.roles, name="Parader")
    if role == None:
        role = await guild.create_role(name="Parader")

    mchan = bot.get_channel(740414745252986970)
    await mchan.send(f"I have been invited to {guild.name}. {role.name} and {channel.name} Have been created successfully")

    joinbed = discord.Embed(
        title="I have Arrived",
        description=f"Thanks for inviting me to {guild.name}. I look forward to spending time with all of you",
        color=randint(0, 0xffffff)
    )

    joinbed.set_thumbnail(url=bot.user.avatar_url)
    joinbed.add_field(name="Help", value="You can view everything i'm capable of with <>help")
    joinbed.add_field(name="Main Server", value="Feel free to join my main server. Get the link with <>parade")
    joinbed.add_field(name="Positioning", value="As someone created to Moderate, be sure to give me a role high enough in order for you to use me to my full potential")

    await channel.send(embed=joinbed)

        


@bot.command()
async def help2(ctx, *, category=None):
    general = discord.Embed(
            title="General",
            description="Below are a list of my General commands.",
            color=randint(0, 0xffffff)
        )

    general.set_thumbnail(url=bot.user.avatar_url)
    general.add_field(name='<>me {message}',
                        value="Displays bot message and deletes user message. Good for roleplay", inline=False)
    general.add_field(name='<>yes', value="Grants Confirmation on use", inline=False)
    general.add_field(name='<>no', value="'Did you really just say that?'", inline=False)
    general.add_field(name='<>heavens_door {@mention}', value="Reveals target's info", inline=False)
    general.add_field(name='<>online', value="If bot responds, Bot is online. If not... then bot is offline", inline=False)
    general.add_field(name='<>afk', value="Sends an AFK message for you", inline=False)
    general.add_field(name='<>back', value="Sends a message announcing your arrival", inline=False)
    general.add_field(name='<>allseeing', value="Reveals Server info", inline=False)
    general.add_field(name="<>soulmate", value="Tells you the first letter of your potential soulmate's name", inline=False)
    general.add_field(name="<>namegen {length of name}", value="Creates a name with the amount of letters you requested. Max is 11, min is 2", inline=False)
    general.add_field(name="<>nohide", value="<>nohide. Inspired by Dank Memer's \"pls snipe\", it shows the last deleted message", inline=False)
    general.add_field(name="<>timer", value="<>timer {minutes}. Sets a timer for the specified amount of minutes.", inline=False)
    general.add_field(name="<>chosenone", value="<>chosenone. Inspired by Discord's joke feature @someone which was a thing a while back", inline=False)
    general.add_field(name="<>parade", value="Returns the invite link to the Official Discord Server", inline=False)
    general.add_field(name="<>suggest {suggestion}", value="Used to make a suggestion in the suggestion channel in the main server", inline=False)
    
    moderator = discord.Embed(
            title="Mod Commands",
            description="These commands require Manage Messages permissions(MM), Manage Roles (MR),Manage Channels(MC), Admin (A) Kick (K) or Ban (B)",
            color=randint(0, 0xffffff)
        )

    moderator.add_field(name='<>zahando {number}', value="Deletes requested number of messages (MM)", inline=False)
    moderator.add_field(name='<>kingcrimson {@mention} {amount}',
                            value="Deletes requested amount of messages from user(MM)", inline=False)
    moderator.add_field(name='<>freeze3 {interval:seconds}',
                            value="Puts on slowmode with amount being the interval(MC)", inline=False)
    moderator.add_field(name='<>zawarudo {time:seconds}',
                            value="Stops people without MC from talking in chat for time(MC)(MR)", inline=False)
    moderator.add_field(name='<>ger', value="Disables effects from freeze3 and za warudo (MC)(MR)", inline=False)
    moderator.add_field(name='<>shadowrealm {@mention}', value="Bans a target (B)", inline=False)
    moderator.add_field(name='<>impactrevive {user id}', value="Unbans a target (B)", inline=False)
    moderator.add_field(name='<>deathnote {@mention}', value="Kicks the mentioned person from the server in 1 minute (K)", inline=False)
    moderator.add_field(name="<>ger_rtz {@Mention}", value="Golden Experience Requiem, Return to zero. Strips the mentioned of all of their roles (MR)", inline=False)
    moderator.add_field(name="<>wipe [amount (optional)] {phrase}", value="Delete the specified number of messages that contain the specified phrase or word.(MM)", inline=False)
    moderator.add_field(name='<>relax', value="mutes all members in the channel for 5 seconds. (A)", inline=False)
    moderator.add_field(name='<>killerqueen {@mention} [time: Default 2 minutes]', value="Strips the mentioned user of their roles for the mentioned amount of minutes. Roles are restored 1 by 1 in 2 minute intervals (A)", inline=False)
    moderator.add_field(name="<>mute {@mention} [time (default 5 minutes)] [reason (optional)", value="Used to mute a user", inline=False)
    moderator.add_field(name="<>relog {amount default=5}", value="Shows the audit log up to the given amount.", inline=False)
    moderator.add_field(name="<>profane", value="enables and disables the profanity filter for a guild")

    actions = discord.Embed(
            title="Action Commands",
            description="Use these to do some stuff",
            color=randint(0, 0xffffff)
        )

    actions.add_field(name='<>hug {@mention}', value="Hugs the one you @mention", inline=False)
    actions.add_field(name='<>kiss {@mention}', value="Kiss the one you want :p", inline=False)
    actions.add_field(name='<>slap {@mention}', value="Slaps the target", inline=False)
    actions.add_field(name='<>punch {@mention}', value="Punches the target", inline=False)
    actions.add_field(name='<>poke {@mention}', value="Pokes the one you Mention", inline=False)
    actions.add_field(name='<>pat {@mention}', value="pats the target", inline=False)
    actions.add_field(name='<>fistbump {@mention}', value="Bumps fists with the one you choose", inline=False)
    actions.add_field(name='<>flex {@mention}', value="Flexes on the person mentioned", inline=False)
    actions.add_field(name='<>cry', value="Aww, you're crying", inline=False)
    actions.add_field(name='<>blush', value="Oh my, you're blushing", inline=False)
    actions.add_field(name='<>pose', value="Display yourself with a brilliant pose", inline=False)

    misc = discord.Embed(
            title="Misc Interactions",
            description="A few of the potential interactions achieveable by just talking in chat",
            color=randint(0, 0xffffff)
        )

    misc.add_field(name="banana", value="Don't ask. If you are going to say it, say it 5 times.", inline=False)
    misc.add_field(name="ZA WARUDO!!!", value="For us people that get the urge to scream this... Only lasts 5 seconds though", inline=False)
    misc.add_field(name="thanks",
                    value="Say thanks or thx. 100% chance of appreciation... When i'm online of course", inline=False)
    misc.add_field(name="oh truth seeking orbs {question} ?",
                    value="""Use this followed by your question and end with a ? receive your response
        example: Oh truth seeking orbs, Will this happen?""", inline=False)
    misc.add_field(name="<>intercom", value="Sends a 'call' request to other servers with me in it. Inspired by Yggdrasil", inline=False)
    misc.add_field(name="<>accept", value="Accepts a 'call' request", inline=False)
    misc.add_field(name="<>endcall", value="Ends an existing 'call' with another server", inline=False)
    misc.add_field(name="<>deny", value="Denies an intercom request", inline=False)
    misc.add_field(name="<>gcall", value="Starts a Multi-Server Intercom", inline=False)
    misc.add_field(name="<>gjoin", value="Joins a Multi-Server Intercom if one is active", inline=False)
    misc.add_field(name="<>gleave", value="Leaves a Multi-Server Intercom once you are in it.")
    misc.add_field(name="<>hme {Message}", value="Sends an anonymous message", inline=False)
    misc.add_field(name="<>fdeathnote {@mention}", value="Similar to <>deathnote, but for everyone to use. (Does not kick, obviously)", inline=False)
    misc.add_field(name="<>emoji {emojiname}", value="Heaven knows when you'd want to use this but hey", inline=False)
    misc.add_field(name="<>mentioned", value="Finds a message that you were mentioned in within the last 200 messages and shows it to you. Misc Command", inline=False)
    misc.add_field(name="<>ping", value="Used to get the bot's ping", inline=False)
    

    gaming = discord.Embed(
            title="Game Commands",
            description="Below are a list of my 'Gaming' commands.",
            color=randint(0, 0xffffff)
        )

    gaming.add_field(name='<>startgame', value="Starts a hangman game", inline=False)
    gaming.add_field(name='<>endgame', value="Ends the hangman game early", inline=False)
    gaming.add_field(name='<>wordadd {words}', value="Add as many words as you would like separated by a comma (, )", inline=False)
    gaming.add_field(name='<>wordclear {words} ', value="Cleanses Hangman's mind of the specified words", inline=False)
    gaming.add_field(name='<>startstory',
                        value="Enters story mode. Get some friends and make a story one word at a time", inline=False)
    gaming.add_field(name='<>endstory', value="Exits story mode then displays the full story", inline=False)

    
    
    battle = discord.Embed(
        title="Battle Commands",
        description="These are a list of all of the battle commands",
        color=randint(0, 0xffffff)
    )

    battle.add_field(name='<>fight {@mention}', value="Starts a fight with the mentioned user", inline=False)
    battle.add_field(name='<>quest', value="Fights an NPC. Good for farming levels. Assuming you win :)", inline=False)
    battle.add_field(name='<>createprofile', value="Creates a profile for fighting", inline=False)
    battle.add_field(name="<>profile [{@mention} optional]", value="Shows you your profile or the profile of the one you @mentioned")
    battle.add_field(name='<>paradecoins', value="Tells you how many Parade Coins you have", inline=False)
    battle.add_field(name="<>grant {@mention} {amount}", value="Gives the @mentioned user the amount of your Parade Coins that you specify", 
    inline=False)
    battle.add_field(name="<>upgrade", value="Shows the upgrade area, where you can upgrade yourself", inline=False)
    battle.add_field(name="<>raid", value="Joins a Boss Raid Battle", inline=False)
    battle.add_field(name="<>paraid", value="Stars a boss raid. Must be Level 40", inline=False)
    battle.add_field(name="<>readd", value="Gives you back Parader role if you ever lose it. Can also be used to get rid of it if you have it", inline=False)
    battle.add_field(name="<>shop", value="Opens the shop", inline=False)
    battle.add_field(name="<>togglefight", value="Toggles your pvp fight state", inline=False)
    battle.add_field(name="<>gear", value="Displays your current loadout", inline=False)
    battle.add_field(name="<>job", value="Go and do a 'regular' job", inline=False)
    battle.add_field(name="<>sell True weapon/armor", value="Used to sell an item you have currently. Example: '<>sell True armor' sells your armor", inline=False)
    battle.add_field(name="<>search", value="Searches for Fellow Paraders in your tier who are available for fighting", inline=False)

    socials = discord.Embed(
        title="Social Commands",
        description="List of my Social Commands",
        color=randint(0, 0xffffff)
    )

    socials.add_field(name="<>createsocial", value="Used to create a social profile", inline=False)
    socials.add_field(name="<>socialprofile/<>sp", value="Used to view your social profile", inline=False)
    socials.add_field(name="<>addfriend {@mention}", value="Used to add someone to your list of friends", inline=False)
    socials.add_field(name="<>acceptfr", value="Used to accept a friend request", inline=False)
    socials.add_field(name="<>denyfr", value="Used to deny a friend request", inline=False)
    socials.add_field(name="<>showfriends", value="Shows all of your friends", inline=False)
    socials.add_field(name="<>addlove {@mention}", value="Used to request a 'relationship' with a user", inline=False)
    socials.add_field(name="<>acceptlove", value="Used to Accept a relationship request", inline=False)
    socials.add_field(name="<>denylove", value="Used to deny a relationship request", inline=False)
    socials.add_field(name="<>newbff {@mention}", value="Request someone to be your bff", inline=False)
    socials.add_field(name="<>acceptbff", value="Accept a Best friend Request", inline=False)
    socials.add_field(name="<>denybff", value="Deny a bff request", inline=False)
    socials.add_field(name="<>newchild {@mention}", value="Use this to add someone as your child", inline=False)
    socials.add_field(name="<>acceptparent", value="Accept the sender as your parent ", inline=False)
    socials.add_field(name="<>denyparent", value="Deny the sender as your parent", inline=False)
    socials.add_field(name="<>pet", value="Used to view your pet", inline=False)
    socials.add_field(name="<>getpet", value="Used to get your first pet.", inline=False)
    socials.add_field(name="<>delpet", value="Used to get rid of your pet... You won't be forgived")
    socials.add_field(name="<>play", value="Play with your pet", inline=False)
    socials.add_field(name="<>feed", value="Feed your pet", inline=False)
    socials.add_field(name="<>updatesocial", value="Used to Update your current/main guild/name", inline=False)


    if category == None:

        await ctx.send("Please use <>help {category name}.")
        await ctx.send("The available categories are 'General', 'Moderator', 'Misc', 'Actions', 'Gaming', 'Battle' and 'Socials'")

    elif category.lower() == "general":
        await ctx.author.send(embed=general)
    
    elif category.lower() == "gaming":
        await ctx.author.send(embed=gaming)
        
    elif category.lower() == "battle":
        await ctx.author.send(embed=battle)

    elif category.lower() == "moderator" or category.lower() == "mod":
        await ctx.author.send(embed=moderator)
    
    elif category.lower() == "misc":
        await ctx.author.send(embed=misc)
    
    elif category.lower() == "actions":
        await ctx.author.send(embed=actions) 

    elif category.lower() == "socials":
        await ctx.author.send(embed=socials) 

    elif category.lower() == "all":
        await ctx.author.send(embed=general)
        await ctx.author.send(embed=moderator)
        await ctx.author.send(embed=gaming)
        await ctx.author.send(embed=misc)
        await ctx.author.send(embed=actions)
        await ctx.author.send(embed=battle)
        await ctx.author.send(embed=socials) 

    else:
        pass

    """elif category.lower() == "lord kevin says to update all now":
        await ctx.message.delete()
        guild = bot.get_guild(739229902921793637)
        channel = discord.utils.get(guild.text_channels, name="general-help")
        await channel.send(embed=general)
        channel = discord.utils.get(guild.text_channels, name="gaming-help")
        await channel.send(embed=gaming)
        channel = discord.utils.get(guild.text_channels, name="battle-commands")
        await channel.send(embed=battle)
        channel = discord.utils.get(guild.text_channels, name="moderator-commands")
        await channel.send(embed=moderator)
        channel = discord.utils.get(guild.text_channels, name="misc-help")
        await channel.send(embed=misc)
        channel = discord.utils.get(guild.text_channels, name="actions-help")
        await channel.send(embed=actions)
        await ctx.send("They have been updated")"""

yes=os.getenv("key")
bot.run(yes)
