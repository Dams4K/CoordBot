import discord
from discord.ext import bridge, commands

from utils.bot_embeds import NormalEmbed

from tests import test_options

# Debug class, only available when utils.References.DEBUG_MODE is True
class DebugCog(commands.Cog):
    ALLOW_STATS = False
    
    def __init__(self, bot):
        self.bot = bot
        
    @bridge.bridge_command(name="hello")
    async def hello(self, ctx):
        embed = NormalEmbed(title="Test")
        await ctx.respond(embed=embed)
    
    @bridge.bridge_command(name="gen_error")
    async def gen_error(self, ctx, *, msg):
        assert False, msg
    
    @commands.command(name="only_command")
    async def only_command(self, ctx):
        await ctx.send(ctx.guild_config.prefix)
    
    @test_options(msg="le message à envoyer")
    @commands.command(name="say")
    async def say(self, ctx, *, msg):
        await ctx.send(msg)

    @commands.slash_command(name="only_slash")
    async def only_slash(self, ctx):
        await ctx.respond(ctx.guild_config.prefix)

    @commands.command(name="colors")
    async def colors(self, ctx):
        colors = [ e for e in dir(discord.Color) if len(e) > 1 and not e.startswith("_") and not e.startswith("from") and not e.startswith("to") and e not in ["random", "embed_background", "value"]]
        colors = list(set(colors))
        for color in colors:
            embed = discord.Embed(title=f"Test color {color}", color=getattr(discord.Color, color)())
            await ctx.send(embed=embed)


    @bridge.bridge_command(name="image")
    async def image(self, ctx, user: discord.Option(discord.Member, "user", required=False) = None):
        embed = discord.Embed(title="QSD")

        file = discord.File("/home/damien/tux.png", filename="tux.png")

        embed.set_image(url="attachment://tux.png")

        await ctx.respond(user.mention if user != None else None, file=file, embed=embed, ephemeral=True)
    
    @bridge.bridge_command(name="tab_in_embed")
    async def tab_in_embed(self, ctx):
        embed = NormalEmbed(title="Tab In Embed")

        embed.description = """Hi
Just a little test
>       i hope it will work
        """

        await ctx.respond(embed=embed)
        
    a = discord.SlashCommandGroup("a")
    b = a.create_subgroup("b")

    @b.command()
    async def c(self, ctx):
        await ctx.respond("d")


def setup(bot):
    bot.add_cog(DebugCog(bot))