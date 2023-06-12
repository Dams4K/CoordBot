from discord import *
from lang import Lang
from utils.bot_embeds import DangerEmbed
from utils.bot_errors import *
from utils.references import References

class ErrorHandling(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_application_command_error(self, ctx, exception):
        await ctx.respond(embed=await self.errors(ctx, exception))
    @Cog.listener()
    async def on_command_error(self, ctx, exception):
        embed = await self.errors(ctx, exception)
        if embed:
            await ctx.send(embed=embed)


    async def errors(self, ctx, exception):
        embed = DangerEmbed(title=ctx.translate("ERROR_OCCURED"), description=exception)
        
        if type(exception) is errors.ApplicationCommandInvokeError:
            original = type(exception.original)

            if original is Article.NotFound:
                embed.description = ctx.translate("ARTICLE_DOES_NOT_EXIST")
            elif original is Object.NotFound:
                embed.description = ctx.translate("OBJECT_DOES_NOT_EXIST")
        

        return embed


def setup(bot):
    if not References.DEBUG_MODE:
        bot.add_cog(ErrorHandling(bot))