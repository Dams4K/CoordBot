import discord
from discord import Option
from discord.ext import bridge
from discord.ext import commands
from utils.data_management import MemberData
from utils.bot_customization import BotEmbed

class GlobalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="profil")
    async def slash_profil(self, ctx, member: Option(discord.Member, "member", required=False) = None):
        await ctx.respond(**await self.profil(ctx, member))

    @commands.command(name="profil")
    async def cmd_profil(self, ctx, member: discord.Member = None):
        await ctx.send(**await self.profil(ctx, member))

    async def profil(self, ctx, member):
        member = ctx.author if member == None else member
        member_data = MemberData(ctx.guild.id, member.id)

        embed = BotEmbed(ctx, title="Profil de " + str(member))
        embed.add_field(name="XP", value=str(member_data.xp))
        embed.add_field(name="Coins", value=str(member_data.money))

        return {"embed": embed}
    
    @bridge.bridge_command(name="utip")
    async def utip(self, ctx):
        embed = BotEmbed(ctx, title="UTIP")
        embed.description = """
[INSERER TEXT COOL]

[INSERER LIEN UTIP]
"""

        await ctx.respond(embed=embed)
        
    @bridge.bridge_command(name="user")
    async def user_info(self, ctx, user: discord.User = None):
        if user == None: user = ctx.author

        await ctx.respond(user.created_at)

def setup(bot):
    bot.add_cog(GlobalCog(bot))