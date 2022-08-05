import discord
from discord.ext import commands
from discord.ext import tasks
from terminal import Terminal

class TerminalCog(commands.Cog):
    terminal = Terminal()

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.terminal.inject_cog(self)
        await self.terminal.start()

    @terminal.command(name="stop")
    async def stop(self):
        await self.bot.close()



def setup(bot):
    bot.add_cog(TerminalCog(bot))