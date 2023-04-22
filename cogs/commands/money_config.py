from discord import *
from data_management import MemberData

class MoneyConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    money = SlashCommandGroup("money", default_member_permissions=Permissions(administrator=True), guild_only=True)

    @money.command(name="add")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def add_money(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_money(amount)
        await ctx.respond(text_key="MONEY_ADDED", text_args={"amount": amount, "member": member})
        

    @money.command(name="remove")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def remove_money(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_money(-amount)
        await ctx.respond(text_key="MONEY_REMOVED", text_args={"amount": amount, "member": member})
    

    @money.command(name="set")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def set_money(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.set_money(amount)
        await ctx.respond(text_key="MONEY_SET", text_args={"amount": amount, "member": member})


def setup(bot):
    bot.add_cog(MoneyConfigCog(bot))