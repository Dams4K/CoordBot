import discord
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import is_admin

class GuildSettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        return is_admin(ctx)

    @bridge.bridge_command(name="setprefix")
    async def set_prefix(self, ctx, new_prefix: str):
        ctx.guild_data.set_prefix(new_prefix)
        await ctx.respond("Prefix changed to " + new_prefix)


def setup(bot):
    bot.add_cog(GuildSettingsCog(bot))