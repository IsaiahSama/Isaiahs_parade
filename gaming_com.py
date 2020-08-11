import discord
from discord.ext import commands
import asyncio
from random import randint
import random


class Gaming(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    isaiah = 493839592835907594

    # Story Making
    message_list = []
    storytelling = False
    currentchannel = None

    banana_count = 0
    annoy_count = 0

    # Hangman
    word_list = []
    hangingchannel = None
    hanging = False
    trycount = 0
    hiddenword = ""
    word = ""

    # Gaming
    # Story

    @commands.command()
    async def startstory(self, ctx):
        self.message_list.clear()
        if not self.hanging and not self.storytelling and ctx.channel is not self.hangingchannel:
            self.storytelling = True
            self.currentchannel = ctx.channel

            await ctx.send("""Story mode has been activated. Get your friends and tell a story one word at a time.
        Use <>endstory to exit story mode and see the full story
        BEGIN!""")
        elif self.hanging and ctx.channel.id == self.hangingchannel.id:
            await ctx.send("A hangman game is currently currently in Progress... Please wait or go elsewhere")
        
        elif self.storytelling:
            await ctx.send("A story is in progress elsewhere :eyes:")

        else:
            await ctx.send("Doesn't seem you can make a story right now")



    @commands.command()
    async def endstory(self, ctx):
        guild = ctx.guild

        if len(self.message_list) == 0:
            await ctx.send("You haven't started a story as yet. Do so with <>startstory")
            return False

        if ctx.channel.id == self.currentchannel.id:
            self.currentchannel = None
            self.storytelling = False

            await ctx.send("Behold your story")

            tale = " ".join(self.message_list)
            tale = tale.strip("<>endstory")
            print(len(tale))

            t2 = False
            t3 = False
            if len(tale) >= 1024:
                tale2 = tale[1020:]
                tale = tale[:1020]
                t2 = True

            if t2:
                if len(tale2) >= 1024:
                    tale3 = tale2[1020:]
                    tale2 = tale2[:1020]
                    t3 = True

            story = discord.Embed(
                title="Listen Closely",
                description=f"Here is the story that the awesome people in {guild} has created",
                color=randint(0, 0xffffff)
            )

            story.set_thumbnail(url=guild.icon_url)
            story.add_field(name="And it goes like", value=f"{tale}")

            await ctx.send(embed=story)

            if t2:
                story2 = discord.Embed(
                    title="Continuing",
                    description=f"Here is the story that the awesome people in {guild} has created",
                    color=randint(0, 0xffffff)
                )

                story2.set_thumbnail(url=guild.icon_url)
                story2.add_field(name="And it goes like", value=f"{tale2}")

                await ctx.send(embed=story2)

            if t3:
                story3 = discord.Embed(
                    title="Continuing",
                    description=f"Here is the story that the awesome people in {guild} has created",
                    color=randint(0, 0xffffff)
                )

                story3.set_thumbnail(url=guild.icon_url)
                story3.add_field(name="And it goes like", value=f"{tale3}")

                await ctx.send(embed=story3)
                
                self.message_list.clear()

        else:
            await ctx.send("A story is being told elsewhere. Please wait until it is done.")


    # Adds words for hangman
    @commands.command()
    async def wordadd(self, ctx, *, words):
        words = words.split(", ")
        for tempword in words:
            if tempword in self.word_list:
                await ctx.send(f"{tempword} is already in list")
            else:
                tempoword = tempword.lower()
                self.word_list.append(tempoword)

        await ctx.send("Words have been added :thumbsup:")


    @commands.command()
    async def wordshow(self, ctx):
        await ctx.send(self.word_list)


    # Clears words from hangman
    @commands.command()
    async def wordremove(self, ctx, *, words):
        words = words.split(', ')
        for word in words:
            if word in self.word_list:
                self.word_list.remove(word)
            else:
                await ctx.send(f"{word} was not found in word list")

        await ctx.send("Succesfully removed words")


    # Start hang game
    @commands.command()
    async def startgame(self, ctx):
        global hangingchannel, hanging, trycount, hiddenword, word
        if len(self.word_list) < 2:
            await ctx.send("Not enough words. Add with <>wordadd")
            return
        trycount = 0
        hangingchannel = ctx.channel
        if not self.storytelling and self.hangingchannel is not self.currentchannel:
            hanging = True
            word = random.choice(self.word_list)
            word = word.rstrip()
            hiddenword = self.hide_word()
            await asyncio.sleep(2)
            await ctx.send(f"The word is {hiddenword}. Now. Carefully, Solve it :smiling_imp:")
        else:
            await ctx.send("A story is being told... Shhh, not now")


    @commands.command()
    async def endgame(self, ctx):
        global hangingchannel, hanging, word
        hanging = False
        hangingchannel = None
        await ctx.send(f"Aww... Game is over.The word was {word}. Maybe Next time")

    
    def hide_word(self):
        hidden_word = []
        for letter in word:
            if letter == " ":
                hidden_word.append(" ")
            else:
                hidden_word.append("-")

            hidden_word = "".join(hidden_word)
            return hidden_word


    @commands.Cog.listener()
    async def on_message(self, message):

        # On message is called when bot receives a message
        if message.author == self.bot.user:
            # Makes sure that bot messages are ignored
            return
        if not self.storytelling or not self.hanging:

            if self.bot.user in message.mentions:
                await message.channel.send(":sunglasses:To view my commands use <>help")            

            
            """# Greeting
            for greeting in ["hello", "sup", "herro", "hey"]:
                if message.content.lower() == greeting:
                    await asyncio.sleep(2)
                    await message.channel.send(f"Hello {message.author.mention} I hope this day finds you well?")

            for greeting in ["gm", "morning", "good morning"]:
                if message.content.lower() == greeting:
                    await message.channel.send(f"Good morning... I hope you had a nice rest {message.author.mention}")

            # dismissing
            for leaving in ["bye", "cya", "ttyl", "bai"]:
                if message.content.lower() == leaving:
                    await message.channel.send(f"Bye, have a good time :yum: {message.author.mention}")"""

            for leaving in ["gn", "nite", "good night"]:
                if message.content.lower() == leaving:
                    await message.channel.send(f"sweet dreams to you {message.author.mention}")

            if "banana" in message.content.lower():
                self.banana_count += 1
                if self.banana_count <= 3:
                    await message.channel.send("Say banana one more time '-'")
                if self.banana_count >= 3:
                    await message.channel.send(f"Please stop now... Please {message.author.mention}!!!")
                if self.banana_count == 5:
                    await message.channel.send("NOW YOU'VE DONE IT... ZA WARUDO!")
                    await message.channel.send(file=discord.File("images/zawarudo.gif"))
                    await message.channel.send(f"{message.author.display_name} made me do it")
                    await message.channel.set_permissions(message.author, send_messages=False)
                    await asyncio.sleep(6)
                    await message.channel.set_permissions(message.author, send_messages=True)
                    await message.channel.send("6 seconds was all I needed to relax again...")
                if self.banana_count >= 6:
                    await message.channel.send("Resetting banana counter")
                    self.banana_count = 0

            if "za warudo!!!" in message.content.lower():
                file=discord.File("images/zawarudo.gif", filename="zawarudo.gif")
                embed = discord.Embed(
                    title="TOKI YO TOMARE",
                    color=randint(0, 0xffffff)
                )
                embed.set_image(url="attachment://zawarudo.gif")

                await message.channel.send(file=file, embed=embed)

                await message.channel.set_permissions(message.author, send_messages=False)
                await asyncio.sleep(5)
                await message.channel.set_permissions(message.author, send_messages=True)
                await message.channel.send(f"Time flows again for {message.author.display_name}")

            if message.content == "?":
                if message.author.id == self.isaiah:
                    await message.channel.send("What??")

        if self.storytelling and message.channel == self.currentchannel:
            self.message_list.append(message.content)

        if self.hanging and message.channel == self.hangingchannel:
            game_done = self.endchk()
            # Sets Message.content To X
            x = message.content.lower()
            # Checks to make sure that team has Tries left
            if self.trycount < 15:
                # Checks to see if the message's content is the same as the selected word
                word = "".join(word)
                if x == word:
                    hiddenword = word
                    game_done = self.endchk()
                # Checks to see if the message's content is in the word, and that the length of the message is less than 1
                elif x in word and len(x) <= 1:
                    # Loops through each letter in the word
                    for chance in range(len(word)):
                        # if the message's content is the same as a letter in the word
                        if x == list(word)[chance]:
                            # Turn Hidden word into a list.
                            hiddenword = list(hiddenword)
                            # Using the same index, set the character at that index to the message's content
                            hiddenword[chance] = x
                            # Turns the hidden word into a string again
                            hiddenword = "".join(hiddenword)
                # If message's content is in the word... and the length of the message is more than 1
                elif x in word:
                    # Sets a variable index_of, to the position of where the first instance of x is found
                    index_of = word.find(x)
                    # Turns hidden word into a list
                    hiddenword = list(hiddenword)
                    # Sets a value letter index to 0.
                    letterindex = 0
                    # For i in range index_of to the length of x + index_of
                    for i in range(index_of, len(x) + index_of):
                        # Sets the character at that position, to be equal to the letter in x it's position
                        hiddenword[i] = x[letterindex]
                        letterindex += 1
                    # turns hidden word into a string
                    hiddenword = "".join(hiddenword)

                else:
                    self.trycount += 1
                    await message.channel.send(
                        f"""That is not in the word. Remember, You can only have a maximum of 15 incorrect attempts.
    You are currently at {self.trycount}""")

            game_done = self.endchk()
            if game_done:
                await message.channel.send(f"Game over. The word is {word}")
            else:
                await message.channel.send(f"The word is {self.hiddenword}. Now. Carefully, Solve it :smiling_imp:")
                await message.channel.send("Keep at it")

        # Category Get For truth seeking orbs
    

    def endchk(self):
        if "-" not in self.hiddenword or self.trycount >= 15:
            self.hangingchannel = None
            self.hanging = False
            self.trycount = 0
            return True
        else:
            return False


def setup(bot):
    bot.add_cog(Gaming(bot))
