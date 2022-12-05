import discord
from discord.ext import commands
from discord.ext import bridge

class StorageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_group(name="inventory")
    @bridge.map_to("show")
    async def inventory(self, ctx):
        await ctx.respond("test")
    
    @inventory.command()
    async def sell(self, ctx):
        await ctx.respond("sell item")

def setup(bot):
    bot.add_cog(StorageCog(bot))