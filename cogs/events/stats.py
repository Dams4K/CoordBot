from discord import *

from data_management import StatsData
from utils.bot_contexts import BotApplicationContext, BotContext

class StatsCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats_data = StatsData()
    
    @Cog.listener()
    async def on_application_command(self, ctx: BotApplicationContext):
        if getattr(ctx.cog, "ALLOW_STATS", True):
            self.stats_data.increment_cmd(ctx)
    
    @Cog.listener()
    async def on_command(self, ctx: BotContext):
        if getattr(ctx.cog, "ALLOW_STATS", True):
            self.stats_data.increment_cmd(ctx)
        

def setup(bot):
    bot.add_cog(StatsCog(bot))