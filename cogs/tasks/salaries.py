import datetime

from discord.ext import commands, tasks

from data_management import GuildSalaries


class SalariesCog(commands.Cog):
    SALARIES_DAYS = [0] # 0 = monday
    SALARIES_TIMES = [datetime.time(hour=8)] # utc time

    def __init__(self, bot):
        self.bot = bot
        self.salaries_task.start()

    @tasks.loop(time=SALARIES_TIMES)
    async def salaries_task(self):
        today = datetime.date.today()
        if today.weekday() in self.SALARIES_DAYS:
            for guild in self.bot.guilds:
                self.bot.logger.info(f"Weekly pay {guild.name}")
                guild_salaries = GuildSalaries(guild.id)
                guild_salaries.pay_role(guild.default_role)
    
        
def setup(bot):
    bot.add_cog(SalariesCog(bot))