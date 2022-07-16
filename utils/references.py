import json
import typing
import os

class _References:
    BOT_PATH: str = "datas/bot.json"

    def __init__(self) -> None:
        with open(self.BOT_PATH, "r") as f:
            data = json.load(f)

            self.BOT_TOKEN = data["bot_token"]
            self.BOT_PREFIX = data["default_prefix"]
            self.VERSION = data["version"]
            
            self.COGS_FOLDER = data["cogs_folder"]
            self.LOGS_FOLDER = os.path.join(data["logs_folder"], 'discord.log')

            self.BETA_GUILDS = data["beta_guilds"]

            self.DEBUG_MODE = data["debug_mode"]

References: _References = _References()