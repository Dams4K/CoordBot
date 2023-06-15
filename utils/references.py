import json
import typing
import os

class _References:
    BOT_PATH: str = "datas/bot.json"
    DEFAULT_LOGS_FOLDER = "datas/logs"

    def __init__(self) -> None:
        if not os.path.exists(self.BOT_PATH):
            os.makedirs(os.path.dirname(self.BOT_PATH))
            with open(self.BOT_PATH, "w") as f:
                data = {
                    "bot_token": input("Bot token > "),
                    "default_prefix": input("Default prefix > "),
                    "version": input("Bot version > "),
                    "cogs_folder": input("Cogs folder > "),
                    "logs_folder": input("Logs folder > "),
                    "debug_mode": input("Enable debug mode (y|N) > "),
                    "suggests_channel_id": input("suggests_channel_id > "),
                    "reports_channel_id": input("reports_channel_id > "),
                }

                json.dump(data, f, indent=4)


        with open(self.BOT_PATH, "r") as f:
            data = json.load(f)

            self.BOT_TOKEN = data["bot_token"]
            self.BOT_PREFIX = data.get("default_prefix", "!")
            self.VERSION = data.get("version", "1.0.0")
            
            self.COGS_FOLDER = data.get("cogs_folder", "cogs")
            self.LOGS_FOLDER = data.get("logs_folder", "datas/logs")

            self.BETA_GUILDS = data.get("beta_guilds", None)

            self.DEBUG_MODE = data.get("debug_mode", False)

            self.SUGGESTS_CHANNEL_ID = data.get("suggests_channel_id", None)
            self.REPORTS_CHANNEL_ID = data.get("reports_channel_id", None)

            self.GUILDS_FOLDER = "datas/guilds/"
    
    def get_guild_folder(self, *end):
        return os.path.join(self.GUILDS_FOLDER, *end)

References: _References = _References()