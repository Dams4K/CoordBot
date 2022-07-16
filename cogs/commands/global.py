import discord
from discord.ext import commands
from discord.ext import bridge

class GlobalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_command(name="profil")
    async def profil(self, ctx):
        pass



def setup(bot):
    bot.add_cog(GlobalCog(bot))