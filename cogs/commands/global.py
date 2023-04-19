from discord import *
from data_management import *
from utils.bot_embeds import *
from utils.bot_autocompletes import *

class GlobalCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    about = SlashCommandGroup("about")

    @about.command(name="object")
    @option("obj", type=GuildObjectConverter, required=True, autocomplete=get_objects)
    async def about_object(self, ctx, obj: GuildObject):
        if obj is None:
            await ctx.respond(text_key="OBJECT_DOES_NOT_EXIST")
            return
        
        embed = NormalEmbed(ctx.guild_config, title=obj.name, description=obj.description)
        await ctx.respond(embed=embed)

    @about.command(name="article")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_articles)
    async def about_article(self, ctx, article: GuildArticle):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
            return
        
        embed = NormalEmbed(ctx.guild_config, title=article.name, description=f"prix: {article.price}")

        roles = [ctx.guild.get_role(role_id).mention for role_id in article.role_ids]
        if roles != []:
            embed.add_field(name="Roles", value="\n".join(roles))
        
        objects = [f"{GuildObject(object_id, ctx.guild.id).name} | {amount}" for object_id, amount in article.object_ids.items()]
        if objects != []:
            embed.add_field(name="Objects", value="\n".join(objects))
        
        await ctx.respond(embed=embed)

    @slash_command(name="profil")
    @option("member", type=Member, required=False, default=None)
    async def slash_profil(self, ctx, member = None):
        member = ctx.author if member == None else member
        await self.show_profil(ctx, member)
    
    @user_command(name="profil")
    async def user_profil(self, ctx, member: Member):
        await self.show_profil(ctx, member, ephemeral=True)
    
    async def show_profil(self, ctx, member: Member, ephemeral=False):
        member_data = MemberData(member.id, ctx.guild.id)

        xp_goal = member_data.get_xp_goal(ctx.guild_config.leveling_formula)
        embed = NormalEmbed(ctx.guild_config, title=ctx.translate("PROFIL_OF", member=member))
        embed.add_field(name=ctx.translate("LEVEL_NAME").capitalize(), value=str(member_data.level))
        embed.add_field(name=ctx.translate("XP_NAME").capitalize(), value=f"{member_data.xp}/{xp_goal}")
        embed.add_field(name=ctx.translate("MONEY_NAME").capitalize(), value=str(member_data.money))
        
        await ctx.respond(embed=embed, ephemeral=ephemeral)


#     @bridge.bridge_command(name="utip")
#     async def utip(self, ctx):
#         embed = NormalEmbed(ctx.guild_config, title="UTIP")
#         embed.description = """
# [INSERER TEXT COOL]

# [INSERER LIEN UTIP]
# """

#         await ctx.respond(embed=embed)


    @slash_command(name="say")
    async def say(self, ctx, *, message: str):
        if ctx.is_app:
            await ctx.respond("message sent", ephemeral=True)
        else:
            await ctx.message.delete()
        
        await ctx.send(message)


def setup(bot):
    bot.add_cog(GlobalCog(bot))