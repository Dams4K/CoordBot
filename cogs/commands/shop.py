import discord
from discord.ext import commands, pages
from discord.ext import bridge
from discord.commands import option
from data_management import *
from utils.bot_embeds import *
from utils.bot_autocompletes import *
from operator import attrgetter

class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("list")
    async def articles(self, ctx):
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
        article.set_price(price)
    
    @articles.command(name="add_item")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("item", type=GuildItemConverter, required=True, autocomplete=get_items)
    @option("quantity", type=int, default=1)
    async def add_article_item(self, ctx, article: GuildArticle, item: GuildItem, quantity):
        print(article, item)
        article.add_item(item, quantity)
    
    @articles.command(name="remove_item")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("item", type=GuildItemConverter, required=True, autocomplete=get_items)
    async def remove_article_item(self, ctx, article: GuildArticle, item: GuildItem):
        article.remove_item(item)

    @articles.command(name="add_role")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("role", type=discord.Role, required=True)
    async def add_article_role(self, ctx, article, role):
        article.add_role(role)
    
    @articles.command(name="buy")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    async def buy_article(self, ctx, article):
        try:
            await article.buy(ctx)
            await ctx.respond("Article acheté")
        except NotEnoughMoney:
            author_money = ctx.author_data.money

            embed = WarningEmbed(ctx.guild_config, title=ctx.translate("E_CANNOT_PURCHASE"))
            embed.description = ctx.translate("E_NOT_ENOUGH_MONEY", money_missing=article.price-author_money, author_money=author_money, article_price=article.price)
            await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ShopCog(bot))