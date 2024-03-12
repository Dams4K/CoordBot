import re
from time import time

import discord
from discord.ext.commands import Converter

from data_management import errors as derrors
from ddm import *
from utils.references import References


class GuildObject(Saveable):
    __slots__ = ("_object_id", "_guild_id", "name", "description", "refundable", "refund_price")

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
            return super(GuildObject, cls).__new__(cls) # We want to create the instance with the __new__ function of Saveable
        return None

    def __init__(self, object_id: int, guild_id: int, create: bool = False):
        self._object_id = str(object_id)
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
    __slots__ = ("_article_id", "_guild_id", "name", "description", "price", "cooldown", "under_cooldown", "object_ids", "role_ids")

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
        self.description: str = ""
        self.price: int = 0
        self.cooldown: int = 0 # In seconds
        self.under_cooldown: dict = {} # member_id: time
        
        self.object_ids: dict = {}
        self.role_ids: list = []

        super().__init__(References.get_guild_folder(os.path.join(GuildArticle.FOLDER % self._guild_id, GuildArticle.FILENAME % self._article_id)))

    @Saveable.update()
    def set_name(self, value: str):
        """Set the name of the article

        Parameters
        ----------
            value: str
                max_length: 32
        
        Returns
        -------
            GuildArticle:
                modified article
        """
        self.name = value[:32]
        return self
    
    @Saveable.update()
    def set_description(self, value: str):
        """Set the description of the article

        Parameters
        ----------
            value: str
                max_length: 1024
        
        Returns
        -------
            GuildArticle:
                modified article
        """
        self.description = value[:1024]
        return self

    @Saveable.update()
    def set_price(self, value: int):
        """Set the price of the article

        Parameters
        ----------
            value: int
        
        Returns
        -------
            GuildArticle:
                modified article
        """
        self.price = int(value)
        return self
    
    @Saveable.update()
    def set_cooldown(self, value: int):
        """Set the cooldown of the article, user will be allowed to buy the article each `cooldown` seconds

        Parameters
        ----------
            value: int
        
        Returns
        -------
            GuildArticle:
                modified article
        """
        self.cooldown = value
        return self

    @Saveable.update()
    def add_object(self, obj: GuildObject, quantity: int = 1):
        obj_id = str(obj._object_id)
        self.object_ids.setdefault(obj_id, 0)
        self.object_ids[obj_id] += quantity
        return self
    
    @Saveable.update()
    def remove_object(self, obj: GuildObject, quantity: int = 1):
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
    
    @Saveable.update()
    async def fetch_roles(self, guild: discord.Guild) -> list:
        roles = []
        dead_roles = []
        guild_roles = {role.id: role for role in await guild.fetch_roles()}

        for role_id in self.role_ids:
            if role_id in guild_roles:
                roles.append(guild_roles[role_id])
            else:
                self.role_ids.remove(role_id)
        
        return roles

    @Saveable.update()
    def save_purchase_time(self, author_id: str, time: int):
        self.under_cooldown[str(author_id)] = round(time)

    def has_object(self, object: GuildObject):
        return str(object._object_id) in self.object_ids

    def get_quantity(self, object: GuildObject):
        return self.object_ids.get(str(object._object_id), 0)

    async def buy(self, ctx, quantity: int) -> int:
        author_data = ctx.author_data
        author_id: str = str(ctx.author.id)

        if self.cooldown > 0: # We can only buy one article so
            quantity = 1
        # Calculates the total price
        price: int = self.price * quantity

        #- PERFORM ALL CHECKS
        # Check if the author is under cooldown
        current_time = time()
        if self.under_cooldown.get(author_id, 0) + self.cooldown > current_time:
            raise derrors.UnderCooldown(ctx.guild_config.language, end_timestamp=self.under_cooldown.get(author_id, 0) + self.cooldown)

        # Check if the member has enough money
        if author_data.money < price:
            raise derrors.NotEnoughMoney(ctx.guild_config.language, money=author_data.money, price=price)
        
        author_inventory: Inventory = author_data.get_inventory()


        for object_id, object_amount in self.object_ids.items():
            if object_amount >= 0:
                continue
            
            author_quantity = author_inventory.get_object_amount(object_id)
            if author_quantity < abs(object_amount * quantity):
                raise derrors.NotEnoughObjects(ctx.guild_config.language)


        #- MAKE THE PURCHASE
        # Save purchase time
        self.save_purchase_time(author_id, current_time)

        # Check if the member has enough objects

        author_data.add_money(-price)

        # Add correct quantity
        for _ in range(quantity):
            for object_id, amount in self.object_ids.items():
                author_inventory.add_object_id(object_id, amount)

        author_data.set_inventory(author_inventory)
        
        for role_id in self.role_ids:
            role = ctx.guild.get_role(role_id)
            if role == None:
                raise derrors.RoleNotFound(ctx.guild_config.language)
            else:
                await ctx.author.add_roles(role)
        
        # Return the quantity bought
        return quantity
    
class GuildArticleConverter(Converter):
    @staticmethod
    def get_article(ctx, name: str) -> GuildArticle:
        if not isinstance(name, str):
            raise derrors.Article.NotFound(ctx.guild_config.language)
        
        pattern = r"\((\d+)\)$" # Detect the last digit in parentheses and if their is nothing after
        result = re.search(pattern, name)
        if result:
            article_id = int(result.group(1))
            article_name = name.replace(f"({article_id})", "").strip() # Without id

            article = GuildArticle(article_id, ctx.guild.id)

            if article.name == article_name:
                # Same name so let's think their are the same
                return article

        if article := GuildArticle.from_name(ctx.guild.id, name):
            return article
        
        raise derrors.Article.NotFound(ctx.guild_config.language)

    async def convert(self, ctx, article_name: str) -> GuildArticle:
        return GuildArticleConverter.get_article(ctx, article_name)

class GuildObjectConverter(Converter):
    @staticmethod
    def get_object(ctx, name: str) -> GuildObject:
        if not isinstance(name, str):
            raise derrors.Object.NotFound(ctx.guild_config.language)
        
        pattern = r"\((\d+)\)$" # Detect the last digit in parentheses and if their is nothing after
        result = re.search(pattern, name)
        if result:
            object_id = int(result.group(1))
            object_name = name.replace(f"({object_id})", "").strip() # Without id

            obj = GuildObject(object_id, ctx.guild.id)

            if obj.name == object_name:
                # Same name so let's think their are the same
                return obj

        if obj := GuildObject.from_name(ctx.guild.id, name):
            return obj
        
        raise derrors.Object.NotFound(ctx.guild_config.language)

    async def convert(self, ctx, object_name: str) -> GuildObject:
        return GuildObjectConverter.get_object(ctx, object_name)
    

class Inventory(Data):
    __slots__ = ("max_size", "object_ids")
    dversion = 2

    def __init__(self):
        self.max_size = -1
        self.object_ids = {}

    @staticmethod
    def convert_version(data):
        data_version = data.get("__dversion", 1)
        
        if data_version == 1:
            data["__dversion"] = 2
            object_ids: list = data.get("object_ids", []) # ["0", "0", "0", "1"]
            
            new_object_ids: dict = {}
            for object_id in object_ids:
                i_object_id = str(object_id)
                new_object_ids.setdefault(i_object_id, 0)
                new_object_ids[i_object_id] += 1
            
            data["object_ids"] = new_object_ids

        return data

    def is_full(self):
        return sum(self.object_ids.values()) >= self.max_size and self.max_size > 0

    def add_object(self, obj: GuildObject, amount: int):
        return self.add_object_id(obj._object_id, amount)
    
    def add_object_id(self, object_id: str, amount: int):
        if self.is_full(): return

        self.object_ids.setdefault(object_id, 0)
        self.object_ids[object_id] += amount

        if self.object_ids[object_id] == 0:
            self.object_ids.pop(object_id)
    
    def remove_object(self, object_id: str, amount: int):
        if amount == -1:
            self.object_ids[object_id] = 0
        else:
            return self.add_object_id(object_id, -amount)

    def get_object_ids(self) -> list:
        return list(self.object_ids.keys())
    
    def get_object_amount(self, object_id: str) -> int:
        return self.object_ids.get(str(object_id), 0)