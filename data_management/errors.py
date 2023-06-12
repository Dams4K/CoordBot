class ArticleError(Exception): pass

class NotEnoughMoney(ArticleError): pass
class NotEnoughObjects(ArticleError): pass

class RoleDidNotExist(ArticleError): pass