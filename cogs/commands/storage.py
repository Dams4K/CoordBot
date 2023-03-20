import discord
from discord.ext import commands
from discord.ext import bridge
from discord.commands import option
from data_management import *
from utils.bot_embeds import NormalEmbed, DangerEmbed
from utils.bot_views import ConfirmView

class StorageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def get_items(self, ctx):
        guild_storage_config = GuildStorageConfig(ctx.interaction.guild_id)
        items = {guild_storage_config.find_item(item.id) for item in guild_storage_config.items}
        if None in items:
            items.remove(None)
        return [f"{item.name} ({item.id})" for item in items]

    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("show")
    @option("member", type=discord.Member, required=False)
    async def inventory(self, ctx, member=None):
        member = ctx.author if member == None else member
        member_data = MemberData(member.id, ctx.guild.id)
        guild_storage_config = GuildStorageConfig(ctx.guild.id)
        
        inventory = member_data.get_inventory()
        items = inventory.get_items()
        player_items = {item: items.count(item) for item in set(items)} # dict {item: quantity of that item}
        if None in player_items: player_items.pop(None)

        description = "\n".join(f"{item.name} | {player_items[item]}" for item in player_items)

        embed = NormalEmbed(ctx.guild_config, title=f"Inventory of {member}")
        embed.description = description

        await ctx.respond(embed=embed)
    
    @inventory.command()
    async def sell(self, ctx):
        await ctx.respond("sell item")
    
    @inventory.command(name="give")
    @option("member", type=discord.Member, description="pick a member", required=True)
    @option("item_name", type=str, description="pick an item", required=True, autocomplete=get_items)
    @option("amount", type=int, required=True, default=1)
    async def give_item(self, ctx, member: discord.Member, item_name: str, amount: int):
        item_id = item_name[item_name.find("(")+1:item_name.find(")")]
        guild_storage_config = GuildStorageConfig(ctx.guild.id)
        member_data = MemberData(member.id, ctx.guild.id)
        member_inventory = member_data.get_inventory()

        item = guild_storage_config.find_item(item_id)
        if item is None:
            await ctx.respond(f"L'item avec l'id `{item_id}` n'existe pas")
        else:
            member_inventory.add_item(item, amount)
            member_data.set_inventory(member_inventory)

            await ctx.respond(f"L'item {item.name} a été donné à {member}")
    

    @bridge.bridge_group(invoke_without_command=True)
    async def items(self, ctx):
        pass

    @items.command(name="create")
    @option("item_id", type=str, required=True)
    @option("item_name", type=str, required=True)
    @option("unique", type=bool, required=False, default=False)
    async def create_item(self, ctx, item_id: str, item_name: str, unique: bool = False):
        guild_storage_config = GuildStorageConfig(ctx.guild_id)
        new_item = Item(item_id, item_name)
        guild_storage_config.create_item(new_item)
        await ctx.respond("item created")
    
    @items.command(name="delete")
    @option("item_name", type=str, required=True, autocomplete=get_items)
    async def delete_item(self, ctx, item_name: str):
        item_id = item_name[item_name.find("(")+1:item_name.find(")")]
        guild_storage_config = GuildStorageConfig(ctx.guild_id)
        item = guild_storage_config.find_item(item_id)
        if item is None:
            await ctx.respond("Cet item n'existe pas")
        else:
            confirm_view = ConfirmView()
            confirm_embed = DangerEmbed(ctx.guild_config, title="Suppression de d'item", description=f"Êtes vous vraiment sûr de vouloir supprimer l`item {item.name}")
            await ctx.respond(embed=confirm_embed, view=confirm_view)
            await confirm_view.wait()
            if confirm_view.confirmed:
                guild_storage_config.delete_item(item)
                for member in ctx.guild.members:
                    member_data = MemberData(member.id, ctx.guild.id)
                    member_inventory = member_data.get_inventory()
                    member_inventory.remove_item(item_id, -1)
                    member_data.set_inventory(member_inventory)

                await ctx.respond(f"L'item {item.name} a bien été supprimé")
            else:
                await ctx.respond("Suppression annulé")

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
        guild_article = GuildArticle.new(ctx.guild.id, name)
        guild_article.set_price(price)

    @articles.command(name="set_price")
    @option("article_name", type=str, required=True, autocomplete=get_article_names)
    @option("price", type=int, required=True)
    async def set_article_price(self, ctx, article_name, price):
        article = self.get_article_from_name(ctx, article_name)
        article.set_price(price)
    
    @articles.command(name="add_item")
    @option("article_name", type=str, required=True, autocomplete=get_article_names)
    @option("item_name", type=str, required=True, autocomplete=lambda ctx: [f"{item.name} ({item.id})" for item in GuildStorageConfig.list_items(ctx)])
    @option("quantity", type=int, default=1)
    async def add_article_item(self, ctx, article_name, item_name, quantity):
        item_id: str = item_name[item_name.rfind("(")+1:item_name.rfind(")")]

        article = self.get_article_from_name(ctx, article_name)
        item = GuildStorageConfig(ctx.guild.id).find_item(item_id)

        article.add_item(item, quantity)
    
    @articles.command(name="add_role")
    @option("article_name", type=str, required=True, autocomplete=get_article_names)
    @option("role", type=discord.Role, required=True)
    async def add_article_role(self, ctx, article_name, role):
        article: GuildArticle = self.get_article_from_name(ctx, article_name)
        article.add_role(role)

def setup(bot):
    bot.add_cog(StorageCog(bot))