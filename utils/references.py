import json
import typing
import os

class _References:
    BOT_PATH: str = "datas/bot.json"

    def __init__(self) -> None:
        with open(self.BOT_PATH, "r") as f:
            data = json.load(f)

            self.BOT_TOKEN = data["bot_token"]
            self.BOT_PREFIX = data.get("default_prefix", "!")
            self.VERSION = data.get("version", "1.0.0")
            
            self.COGS_FOLDER = data["cogs_folder"]
            self.LOGS_FOLDER = os.path.join(data["logs_folder"], 'discord.log')

            self.BETA_GUILDS = data.get("beta_guilds", [])

            self.DEBUG_MODE = data.get("debug_mode", False)

            self.SUGGESTS_CHANNEL_ID = data.get("suggests_channel_id", None)
            self.REPORTS_CHANNEL_ID = data.get("reports_channel_id", None)

            self.GUILDS_FOLDER = "datas/guilds/"
    
    def get_guild_folder(self, *end):
        return os.path.join(self.GUILDS_FOLDER, *end)

References: _References = _References()