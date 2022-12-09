import discord
from discord.ext import commands
from discord.ext import bridge
from discord.commands import option
from data_management import GuildStorageConfig, MemberData, Item
from utils.bot_embeds import NormalEmbed, DangerEmbed
from utils.bot_views import ConfirmView

class StorageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def get_items(self, ctx):
        guild_storage_config = GuildStorageConfig(ctx.interaction.guild_id)
        return [item.id for item in guild_storage_config.get_items()]

    @bridge.bridge_group(name="inventory", invoke_without_command=True)
    @bridge.map_to("show")
    @option("member", type=discord.Member, required=False)
    async def inventory(self, ctx, member=None):
        member = ctx.author if member == None else member
        member_data = MemberData(ctx.guild.id, member.id)
        guild_storage_config = GuildStorageConfig(ctx.guild.id)
        
        inventory = member_data.get_inventory()
        items_ids = inventory.get_items_ids()
        player_items = {guild_storage_config.find_item(item_id): items_ids.count(item_id) for item_id in set(items_ids)}
        if None in player_items: player_items.pop(None)

        description = "\n".join(f"{item.name} | {player_items[item]}" for item in player_items)

        embed = NormalEmbed(ctx.guild_config, title=f"Inventory of {member}")
        embed.description = description

        await ctx.respond(embed=embed)
    
    @inventory.command()
    async def sell(self, ctx):
        await ctx.respond("sell item")
    
    @inventory.command()
    @option("member", type=discord.Member, description="pick a member", required=True)
    @option("item_id", type=str, description="pick an item", required=True, autocomplete=get_items)
    @option("amount", type=int, required=True, default=1)
    async def give(self, ctx, member: discord.Member, item_id: str, amount: int):
        guild_storage_config = GuildStorageConfig(ctx.guild.id)
        member_data = MemberData(ctx.guild.id, member.id)
        member_inventory = member_data.get_inventory()

        item = guild_storage_config.find_item(item_id)
        if item is None:
            await ctx.respond(f"L'item avec l'id `{item_id}` n'existe pas")
        else:
            member_inventory.add_item(item, amount)
            member_data.set_inventory(member_inventory)

            await ctx.respond(f"L'item {item.name} a été donné à {member}")
    

    @bridge.bridge_group(name="items", invoke_without_command=True)
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
    @option("item_id", type=str, required=True, autocomplete=get_items)
    async def delete_item(self, ctx, item_id: str):
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
                await ctx.respond(f"L'item {item.name} a bien été supprimé")
            else:
                await ctx.respond("Suppression annulé")

def setup(bot):
    bot.add_cog(StorageCog(bot))