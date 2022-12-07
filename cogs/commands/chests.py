import discord
import aiohttp
from io import BytesIO
from discord import Option
from discord.ext import bridge
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup
from utils.permissions import *
from data_management import ChestData
from utils.bot_embeds import NormalEmbed

class ChestsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    chests = SlashCommandGroup("chests", "chests settings")
    chests.checks = [is_admin]


    @bridge.bridge_command(name="open_chest")
    async def open_chest(self, ctx, id: int):
        #-- BAD
        #
        # avatar_r = requests.get(ctx.author.avatar)
        # webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar_r.content)
        # await webhook.send("qszduqjshds oujdo")

        #- BETTER
        async with aiohttp.ClientSession() as session:
            async with session.get(str(ctx.author.avatar)) as resp:
                webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=await resp.read())
                await webhook.send("qszduqjshds oujdo")

    @chests.command(name="create")
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
    bot.add_cog(ChestsCog(bot))