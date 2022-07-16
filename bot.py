import discord
import logging
import os
from utils.references import References
from utils.bot_contexts import *
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


    async def get_application_context(self, interaction, cls = BotApplicationContext):
        return await super().get_application_context(interaction, cls=cls)

    async def get_context(self, message, *, cls = BotContext):
        return await super().get_context(message, cls=cls)


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
