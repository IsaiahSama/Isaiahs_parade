import discord
from discord.ext import commands
import asyncio
from random import randint
import random
from gameclass import wordgame
import os


class Gaming(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    isaiah = 493839592835907594

    if os.path.exists("hangwords.txt"):
        with open("hangwords.txt") as w:
            x = w.read()
            word_list = x.split(',')

    else:
        word_list = []

    banana_count = 0


    channels = []

    @commands.command()
    async def startstory(self, ctx):
        
        if await self.chancheck(ctx.channel.id):
            await ctx.send("A story is already being told here or hangman is being played here")
            return

        storygame = wordgame(ctx.channel.id, "story")
        self.channels.append(storygame)
        
        await ctx.send("""Story mode has been activated. Get your friends and tell a story one word at a time.
        Use <>endstory to exit story mode and see the full story
        BEGIN!""")


    @commands.command()
    async def endstory(self, ctx):
        if not await self.chancheck(ctx.channel.id):
            await ctx.send("You haven't started a story as yet. Do so with <>startstory")
            return

        else:
            wordstory = await self.getobj(ctx.channel.id)
            if wordstory.mode != "story":
                await ctx.send("There was never a story being told here :face_with_monocle:")
                return

            await ctx.send("Behold your story")

            tale = " ".join(wordstory.storywords)

            if len(tale) <= 1024:
                story = discord.Embed(
                    title="Listen Closely",
                    description=f"Here is the story that the awesome people in {ctx.guild} has created",
                    color=randint(0, 0xffffff)
                )

                story.set_thumbnail(url=ctx.guild.icon_url)
                story.add_field(name="And it goes like", value=f"{tale}")

                await ctx.send(embed=story)
            
            else:
                await ctx.send(f"**{tale}**")

            self.channels.remove(wordstory)


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
        
        with open("hangwords.txt", "w") as w:
            x = ', '.join(self.word_list)
            w.write(x)

        await ctx.send("Words have been added :thumbsup:")


    @commands.command()
    async def wordshow(self, ctx):
        if not self.word_list:
            await ctx.send("No words to send")
            return
        x = ', '.join(self.word_list[:150])
        await ctx.send(x)


    # Clears words from hangman
    @commands.command()
    async def wordremove(self, ctx, *, words):
        words = words.split(', ')
        if not self.word_list:
            await ctx.send("There are no words to remove")
            return
        for word in words:
            if word in self.word_list:
                self.word_list.remove(word)
            else:
                await ctx.send(f"{word} was not found in word list")
        with open("hangwords.txt", "w") as w:
            x = ', '.join(self.word_list)
            w.write(x)

        await ctx.send("Succesfully removed words")


    # Start hang game
    @commands.command()
    async def startgame(self, ctx):
        if len(self.word_list) < 2:
            await ctx.send("Not enough words. Add with <>wordadd {words}")
            return
        
        if await self.chancheck(ctx.channel.id):
            await ctx.send("Either a hangman game is in progress, or a story is being told. Please go elsewhere")
            return
        
        else:
            word = random.choice(self.word_list)
            word = word.rstrip()
            hanggame = wordgame(ctx.channel.id, "hang", hangword=word, trycount=0)
            hanggame.hiddenword = await self.hide_word(hanggame)
            await ctx.send(f"The word is {hanggame.hiddenword}. Now. Carefully, Solve it :smiling_imp:")
            self.channels.append(hanggame)



    @commands.command()
    async def endgame(self, ctx):
        if await self.chancheck(ctx.channel.id):
            hangobj = await self.getobj(ctx.channel.id)
            if hangobj.mode != "hang":
                await ctx.send("No one was playing hangman here")
                return

            await ctx.send(f"Aww... Game is over. The word was {hangobj.hangword}. Maybe Next time")
            self.channels.remove(hangobj)
        
        else:
            await ctx.send("Start a game wtih <>startgame before ending it :bowing:")

    
    async def hide_word(self, hangobject):
        word = hangobject.hangword
        hidden_word = []
        for letter in word:
            if letter == " ":
                hidden_word.append(" ")
            else:
                hidden_word.append("-")

        hidden_word = "".join(hidden_word)
        return hidden_word

    async def chancheck(self, idtochk):
        for chan in self.channels:
            if idtochk == chan.chanid:
                return True

        else:
            return False

    async def getobj(self, idtoget):
        for chan in self.channels:
            if idtoget == chan.chanid:
                return chan


    @commands.Cog.listener()
    async def on_message(self, message):

        # On message is called when bot receives a message
        if message.author == self.bot.user:
            # Makes sure that bot messages are ignored
            return

        if message.content.startswith("<>"):
            return
        
        if not await self.chancheck(message.channel.id):

            if self.bot.user in message.mentions:
                await message.channel.send(":sunglasses:To view my commands use <>help")            

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
            
        else:
            chanobj = await self.getobj(message.channel.id)
            if chanobj.mode == "story":
                chanobj.storywords.append(f" {message.content}")
                print(chanobj.storywords)
            else:
                game_done = await self.endchk(chanobj)
                # Sets Message.content To X
                x = message.content.lower()
                # Checks to make sure that team has Tries left
                if chanobj.trycount < 15:
                    # Checks to see if the message's content is the same as the selected word
                    word = "".join(chanobj.hangword)
                    if x == word:
                        chanobj.hiddenword = word
                        game_done = await self.endchk(chanobj)
                    # Checks to see if the message's content is in the word, and that the length of the message is 1
                    elif x in word and len(x) == 1:
                        # Loops through each letter in the word
                        for chance in range(len(word)):
                            # if the message's content is the same as a letter in the word
                            if x == list(word)[chance]:
                                # Turn Hidden word into a list.
                                hiddenword = list(chanobj.hiddenword)
                                # Using the same index, set the character at that index to the message's content
                                hiddenword[chance] = x
                                # Turns the hidden word into a string again
                                chanobj.hiddenword = "".join(hiddenword)
                    # If message's content is in the word... and the length of the message is more than 1
                    elif x in word:
                        # Sets a variable index_of, to the position of where the first instance of x is found
                        index_of = word.find(x)
                        # Turns hidden word into a list
                        hiddenword = list(chanobj.hiddenword)
                        # Sets a variable letter index to 0.
                        letterindex = 0
                        # For i in range index_of to the length of x + index_of
                        for i in range(index_of, len(x) + index_of):
                            # Sets the character at that position, to be equal to the letter in x it's position
                            hiddenword[i] = x[letterindex]
                            letterindex += 1
                        # turns hidden word into a string
                        chanobj.hiddenword = "".join(hiddenword)

                    else:
                        chanobj.trycount += 1
                        await message.channel.send(
                            f"""That is not in the word. Remember, You can only have a maximum of 15 incorrect attempts.
        You are currently at {chanobj.trycount}""")

                game_done = await self.endchk(chanobj)
                if game_done:
                    await message.channel.send(f"Game over. The word is {word}")
                    self.channels.remove(chanobj)
                else:
                    await message.channel.send(f"The word is {chanobj.hiddenword}. Now. Carefully, Solve it :smiling_imp:")
                    await message.channel.send("Keep at it")
    

    async def endchk(self, obj):
        if "-" not in obj.hiddenword or obj.trycount >= 15:
            return True
        else:
            return False


def setup(bot):
    bot.add_cog(Gaming(bot))
