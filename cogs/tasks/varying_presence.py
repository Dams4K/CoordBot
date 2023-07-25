from discord import *
from discord.ext import tasks

class VaryingPresence(Cog):
    ACTIVITIES = [
        Activity(name="OMORI - It Means Everything [lofi hiphop/chillhop remix]", type=ActivityType.listening, url="https://www.youtube.com/watch?v=88DcHP-wEyY"),
        Activity(name="Machinarium Soundtrack 00 - By the Wall", type=ActivityType.listening, url="https://www.youtube.com/watch?v=jex5rtwx94k&ab_channel=GoodMomo")
    ]

    def __init__(self, bot) -> None:
        self.bot = bot
        self.activity_index = 0

    @Cog.listener()
    async def on_ready(self):
        self.change_presence.start()

    @tasks.loop(minutes=2, seconds=30)
    async def change_presence(self):
        if self.activity_index+1 >= len(self.ACTIVITIES):
            self.activity_index = 0
        else:
            self.activity_index += 1
        
        await self.bot.change_presence(activity=self.ACTIVITIES[self.activity_index])


def setup(bot):
    bot.add_cog(VaryingPresence(bot))