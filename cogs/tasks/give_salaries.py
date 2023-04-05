import discord
import datetime
import shutil
import os
from discord.ext import commands, tasks

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
            return
        
def setup(bot):
    bot.add_cog(GiveSalariesCog(bot))