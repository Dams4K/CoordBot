import discord
import random
from ddm import *
from utils.references import References
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
        
    def add_item(self, item, weight):
        pass


class Item(Data):
    def __init__(self, item_id: str = "no_id", item_name: str = "no_name"):
        self.id = item_id
        self.name = item_name

        super().__init__()

class Inventory(Data):
    def __init__(self, max_size: int, items: list):
        self.max_size = max_size
        self.item_ids = [item._item_id for item in items]

    def is_full(self):
        return len(self.item_ids) >= self.max_size and self.max_size > 0

    def add_item(self, item: Item, amount: int):
        if self.is_full(): return
        
        self.item_ids.extend([item._item_id] * amount)
    def add_item_id(self, item_id: str, amount: int):
        if self.is_full(): return

        self.item_ids.extend([item_id] * amount)
    
    def remove_item(self, item_id, amount: int):
        if amount == -1:
            amount = len(self.item_ids)
        n = 0
        while n < amount:
            if not item_id in self.item_ids: break
            self.item_ids.remove(item_id)
            n += 1

    def get_item_ids(self):
        return self.item_ids

class GuildItem(Saveable):
    FOLDER: str = "%s/items"
    FILENAME: str = "%s.json"

    @staticmethod
    def list_items(guild_id: int) -> list:
        items: list = []
        items_folder: str = References.get_guild_folder(GuildItem.FOLDER % guild_id)

        if os.path.exists(items_folder):
            for filename in os.listdir(items_folder):
                file_path = os.path.join(items_folder, filename)
                if os.path.isfile(file_path):
                    item_id: int = int(filename.replace(".json", ""))
                    items.append(GuildItem(item_id, guild_id))
        
        return items

    @staticmethod
    def from_name(guild_id: int, item_name: str):
        items = GuildItem.list_items(guild_id)
        for item in items:
            if item.name == item_name:
                return item

    @staticmethod
    def new(guild_id: int, item_name: str):
        new_id = 0
        folder = References.get_guild_folder(GuildItem.FOLDER % guild_id)
        if os.path.exists(folder):
            ids = [int(filename.replace(".json", "")) for filename in os.listdir(folder)]
            if ids != []:
                new_id = max(ids)+1
        return GuildItem(new_id, guild_id, create=True).set_name(item_name)

    def __new__(cls, item_id: int, guild_id: int, create: bool = False):
        path = References.get_guild_folder(os.path.join(GuildItem.FOLDER % guild_id, GuildItem.FILENAME % item_id))
        if os.path.exists(path) or create:
            return super(Saveable, cls).__new__(cls)
        return None

    def __init__(self, item_id: int, guild_id: int, create: bool = False):
        self._item_id = item_id
        self._guild_id = guild_id
        self.name = "NoName"

        path = os.path.join(GuildItem.FOLDER % guild_id, GuildItem.FILENAME % item_id)
        super().__init__(References.get_guild_folder(path))
    
    @Saveable.update()
    def set_name(self, new_name):
        self.name = new_name
        return self

class GuildArticle(Saveable):
    FOLDER: str = "%s/articles"
    FILENAME: str = "%s.json"

    @staticmethod
    def list_articles(ctx) -> list:
        guild_id: int = ctx.interaction.guild.id
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
        self.name: str = "None"
        self.price: float = 0
        
        self.item_ids: dict = {}
        self.role_ids: list = []

        super().__init__(References.get_guild_folder(os.path.join(GuildArticle.FOLDER % self._guild_id, GuildArticle.FILENAME % self._article_id)))

    @Saveable.update()
    def set_name(self, new_name: str):
        self.name = new_name
        return self

    @Saveable.update()
    def set_price(self, new_price: float):
        self.price = new_price
        return self
    
    @Saveable.update()
    def add_item(self, new_item: GuildItem, quantity: int):
        self.item_ids[new_item._item_id] = quantity
        return self
    @Saveable.update()
    def remove_item(self, item: GuildItem):
        self.pop(item)
        return self
    
    @Saveable.update()
    def add_role(self, new_role: discord.Role):
        if not new_role.id in self.role_ids:
            self.role_ids.append(new_role.id)
        return self
    
    async def buy(self, ctx):
        author_data = ctx.author_data

        if author_data.money < self.price:
            raise errors.NotEnoughMoney
        else:
            author_data.money -= self.price
            author_inventory: Inventory = author_data.get_inventory()
            for item_id, amount in self.item_ids.items():
                author_inventory.add_item_id(item_id, amount)
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

        article_id: int = int(arg[arg.rfind("(")+1:arg.rfind(")")])
        return GuildArticle(article_id, ctx.guild.id)

class GuildItemConverter:
    async def convert(*args):
        ctx = args[0]
        arg = args[1]
        if len(args) > 2:
            ctx = args[1]
            arg = args[2]
        
        if not isinstance(arg, str):
            return None
        
        item_id = None
        if arg.isdecimal():
            item_id: str = arg
        else:
            item_id: str = arg[arg.rfind("(")+1:arg.rfind(")")]
        
        if not (item_id is None) and item_id.isdecimal():
            return GuildItem(item_id, ctx.guild.id)
        else:
            return GuildItem.from_name(ctx.guild.id, arg)