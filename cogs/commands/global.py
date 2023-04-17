import discord
from discord import option
from discord.ext import bridge
from discord.ext import commands
from data_management import MemberData
from utils.bot_embeds import NormalEmbed

class GlobalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="profil")
    @option("member", type=discord.Member, required=False, default=None)
    async def profil(self, ctx, member = None):
        member = ctx.author if member == None else member
        await self.show_profil(ctx, member)
    
    @discord.user_command(name="profil")
    async def user_profil(self, ctx, member: discord.Member):
        await self.show_profil(ctx, member, ephemeral=True)
    
    async def show_profil(self, ctx, member: discord, ephemeral=False):
        member_data = MemberData(member.id, ctx.guild.id)

        xp_goal = member_data.get_xp_goal(ctx.guild_config.leveling_formula)
        embed = NormalEmbed(ctx.guild_config, title=ctx.translate("PROFIL_OF", member=member))
        embed.add_field(name=ctx.translate("LEVEL_NAME").capitalize(), value=str(member_data.level))
        embed.add_field(name=ctx.translate("XP_NAME").capitalize(), value=f"{member_data.xp}/{xp_goal}")
        embed.add_field(name=ctx.translate("MONEY_NAME").capitalize(), value=str(member_data.money))
        
        await ctx.respond(embed=embed, ephemeral=ephemeral)


    @bridge.bridge_command(name="utip")
    async def utip(self, ctx):
        embed = NormalEmbed(ctx.guild_config, title="UTIP")
        embed.description = """
[INSERER TEXT COOL]

[INSERER LIEN UTIP]
"""

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(GlobalCog(bot))