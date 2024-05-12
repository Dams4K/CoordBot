from discord import *
from discord.ext import tasks

from data_management import *

from pympler.asizeof import asizeof

class AnalyzerCog(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        self.analyze.start()

    @tasks.loop(seconds=0.01)
    async def analyze(self):
        size = self.get_total_data_size(GuildConfig, GuildLanguage, GuildSalaries, GuildLevelingConfig, MemberData, GuildArticle, GuildObject)
        self.bot.MEM_USAGE = size
        if size > self.bot.MAX_MEM_USAGE:
            self.bot.MAX_MEM_USAGE = size

    def get_total_data_size(self, *data_classes):
        total = 0
        for clazz in data_classes:
            if not issubclass(clazz, Saveable):
                continue
            total += asizeof(clazz.instances)

        return total

        

def setup(bot):
    bot.add_cog(AnalyzerCog(bot))