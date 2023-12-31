import io
import traceback

from discord import *
from discord.ext import commands

from data_management.errors import *
from utils.bot_embeds import DangerEmbed
from utils.references import References


class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_event_error(self, event_name, exc, *args, **kwargs):
        """WARNING
        If there is any errors in this function, everything will break because this function will be called again.
        """
        if isinstance(args[0], Message):
            ctx = await self.bot.get_context(args[0])
            await self.errors(ctx, exc)
        else:
            detailed_exception = "".join(traceback.format_exception(exc))
            print(detailed_exception)
    
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
            detailed_exception = "".join(traceback.format_exception(exception))

            self.bot.logger.error(detailed_exception)
            exception_message = ctx.translate("UNKNOWN_ERROR_OCCURRED")

            report_channel = self.bot.get_channel(References.REPORTS_CHANNEL_ID)

            if len(detailed_exception) > 200:
                file = File(io.StringIO(detailed_exception), filename="detailed_exception-{time.time()}.txt")
                await report_channel.send(file=file)
            else:
                await report_channel.send(embed=DangerEmbed(title=ctx.translate("UNKNOWN_ERROR"), description=detailed_exception))

            # exception is not known
        embed = getattr(original_exception, "EMBED", DangerEmbed)(title=ctx.translate("ERROR_OCCURED"), description=exception_message)
        
        return embed


def setup(bot):
    if not References.DEBUG_MODE:
        bot.add_cog(ErrorHandler(bot))