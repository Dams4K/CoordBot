class ArticleError(Exception): pass
class NotEnoughMoney(ArticleError): pass
class RoleDidNotExist(ArticleError): pass