from discord import *

from data_management import *
from utils.bot_commands import BotSlashCommandGroup
from utils.bot_embeds import *
from utils.permissions import *


class DefaultCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    default = BotSlashCommandGroup("default", default_member_permissions=Permissions(administrator=True), guild_only=True)
    member = default.create_subgroup("member")
    inventory = default.create_subgroup("inventory")

    @member.command(name="experience")
    @option("amount", type=int, required=True)
    async def member_xp(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_xp(amount)

    @member.command(name="level")
    @option("amount", type=int, required=True)
    async def member_level(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_level(amount)

    
    @member.command(name="money")
    @option("amount", type=int, required=True)
    async def member_money(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_money(amount)

    @member.command(name="show")
    async def member_show(self, ctx):
        default_member = DefaultMemberData(ctx.guild.id)

        xp_goal = default_member.get_xp_goal(ctx.guild_config.leveling_formula)
        embed = InformativeEmbed(title=ctx.translate("PROFIL_OF", member="*username#0000*"))
        embed.add_field(name=ctx.translate("LEVEL").capitalize(), value=str(default_member.level))
        embed.add_field(name=ctx.translate("XP").capitalize(), value=f"{default_member.xp}/{xp_goal}")
        embed.add_field(name=ctx.translate("MONEY").capitalize(), value=str(default_member.money))
        
        await ctx.respond(embed=embed)

    # @inventory.command(name="max-size")
    # @option("size", type=int, required=True)
    # async def default_size(self, ctx, size):
    #     default_member = DefaultMemberData(ctx.guild.id)
    #     inventory = default_member.get_inventory()

    #     inventory.max_size = size

    #     default_member.set_inventory(inventory)
    


def setup(bot):
    bot.add_cog(DefaultCog(bot))