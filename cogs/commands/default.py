from discord import *
from utils.permissions import *
from data_management import *

class DefaultCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    default = SlashCommandGroup("default", default_member_permissions=Permissions(administrator=True))
    member_sub = default.create_subgroup("member")
    inventory_sub = default.create_subgroup("inventory")

    @member_sub.command(name="xp")
    @option("amount", type=int, required=True)
    async def default_xp(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_xp(amount)

    @member_sub.command(name="level")
    @option("amount", type=int, required=True)
    async def default_level(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_level(amount)

    
    @member_sub.command(name="money")
    @option("amount", type=int, required=True)
    async def default_money(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_money(amount)

    @inventory_sub.command(name="max-size")
    @option("size", type=int, required=True)
    async def default_size(self, ctx, size):
        pass


def setup(bot):
    bot.add_cog(DefaultCog(bot))