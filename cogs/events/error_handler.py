from discord import *
from discord.ext import commands

from data_management.errors import *
from lang import Lang
from utils.bot_embeds import DangerEmbed
from utils.references import References


class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_application_command_error(self, ctx, exception: errors.ApplicationCommandInvokeError):
        await ctx.respond(embed=await self.errors(ctx, exception))
    @Cog.listener()
    async def on_command_error(self, ctx, exception):
        embed = await self.errors(ctx, exception)
        if embed:
            await ctx.send(embed=embed)


    async def errors(self, ctx, exception):
        exception_message = str(exception)
        if isinstance(exception, commands.errors.CommandNotFound):
            return None

        if hasattr(exception, "original"):
            exception_message = str(exception.original)

        embed = DangerEmbed(title=ctx.translate("ERROR_OCCURED"), description=exception_message)
        
        return embed


def setup(bot):
    if not References.DEBUG_MODE:
        bot.add_cog(ErrorHandler(bot))