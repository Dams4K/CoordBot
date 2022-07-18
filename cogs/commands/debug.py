import discord
from discord.ext import commands
from discord.ext import bridge
from utils.bot_customization import BotEmbed

class DebugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_command(name="hello")
    async def hello(self, ctx):
        embed = BotEmbed(ctx, title="Test")
        await ctx.respond(embed=embed)
    
    @bridge.bridge_command(name="gen_error")
    async def gen_error(self, ctx, *, msg):
        assert False, msg
    
    @commands.command(name="only_command")
    async def only_command(self, ctx):
        await ctx.send(ctx.guild_data.get_prefix())
    
    @commands.slash_command(name="only_slash")
    async def only_slash(self, ctx):
        await ctx.respond(ctx.guild_data.get_prefix())

def setup(bot):
    bot.add_cog(DebugCog(bot))