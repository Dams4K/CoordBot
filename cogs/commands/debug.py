import discord
from discord.ext import commands
from discord.ext import bridge

class DebugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_command(name="hello")
    async def profil(self, ctx):
        await ctx.respond("world")



def setup(bot):
    bot.add_cog(DebugCog(bot))