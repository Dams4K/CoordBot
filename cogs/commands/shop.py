import discord
from discord.ext import commands
from discord.ext import bridge
from discord.commands import option
from data_management import *
from utils.bot_embeds import DangerEmbed, WarningEmbed

class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_article_names(self, ctx):
        return [f"{article.name} ({article._article_id})" for article in GuildArticle.list_articles(ctx)]
    def get_article_from_name(self, ctx, article_name) -> GuildArticle:
        article_id: int = int(article_name[article_name.rfind("(")+1:article_name.rfind(")")])
        return GuildArticle(article_id, ctx.guild.id)

    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("all")
    async def articles(self, ctx):
        pass
    
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
    @option("item_name", type=str, required=True, autocomplete=lambda ctx: [f"{item.name} ({item.id})" for item in GuildStorageConfig.list_items(ctx)])
    @option("quantity", type=int, default=1)
    async def add_article_item(self, ctx, article, item_name, quantity):
        item = GuildStorageConfig(ctx.guild.id).find_item(item_id)

        article.add_item(item, quantity)
    
    @articles.command(name="remove_item")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_article_names)
    @option("item_name", type=str, required=True, autocomplete=lambda ctx: [f"{item.name} ({item.id})" for item in GuildStorageConfig.list_items(ctx)])
    async def remove_article_item(self, ctx, article, item_name):
        print(article)
        print(item_name)

    @articles.command(name="add_role")
    @option("article_name", type=str, required=True, autocomplete=get_article_names)
    @option("role", type=discord.Role, required=True)
    async def add_article_role(self, ctx, article_name, role):
        article: GuildArticle = self.get_article_from_name(ctx, article_name)
        article.add_role(role)
    
    @articles.command(name="buy")
    @option("article_name", type=str, required=True, autocomplete=get_article_names)
    async def buy_article(self, ctx, article_name):
        article: GuildArticle = self.get_article_from_name(ctx, article_name)
        try:
            await article.buy(ctx)
        except NotEnoughMoney:
            author_money = ctx.author_data.money

            embed = WarningEmbed(ctx.guild_config, title=ctx.translate("E_CANNOT_PURCHASE"))
            embed.description = ctx.translate("E_NOT_ENOUGH_MONEY", money_missing=article.price-author_money, author_money=author_money, article_price=article.price)
            await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ShopCog(bot))