import discord
from discord.ext import commands

class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, exception):
        embed=discord.Embed(title="Application Error", description=exception, color=discord.Colour.red())
        await ctx.respond(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        embed=discord.Embed(title="Command Error", description=exception, color=discord.Colour.red())
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(ErrorHandling(bot))