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
    @option("amount", type=int, required=True)
    async def member_xp(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_xp(amount)
    
    @member.command(name="default_level")
    @option("amount", type=int, required=True)
    async def member_level(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_level(amount)
    
    @member.command(name="default_money")
    @option("amount", type=int, required=True)
    async def member_money(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_money(amount)


def setup(bot):
    bot.add_cog(DefaultMemberCog(bot))