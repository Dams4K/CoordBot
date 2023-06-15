from discord import *

from data_management import *
from utils.bot_commands import BotSlashCommandGroup
from utils.bot_embeds import *


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

        await ctx.respond(text_key="DEFAULT_MEMBER_XP_CHANGED", text_args={"amount": amount})

    @member.command(name="level")
    @option("amount", type=int, required=True)
    async def member_level(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_level(amount)

        await ctx.respond(text_key="DEFAULT_MEMBER_LEVEL_CHANGED", text_args={"amount": amount})

    
    @member.command(name="money")
    @option("amount", type=int, required=True)
    async def member_money(self, ctx, amount: int):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_money(amount)

        await ctx.respond(text_key="DEFAULT_MEMBER_MONEY_CHANGED", text_args={"amount": amount})

    @member.command(name="show")
    async def member_show(self, ctx):
        default_member = DefaultMemberData(ctx.guild.id)

        xp_goal = default_member.get_xp_goal(ctx.guild_config.leveling_formula)
        embed = InformativeEmbed(title=ctx.translate("PROFIL_OF", member="*username#0000*"))
        embed.add_field(name=ctx.translate("LEVEL_NAME"), value=str(default_member.level))
        embed.add_field(name=ctx.translate("XP_NAME"), value=f"{default_member.xp}/{xp_goal}")
        embed.add_field(name=ctx.translate("MONEY_NAME"), value=str(default_member.money))
        
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(DefaultCog(bot))