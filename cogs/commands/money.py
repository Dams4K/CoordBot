import discord
from discord import option, SlashCommandGroup
from discord.ext import commands
from utils.permissions import is_admin
from data_management import MemberData

class MoneyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        return is_admin(ctx)

    money = SlashCommandGroup("money")

    @money.command(name="add")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def add_money(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_money(amount)
        await ctx.respond(text_key="MONEY_ADDED", text_args={"amount": amount, "member": member})
        

    @money.command(name="remove")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def remove_money(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_money(-amount)
        await ctx.respond(text_key="MONEY_REMOVED", text_args={"amount": amount, "member": member})
    

    @money.command(name="set")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def set_money(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.set_money(amount)
        await ctx.respond(text_key="MONEY_SET", text_args={"amount": amount, "member": member})


def setup(bot):
    bot.add_cog(MoneyCog(bot))