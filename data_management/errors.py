from lang import Lang

class BotException(Exception):
    KEY = ""

    def __init__(self, lang: str, **kwargs) -> None:
        super().__init__(Lang.get_text(self.KEY, lang, **kwargs))

class Object(BotException):
    class NotFound(BotException): pass

class Article(BotException):
    class NotFound(BotException): pass

class NotEnoughMoney(BotException):
    KEY = "NOT_ENOUGH_MONEY"
class NotEnoughObjects(BotException):
    KEY = "NOT_ENOUGH_OBJECTS"

class RoleDidNotExist(BotException): pass