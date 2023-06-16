from discord import *
from data_management import *
from operator import attrgetter
from prefixed import Float
from utils.bot_embeds import NormalEmbed
from utils.bot_commands import BotSlashCommandGroup

class FormatterDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class RankingFormatter:
    EMOJIS = {
        1: "<:First:798229195549179915>",
        2: "<:Second:798266104761024582>",
        3: "<:Third:798229194743611434> "
    }

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
        
        previous_competitor = None
        for i in range(len(ranking.keys())):
            position = list(ranking.keys())[i]
            next_position = list(ranking.keys())[i+1] if i < len(ranking)-1 else None
            competitors = ranking[position]

            next_competitor = ranking[next_position][0] if next_position != None else None
            same_level_previous = previous_competitor != None and previous_competitor.level == competitors[0].level
            same_level_next = next_position != None and next_competitor.level == competitors[0].level

            show_optionals = len(competitors) > 1 or same_level_previous or same_level_next

            for competitor in competitors:
                format_dict = {attr_name: getattr(competitor, attr_name) for attr_name in self.sort_attrs}
                format_dict.update({
                    "competitor": competitor,
                    "pos": position
                })
                can_be_shown = lambda k, v: callable(v) and (not k in optional or (k in optional and show_optionals))
                format_dict.update({k: (v(format_dict) if can_be_shown(k, v) else "") for k, v in kwargs.items()})

                str_list.append(str_format.format_map(FormatterDict(format_dict)))

                previous_competitor = competitor

        return "\n".join(str_list[:15]) # 15 max number of competitors shown



class RankingCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    ranking = BotSlashCommandGroup("ranking", guild_only=True)

    @ranking.command(name="level")
    async def ranking_level(self, ctx):
        members_data = [MemberData(member.id, ctx.guild.id) for member in ctx.guild.members]
        default_member = DefaultMemberData(ctx.guild.id)
        members_data = list(filter(lambda md: md.level > default_member.level or md.xp > default_member.xp, members_data))

        ranking_formatter = RankingFormatter(members_data, ("level", "xp"))

        get_competitor_name = lambda d: discord.utils.find(lambda m: m.id == d["competitor"]._member_id, ctx.guild.members)
        get_level = lambda d: f"{Float(d['competitor'].level):.2h}" if len(str(d["competitor"].level)) > 3 else d["competitor"].level
        get_xp = lambda d: f"({Float(d['competitor'].xp):.2h})" if len(str(d["competitor"].xp)) > 3 else f"({d['competitor'].xp})"
        get_pos = lambda d: RankingFormatter.EMOJIS[d['pos']] if d["pos"] in RankingFormatter.EMOJIS else f"{d['pos']}."
        
        ranking_str = ranking_formatter.get_ranking_string("{pos} {competitor_name.mention}: {level} {xp}", optional={"xp"}, competitor_name=get_competitor_name, level=get_level, xp=get_xp, pos=get_pos)
        
        embed = NormalEmbed(title=ctx.translate("LEVEL_RANKING"))
        embed.description = ranking_str if ranking_str != "" else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)
    
    @ranking.command(name="money")
    async def ranking_level(self, ctx):
        members_data = [MemberData(member.id, ctx.guild.id) for member in ctx.guild.members]
        default_member = DefaultMemberData(ctx.guild.id)
        members_data = list(filter(lambda md: md.money > default_member.money, members_data))
        
        ranking_formatter = RankingFormatter(members_data, ("money",))

        get_competitor_name = lambda d: discord.utils.find(lambda m: m.id == d['competitor']._member_id, ctx.guild.members)
        get_money = lambda d: f"{Float(d['competitor'].money):.2h}" if len(str(d['competitor'].money)) > 3 else d['competitor'].money
        get_pos = lambda d: RankingFormatter.EMOJIS[d['pos']] if d["pos"] in RankingFormatter.EMOJIS else f"{d['pos']}."

        ranking_str = ranking_formatter.get_ranking_string("{pos} {competitor_name.mention}: {money}", competitor_name=get_competitor_name, money=get_money, pos=get_pos)

        embed = NormalEmbed(title=ctx.translate("MONEY_RANKING"))
        embed.description = ranking_str if ranking_str != "" else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RankingCog(bot))