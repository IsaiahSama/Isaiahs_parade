import discord
from discord.ext import commands
from random import randint
import asyncio
import random
import math
from googletrans import Translator
import googletrans


class afkuser:
    def __init__(self, user, id, guild, message):
        self.user = user
        self.id = id
        self.guild = guild
        self.message = message

class General(commands.Cog):
    """General commands for general usage"""

    def __init__(self, bot):
        self.bot = bot

    # General
    @commands.command(brief="Sends your message as an embed", help="Sends a message as an embed", usage="message")
    async def me(self, ctx, *, arg):
        user_role = ctx.author.roles[-1]

        rolecolor = user_role.color
        if not rolecolor:
            rolecolor = randint(0, 0xffffff)

        embed = discord.Embed(
            title=f"{ctx.author.display_name}:",
            description=f"{arg}",
            color=rolecolor
        )

        await ctx.send(embed=embed)
        await ctx.message.delete()

    # Grants the user affirmation
    @commands.command(brief="Yes", help="Still Yes")
    async def yes(self, ctx):
        await ctx.message.delete()
        await ctx.send("```I absolutely, 10 billion% , agree with your statement.```")

    # Grant the NO!
    @commands.command(brief="No", help="Still no")
    async def no(self, ctx):
        await ctx.message.delete()
        await ctx.send("I know you didn't really just say that '-'")

    # Heavens Door
    @commands.command(brief="Shows detail information on a user", help="Shows detailed information on a user", usage="optional[@user]")
    async def heavens_door(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        file = discord.File("./images/hd1.gif", filename="hd1.gif")
        user_roles = ", ".join([role.mention for role in member.roles if role != ctx.guild.default_role])
        if not user_roles:
            user_roles = "No Roles"
        if member.activity is None:
            actividad = "None"
        else:
            actividad = member.activity.name
        embed = discord.Embed(
            title='Heavens Door',
            description='With my stand Heavens Door, There is nothing I do not know',
            color=randint(0, 0xffffff)
        )

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="attachment://hd1.gif")
        embed.add_field(name='Display Name:', value=f"{member.display_name}")
        embed.add_field(name='Current Activity:', value=f"{actividad}")
        embed.add_field(name='Current Status:', value=f"{member.status}")
        embed.add_field(name='On Mobile:', value=f"{member.is_on_mobile()}")
        embed.add_field(name='Date Joined Server:',
                        value=f'{member.joined_at.strftime("%d/%m/%y")}')
        embed.add_field(name='Date Account Created:',
                        value=f'{member.created_at.strftime("%d/%m/%y")}')
        embed.add_field(name='Highest Role:', value=f"{member.top_role}")
        embed.add_field(name='Roles:', value=f"{user_roles}")

        await ctx.send(file=file, embed=embed)

    # Check for bot being online
    @commands.command(brief="Displays if the bot is online or not", help="Useful for checking if the bot is online or not")
    async def online(self, ctx, conf="No"):
        await ctx.message.delete()
        if ctx.author.id == 493839592835907594 and conf.lower() == "yes":
            for server in self.bot.guilds:
                role = discord.utils.get(server.roles, name="Parader")
                channel = discord.utils.get(
                    server.text_channels, name="parade-room")
                await channel.send(f"{role.name} I have returned.")

        await ctx.send("I am indeed online")


    @commands.command(brief="Shows information on the current server", help="Shows information about the current server")
    async def allseeing(self, ctx):
        guild = ctx.guild
        numchan = len(ctx.guild.channels)

        rolnum = len(guild.roles)

        guilded = discord.Embed(
            title="BILL! LET'S MAKE A DEAL",
            description="I summon The All Seeing Eye",
            color=randint(0, 0xffffff)
        )

        guilded.set_thumbnail(url=guild.icon_url)
        guilded.set_image(
            url="https://media1.tenor.com/images/2d1a5e1389e8a85a5d394b529b06c52d/tenor.gif?itemid=4864289")
        guilded.add_field(name="Guild Name", value=f"{guild.name}")
        guilded.add_field(name="Date Created",
                          value=f"{guild.created_at.strftime('%d/%m/%y')}")
        guilded.add_field(name="Guild Region", value=f"{guild.region}")
        guilded.add_field(name="Guild Owner", value=f"{guild.owner}")
        guilded.add_field(name="Number of Members",
                          value=f"{guild.member_count}")
        guilded.add_field(name="Number of Channels", value=f"{numchan}")
        guilded.add_field(name="Number of roles", value=f"{rolnum}")

        await ctx.send(embed=guilded)

    # Timer

    @commands.command(brief="starts a timer for x minutes", help="Use this to set a timer for a specified amount of time.", usage="time")
    async def timer(self, ctx, lot: int = None):
        if lot == None:
            await ctx.send("You did not specify a time in minutes")
            return False
        elif lot == 0:
            await ctx.send(f"Bring bring, {ctx.author.display_name} your time is up... Wow, who would have guessed")
            return False
        elif lot < 0:
            await ctx.send(f"Ha... Very funny. No timer for you")
            return False
        else:
            pass

        await ctx.send(f"I have set your timer for {lot} minutes.")
        lot *= 60
        await asyncio.sleep(lot)
        await ctx.send(f"{ctx.author.mention}. Your time is up :thumbsup:")

    # Member of the day

    @commands.command(brief="Picks a random member", help="Selects a random member")
    async def chosenone(self, ctx):
        guild = ctx.guild
        chosen = random.choice(guild.members)
        await ctx.send("Congratulations, The chosen member is...")
        await asyncio.sleep(3)
        await ctx.send(f"{chosen.display_name}")

    @commands.command(brief="Translates any given text into english", help="Translates any given text to english", usage="non-english_text")
    async def translate(self, ctx, *, text):
        translator = Translator()
        result = translator.translate(text)
        await ctx.send(result.text)

    @commands.command(brief="Translates any given text to language specified", help='Translates any given text to the language specified', usage="language text_to_translate")
    async def translateto(self, ctx, lang: str, *, text):
        lang = lang.lower()
        languages = googletrans.LANGUAGES

        lang_to_trans = [k for k, v in languages.items() if lang.lower() in [k, v]]
        if not lang_to_trans: 
            await ctx.send(f"{lang} could not be found")
            return

        lang_to_trans = lang_to_trans[0]

        translator = Translator()
        result = translator.translate(text, dest=languages[lang_to_trans])
        await ctx.send(result.text)

    # List of all Letters in the Alphabet
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
               "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    # List of Vowels
    vowels = ["a", "e", "i", "o", "u", "h"]

    # List of Consonants. For the sake of Laziness, we will use a function
    # Defines empty list called consonants, only containing H since I want H to be in both
    consonants = ["h"]

    # Creates for loop to loop through each letter in the alphabet
    for letter in letters:
        # Checks to see if the letter is a vowel
        if letter not in vowels:
            # If letter is not a vowel, then add it to the consonants List
            consonants.append(letter)

    # Random Letter
    @commands.command(brief="Mhm... Soulmate", help="Displays the first letter of the name of your soulmate... probably")
    async def soulmate(self, ctx):
        await ctx.send(f"The person who will become your soulmate. Their name... begins with {random.choice(self.letters)}")

    @commands.command(brief="Generates a name", help="Generates a name for you", usage="length_of_name")
    async def namegen(self, ctx, length: int):
        if length <= 1:
            length = 2
        elif length > 11:
            length = 11
        else:
            pass
        name = self.makename(length)
        await ctx.send(f"Your name is {name}")


    # Functions    

    def consonantchk(self, x):
        if x in self.consonants:
            return True
        else:
            return False

    def makename(self, length):
        # Creates empty list which will store the name as it is created
        genname = []

        # Loops through the length of the name, and creates letters based on logic
        for number in range(length):
            # Selects a random letter from the alphabet
            letter = random.choice(self.letters)

            # For the first letter, just add it to genname
            if number == 0:
                genname.append(letter.upper())

            else:
                # Creates a variable called prevletter, which takes the value of the previous letter
                prevletter = genname[number-1].lower()

                isconsonant = self.consonantchk(prevletter)

                if isconsonant:
                    letter = random.choice(self.vowels)
                    # Checks to make sure the letter is not an H
                    if prevletter == "h":
                        while letter == "h":
                            letter = random.choice(self.vowels)

                    if prevletter == "q":
                        letter = "u"
                else:
                    pass

                genname.append(letter)

        genname = "".join(genname)
        return genname

    isafk = []

    # Afk
    @commands.command(brief="Sends you afk", help="Shows that you have gone afk", usage="Optional[reason]")
    async def afk(self, ctx, *, afkmsg="No reason, Just afk"):
        for afkperson in self.isafk:
            if ctx.author.id == afkperson.id and ctx.guild == afkperson.guild:
                await ctx.send("You are already afk. Simply do <>back to let me know that you have returned")
                return

        afkman = afkuser(ctx.author, ctx.author.id, ctx.guild, afkmsg)
        self.isafk.append(afkman)
        await ctx.send(f"Goodbye {ctx.author.mention}, we eagerly await your return")
        try:
            await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
        except discord.errors.Forbidden:
            pass

    # back

    @commands.command(brief="Used to return from AFK", help="Sets you back to normal indicating that you have returned")
    async def back(self, ctx):
        for afkperson in self.isafk:
            if ctx.author.id == afkperson.id and ctx.guild == afkperson.guild:
                try:
                    name = ctx.author.display_name.strip("[AFK]")
                    await ctx.author.edit(nick=f"{name}")
                except discord.errors.Forbidden: pass
                self.isafk.remove(afkperson)
                await ctx.send(f"Welcome back {ctx.author.mention}, you were missed... By me at least")
            return

        if ctx.author.display_name.startswith("[AFK] "):
            try:
                name = ctx.author.display_name.strip("[AFK] ")
                await ctx.author.edit(nick=f"{name}")
            except discord.errors.Forbidden: pass

        await ctx.send("Look at you pretending that you were gone")

    @commands.command(brief="Quotes a message", help="Similar to discord's old quote function. (The message link is easily copied by right clicking the message)", usage="message_link")
    async def quote(self, ctx, messageLink, *, msg=" "):
        messageLink = messageLink.split("/")
        try:
            message_guild = int(messageLink[-3])
            message_channel = int(messageLink[-2])
            message_id = int(messageLink[-1])  
        except ValueError:
            await ctx.send("Something is wrong with your message link.")
            return

        if not message_guild == ctx.guild.id: await ctx.send("That message does not belong to this server"); return
        channel = ctx.guild.get_channel(message_channel)
        try:
            message = await channel.fetch_message(message_id)
        except discord.errors.NotFound:
            await ctx.send("The message you may be looking for could not be found :thinking:")
            return
        content = message.content
        await ctx.send(f"> {content} - {message.author.display_name}\n```{ctx.author.name}: {msg}``` \n Link: {message.jump_url}")
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        """if message.content.startswith("<>back"):
            return
        for afkperson in self.isafk:
            if afkperson.id == message.author.id and afkperson.guild == message.guild:
                await message.channel.send("Have you returned to us? If so, do <>back")"""

        for afkthing in self.isafk:
            if afkthing.user in message.mentions and afkthing.guild is message.guild:
                await message.channel.send(f"{afkthing.user.name} went afk saying \"{afkthing.message}\"")

    cd = 60 * 60

    @commands.command(brief="Make a suggestion", help="Makes a suggestion to the bot developer", usage="content")
    @commands.cooldown(1, cd, commands.BucketType.user)
    async def suggest(self, ctx, *, content):
        if len(content) <= 2:
            await ctx.send("Don't waste our time")
            return

        channel = self.bot.get_channel(739248905379643422)

        embed = discord.Embed(
            title=f"{ctx.author.name} from {ctx.guild}:",
            description=content,
            color=randint(0, 0xffffff)
        )
        msg = await channel.send(embed=embed)
        await msg.add_reaction("\U00002b50")
        await ctx.send("Your suggesstion was made")


def setup(bot):
    bot.add_cog(General(bot))
