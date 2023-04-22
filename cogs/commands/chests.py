import discord
import aiohttp
from io import BytesIO
from discord import option
from discord.ext import bridge
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup
from utils.permissions import *
from data_management import ChestData
from utils.bot_embeds import NormalEmbed

class ChestsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_command(name="open_chest")
    async def open_chest(self, ctx, id: int):
        #-- BAD
        #
        # avatar_r = requests.get(ctx.author.avatar)
        # webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar_r.content)
        # await webhook.send("qszduqjshds oujdo")

        #- BETTER
        async with aiohttp.ClientSession() as session:
            print(ctx.author.avatar)
            webhook = await ctx.channel.create_webhook(name="qsdqsdsq")
            # async with session.get("https://i.pinimg.com/originals/3d/4c/74/3d4c74196be6a034b30d5c94bb46c221.gif") as resp:
            #     webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=await resp.read())
            #     await webhook.send("qszduqjshds oujdo")

    @bridge.bridge_group()
    async def chests(self, ctx):
        pass

    @chests.command(name="create")
    @option("chest_name", type=str, required=True)
    async def create_chest(self, ctx, chest_name: str):
        chest = ChestData(ctx.guild.id)
        chest.set_name(chest_name)
        await ctx.respond(f"chest {chest.name} (id {chest.chest_id}) has been created")

    
    @chests.command(name="delete")
    async def delete_chest(self, ctx, chest_id: int):
        chest = ChestData(ctx.guild.id, chest_id)
        chest.delete()
        await ctx.respond(f"Chest {chest.name} has been deleted")


def setup(bot):
    # bot.add_cog(ChestsCog(bot))
    pass