import discord
from discord.ext import commands
from discord.ext import bridge
from utils.data_manager import MemberData
from utils.bot_customization import BotEmbed

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="reset")
    async def slash_reset(self, ctx, member: discord.Option(discord.Member, "member", required=True)):
        await ctx.respond(**await self.reset(ctx, member))

    @commands.command(name="reset")
    async def cmd_reset(self, ctx, member: discord.Member):
        await ctx.send(**await self.reset(ctx, member))

    async def reset(self, ctx, member):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.reset()
        
        embed = BotEmbed(ctx, title="Reset")
        embed.description = f"{member} a été reset"
        return {"embed": embed}

def setup(bot):
    bot.add_cog(AdminCog(bot))