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

    @commands.command(name="colors")
    async def colors(self, ctx):
        colors = [ e for e in dir(discord.Color) if len(e) > 1 and not e.startswith("_") and not e.startswith("from") and not e.startswith("to") and e not in ["random", "embed_background", "value"]]
        colors = list(set(colors))
        print(colors)
        for color in colors:
            print(color)
            embed = discord.Embed(title=f"Test color {color}", color=getattr(discord.Color, color)())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DebugCog(bot))