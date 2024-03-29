import discord
from discord.ext import commands
import asyncio
import random
from random import randint

class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        if command.usage:
            return f'{self.clean_prefix}{command.name} {command.usage}'
        return f'{self.clean_prefix}{command.name}'

    def command_not_found(self, string):
        raise commands.CommandNotFound

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"Showing help for {command.qualified_name}",
            color=randint(0, 0xffffff)
        )
        if command.usage:
            embed.add_field(name="Usage:", value=f"```{self.clean_prefix}{command.name} {command.usage}```", inline=False)
        else:
            embed.add_field(name="Usage:", value=f"```{self.clean_prefix}{command.name}```", inline=False)

        embed.add_field(name="Brief:", value=f"```{command.brief}```", inline=False)
        embed.add_field(name="Help:", value=f"```{command.help}```", inline=False)
        if command.aliases:
            embed.add_field(name="Aliases", value=f"```{command.aliases}```")
        if command.cog:
            embed.add_field(name="Cog:", value=f"```{command.cog.qualified_name}```")
    
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_cog_help(self, cog):
        to_loop = await self.filter_commands(cog.get_commands())
        if not to_loop: await self.get_destination().send("This Cog has no commands."); return
        terminator = 1
        starting, ending = 0, 25
        if len(to_loop) > 25:
            terminator = len(to_loop) // 25 + 1
        for _ in range(terminator):
            embed = discord.Embed(
                title=f"Showing information on {cog.qualified_name}",
                description=cog.description,
                color=randint(0, 0xffffff)
            )
            for command in to_loop[starting:ending]:
                embed.add_field(name=f"{self.clean_prefix}{command.qualified_name}", value=f"```{command.brief}```")
            embed.set_footer(text=self.get_opening_note())

            try:
                author = self.context.author
                await author.send(embed=embed)
            except Exception:
                await self.get_destination().send(embed=embed)
            starting, ending = starting + 25, ending + 25
            await asyncio.sleep(1)


    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Showing help for you",
            color=randint(0, 0xffffff)
        )

        to_loop = [k for k in mapping.keys() if k]

        to_loop = list(set(to_loop))
        for cog in to_loop:
            if cog.description:
                embed.add_field(name=cog.qualified_name, value=f"```{cog.description}```")
            
        embed.set_footer(text=self.get_opening_note())
        await self.get_destination().send(embed=embed)

    
class MyHelp(commands.Cog):
    """Shows this help message"""

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self


def setup(bot):
    bot.add_cog(MyHelp(bot))