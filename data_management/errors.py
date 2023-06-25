from lang import Lang

class BotException(Exception):
    KEY = ""

    def __init__(self, lang: str = "en", **kwargs) -> None:
        super().__init__(Lang.get_text(self.KEY, lang, **kwargs))

class Object(BotException):
    class NotFound(BotException): pass

class Article(BotException):
    class NotFound(BotException): pass

class NotEnoughMoney(BotException):
    KEY = "NOT_ENOUGH_MONEY"
class NotEnoughObjects(BotException):
    KEY = "NOT_ENOUGH_OBJECTS"

class UnderCooldown(BotException):
    KEY = "ARE_UNDER_COOLDOWN"

class RoleDidNotExist(BotException): pass