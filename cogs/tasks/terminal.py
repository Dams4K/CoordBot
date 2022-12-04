import discord
import os
from discord.ext import commands
from discord.ext import tasks
from terminal import Terminal
from utils.references import References

class TerminalCog(commands.Cog):
    terminal = Terminal()

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.terminal.inject_cog(self)
        self.terminal.prefix = f"{self.bot.user} > "
        await self.terminal.start()

    @terminal.command(name="stop")
    async def stop(self):
        await self.bot.close()

    @terminal.command(name="reload", aliases=["rl"])
    async def reload(self):
        print("Cogs reloaded")
        self.bot.reload_cogs(References.COGS_FOLDER)
    
    @terminal.command(name="clear", aliases=["cls"])
    async def clear(self):
        os.system("clear||cls")


def setup(bot):
    return
    bot.add_cog(TerminalCog(bot))