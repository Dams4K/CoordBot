import discord
from discord import option, SlashCommandGroup
from discord.ext import commands, pages
from data_management import *
from utils.bot_embeds import *
from utils.bot_autocompletes import *
from utils.bot_views import ConfirmView
from operator import attrgetter

class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    articles = SlashCommandGroup("articles")

    @articles.command(name="list")
    async def list_articles(self, ctx):
        articles = GuildArticle.list_articles(ctx.guild.id)
        sorted_articles = sorted(articles, key=attrgetter("_article_id"))

        embed_pages = []
        articles_description = []
        for i in range(len(sorted_articles)):
            article = sorted_articles[i]
            articles_description.append(f"{article.name} ({article._article_id})")
            if (i+1) % 20 == 0 or i+1 == len(sorted_articles):
                embed = NormalEmbed(ctx.guild_config, title="Articles")
                embed.description = "\n".join(articles_description)
                embed_pages.append(embed)
                articles_description.clear()
        
        paginator = pages.Paginator(pages=embed_pages)
        if hasattr(ctx, "interaction"):
            await paginator.respond(ctx.interaction)
        else:
            await paginator.send(ctx)
    
    @articles.command(name="create")
    @option("name", type=str, max_length=32, required=True)
    @option("price", type=float, required=True)
    async def create_article(self, ctx, name, price):
        guild_article = GuildArticle.new(ctx.guild.id, name).set_price(price)
    
    @articles.command(name="set_price")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("price", type=int, required=True)
    async def set_article_price(self, ctx, article, price):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
        else:
            article.set_price(price)
    
    @articles.command(name="add_object")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("obj", type=GuildObjectConverter, required=True, autocomplete=get_objects)
    @option("quantity", type=int, default=1)
    async def add_article_object(self, ctx, article: GuildArticle, obj: GuildObject, quantity):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
            return

        if obj is None:
            await ctx.respond(text_key="OBJECT_DOES_NOT_EXIST")
            return

        article.add_object(obj, quantity)
        await ctx.respond(text_key="ARTICLE_OBJECT_ADDED", text_args={"object": obj.name, "article": article.name})
    
    @articles.command(name="remove_object")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("obj", type=GuildObjectConverter, required=True, autocomplete=get_objects)
    async def remove_article_object(self, ctx, article: GuildArticle, obj: GuildObject):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
            return
        if obj is None:
            await ctx.respond(text_key="OBJECT_DOES_NOT_EXIST")
            return
        
        article.remove_object(obj)
        await ctx.respond(text_key="ARTICLE_OBJECT_REMOVED", text_args={"object": obj.name, "article": article.name})

    @articles.command(name="add_role")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("role", type=discord.Role, required=True)
    async def add_article_role(self, ctx, article: GuildArticle, role: discord.Role):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
            return
        
        article.add_role(role)
        embed = NormalEmbed(ctx.guild_config, title=ctx.translate("ARTICLE_ROLE_ADDED"), description=ctx.translate("ARTICLE_ROLE_ADDED_DESC", role=role.mention, article=article.name))
        await ctx.respond(embed=embed)
    
    @articles.command(name="remove_role")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("role", type=discord.Role, required=True)
    async def remove_article_role(self, ctx, article: GuildArticle, role: discord.Role):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
            return
        article.remove_role(role)
        embed = NormalEmbed(ctx.guild_config, title=ctx.translate("ARTICLE_ROLE_REMOVED"), description=ctx.translate("ARTICLE_ROLE_REMOVED_DESC", role=role.mention, article=article.name))
        await ctx.respond(embed=embed)

    @articles.command(name="about")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    async def article_about(self, ctx, article: GuildArticle):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
            return
        
        embed = NormalEmbed(ctx.guild_config, title=article.name, description=f"prix: {article.price}")
        embed.add_field(name="Roles", value="\n".join([ctx.guild.get_role(role_id).mention for role_id in article.role_ids]))
        embed.add_field(name="Objects", value="\n".join([f"{GuildObject(object_id, ctx.guild.id).name} | {amount}" for object_id, amount in article.object_ids.items()]))

        await ctx.respond(embed=embed)

    @articles.command(name="delete")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    async def delete_article(self, ctx, article: GuildArticle):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
        else:
            confirm_view = ConfirmView()
            confirm_embed = DangerEmbed(ctx.guild_config, title=ctx.translate("DELETION"), description=ctx.translate("ARTICLE_DELETION_CONFIRMATION", article=article.name))
            await ctx.respond(embed=confirm_embed, view=confirm_view)
            await confirm_view.wait()
            if confirm_view.confirmed:
                article.delete()
                await ctx.respond(text_key="ARTICLE_DELETION_PERFORMED", text_args={"article": article.name})
            else:
                await ctx.respond(text_key="DELETION_CANCELLED")

    @articles.command(name="buy")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    async def buy_article(self, ctx, article):
        if article is None:
            await ctx.respond(text_key="ARTICLE_DOES_NOT_EXIST")
        else:
            try:
                await article.buy(ctx)
                await ctx.respond(text_key="ARTICLE_PURCHASED", text_args={"article": article.name})
            except NotEnoughMoney:
                author_money = ctx.author_data.money

                embed = WarningEmbed(ctx.guild_config, title=ctx.translate("E_CANNOT_PURCHASE"))
                embed.description = ctx.translate("E_NOT_ENOUGH_MONEY", money_missing=article.price-author_money, author_money=author_money, article_price=article.price)
                await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ShopCog(bot))