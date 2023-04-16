import discord
from discord import option
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import *
from data_management import *

class DefaultMemberCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group()
    async def member(self, ctx):
        pass
    
    @member.command(name="default_xp")
    @option("value", type=int, required=True)
    async def member_xp(self, ctx, value: int):
        pass


def setup(bot):
    bot.add_cog(DefaultMemberCog(bot))