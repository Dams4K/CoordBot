from operator import attrgetter

from discord import *
from discord.utils import escape_markdown, find
from prefixed import Float

from data_management import *
from utils.bot_commands import BotSlashCommandGroup
from utils.bot_embeds import NormalEmbed


class FormatterDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class RankingFormatter:
    EMOJIS = {
        1: "<:first:1132001952889327657>",
        2: "<:second:1132001951228375070>",
        3: "<:third:1132001948229447780>"
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
    
    def get_ranking_string(self, str_format: str, optionals: set = {}, max_competitor = 15, last_position: int = 10, **kwargs: dict) -> str:
        ranking: dict = self.get_ranking_list()

        str_list: list = []
        
        previous_competitor = None
        for i in range(len(ranking.keys())):
            position = list(ranking.keys())[i]
            if position > last_position: # Last position reached, we got all the competitor we need
                break

            next_position = list(ranking.keys())[i+1] if i < len(ranking)-1 else None
            competitors = ranking[position]

            next_competitor = ranking[next_position][0] if next_position != None else None
            
            # TODO: optimize
            previous_competitor_same_required = None
            next_competitor_same_required = None
            for sort_attr in self.sort_attrs:
                if sort_attr in optionals:
                    continue
                
                previous_competitor_attr = getattr(previous_competitor, sort_attr) if not previous_competitor is None else False
                competitor_attr = getattr(competitors[0], sort_attr)
                next_competitor_attr = getattr(next_competitor, sort_attr) if not next_position is None else False

                if previous_competitor_same_required is None:
                    previous_competitor_same_required = previous_competitor_attr == competitor_attr
                else:
                    previous_competitor_same_required = previous_competitor_same_required and previous_competitor_attr == competitor_attr

                if next_competitor_same_required is None:
                    next_competitor_same_required = next_competitor_attr == competitor_attr
                else:
                    next_competitor_same_required = next_competitor_same_required and next_competitor_attr == competitor_attr
            
            show_optionals = len(competitors) > 1 or previous_competitor_same_required or next_competitor_same_required

            for competitor in competitors:
                if len(str_list) >= max_competitor:
                    str_list.append("...")
                    break

                format_dict = {attr_name: getattr(competitor, attr_name) for attr_name in self.sort_attrs}
                format_dict.update({
                    "competitor": competitor,
                    "pos": position
                })
                can_be_shown = lambda k, v: callable(v) and (not k in optionals or (k in optionals and show_optionals))
                format_dict.update({k: (v(format_dict) if can_be_shown(k, v) else "") for k, v in kwargs.items()})

                str_list.append(str_format.format_map(FormatterDict(format_dict)))

                previous_competitor = competitor
            
            if len(str_list) >= max_competitor:
                    break
                
        return "\n".join(str_list)


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

        # WTF is going on????
        get_competitor_name = lambda d: escape_markdown(find(lambda m: m.id == d["competitor"]._member_id, ctx.guild.members).display_name)
        get_level = lambda d: f"{Float(d['competitor'].level):.2h}" if len(str(d["competitor"].level)) > 3 else d["competitor"].level
        get_xp = lambda d: f"({Float(d['competitor'].xp):.2h})" if len(str(d["competitor"].xp)) > 3 else f"({d['competitor'].xp})"
        get_pos = lambda d: RankingFormatter.EMOJIS[d['pos']] if d["pos"] in RankingFormatter.EMOJIS else f"{d['pos']}\."
        
        ranking_str = ranking_formatter.get_ranking_string("{pos} {competitor_name}: {level} {xp}", optional={"xp"}, competitor_name=get_competitor_name, level=get_level, xp=get_xp, pos=get_pos)
        
        embed = NormalEmbed(title=ctx.translate("LEVEL_RANKING"))
        embed.description = ranking_str if ranking_str != "" else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)
    
    @ranking.command(name="money")
    async def ranking_money(self, ctx):
        members_data = [MemberData(member.id, ctx.guild.id) for member in ctx.guild.members]
        default_member = DefaultMemberData(ctx.guild.id)
        members_data = list(filter(lambda md: md.money > default_member.money, members_data))
        
        ranking_formatter = RankingFormatter(members_data, ("money",))

        # WTF is going on????
        get_competitor_name = lambda d: escape_markdown(find(lambda m: m.id == d['competitor']._member_id, ctx.guild.members).display_name)
        get_money = lambda d: f"{Float(d['competitor'].money):.2h}" if len(str(d['competitor'].money)) > 3 else d['competitor'].money
        get_pos = lambda d: RankingFormatter.EMOJIS[d['pos']] if d["pos"] in RankingFormatter.EMOJIS else f"{d['pos']}\."

        ranking_str = ranking_formatter.get_ranking_string("{pos} {competitor_name}: {money}", competitor_name=get_competitor_name, money=get_money, pos=get_pos)
        
        embed = NormalEmbed(title=ctx.translate("MONEY_RANKING"))
        embed.description = ranking_str if ranking_str != "" else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RankingCog(bot))