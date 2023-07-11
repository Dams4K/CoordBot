from lang import Lang
from utils.bot_embeds import *

class BotException(Exception):
    KEY = ""
    EMBED = DangerEmbed

    def __init__(self, lang: str = "en", **kwargs) -> None:
        super().__init__(Lang.get_text(self.KEY, lang, **kwargs))

class Object(BotException):
    class NotFound(BotException):
        KEY = "OBJECT_DOES_NOT_EXIST"

class Article(BotException):
    class NotFound(BotException):
        KEY = "ARTICLE_DOES_NOT_EXIST"

class NotEnoughMoney(BotException):
    KEY = "NOT_ENOUGH_MONEY"
    EMBED = WarningEmbed
class NotEnoughObjects(BotException):
    KEY = "NOT_ENOUGH_OBJECTS"
    EMBED = WarningEmbed

class UnderCooldown(BotException):
    KEY = "ARE_UNDER_COOLDOWN"
    EMBED = WarningEmbed

class RoleNotFound(BotException):
    KEY = "ROLE_NOT_FOUND"