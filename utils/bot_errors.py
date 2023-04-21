class BotException(Exception): pass

class Object(BotException):
    class NotFound(BotException): pass

class Article(BotException):
    class NotFound(BotException): pass