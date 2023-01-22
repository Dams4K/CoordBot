import discord
from discord import option
from discord.commands import slash_command, SlashCommandGroup
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import is_admin
from data_management import MemberData

class MoneyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @bridge.bridge_group(checks=[is_admin])
    async def money(self, ctx): pass

    @money.command(name="add")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def add_money(self, ctx, member, amount):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.add_money(amount)
        await ctx.respond(text_key="MONEY_ADDED", text_args={"amount": amount, "member": member})
        

    @money.command(name="remove")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def remove_money(self, ctx, member, amount):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.add_money(-amount)
        await ctx.respond(text_key="MONEY_REMOVED", text_args={"amount": amount, "member": member})
    

    @money.command(name="set")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def set_money(self, ctx, member, amount):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.set_money(amount)
        await ctx.respond(text_key="MONEY_SET", text_args={"amount": amount, "member": member})

        

def setup(bot):
    bot.add_cog(MoneyCog(bot))