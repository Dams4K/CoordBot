import asyncio
import logging
import os
from datetime import datetime

import discord
from discord.ext import bridge

from data_management import GuildConfig
from utils.bot_contexts import *
from utils.help_command import BotHelpCommand
from utils.references import References

class CoordBot(bridge.Bot):
    def __init__(self):
        super().__init__(
            self.get_prefix, case_insensitive=True, intents=discord.Intents.all(),
            debug_guilds=References.BETA_GUILDS, help_command=BotHelpCommand()
        )

        if not os.path.exists(References.LOGS_FOLDER):
            os.makedirs(References.LOGS_FOLDER)
        
        file_name = datetime.now().strftime("%Y%m%d_%H%M%S.log")
        file_path = os.path.join(References.LOGS_FOLDER, file_name)
        with open(file_path, "w") as f: pass # create the log file lol

        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename=file_path, encoding='utf-8', mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

    
    async def on_ready(self):
        os.system("clear||cls")
        print(self.user, "is now ready")
        print("bot version:", References.VERSION)
        print("py-cord version:", discord.__version__)
        print("extensions:", end="")
        print("\n  - ".join([""] + self.extensions_path()))
        
        await self.change_presence(status=discord.Status.idle, activity=discord.Streaming(name="blablabla", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

    async def get_application_context(self, interaction, cls = BotApplicationContext):
        return await super().get_application_context(interaction, cls=cls)

    async def get_context(self, message, *, cls = BotContext):
        return await super().get_context(message, cls=cls)

    async def get_autocomplete_context(self, interaction, cls = BotAutocompleteContext):
        return await super().get_autocomplete_context(interaction, cls)

    def load_cogs(self, path: str):
        for cog_file in self.get_cogs_file(path):
            if "debug" in cog_file and not References.DEBUG_MODE: continue
            err = self.load_extension(cog_file.replace("/", ".")[:-3])

    def reload_cogs(self, path: str):
        for cog_file in self.get_cogs_file(path):
            if "debug" in cog_file and not References.DEBUG_MODE: continue
            self.reload_extension(cog_file.replace("/", ".")[:-3])
    
    
    def get_cogs_file(self, path: str) -> list:
        cogs_file = []

        for filename in os.listdir(path):
            if os.path.isfile(path + "/" + filename):
                if filename.endswith(".py"):
                    cogs_file.append(f"{path}/{filename}")
            
            elif os.path.isdir(path + "/" + filename):
                cogs_file += self.get_cogs_file(path + "/" + filename)

        return cogs_file

    def extensions_path(self):
        return [str(ext.__name__).replace(".", "/") + ".py" for ext in self.extensions.values()]


    async def get_prefix(self, message):
        if message.guild is None:
            return References.BOT_PREFIX
        else:
            return GuildConfig(message.guild.id).prefix