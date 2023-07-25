from discord import *
from discord.ext import commands

from data_management.errors import *
from utils.bot_embeds import DangerEmbed
from utils.references import References


class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_application_command_error(self, ctx, exception: errors.ApplicationCommandInvokeError):
        if embed := await self.errors(ctx, exception):
            await ctx.respond(embed=embed)
    
    @Cog.listener()
    async def on_command_error(self, ctx, exception):
        if embed := await self.errors(ctx, exception):
            await ctx.send(embed=embed)


    async def errors(self, ctx, exception):
        original_exception = getattr(exception, "original", None)
        
        # Ignore all "Command not found" errors
        if isinstance(exception, commands.errors.CommandNotFound):
            return None

        exception_message = str(original_exception or exception)
        if getattr(original_exception, "KEY", None) is None:
            print("Unknown error has occured, see logs for more informations")
            self.bot.logger.error(str(exception))
            exception_message = "Unknown error has occured - Report has been sent"

            # exception is not known
        embed = getattr(original_exception, "EMBED", DangerEmbed)(title=ctx.translate("ERROR_OCCURED"), description=exception_message)
        
        return embed


def setup(bot):
    if not References.DEBUG_MODE:
        bot.add_cog(ErrorHandler(bot))