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
    
    #TODO: optimised
    async def get_items(self, ctx):
        guild_id = ctx.interaction.guild.id
        item_names = [item.name for item in GuildItem.list_items(guild_id)]

        result = []
        for item in GuildItem.list_items(guild_id):
            if not item.name.startswith(ctx.value):
                continue

            formatted = item.name
            if item_names.count(item.name) > 1:
                formatted += f" ({item._item_id})"
            result.append(formatted)

        return result

    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("show")
    @option("member", type=discord.Member, required=False)
    async def inventory(self, ctx, member=None):
        member = ctx.author if member == None else member
        member_data = MemberData(member.id, ctx.guild.id)
        guild_storage_config = GuildStorageConfig(ctx.guild.id)
        
        inventory = member_data.get_inventory()
        item_ids = inventory.get_item_ids()
        player_items = {guild_storage_config.find_item(item_id): item_ids.count(item_id) for item_id in set(item_ids)} # dict {item: quantity of that item}
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
    @option("item", type=GuildItemConverter, description="pick an item", required=True, autocomplete=get_items)
    @option("amount", type=int, default=1)
    async def give_item(self, ctx, member: discord.Member, item: GuildItem, amount: int):
        member_data = MemberData(member.id, ctx.guild.id)
        member_inventory = member_data.get_inventory()

        if item is None:
            await ctx.respond(f"L'item n'existe pas")
        else:
            member_inventory.add_item(item, amount)
            member_data.set_inventory(member_inventory)

            await ctx.respond(f"L'item {item.name} a été donné à {member}")
    

    @bridge.bridge_group(invoke_without_command=True)
    async def items(self, ctx):
        pass

    @items.command(name="create")
    @option("name", type=str, required=True)
    @option("unique", type=bool, default=False)
    async def create_item(self, ctx, name: str, unique: bool):
        new_item = GuildItem.new(ctx.guild.id, name)
        await ctx.respond("item created")
    
    @items.command(name="delete")
    @option("item", type=GuildItemConverter, required=True, autocomplete=get_items)
    async def delete_item(self, ctx, item: GuildItem):
        if item is None:
            await ctx.respond("Cet item n'existe pas")
        else:
            confirm_view = ConfirmView()
            confirm_embed = DangerEmbed(ctx.guild_config, title="Suppression de d'item", description=f"Êtes vous vraiment sûr de vouloir supprimer l`item {item.name}")
            await ctx.respond(embed=confirm_embed, view=confirm_view)
            await confirm_view.wait()
            if confirm_view.confirmed:
                item.delete()
                await ctx.respond(f"L'item {item.name} a bien été supprimé")
            else:
                await ctx.respond("Suppression annulé")


def setup(bot):
    bot.add_cog(StorageCog(bot))