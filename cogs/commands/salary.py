import discord
from discord import option
from discord.ext import commands
from discord.ext import bridge
from data_management import GuildSalaries

class SalaryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("list")
    async def salary(self, ctx):
        salaries = GuildSalaries(ctx.guild.id)

    @salary.command(name="add")
    @option("role", type=discord.Role, required=True)
    @option("pay", type=int, required=True)
    async def add_salary(self, ctx, role: discord.Role, pay: int):
        salaries = GuildSalaries(ctx.guild.id)
        salaries.add_salary(role, pay)
    
    @salary.command(name="erease")
    @option("role", type=discord.Role, requited=True)
    async def erease_salary(self, ctx, role: discord.Role):
        salaries = GuildSalaries(ctx.guild.id)
        salaries.remove_salary(role)
        


def setup(bot):
    bot.add_cog(SalaryCog(bot))