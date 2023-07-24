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
    
    def get_ranking_string(self, str_format: str, max_competitors = 15, last_position: int = 10, differentiators: set = {}, optionals: set = {}, **kwargs: dict) -> str:
        ranking: dict = self.get_ranking_list()
        total_competitors = 0

        str_list: list = []

        previous_show_optionals = False
        for i, (position, competitors) in enumerate(ranking.items()):
            # Last position is reached?
            if position > last_position:
                break
            
            # Get next pos competitor
            next_pos_competitor = next_pos_competitor_attrs = None
            next_pos_competitor_differentiating_attrs = {}
            if i+1 < len(ranking):
                next_pos_competitor = list(ranking.values())[i+1][0]
                next_pos_competitor_attrs = self.get_competitor_attrs(next_pos_competitor)
                next_pos_competitor_differentiating_attrs = {k: v for k, v in next_pos_competitor_attrs.items() if k in differentiators}

            for competitor in competitors:
                if total_competitors >= max_competitors:
                    str_list.append("...")
                    break

                competitor_attrs = self.get_competitor_attrs(competitor)
                competitor_attrs.update({
                    "competitor": competitor,
                    "pos": position
                })

                competitor_differentiating_attrs = {k: v for k, v in competitor_attrs.items() if k in differentiators}

                show_optionals = next_pos_competitor_differentiating_attrs == competitor_differentiating_attrs

                format_dict = {}
                can_be_shown = lambda k, v: callable(v) and (not k in optionals or (k in optionals and (show_optionals or previous_show_optionals)))
                format_dict.update({k: (v(competitor_attrs) if can_be_shown(k, v) else "") for k, v in kwargs.items()})

                previous_show_optionals = show_optionals

                str_list.append(str_format.format_map(FormatDict(format_dict)))
                total_competitors += 1

            if total_competitors >= max_competitors:
                    break

        return "\n".join(str_list), total_competitors or last_position
    
    
    def get_competitor_attrs(self, competitor):
        return {attr_name: getattr(competitor, attr_name) for attr_name in self.sort_attrs}


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
        get_level = lambda d: f"{Float(d['level']):.2h}" if len(str(d["level"])) > 3 else d["level"]
        get_xp = lambda d: f"({Float(d['xp']):.2h})" if len(str(d["xp"])) > 3 else f"({d['xp']})"
        # get_xp = lambda d: print(d)
        get_pos = lambda d: RankingFormatter.EMOJIS[d['pos']] if d["pos"] in RankingFormatter.EMOJIS else f"{d['pos']}\."
        
        ranking_str, competitors_number = ranking_formatter.get_ranking_string("{pos} {competitor_name}: {level} {xp}", differentiators={"level"}, optionals={"xp"}, competitor_name=get_competitor_name, level=get_level, xp=get_xp, pos=get_pos)
        
        embed = NormalEmbed(title=ctx.translate("LEVEL_RANKING", competitors_number=competitors_number))
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

        ranking_str, competitors_number = ranking_formatter.get_ranking_string("{pos} {competitor_name}: {money}", differentiators={"money"}, competitor_name=get_competitor_name, money=get_money, pos=get_pos)
        
        embed = NormalEmbed(title=ctx.translate("MONEY_RANKING", competitors_number=competitors_number))
        embed.description = ranking_str if ranking_str != "" else ctx.translate("NOBODY_IN_RANKING")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RankingCog(bot))