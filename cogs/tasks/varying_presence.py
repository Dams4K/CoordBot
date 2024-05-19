from discord import *
from discord.ext import tasks


class VaryingPresence(Cog):
    @staticmethod
    def create_button(label: str, url: str):
        return {"label": label, "url": url}

    ACTIVITIES = [
        Activity(name="OMORI - It Means Everything [lofi hiphop/chillhop remix]", type=ActivityType.listening),
        Activity(name="Machinarium Soundtrack 00 - By the Wall", type=ActivityType.listening),
        Activity(name="Senbeï & Proleter - Lady Vengeance", type=ActivityType.listening),
        Activity(name="Imaginary Interlude - C418", type=ActivityType.listening),
        Activity(name="Monodrama - Ignant Benches", type=ActivityType.listening),
        Game(name="Tunic"),
        Game(name="Hyper Light Drifter"),
        Game(name="Outer Wilds"),
        Game(name="Fez"),
        Game(name="Omori"),
        Activity(name="The Great Review", type=ActivityType.watching),
        Activity(name="FMA B", type=ActivityType.watching),
        Activity(name="Omniscient Reader's Viewpoint", type=ActivityType.watching),
    ]

    def __init__(self, bot) -> None:
        self.bot = bot
        self.activity_index = 0

    @Cog.listener()
    async def on_ready(self):
        self.change_presence.start()

    @tasks.loop(minutes=6)
    async def change_presence(self):
        if self.activity_index+1 >= len(self.ACTIVITIES):
            self.activity_index = 0
        else:
            self.activity_index += 1
        
        await self.bot.change_presence(activity=self.ACTIVITIES[self.activity_index])


def setup(bot):
    bot.add_cog(VaryingPresence(bot))