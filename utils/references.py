import json
import typing

class _References:
    BOT_PATH: str = "datas/bot.json"

    BOT_TOKEN: str
    BOT_PREFIX: str
    VERSION: str
    COGS_FOLDER: str

    BETA_GUILDS: typing.List[int]

    def __init__(self) -> None:
        with open(self.BOT_PATH, "r") as f:
            data = json.load(f)

            self.BOT_TOKEN = data["bot_token"]
            self.BOT_PREFIX = data["default_prefix"]
            self.VERSION = data["version"]
            
            self.COGS_FOLDER = data["cogs_folder"]

            self.BETA_GUILDS = data["beta_guilds"]

References: _References = _References()