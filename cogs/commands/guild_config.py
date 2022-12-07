import discord
from discord import option
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import is_admin

class GuildConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        return is_admin(ctx)

    @bridge.bridge_command(name="setprefix")
    @option("prefix", type=str, required=True)
    async def set_prefix(self, ctx, prefix: str):
        ctx.guild_config.set_prefix(prefix)
        await ctx.respond("Prefix changed to " + prefix)


def setup(bot):
    bot.add_cog(GuildConfigCog(bot))