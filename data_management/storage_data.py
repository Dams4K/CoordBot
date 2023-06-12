import discord
import random
from ddm import *
from utils.references import References
from utils.bot_errors import *
from data_management import errors

class ChestData(Saveable):
    def __init__(self, guild_id, chest_name: str = "No name", chest_id = -1):
        self._guild_id = guild_id

        # create the next id usable
        if chest_id == -1:
            dirname = References.get_guild_folder(f"{self._guild_id}/chests")
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            
            chests_id = [-1] + [int(i.split(".")[0]) for i in os.listdir(dirname)]
            chest_id = sorted(chests_id)[-1]+1

        self._chest_id = chest_id
        self.name = chest_name

        super().__init__(References.get_guild_folder(f"{self._guild_id}/chests/{self._chest_id}.json"))

    @Saveable.update()
    def set_name(self, new_name):
        self.name = new_name

    @Saveable.update()
    def add_loot(self, loot):
        pass
    
    @Saveable.update()
    def remove_loot(self, loot):
        pass

    def open(self):
        pass

    def delete(self):
        os.remove(self.file_path)


class Loot(Saveable):
    def __init__(self, loot_id: int, guild_id: int):
        self._loot_id = loot_id
        self._guild_id = guild_id

        super().__init__(References.get_guild_folder(f"{guild_id}/loots/{loot_id}.json"))
        
    def add_object(self, object, weight):
        pass


class GuildObject(Saveable):
    FOLDER: str = "%s/objects"
    FILENAME: str = "%s.json"

    @staticmethod
    def list_objects(guild_id: int) -> list:
        objects: list = []
        objects_folder: str = References.get_guild_folder(GuildObject.FOLDER % guild_id)

        if os.path.exists(objects_folder):
            for filename in os.listdir(objects_folder):
                file_path = os.path.join(objects_folder, filename)
                if os.path.isfile(file_path):
                    object_id: int = int(filename.replace(".json", ""))
                    objects.append(GuildObject(object_id, guild_id))
        
        return objects

    @staticmethod
    def from_name(guild_id: int, object_name: str):
        objects = GuildObject.list_objects(guild_id)
        for obj in objects:
            if obj.name == object_name:
                return obj

    @staticmethod
    def new(guild_id: int, object_name: str):
        new_id = 0
        folder = References.get_guild_folder(GuildObject.FOLDER % guild_id)
        if os.path.exists(folder):
            ids = [int(filename.replace(".json", "")) for filename in os.listdir(folder)]
            if ids != []:
                new_id = max(ids)+1
        return GuildObject(new_id, guild_id, create=True).set_name(object_name)

    def __new__(cls, object_id: int, guild_id: int, create: bool = False):
        path = References.get_guild_folder(os.path.join(GuildObject.FOLDER % guild_id, GuildObject.FILENAME % object_id))
        if os.path.exists(path) or create:
            return super(Saveable, cls).__new__(cls)
        return None

    def __init__(self, object_id: int, guild_id: int, create: bool = False):
        self._object_id = object_id
        self._guild_id = guild_id
        self.name = "NoName"
        self.description = ""
        self.refundable = False
        self.refund_price = 0

        path = os.path.join(GuildObject.FOLDER % guild_id, GuildObject.FILENAME % object_id)
        super().__init__(References.get_guild_folder(path))
    
    @Saveable.update()
    def set_name(self, new_name):
        self.name = new_name[:32]
        return self

    @Saveable.update()
    def set_description(self, new_description):
        self.description = new_description[:1024]
        return self

    @Saveable.update()
    def set_refundable(self, is_refundable, refund_price):
        self.refundable = is_refundable
        self.refund_price = refund_price
        return self

class GuildArticle(Saveable):
    FOLDER: str = "%s/articles"
    FILENAME: str = "%s.json"

    @staticmethod
    def list_articles(guild_id) -> list:
        articles: list = []
        articles_folder: str = References.get_guild_folder(GuildArticle.FOLDER % guild_id)

        if os.path.exists(articles_folder):
            for filename in os.listdir(articles_folder):
                file_path = os.path.join(articles_folder, filename)
                if os.path.isfile(file_path):
                    article_id: int = int(filename.replace(".json", ""))
                    articles.append(GuildArticle(article_id, guild_id))
        
        return articles
        
    @staticmethod
    def from_name(guild_id: int, article_name: str):
        articles = GuildArticle.list_articles(guild_id)
        for article in articles:
            if article.name == article_name:
                return article

    @staticmethod
    def new(guild_id: int, article_name: str):
        new_id = 0
        articles_folder = References.get_guild_folder(GuildArticle.FOLDER % guild_id)
        if os.path.exists(articles_folder):
            ids = [int(filename.replace(".json", "")) for filename in os.listdir(articles_folder)]
            if ids != []:
                new_id = max(ids)+1
        return GuildArticle(new_id, guild_id).set_name(article_name)

    def __init__(self, article_id, guild_id):
        self._article_id = article_id
        self._guild_id = guild_id
        self.name: str = "no name"
        self.description: str = "*no description*"
        self.price: int = 0
        
        self.object_ids: dict = {}
        self.role_ids: list = []

        super().__init__(References.get_guild_folder(os.path.join(GuildArticle.FOLDER % self._guild_id, GuildArticle.FILENAME % self._article_id)))

    @Saveable.update()
    def set_name(self, new_name: str):
        self.name = new_name
        return self
    
    @Saveable.update()
    def set_description(self, new_description: str):
        self.description = new_description
        return self

    @Saveable.update()
    def set_price(self, new_price: int):
        self.price = int(new_price)
        return self
    
    @Saveable.update()
    def add_object(self, obj: GuildObject, quantity: int):
        obj_id = str(obj._object_id)
        self.object_ids.setdefault(obj_id, 0)
        self.object_ids[obj_id] += quantity
        return self
    
    @Saveable.update()
    def remove_object(self, obj: GuildObject, quantity: int):
        return self.add_object(obj, -quantity)
    
    @Saveable.update()
    def add_role(self, role: discord.Role):
        if not role.id in self.role_ids:
            self.role_ids.append(role.id)
        return self

    @Saveable.update()
    def remove_role(self, role: discord.Role):
        if role.id in self.role_ids:
            self.role_ids.remove(role.id)
    
    def has_object(self, object: GuildObject):
        return str(object._object_id) in self.object_ids

    def get_quantity(self, object: GuildObject):
        return self.object_ids.get(str(object._object_id), 0)

    async def buy(self, ctx, quantity: int):
        author_data = ctx.author_data
        price = self.price * quantity

        # Check if the member has enough money
        if author_data.money < price:
            raise errors.NotEnoughMoney
        
        author_inventory: Inventory = author_data.get_inventory()
        # Check if the member has enough objects
        for object_id, object_amount in self.object_ids.items():
            if object_amount >= 0:
                continue
            
            author_quantity = author_inventory.object_ids.count(str(object_id))
            if author_quantity < abs(object_amount * quantity):
                raise errors.NotEnoughObjects

        author_data.set_money(author_data.money - price)

        for _ in range(quantity):
            for object_id, amount in self.object_ids.items():
                author_inventory.add_object_id(str(object_id), amount)

        author_data.set_inventory(author_inventory)
        
        for role_id in self.role_ids:
            role = ctx.guild.get_role(role_id)
            if role == None:
                raise errors.RoleDidNotExist
            else:
                await ctx.author.add_roles(role)
    
class GuildArticleConverter:
    async def convert(*args):
        ctx = args[0]
        arg = args[1]
        if len(args) > 2:
            ctx = args[1]
            arg = args[2]
        
        if not isinstance(arg, str):
            raise Article.NotFound()
        
        article_id = None
        if arg.isdecimal():
            article_id: str = arg
        else:
            article_id: str = arg[arg.rfind("(")+1:arg.rfind(")")]
        
        article = None

        if not (article_id is None) and article_id.isdecimal():
            article = GuildArticle(article_id, ctx.guild.id)
        else:
            article = GuildArticle.from_name(ctx.guild.id, arg)
        
        if article is None:
            raise Article.NotFound()

        return article

class GuildObjectConverter:
    async def convert(*args):
        ctx = args[0]
        arg = args[1]
        if len(args) > 2:
            ctx = args[1]
            arg = args[2]
        
        if not isinstance(arg, str):
            raise Object.NotFound()
        
        object_id = None
        if arg.isdecimal():
            object_id: str = arg
        else:
            object_id: str = arg[arg.rfind("(")+1:arg.rfind(")")]
        
        obj = None

        if not (object_id is None) and object_id.isdecimal():
            obj = GuildObject(object_id, ctx.guild.id)
        else:
            obj = GuildObject.from_name(ctx.guild.id, arg)

        if obj is None:
            raise Object.NotFound()

        return obj
    

class Inventory(Data):
    def __init__(self, max_size: int, objects: list):
        self.max_size = max_size
        self.object_ids = [obj._object_id for obj in objects]

    def is_full(self):
        return len(self.object_ids) >= self.max_size and self.max_size > 0

    def add_object(self, obj: GuildObject, amount: int):
        if self.is_full(): return
        
        self.object_ids.extend([obj._object_id] * amount)
    def add_object_id(self, object_id: str, amount: int):
        if amount < 0:
            amount_removed = 0
            while amount_removed < abs(amount) and self.object_ids.count(object_id) > 0:
                self.object_ids.remove(object_id)
                amount_removed += 1
        elif not self.is_full():
            self.object_ids.extend([object_id] * amount)
    
    def remove_object(self, object_id, amount: int):
        if amount == -1:
            amount = len(self.object_ids)
        n = 0
        while n < amount:
            if not object_id in self.object_ids: break
            self.object_ids.remove(object_id)
            n += 1

    def get_object_ids(self):
        return self.object_ids