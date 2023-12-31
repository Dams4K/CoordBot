from discord import *
from discord.ext import tasks

from data_management import *

from pympler.asizeof import asizeof
import sys

class AnalyzerCog(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        self.analyze.start()

    @tasks.loop(seconds=0.1)
    async def analyze(self):
        print(asizeof(MemberData.instances), MemberData.instances)
        
        # ids_to_del = []
        # for inst_id, weak_inst in MemberData.instances.items():
        #     if weak_inst() is None:
        #         ids_to_del.append(inst_id)

        # for inst_id in ids_to_del:
        #     MemberData.instances.pop(inst_id)
        

def setup(bot):
    bot.add_cog(AnalyzerCog(bot))