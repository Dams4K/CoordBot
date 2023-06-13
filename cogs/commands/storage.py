from operator import attrgetter

from discord import *
from discord.ext import commands, pages

from data_management import *
from utils.bot_autocompletes import *
from utils.bot_commands import *
from utils.bot_embeds import DangerEmbed, NormalEmbed
from utils.bot_views import ConfirmView


class StorageCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    inventory = BotSlashCommandGroup("inventory", guild_only=True)

    @inventory.command(name="show")
    @option("member", type=Member, required=False)
    async def slash_show_inventory(self, ctx, member=None):
        member = ctx.author if member == None else member
        await self.show_inventory(ctx, member)
    
    @bot_user_command(name="inventory")
    @guild_only()
    async def user_show_inventory(self, ctx, member: Member):
        await self.show_inventory(ctx, member, ephemeral=True)

    async def show_inventory(self, ctx, member, ephemeral=False):
        member_data = MemberData(member.id, ctx.guild.id)

        inventory = member_data.get_inventory()
        object_ids = inventory.get_object_ids()
        player_objects = {GuildObject(object_id, ctx.guild.id): object_ids.count(object_id) for object_id in set(object_ids)} # dict {object: quantity of that object}
        if None in player_objects: player_objects.pop(None)

        description = "\n".join(f"{obj.name} | {player_objects[obj]}" for obj in player_objects)

        embed = NormalEmbed(ctx.translate("INVENTORY_OF", member=member))
        embed.description = description

        await ctx.respond(embed=embed, ephemeral=ephemeral)

    # @inventory.command() # TODO: v4.1
    # async def sell(self, ctx):
    #     await ctx.respond("sell object")
    

def setup(bot):
    bot.add_cog(StorageCog(bot))