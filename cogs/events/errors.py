import discord
from discord.ext import commands
from lang import Lang
from utils.bot_embeds import DangerEmbed

class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, exception):
        await ctx.respond(embed=await self.errors(ctx, exception))
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        embed = await self.errors(ctx, exception)
        if embed:
            await ctx.send(embed=embed)


    async def errors(self, ctx, exception):
        embed = DangerEmbed(ctx.guild_config, title="Command Error", description=exception)
        
        if type(exception) is commands.errors.CommandError:
            embed.description = ctx.translate("E_CommandError")
        elif type(exception) is commands.errors.CommandNotFound:
            return None
        elif type(exception) is commands.errors.MissingRequiredArgument:
            embed.description = Lang.get_text("E_MissingRequiredArgument", language)

        return embed


def setup(bot):
    # bot.add_cog(ErrorHandling(bot))
    pass