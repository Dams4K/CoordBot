import discord
from discord.ext import commands, bridge
from data_management import *
from utils.bot_embeds import NormalEmbed
from operator import attrgetter
from prefixed import Float

class RankingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group()
    async def ranking(self, ctx):
        pass

    @ranking.command(name="level")
    async def ranking_level(self, ctx):
        members_data = [MemberData(member.id, ctx.guild.id) for member in ctx.guild.members]
        default_member = GuildDefaultMemberData(ctx.guild.id)
        members_data = list(filter(lambda md: md.level > default_member.level or md.xp > default_member.xp, members_data))
        members_data.sort(key=attrgetter("level", "xp"), reverse=True)
        
        formatted_top = []
        for i in range(0, min(15, len(members_data))):
            member_data = members_data[i]
            member = discord.utils.find(lambda m: m.id == member_data._member_id, ctx.guild.members)
            formatted_top.append(f"{i+1}. {member.name if member is not None else None}: {member_data.level} ({Float(member_data.xp):.2h})")

        embed = NormalEmbed(ctx.guild_config, title="Top 15 levels")
        embed.description = "\n".join(formatted_top) if formatted_top != [] else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)
    
    @ranking.command(name="money")
    async def ranking_level(self, ctx):
        members_data = [MemberData(member.id, ctx.guild.id) for member in ctx.guild.members]
        default_member = GuildDefaultMemberData(ctx.guild.id)
        members_data = list(filter(lambda md: md.money > default_member.money, members_data))
        members_data.sort(key=attrgetter("money"), reverse=True)
        
        formatted_top = []
        for i in range(0, min(15, len(members_data))):
            member_data = members_data[i]
            member = discord.utils.find(lambda m: m.id == member_data._member_id, ctx.guild.members)
            formatted_top.append(f"{i+1}. {member.name if member is not None else None}: {Float(member_data.money):.2h}")

        embed = NormalEmbed(ctx.guild_config, title="Top 15 money")
        embed.description = "\n".join(formatted_top) if formatted_top != [] else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RankingCog(bot))