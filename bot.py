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


    def load_cogs(self, path: str):
        for cog_file in self.get_cogs_file(path):
            self.load_extension(cog_file.replace("/", ".")[:-3])


    def get_cogs_file(self, path: str) -> list:
        cogs_file = []

        for filename in os.listdir(path):
            if os.path.isfile(path + "/" + filename):
                if filename.endswith(".py"):
                    cogs_file.append(f"{path}/{filename}")
            
            elif os.path.isdir(path + "/" + filename):
                cogs_file += self.get_cogs_file(path + "/" + filename)

        return cogs_file


    async def get_prefix(bot, message):
        return References.BOT_PREFIX
