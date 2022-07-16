import discord
from discord import Option
from discord.commands import slash_command, SlashCommandGroup
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import *
from utils.bot_contexts import MemberData

class LevelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    xp = SlashCommandGroup("xp", "xp management")
    xp.checks = [is_admin]

    @xp.command(name="add")
    async def add_xp(self, ctx,
        member: Option(discord.Member, "member", required=True),
        amount: Option(int, "amount", required=True),
    ):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.add_xp(amount)
        await ctx.respond("qsdqsdqsdqsd")
        

    @xp.command(name="remove")
    async def remove_xp(self, ctx,
        member: Option(discord.Member, "member", required=True),
        amount: Option(int, "amount", required=True),
    ):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.remove_xp(amount)
        await ctx.respond("qsdqsdqsdqsd")
    

    @xp.command(name="set")
    async def remove_xp(self, ctx,
        member: Option(discord.Member, "member", required=True),
        amount: Option(int, "amount", required=True),
    ):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.set_xp(amount)
        await ctx.respond("qsdqsdqsdqsd")


def setup(bot):
    bot.add_cog(LevelsCog(bot))