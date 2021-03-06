import discord
from discord.ext import commands, tasks
import asyncio
import random
from random import randint
import os

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    now_playing = []

    @commands.command()
    @commands.is_owner()
    async def joinme(self, ctx):
        vc = ctx.author.voice
        if vc == None:
            await ctx.send("You are not in a voice channel")
            return
        try:
            await vc.channel.connect()
            await ctx.send(f"Successfully connected to {vc.channel.name}")
            # await ctx.voice_client.play(discord.FFmpegOpusAudio("isehjoin.mp3"))
        except:
            await ctx.send(f"You in the wrong channel bruv... I'm in {ctx.voice_client.channel.name}")

    @commands.command()
    @commands.is_owner()
    async def playtune(self, ctx, *, song=None):
        vc = ctx.author.voice
        if vc is None:
            await ctx.send("You ain't in a voice channel")
            return

        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel")
            return

        if vc.channel != ctx.voice_client.channel:
            await ctx.send(f"You in the wrong channel... I'm in {ctx.voice_client.channel.name}")
            return

        content = os.listdir("C:\\Users\\zelda\\onedrive\\music")
        
        content = set(content)
        content = list(content)
        if song is None:
            link = random.choice(content)

        elif not song.isnumeric():
            link = [s for s in content if song.lower() in s.lower()]
            if link:
                if len(link) > 1:
                    allz = "\n".join(link)
                    await ctx.send(allz)
                    return
                link = link[0]
            else:
                await ctx.send("That sound could not be found")
                link = random.choice(content)
        else:
            song = int(song)
            await ctx.send(f"Playing {song} songs")
            await self.playmore(ctx, content, song)


        if ctx.voice_client.is_connected():
            await ctx.send(f"Playing {link}")
            source = discord.FFmpegOpusAudio(f"C:\\users\\zelda\\onedrive\\music\\{link}")
            ctx.voice_client.play(source)
        

    @commands.command()
    @commands.is_owner()
    async def groove(self, ctx, *, song):       
        content = list(set(os.listdir("C:\\Users\\zelda\\onedrive\\music")))

        link = [s for s in content if song.lower() in s.lower()]
        if link:
            if len(link) > 1:
                allz = "\n".join(link)
                await ctx.send(allz)
                return
            link = link[0]
            await ctx.send(link)
            os.system(f'\"{link}\"')
        else:
            await ctx.send("That sound could not be found") 

    @commands.command()
    @commands.is_owner()
    async def playall(self, ctx):
        vc = ctx.author.voice
        if vc is None:
            await ctx.send("You ain't in a voice channel dawg")
            return

        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel")
            return

        if vc.channel != ctx.voice_client.channel:
            await ctx.send(f"You in the wrong channel bruv... I'm in {ctx.voice_client.channel.name}")
            return

        content = list(set(os.listdir("C:\\Users\\zelda\\onedrive\\music")))
        await self.playmore(ctx, content)

    async def playmore(self, ctx, content):
        link = random.choice(content)
        for x in range(len(content)):
            await ctx.send(f"Now Playing: Number {x}: {link}")
            source = discord.FFmpegOpusAudio(f"C:\\users\\zelda\\onedrive\\music\\{link}")
            
            link = random.choice(content)
            ctx.voice_client.play(source)
            while ctx.voice_client.is_playing():
                await asyncio.sleep(5)
            
        return
            
    @commands.command()
    @commands.is_owner()
    async def alarm(self, ctx, time: int):
        await ctx.send(f"Set an alarm for {time} minutes")
        # time *= 60
        await asyncio.sleep(time)    

    @commands.command()
    @commands.is_owner()
    async def jazzclock(self, ctx, member:discord.Member):
        await ctx.send(f"Waiting for {member.name} to come online")
        while member.status == discord.Status.offline: 
            await asyncio.sleep(20)
            
        await asyncio.sleep(5)
        vc = ctx.author.voice
        await vc.channel.connect()
        content = os.listdir("C:\\Users\\zelda\\onedrive\\music")
        link = random.choice(content)
        source = discord.FFmpegOpusAudio(f"C:\\users\\zelda\\onedrive\\music\\{link}")
        
        counter = 0
        await member.send("Welcome to the realm of online my jazz >:)")
        await ctx.author.send("hey hey... awaken")
        await ctx.send(f"{ctx.author.mention} awaken my good sir")
        while True:
            counter += 1
            try:
                ctx.voice_client.play(source)
                while ctx.voice_client.is_playing(): 
                    await asyncio.sleep(10)
                    continue
            except AttributeError:
                break
            if counter == 10: break




    @commands.command()
    @commands.is_owner()
    async def pause(self, ctx):
        vc = ctx.author.voice
        if vc is None:
            await ctx.send("You ain't in a voice channel dawg")
            return

        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel")
            return

        if vc.channel != ctx.voice_client.channel:
            await ctx.send("You in the wrong channel bruv... like actually Or maybe I'm not in one :thinking:")
            return

        if not ctx.voice_client.is_paused():
            ctx.voice_client.pause()
        else:
            await ctx.send("How much quieter do you want me to be '-'")

    @commands.command()
    async def resume(self, ctx):
        vc = ctx.author.voice
        if vc is None:
            await ctx.send("You ain't in a voice channel dawg")
            return

        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel")
            return

        if vc.channel != ctx.voice_client.channel:
            await ctx.send("You in the wrong channel bruv... like actually Or maybe I'm not in one :thinking:")
            return
            
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            await ctx.send("I WAS always playing for you")

    @commands.command()
    async def stop(self, ctx):
        vc = ctx.author.voice
        if vc is None:
            await ctx.send("You ain't in a voice channel dawg")
            return
            
        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel")
            return

        if vc.channel != ctx.voice_client.channel:
            await ctx.send("You in the wrong channel bruv... like actually Or maybe I'm not in one :thinking:")
            return
            
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        else:
            await ctx.send("Bye BYe")
        

    @commands.command(aliases=["dc"])
    async def leaveme(self, ctx):
        await ctx.send(f"Left {ctx.voice_client.channel.name}")
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))
