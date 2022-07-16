import discord
from discord.ext import commands
from discord.ext import bridge
from utils.bot_customization import BotEmbed
from utils.utils import aexec

class DebugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_command(name="hello")
    async def hello(self, ctx):
        embed = BotEmbed("Test")
        await ctx.respond(embed=embed)
    

def setup(bot):
    bot.add_cog(DebugCog(bot))