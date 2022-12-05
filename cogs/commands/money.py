import discord
from discord import Option
from discord.commands import slash_command, SlashCommandGroup
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import is_admin
from utils.data_management import MemberData

class MoneyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    money = SlashCommandGroup("money", "money management")
    money.checks = [is_admin]

    @money.command(name="add")
    async def add_money(self, ctx,
        member: Option(discord.Member, "member", required=True),
        amount: Option(int, "amount", required=True),
    ):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.add_money(amount)
        await ctx.respond("qsdqsdqsdqsd")
        

    @money.command(name="remove")
    async def remove_money(self, ctx,
        member: Option(discord.Member, "member", required=True),
        amount: Option(int, "amount", required=True),
    ):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.add_money(-amount)
        await ctx.respond("qsdqsdqsdqsd")
    

    @money.command(name="set")
    async def set_money(self, ctx,
        member: Option(discord.Member, "member", required=True),
        amount: Option(int, "amount", required=True),
    ):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.set_money(amount)
        await ctx.respond("qsdqsdqsdqsd2")

        

def setup(bot):
    bot.add_cog(MoneyCog(bot))