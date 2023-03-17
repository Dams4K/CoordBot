import discord
from discord.ext import commands, bridge
from data_management import *
from operator import attrgetter
from prefixed import Float
from utils.bot_embeds import NormalEmbed

class FormatterDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class RankingFormatter:
    def __init__(self, competitors, sort_attrs: list):
        self.competitors = competitors
        self.sort_attrs = sort_attrs
    
    def get_ranking_list(self) -> dict:
        sorted_competitors: list = sorted(self.competitors, key=attrgetter(*self.sort_attrs), reverse=True)
        
        ranking: dict = {}
        last_position = None
        last_attrs = [None] * len(self.sort_attrs)
        for i in range(len(sorted_competitors)):
            competitor = sorted_competitors[i]
            
            position = i+1
            current_attrs = [getattr(competitor, attr_name) for attr_name in self.sort_attrs]
            if last_attrs == current_attrs:
                position = last_position
            
            last_position = position
            last_attrs = current_attrs

            ranking.setdefault(position, [])
            ranking[position].append(competitor)

        return ranking
    
    def get_ranking_string(self, str_format: str, optional: set = {}, **kwargs: dict) -> str:
        ranking: dict = self.get_ranking_list()

        str_list: list = []
        for i in range(len(ranking)):
            position = list(ranking.keys())[i]
            for competitor in ranking[position]:
                format_dict = {attr_name: getattr(competitor, attr_name) for attr_name in self.sort_attrs}
                format_dict.update({
                    "competitor": competitor,
                    "pos": position
                })
                format_dict.update({k: v(competitor) for k, v in kwargs.items() if callable(v)})

                str_list.append(str_format.format_map(FormatterDict(format_dict)))
        
        return "\n".join(str_list)



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

        ranking_formatter = RankingFormatter(members_data, ("level", "xp"))

        get_competitor_name = lambda c: discord.utils.find(lambda m: m.id == c._member_id, ctx.guild.members)
        get_level = lambda c: f"{Float(c.level):.2h}" if len(str(c.level)) > 3 else c.level
        get_xp = lambda c: f"({Float(c.xp):.2h})" if len(str(c.xp)) > 3 else f"({c.xp})"
        
        ranking_str = ranking_formatter.get_ranking_string("{pos}. {competitor_name.name}: {level} {xp}", optional={"xp"}, competitor_name=get_competitor_name, level=get_level, xp=get_xp)
        
        embed = NormalEmbed(ctx.guild_config, title="Top 15 levels")
        embed.description = ranking_str if ranking_str != "" else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)
    
    @ranking.command(name="money")
    async def ranking_level(self, ctx):
        members_data = [MemberData(member.id, ctx.guild.id) for member in ctx.guild.members]
        default_member = GuildDefaultMemberData(ctx.guild.id)
        members_data = list(filter(lambda md: md.money > default_member.money, members_data))
        
        ranking_formatter = RankingFormatter(members_data, ("money",))

        get_competitor_name = lambda c: discord.utils.find(lambda m: m.id == c._member_id, ctx.guild.members)
        get_money = lambda c: f"{Float(c.money):.2h}" if len(str(c.money)) > 3 else c.money

        ranking_str = ranking_formatter.get_ranking_string("{pos}. {competitor_name.name}: {money}", competitor_name=get_competitor_name, money=get_money)

        embed = NormalEmbed(ctx.guild_config, title="Top 15 money")
        embed.description = ranking_str if ranking_str != "" else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RankingCog(bot))