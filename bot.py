import discord
import logging
import os
from utils.references import References
from discord.ext import bridge

class GDCPBot(bridge.Bot):
    def __init__(self):
        super().__init__(
            self.get_prefix, case_insensitive=True, help_command=None, intents=discord.Intents.all(), debug_guilds=References.BETA_GUILDS
        )

        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(filename=References.LOGS_FOLDER, encoding='utf-8', mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

    
    async def on_ready(self):
        os.system("clear||cls")
        print(self.user, "is now ready")
        print("version:", References.VERSION)

    async def get_prefix(bot, message):
        return References.BOT_PREFIX
