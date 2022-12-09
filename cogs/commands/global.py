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
        member_data = MemberData(ctx.guild.id, member.id)

        embed = NormalEmbed(ctx.guild_config, title="Profil de " + str(member))
        embed.add_field(name="XP", value=str(member_data.xp))
        embed.add_field(name="Coins", value=str(member_data.money))

        await ctx.respond(embed=embed)
    
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