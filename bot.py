import discord
import os
from utils.references import References
from discord.ext import bridge

class GDCPBot(bridge.Bot):
    def __init__(self):
        super().__init__(
            self.get_prefix, case_insensitive=True, help_command=None, intents=discord.Intents.all(), debug_guilds=References.BETA_GUILDS
        )
    
    async def on_ready(self):
        os.system("clear||cls")
        print(self.user, "is now ready")
        print("version:", References.VERSION)

    async def get_prefix(bot, message):
        return References.BOT_PREFIX
