import discord
import datetime
import shutil
import os
from discord.ext import commands, tasks
from data_management import GuildSalaries

class GiveSalariesCog(commands.Cog):
    SALARIES_DAYS = [0]
    SALARIES_TIMES = [datetime.time(hour=8, tzinfo=datetime.timezone.utc)]

    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        return self.bot.is_owner(ctx.author)

    @tasks.loop(time=SALARIES_TIMES)
    async def salaries_task(self):
        today = datetime.date.today()
        if today.isoweekday() in [SALARIES_DAYS]:
            for guild in self.bot.guilds:
                guild_salaries = GuildSalaries(guild.id) # TODO: add pay_guild(guild) and add /salaries pay_guild command
                for member in guild.members:
                    guild_salaries.pay_member(member)
        
def setup(bot):
    bot.add_cog(GiveSalariesCog(bot))