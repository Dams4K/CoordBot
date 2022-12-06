import discord
from discord.ext import commands
from discord.ext import bridge
from data_management import MemberData, Item

class StorageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_group(name="inventory")
    @bridge.map_to("show")
    async def inventory(self, ctx):
        await ctx.respond(ctx.author_data.get_inventory())
    
    @inventory.command()
    async def sell(self, ctx):
        await ctx.respond("sell item")
    
    @inventory.command()
    async def give(self, ctx, member: discord.Member, item_name: str):
        member_data = MemberData(ctx.guild.id, member.id)
        member_inventory = member_data.get_inventory()

        member_inventory.add_item(Item(item_name))

        member_data.set_inventory(member_inventory)

        await ctx.respond("item gived")

def setup(bot):
    bot.add_cog(StorageCog(bot))